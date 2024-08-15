from enum import Enum


class ParameterType(Enum):
    TextField = "TextField"
    Cron = "Cron"
    Select = "Select"
    Autocomplete = "Autocomplete"
    CheckBox = "CheckBox"
    Switch = "Switch"
    SwitchWithParameter = "SwitchWithParameter"
    Code = "Code"
    FilterList = "FilterList"
    SelectByParameter = "SelectByParameter"
    Password = "Password"
    ListObject = "ListObject"
    ListString = "ListString"
    Group = "Group"


class ConnectorDirection(Enum):
    input = "input"
    output = "output"
    both = "both"


class DataSendingStatus(Enum):
    success = "success"
    failed = "failed"
