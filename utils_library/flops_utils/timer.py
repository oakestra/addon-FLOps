from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Union


def _get_duration(
    start: datetime,
    end: datetime,
    human_readable: bool = False,
) -> Union[float, str]:
    duration = end - start
    if not human_readable:
        return duration

    total_seconds = int(duration.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    human_readable_res = ""
    if minutes:
        human_readable_res += f"'{minutes}' minutes and "
    human_readable_res += f"{seconds} seconds"
    return human_readable_res


@dataclass
class TimeFrame:
    start_time: datetime = field(default_factory=datetime.now, init=False)
    end_time: datetime = field(default=None, init=False)

    def end_time_frame(self) -> datetime:
        self.end_time = datetime.now()
        return self.end_time

    def get_duration(self, human_readable: bool = False) -> Union[float, str]:
        return _get_duration(
            start=self.start_time,
            end=(self.end_time or self.end_time_frame()),
            human_readable=human_readable,
        )


@dataclass
class Timer:
    time_stamps: Dict[str, datetime] = field(default_factory=dict)
    time_frames: Dict[str, TimeFrame] = field(default_factory=dict)

    def create_new_time_stamp(self, name: str) -> datetime:
        new_timestamp = datetime.now()
        self.time_stamps[name] = new_timestamp
        return new_timestamp

    def start_new_time_frame(self, name: str) -> TimeFrame:
        new_time_frame = TimeFrame()
        self.time_frames[name] = new_time_frame
        return new_time_frame

    def end_time_frame(self, name: str) -> TimeFrame:
        time_frame = self.time_frames[name]
        time_frame.end_time_frame()
        return time_frame

    def get_timestamp(self, name: str) -> datetime:
        return self.time_stamps.get(name, self.create_new_time_stamp(name))

    def get_time_frame(self, name: str) -> TimeFrame:
        return self.time_frames.get(name, self.start_new_time_frame(name))

    def get_duration_between_timestamps(
        self,
        timestamp_a_name: str,
        timestamp_b_name: str,
        human_readable: bool = False,
    ) -> Union[float, str]:
        return _get_duration(
            start=self.time_stamps[timestamp_a_name],
            end=self.time_stamps[timestamp_b_name],
            human_readable=human_readable,
        )
