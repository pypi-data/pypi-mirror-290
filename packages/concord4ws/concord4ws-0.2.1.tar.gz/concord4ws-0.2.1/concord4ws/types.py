from typing import Annotated, Literal, Optional, Tuple
import typing
from pydantic import BaseModel as PydanticBaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(alias_generator=to_camel)


# data types


ZoneType = Literal["hardwired", "rf", "touchpad"]
ZoneStatus = Literal[
    "normal", "tripped", "faulted", "alarm", "trouble", "bypassed", "unknown"
]
PartitionArmingLevel = Literal["off", "stay", "away", "phoneTest", "sensorTest"]
PanelType = Literal["concord", "concordExpress", "concordExpress4", "concordEuro"]
ArmingLevel = Literal["zoneTest", "off", "home", "away", "night", "silent"]
Feature = Literal[
    "chime", "energySaver", "noDelay", "latchKey", "silentArm", "quickArm"
]


class ZoneData(BaseModel):
    partition_number: int
    area_number: int
    group_number: int
    zone_number: int
    zone_type: ZoneType
    zone_status: ZoneStatus
    zone_text: str

    def id(self) -> str:
        return f"p{self.partition_number}-z{self.zone_number}"

    def group_id(self) -> str:
        return f"p{self.partition_number}-g{self.group_number}"

    def callback_id(self) -> str:
        return self.id()


class ZoneStatusData(BaseModel):
    partition_number: int
    area_number: int
    zone_number: int
    zone_status: ZoneStatus

    def zone_id(self) -> str:
        return f"p{self.partition_number}-z{self.zone_number}"

    def callback_id(self) -> str:
        return self.zone_id()


class PartitionData(BaseModel):
    partition_number: int
    area_number: int
    arming_level: PartitionArmingLevel
    zones: list[str]

    def id(self) -> int:
        return self.partition_number

    def callback_id(self) -> str:
        return f"p{self.partition_number}"


class GroupData(BaseModel):
    partition_number: int
    number: int
    zones: list[str]

    def id(self) -> str:
        return f"p{self.partition_number}-g{self.number}"


class PanelData(BaseModel):
    panel_type: PanelType
    hardware_revision: str
    software_revision: str
    serial_number: str


class ArmingLevelData(BaseModel):
    partition_number: int
    area_number: int
    arming_level: ArmingLevel

    def callback_id(self) -> str:
        return f"p{self.partition_number}"


class FeatureState(BaseModel):
    partition_number: int
    area_number: int
    feature_state: Feature


class TimeDate(BaseModel):
    hour: int
    minute: int
    month: int
    day: int
    year: int


class SuperBusDevData(BaseModel):
    partition_number: int
    area_number: int
    device_id: tuple[int, int, int]
    device_status: Literal["ok", "failed"]


class SuperBusCapabilityData(BaseModel):
    capability: str
    data: Optional[int] = None


class SuperBusDevCapData(BaseModel):
    device_id: tuple[int, int, int]
    capability: SuperBusCapabilityData


class SubEventData(BaseModel):
    sub_event: str
    user_number: Optional[tuple[int, int]] = None


class EventData(BaseModel):
    event: str
    data: SubEventData


class AlarmTroubleData(BaseModel):
    partition_number: int
    area_number: int
    source_type: str
    source_number: tuple[int, int, int]
    event: EventData


class TouchpadDisplay(BaseModel):
    partition_number: int
    area_number: int
    message_type: int
    display_tokens: list[int]
    text: str


Zones = dict[str, ZoneData]
Partitions = dict[int, PartitionData]
Groups = dict[str, GroupData]


class State(BaseModel):
    panel: PanelData
    zones: Zones
    partitions: Partitions
    groups: Groups


# message types


class ConcordAckMessage(BaseModel):
    type: Literal["ack"]


class ConcordNakMessage(BaseModel):
    type: Literal["nak"]


class ConcordPanelTypeMessage(BaseModel):
    type: Literal["panelType"]
    data: PanelData


class ConcordAutomationEventLostMessage(BaseModel):
    type: Literal["automationEventLost"]
    data: list[int]


class ZoneDataMessage(BaseModel):
    type: Literal["zoneData"]
    data: ZoneData


class PartitionDataMessage(BaseModel):
    type: Literal["partitionData"]
    data: PartitionData


class SuperBusDevDataMessage(BaseModel):
    type: Literal["superBusDevData"]
    data: SuperBusDevData


class SuperBusDevCapMessage(BaseModel):
    type: Literal["superBusDevCap"]
    data: SuperBusDevCapData


class OutputDataMessage(BaseModel):
    type: Literal["outputData"]
    data: list[int]


class EqptListDoneMessage(BaseModel):
    type: Literal["eqptListDone"]


class SchedDataMessage(BaseModel):
    type: Literal["schedData"]
    data: list[int]


class SchedEventDataMessage(BaseModel):
    type: Literal["schedEventData"]
    data: list[int]


class LightAttachMessage(BaseModel):
    type: Literal["lightAttach"]
    data: list[int]


class ClearImageMessage(BaseModel):
    type: Literal["clearImage"]
    data: list[int]


class ZoneStatusMessage(BaseModel):
    type: Literal["zoneStatus"]
    data: ZoneStatusData


class ArmingLevelMessage(BaseModel):
    type: Literal["armingLevel"]
    data: ArmingLevelData


class AlarmTroubleMessage(BaseModel):
    type: Literal["alarmTrouble"]
    data: AlarmTroubleData


class EntryExitDelayMessage(BaseModel):
    type: Literal["entryExitDelay"]
    data: list[int]


class SirenSetupMessage(BaseModel):
    type: Literal["sirenSetup"]
    data: list[int]


class SirenSyncMessage(BaseModel):
    type: Literal["sirenSync"]


class SirenGoMessage(BaseModel):
    type: Literal["sirenGo"]


class TouchpadMessage(BaseModel):
    type: Literal["touchpad"]
    data: TouchpadDisplay


class SirenStopMessage(BaseModel):
    type: Literal["sirenStop"]
    data: list[int]


class FeatStateMessage(BaseModel):
    type: Literal["featState"]
    data: FeatureState


class TempMessage(BaseModel):
    type: Literal["temp"]
    data: list[int]


class TimeAndDateMessage(BaseModel):
    type: Literal["timeAndDate"]
    data: TimeDate


class LightsStateMessage(BaseModel):
    type: Literal["lightsState"]
    data: list[int]


class UserLightsMessage(BaseModel):
    type: Literal["userLights"]
    data: list[int]


class KeyfobMessage(BaseModel):
    type: Literal["keyfob"]
    data: list[int]


ConcordReceivedMessageType = (
    ConcordAckMessage
    | ConcordNakMessage
    | ConcordPanelTypeMessage
    | ConcordAutomationEventLostMessage
    | ZoneDataMessage
    | PartitionDataMessage
    | SuperBusDevDataMessage
    | SuperBusDevCapMessage
    | OutputDataMessage
    | EqptListDoneMessage
    | SchedDataMessage
    | SchedEventDataMessage
    | LightAttachMessage
    | ClearImageMessage
    | ZoneStatusMessage
    | ArmingLevelMessage
    | AlarmTroubleMessage
    | EntryExitDelayMessage
    | SirenSetupMessage
    | SirenSyncMessage
    | SirenGoMessage
    | TouchpadMessage
    | SirenStopMessage
    | FeatStateMessage
    | TempMessage
    | TimeAndDateMessage
    | LightsStateMessage
    | UserLightsMessage
    | KeyfobMessage
)


class ConcordReceivedMessage(BaseModel):
    type: Literal["message"]
    data: ConcordReceivedMessageType = Field(..., discriminator="type")


class StateReceivedMessage(BaseModel):
    type: Literal["state"]
    data: State


ConcordMessageType = StateReceivedMessage | ConcordReceivedMessage
ReceivableMessage = Annotated[ConcordMessageType, Field(discriminator="type")]


# command types

ListRequestType = Literal[
    "allData",
    "zoneData",
    "partData",
    "busDevData",
    "busCapData",
    "outputData",
    "scheduleData",
    "eventData",
    "lightAttach",
]

Keypress = Literal[
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "*",
    "#",
    "policePanic",
    "auxPanic",
    "firePanic",
    "lightsOn",
    "lightsOff",
    "lightsToggle",
    "keyswitchOn",
    "keyswitchOff",
    "keyswitchToggle",
    "fireTPAcknowledge",
    "fireTPSilence",
    "fireTPFireTest",
    "fireTPSmokeReset",
    "keyfobDisarm",
    "keyfobArm",
    "keyfobLights",
    "keyfobStar",
    "keyfobArmDisarm",
    "keyfobLightsStar",
    "keyfobLongLights",
    "keyfobDirectArmLevelThree",
    "keyfobDirectArmLevelTwo",
    "keyfobArmStar",
    "keyfobDisarmLights",
    "TPAKey",
    "TPBKey",
    "TPCKey",
    "TPDKey",
    "TPEKey",
    "TPFKey",
]

ArmMode = Literal["stay", "away"]
ArmLevel = Literal["normal", "silent", "instant"]


class ConcordListCommand(BaseModel):
    message: Literal["list"] = "list"
    params: ListRequestType


class ArmOptions(BaseModel):
    mode: ArmMode
    code: list[Keypress]
    level: Optional[ArmLevel] = None
    partition: Optional[int] = None


class DisarmOptions(BaseModel):
    code: list[Keypress]
    partition: Optional[int] = None


class ConcordArmCommand(BaseModel):
    message: Literal["arm"] = "arm"
    params: ArmOptions


class ConcordDisarmCommand(BaseModel):
    message: Literal["disarm"] = "disarm"
    params: DisarmOptions


class ConcordToggleChimeCommand(BaseModel):
    message: Literal["toggleChime"] = "toggleChime"
    params: Optional[int] = None


class ConcordKeypressCommand(BaseModel):
    message: Literal["keypress"] = "keypress"
    params: Tuple[int, list[Keypress]]


class ConcordDynamicDataRefreshCommand(BaseModel):
    message: Literal["dynamicDataRefresh"] = "dynamicDataRefresh"


ConcordCommandType = (
    ConcordListCommand
    | ConcordArmCommand
    | ConcordDisarmCommand
    | ConcordToggleChimeCommand
    | ConcordKeypressCommand
    | ConcordDynamicDataRefreshCommand
)


class CommandSendableMessage(BaseModel):
    type: Literal["command"] = "command"
    data: ConcordCommandType = Field(..., discriminator="message")


class GetStateSendableMessage(BaseModel):
    type: Literal["getState"] = "getState"


SendableMessageType = CommandSendableMessage | GetStateSendableMessage
SendableMessage = Annotated[SendableMessageType, Field(discriminator="type")]

# helper functions


def partition_arming_level_to_arming_level(level: PartitionArmingLevel) -> ArmingLevel:
    if level == "off":
        return "off"
    if level == "stay":
        return "home"
    if level == "away":
        return "away"
    if level == "phoneTest":
        return "zoneTest"
    if level == "sensorTest":
        return "zoneTest"


def arming_level_to_partition_arming_level(level: ArmingLevel) -> PartitionArmingLevel:
    if level == "off":
        return "off"
    if level == "home":
        return "stay"
    if level == "away":
        return "away"
    if level == "zoneTest":
        return "phoneTest"

    return "off"


def code_to_keypresses(code: str) -> list[Keypress]:
    all_keypresses = typing.get_args(Keypress)

    try:
        return [all_keypresses[all_keypresses.index(char)] for char in code]
    except ValueError:
        raise Concord4KeypressError("invalid keypress in code")


class Concord4KeypressError(Exception):
    """Class for exceptions for Concord4's keypress"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
