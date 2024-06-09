import abc
import sys
from dataclasses import dataclass, field
from typing import ClassVar

from flops_utils.mqtt_topics import Status, Subject, SupportedTopic, Topic
from flops_utils.timer import Timer
from notification_management import notify_manager, notify_observer


@dataclass
class Context(abc.ABC):
    build_plan_trigger: ClassVar[callable]
    mqtt_subject: ClassVar[Subject]

    image_registry_url: str
    flops_project_id: str
    mqtt_ip: str
    project_observer_ip: str
    deactivate_notifications: bool
    timer: Timer = field(default_factory=Timer, init=False)
    new_image_name_prefix: str = field(default="", init=False)
    new_image_tag: str = field(default="", init=False)

    def __post_init__(self):
        global _context
        _context = self

    def trigger_build_plan(self) -> None:
        self.build_plan_trigger()

    def set_new_image_name_prefix(self, new_image_name_prefix: str) -> None:
        self.new_image_name_prefix = new_image_name_prefix

    def set_new_image_tag(self, new_image_tag: str) -> None:
        self.new_image_tag = new_image_tag

    def _build_image_name(self, infix: str = None) -> str:
        if infix:
            return f"{self.new_image_name_prefix}/{infix}:{self.new_image_tag}"
        else:
            return f"{self.new_image_name_prefix}:{self.new_image_tag}"

    def get_protocol_free_image_registry_url(self) -> str:
        return self.image_registry_url.removeprefix("http://").removeprefix("https://")

    def get_image_name(self) -> str:
        return self._build_image_name()

    def notify_about_failed_build_and_terminate(self, error_msg: str) -> None:
        notify_manager(
            context=self,
            topic=Topic(
                subject=self.mqtt_subject,
                status=Status.FAILED,
            ).find_matching_supported_topic(),
            error_msg=error_msg,
        )
        notify_observer(context=self, msg=error_msg)
        sys.exit(1)

    def notify_about_successful_builder_process(self) -> None:
        msg_payload = {}
        for name, time_frame in self.timer.time_frames.items():
            msg_payload[name] = time_frame.get_duration(human_readable=True)

        notify_manager(
            context=self,
            topic=Topic(
                subject=self.mqtt_subject,
                status=Status.SUCCESS,
            ).find_matching_supported_topic(),
            msg_payload=msg_payload,
        )
        notify_observer(context=self, msg=str(msg_payload))
