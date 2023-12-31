from typing import Union, List
from dataclasses import dataclass


class Command:
    pass


@dataclass
class DeleteWebhook(Command):
    secret: str
    token: str
    url: str


@dataclass
class UpdateWebhook(Command):
    secret: str
    token: str
    url: str


@dataclass
class ConfigWebhook(Command):
    secret: str
    token: str
    url: str


@dataclass
class ReportEvent(Command):
    eventType: str
    eventVersion: str
    context: dict


@dataclass
class ExecManualScene(Command):
    secret: str
    token: str
    scene_id: str


@dataclass
class SendDeviceCtrlCmd(Command):
    secret: str
    token: str
    dev_id: str
    cmd_type: str
    cmd_value: str
    cmd_param: Union[str, dict]


@dataclass
class SwitchBotDevCommand(Command):
    commandType: str
    command: str
    parameter: Union[str, dict]


@dataclass
class CheckAuthToken(Command):
    secret: str
    token: str


@dataclass
class GetDeviceList(Command):
    secret: str
    token: str


@dataclass
class RequestSync(Command):
    user_id: str
    devices: List[dict]


@dataclass
class ReportState(Command):
    state: dict


@dataclass
class Disconnect(Command):
    user_id: str
