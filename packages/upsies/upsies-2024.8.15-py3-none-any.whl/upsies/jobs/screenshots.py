"""
Create screenshots from video file(s)
"""

import collections
import os
import queue

from .. import errors
from ..utils import LazyModule, daemon, fs, image, timestamp, torrent, video
from . import JobBase

import logging  # isort:skip
_log = logging.getLogger(__name__)

DEFAULT_NUMBER_OF_SCREENSHOTS = 2

natsort = LazyModule(module='natsort', namespace=globals())


class ScreenshotsJob(JobBase):
    """
    Create screenshots from video file(s)

    This job adds the following signals to the :attr:`~.JobBase.signal`
    attribute:

        ``screenshots_total``
            Emitted before screenshots are created. Registered callbacks get the
            total number of screenshots as a positional argument.
    """

    name = 'screenshots'
    label = 'Screenshots'
    cache_id = None

    def initialize(self, *, content_path, precreated=(),
                   exclude_files=(), timestamps=(), count=0,
                   from_all_videos=False, optimize='default'):
        """
        Set internal state

        :param str content_path: Path to file or directory or sequence of paths
        :param precreated: Sequence of paths of already existing screenshots

            These do not count towards the wanted number of screenshots.
            `count` screenshots are created in addition to any precreated
            screenshots.
        :param exclude_files: Sequence of glob patterns (:class:`str`) and
            :class:`re.Pattern` objects (return value from :func:`re.compile`)
            that are matched against the relative path beneath `content_path`

            Glob patterns are matched case-insensitively.

            .. note:: Non-video files and stuff like `Sample.mkv` are always
                      excluded by :func:`.video.filter_main_videos`.
        :param timestamps: Screenshot positions in the video
        :type timestamps: sequence of "[[H+:]M+:]S+" strings or seconds
        :param count: How many screenshots to make
        :param bool from_all_videos: Whether to take `count` screenshots from
            each video file or only from the first video

            See :func:`.video.find_videos` for more information.

        :param optimize: `level` argument for :func:`~image.optimize`

            If this is ``"default"``, missing optimization dependencies are
            silently ignored.

        If `timestamps` and `count` are not given, screenshot positions are
        picked at even intervals. If `count` is larger than the number of
        `timestamps`, more timestamps are added.
        """
        self._content_path = content_path
        self._precreated = precreated
        self._exclude_files = exclude_files
        self._timestamps = timestamps
        self._count = count
        self._from_all_videos = from_all_videos
        self._optimize = optimize
        self._screenshots_created = 0
        self._screenshots_total = -1
        self._screenshots_process = None
        self._optimize_process = None
        self._screenshots_by_file = collections.defaultdict(lambda: [])
        self.signal.add('screenshots_total', record=True)

    async def run(self):
        """Execute subprocesses for screenshot creation and optimization"""
        # Execute subprocesses
        self._execute_screenshots_process()
        if self._optimize not in ('none', None):
            self._execute_optimize_process()

        # Wait for subprocesses
        await self._screenshots_process.join()
        if self._optimize_process:
            await self._optimize_process.join()

    def _execute_screenshots_process(self):
        self._screenshots_process = daemon.DaemonProcess(
            name='_screenshots_process',
            target=_screenshots_process,
            kwargs={
                'content_path': self._content_path,
                'precreated': self._precreated,
                'exclude_files': self._exclude_files,
                'timestamps': self._timestamps,
                'count': self._count,
                'from_all_videos': self._from_all_videos,
                'output_dir': self.home_directory,
                'overwrite': self.ignore_cache,
            },
            info_callback=self._handle_info,
            error_callback=self._handle_error,
        )
        self._screenshots_process.start()

    def _execute_optimize_process(self):
        self._optimize_process = daemon.DaemonProcess(
            name='_optimize_process',
            target=_optimize_process,
            kwargs={
                'level': self._optimize,
                'overwrite': self.ignore_cache,
                # Ignore missing dependecy if we do "default" optimization
                'ignore_dependency_error': (
                    True
                    if self._optimize == 'default' else
                    False
                ),
                'cache_directory': self.cache_directory,
            },
            info_callback=self._handle_info,
            error_callback=self._handle_error,
        )
        self._optimize_process.start()

    def _handle_info(self, info):
        if not self.is_finished:
            if 'screenshots_total' in info:
                self._screenshots_total = info['screenshots_total']
                self.signal.emit('screenshots_total', self._screenshots_total)

            if 'screenshot_path' in info:
                if self._optimize_process:
                    _log.debug('Screenshot: %s: %.2f KiB',
                               info['screenshot_path'],
                               fs.file_size(info['screenshot_path']) or 0 / 1024)
                    self._optimize_process.send(
                        daemon.MsgType.info,
                        (info['screenshot_path'], info['video_path']),
                    )

                else:
                    _log.debug('Screenshot: %s: %.2f KiB',
                               info['screenshot_path'],
                               fs.file_size(info['screenshot_path']) or 0 / 1024)
                    self.send(info['screenshot_path'], info['video_path'])

            elif 'optimized_screenshot_path' in info:
                _log.debug('Optimized %s: %.2f KiB',
                           info['optimized_screenshot_path'],
                           fs.file_size(info['optimized_screenshot_path']) or 0 / 1024)
                self.send(info['optimized_screenshot_path'], info['video_path'])

            if self.screenshots_created == self.screenshots_total:
                self._screenshots_process.stop()
                if self._optimize_process:
                    self._optimize_process.stop()

    def _handle_error(self, error):
        if isinstance(error, BaseException):
            raise error
        else:
            self.error(error)

    def terminate(self):
        """
        Stop screenshot creation and optimization subprocesses before
        terminating the job
        """
        if self._screenshots_process:
            self._screenshots_process.stop()
        if self._optimize_process:
            self._optimize_process.stop()
        super().terminate()

    @property
    def exit_code(self):
        """`0` if all screenshots were made, `1` otherwise, `None` if unfinished"""
        if self.is_finished:
            if self.screenshots_total < 0:
                # Job is finished but _screenshots_process() never sent us
                # timestamps. That means we're either using previously cached
                # output or the job was cancelled while _screenshots_process()
                # was still initializing.
                if self.output:
                    # If we have cached output, assume the cached number of
                    # screenshots is what the user wanted because the output of
                    # unsuccessful jobs is not cached (see
                    # JobBase._write_cache()).
                    return 0
                else:
                    return 1
            elif len(self.output) == self.screenshots_total:
                return 0
            else:
                return 1

    @property
    def content_path(self):
        """
        Path or sequence of file paths

        If this is set to a single path, appropriate files are picked by
        :func:`~.video.find_videos`.

        If this is set to a sequence of file paths, non-video files and uncommon
        playback durations are excluded. (See
        :func:`~.video.filter_main_videos`.)

        See also :attr:`from_all_videos`.

        Setting this property when this job :attr:`~.JobBase.was_started` raises
        :class:`RuntimeError`.
        """
        return self._content_path

    @content_path.setter
    def content_path(self, content_path):
        if self.was_started:
            raise RuntimeError('Cannot set content_path after job has been started')
        else:
            self._content_path = content_path

    @property
    def exclude_files(self):
        """
        Sequence of glob and :class:`regex <re.Pattern>` patterns to exclude

        See :meth:`initialize` for more information.

        Setting this property when this job :attr:`~.JobBase.was_started` raises
        :class:`RuntimeError`.
        """
        return self._exclude_files

    @exclude_files.setter
    def exclude_files(self, exclude_files):
        if self.was_started:
            raise RuntimeError('Cannot set exclude_files after job has been started')
        else:
            self._exclude_files = exclude_files

    @property
    def from_all_videos(self):
        """
        Whether to make screenshots from all video files or only the first

        Setting this property when this job :attr:`~.JobBase.was_started` raises
        :class:`RuntimeError`.
        """
        return self._from_all_videos

    @from_all_videos.setter
    def from_all_videos(self, from_all_videos):
        if self.was_started:
            raise RuntimeError('Cannot set from_all_videos after job has been started')
        else:
            self._from_all_videos = from_all_videos

    @property
    def count(self):
        """
        How many screenshots to make per video file

        Setting this property when this job :attr:`~.JobBase.was_started` raises
        :class:`RuntimeError`.
        """
        return self._count

    @count.setter
    def count(self, count):
        if self.was_started:
            raise RuntimeError('Cannot set count after job has been started')
        else:
            self._count = count

    @property
    def timestamps(self):
        """
        Specific list of timestamps to make

        Setting this property when this job :attr:`~.JobBase.was_started` raises
        :class:`RuntimeError`.
        """
        return self._timestamps

    @timestamps.setter
    def timestamps(self, timestamps):
        if self.was_started:
            raise RuntimeError('Cannot set timestamps after job has been started')
        else:
            self._timestamps = timestamps

    @property
    def screenshots_total(self):
        """
        Total number of screenshots to make

        .. note:: This is ``-1`` until the subprocess that creates the
                  screenshots is executed and determined the number of
                  screenshots.
        """
        return self._screenshots_total

    @property
    def screenshots_created(self):
        """Total number of screenshots made so far"""
        return self._screenshots_created

    @property
    def screenshots_by_file(self):
        """
        Map source video file paths to sequence of generated screenshot file
        paths so far
        """
        return {
            video_path: tuple(screenshot_paths)
            for video_path, screenshot_paths in self._screenshots_by_file.items()
        }

    def send(self, screenshot_path, video_path):
        self._screenshots_created += 1
        self._screenshots_by_file[video_path].append(screenshot_path)
        return super().send(screenshot_path)


def _screenshots_process(
        output_queue, input_queue,
        *,
        content_path, precreated, exclude_files, timestamps, count,
        from_all_videos, output_dir, overwrite,
):
    video_files = list(_get_video_files(
        output_queue,
        content_path=content_path,
        exclude_files=exclude_files,
    ))
    if not video_files:
        output_queue.put((daemon.MsgType.error, 'No videos found'))
        return

    if not from_all_videos:
        # Only create screenshots from first video
        del video_files[1:]

    try:
        timestamps_map = _map_timestamps(
            video_files=video_files,
            timestamps=timestamps,
            count=count,
        )
    except errors.ContentError as e:
        output_queue.put((daemon.MsgType.error, str(e)))

    else:
        # Herald how many screenshots we are going to make
        screenshots_total = sum((len(ts) for ts in timestamps_map.values()))
        screenshots_total += len(precreated)
        output_queue.put((daemon.MsgType.info, {'screenshots_total': screenshots_total}))

        try:
            _screenshot_video_files(
                output_queue, input_queue,
                precreated=precreated,
                timestamps_map=timestamps_map,
                output_dir=output_dir,
                overwrite=overwrite,
            )
        except SystemExit:
            # _maybe_terminate signals termination by raising SystemExit. This
            # shouldn't cause any issues as long as we actually exit here.
            pass


def _get_video_files(output_queue, *, content_path, exclude_files):
    # Make list of appropriate video file(s) from `content_path`
    try:
        filtered_files = torrent.filter_files(content_path, exclude=exclude_files)
        return video.filter_main_videos(filtered_files)
    except errors.ContentError as e:
        output_queue.put((daemon.MsgType.error, str(e)))
        return []


def _screenshot_video_files(output_queue, input_queue, *, precreated, timestamps_map, output_dir, overwrite):
    # User-provided precreated screenshots
    for screenshot_file in precreated:
        output_queue.put((daemon.MsgType.info, {
            'screenshot_path': screenshot_file,
            'video_path': '',
        }))

    # Make all screenshots from all video files
    for video_file, timestamps in timestamps_map.items():
        _maybe_terminate(input_queue=input_queue)
        _screenshot_video_file(
            output_queue, input_queue,
            video_file=video_file,
            timestamps=timestamps,
            output_dir=output_dir,
            overwrite=overwrite,
        )


def _screenshot_video_file(output_queue, input_queue, *, video_file, timestamps, output_dir, overwrite):
    # Make all screenshots from one video file
    for ts in timestamps:
        _maybe_terminate(input_queue=input_queue)
        _make_screenshot(
            output_queue,
            video_file=video_file,
            timestamp=ts,
            output_dir=output_dir,
            overwrite=overwrite,
        )


def _make_screenshot(output_queue, *, video_file, timestamp, output_dir, overwrite):
    # Make one screenshot from one video file
    screenshot_file = os.path.join(
        output_dir,
        fs.basename(video_file) + f'.{timestamp}.png',
    )

    # Screenshot already exists?
    if not overwrite and os.path.exists(screenshot_file):
        output_queue.put((daemon.MsgType.info, {
            'video_path': video_file,
            'screenshot_path': screenshot_file,
        }))

    else:
        try:
            return_value = image.screenshot(
                video_file=video_file,
                screenshot_file=screenshot_file,
                timestamp=timestamp,
            )
        except errors.ScreenshotError as e:
            output_queue.put((daemon.MsgType.error, str(e)))
        else:
            output_queue.put((daemon.MsgType.info, {
                'video_path': video_file,
                'screenshot_path': return_value,
            }))


def _map_timestamps(*, video_files, timestamps, count):
    # Map each video_file to a sequence of timestamps
    timestamps_map = {}
    for video_file in video_files:
        timestamps_map[video_file] = _validate_timestamps(
            video_file=video_file,
            timestamps=timestamps,
            count=count,
        )
    return timestamps_map


def _validate_timestamps(*, video_file, timestamps, count):
    # Validate, normalize, deduplicate and sort timestamps

    # Stay clear of the last 10 seconds
    duration = video.duration(video_file)
    if duration < 1:
        raise errors.ContentError(f'Video duration is too short: {duration}s')

    timestamps_pretty = set()
    for ts in timestamps:
        try:
            ts = max(0, min(duration, timestamp.parse(ts)))
        except ValueError as e:
            raise errors.ContentError(e)
        timestamps_pretty.add(timestamp.pretty(ts))

    if not timestamps and not count:
        count = DEFAULT_NUMBER_OF_SCREENSHOTS

    # Add more timestamps if the user didn't specify enough
    if count > 0 and len(timestamps_pretty) < count:
        # Convert timestamp strings to seconds
        timestamps = sorted(timestamp.parse(ts) for ts in timestamps_pretty)

        # Fractions of video duration
        positions = [ts / duration for ts in timestamps]

        # Include start and end of video
        if 0.0 not in positions:
            positions.insert(0, 0.0)
        if 1.0 not in positions:
            positions.append(1.0)

        # Insert timestamps between the two positions with the largest distance
        looped = 0
        while len(timestamps_pretty) < count:
            pairs = [(a, b) for a, b in zip(positions, positions[1:])]
            max_distance, pos1, pos2 = max((b - a, a, b) for a, b in pairs)
            position = ((pos2 - pos1) / 2) + pos1
            timestamps_pretty.add(timestamp.pretty(duration * position))
            positions.append(position)
            positions.sort()

            # If the duration in seconds is smaller than `count`, avoid
            # endlessly looping.
            looped += 1
            if looped > count:
                break

    assert timestamps_pretty, timestamps_pretty
    return natsort.natsorted(timestamps_pretty)


def _maybe_terminate(*, input_queue):
    try:
        typ, msg = input_queue.get_nowait()
    except queue.Empty:
        pass
    else:
        if typ == daemon.MsgType.terminate:
            raise SystemExit('Terminated')


def _read_queue_until_empty(*, input_queue):
    msgs = []
    while True:
        try:
            typ, msg = input_queue.get(timeout=0.01)
        except queue.Empty:
            return msgs
        else:
            msgs.append((typ, msg))


def _optimize_process(
        output_queue, input_queue,
        *,
        level, overwrite, ignore_dependency_error, cache_directory,
):
    # Get as many queued screenshots as possible. Check if there's a termination
    # sentinel before optimizing each screenshot to avoid processing all the
    # screenshots before Ctrl-C takes effect.
    msgs = []
    while True:
        new_msgs = _read_queue_until_empty(input_queue=input_queue)
        msgs.extend(new_msgs)

        if any(typ is daemon.MsgType.terminate for typ, msg_ in msgs):
            break

        elif msgs:
            typ_, (screenshot_file, video_file) = msgs.pop(0)
            _optimize_screenshot(
                output_queue=output_queue,
                screenshot_file=screenshot_file,
                video_file=video_file,
                level=level,
                overwrite=overwrite,
                ignore_dependency_error=ignore_dependency_error,
                cache_directory=cache_directory,
            )


def _optimize_screenshot(
        output_queue,
        *,
        screenshot_file, video_file, level, overwrite, ignore_dependency_error, cache_directory,
):
    output_file = fs.ensure_path_in_cache(
        os.path.join(
            fs.dirname(screenshot_file),
            (
                fs.basename(fs.strip_extension(screenshot_file))
                + '.'
                + f'optimized={level}'
                + '.'
                + fs.file_extension(screenshot_file)
            )
        ),
        cache_directory,
    )

    if not overwrite and os.path.exists(output_file):
        output_queue.put((daemon.MsgType.info, {
            'optimized_screenshot_path': output_file,
            'video_path': video_file,
        }))

    else:
        try:
            return_value = image.optimize(
                screenshot_file,
                level=level,
                output_file=output_file,
            )

        except errors.ImageOptimizeError as e:
            output_queue.put((daemon.MsgType.error, str(e)))

        except errors.DependencyError as e:
            if ignore_dependency_error:
                # Act like we optimized `screenshot_file`
                output_queue.put((daemon.MsgType.info, {
                    'optimized_screenshot_path': screenshot_file,
                    'video_path': video_file,
                }))
            else:
                raise e

        else:
            output_queue.put((daemon.MsgType.info, {
                'optimized_screenshot_path': return_value,
                'video_path': video_file,
            }))
