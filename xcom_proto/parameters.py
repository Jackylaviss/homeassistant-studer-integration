#! /usr/bin/env python3

##
# Definition of all parameters / constants used in the Xcom protocol
##

import struct
from dataclasses import dataclass


class UnknownDatapointException(Exception):
    pass

@dataclass
class ValueTuple:
    id: int
    value: str

    def __eq__(self, __o: object) -> bool:
        if __o.__class__ is self.__class__:
            return __o.id == self.id
        return __o == self.id

    def __ne__(self, __o: object) -> bool:
        if __o.__class__ is self.__class__:
            return __o.id != self.id
        return __o != self.id

    def __str__(self) -> str:
        return self.value

@dataclass
class Datapoint:
    id: int
    name: str
    type: str
    unit: str = ""

    def __eq__(self, __o: object) -> bool:
        if __o.__class__ is self.__class__:
            return __o.id == self.id
        return __o == self.id

    def __ne__(self, __o: object) -> bool:
        if __o.__class__ is self.__class__:
            return __o.id != self.id
        return __o != self.id

    def unpackValue(self, value: bytes):
        if self.type is TYPE_FLOAT:
            return struct.unpack("<f", value)[0]
        if self.type is TYPE_SINT:
            return struct.unpack("<i", value)[0]
        if self.type is TYPE_BOOL:
            return struct.unpack("<?", value)[0]
        if self.type is TYPE_SHORT_ENUM:
            return struct.unpack("<h", value)[0]
        if self.type is TYPE_LONG_ENUM:
            return struct.unpack("<I", value)[0]
        if self.type is TYPE_STRING:
            return value.decode("iso8859-15")
        if self.type is TYPE_BYTES:
            return value

        raise TypeError("Unknown datatype", self)

    def packValue(self, value) -> bytes:
        if self.type is TYPE_FLOAT:
            return struct.pack("<f", value)
        if self.type is TYPE_SINT:
            return struct.pack("<i", value)
        if self.type is TYPE_BOOL:
            return struct.pack("<?", value)
        if self.type is TYPE_SHORT_ENUM:
            return struct.pack("<H", value)
        if self.type is TYPE_LONG_ENUM:
            return struct.pack("<I", value)
        if self.type is TYPE_STRING:
            return str(value).encode("iso8859-15")
        if self.type is TYPE_BYTES:
            return bytes(value)

        raise TypeError("Unknown datatype", self)

    @staticmethod
    def unpackValueByID(id: int, value: bytes):
        dataPoint = Dataset.getParamByID(id)
        return dataPoint.unpackValue(value)


### data types
TYPE_BOOL       = "BOOL"
TYPE_SINT       = "INTEGER"
TYPE_FLOAT      = "FLOAT"
TYPE_SHORT_ENUM = "ENUM_SHORT"
TYPE_LONG_ENUM  = "ENUM_LONG"
TYPE_STRING     = "STRING"
TYPE_BYTES      = "BYTES"

### service_id
PROPERTY_READ   = b'\x01'
PROPERTY_WRITE  = b'\x02'

### object_type
TYPE_INFO       = b'\x01\x00'
TYPE_PARAMETER  = b'\x02\x00'
TYPE_MESSAGE    = b'\x03\x00'
TYPE_GUID       = b'\x04\x00'
TYPE_DATALOG    = b'\x05\x00'

### property_id
QSP_VALUE           = b'\x05\x00'
QSP_MIN             = b'\x06\x00'
QSP_MAX             = b'\x07\x00'
QSP_LEVEL           = b'\x08\x00'
QSP_UNSAVED_VALUE   = b'\x0D\x00'

## values for QSP_LEVEL
QSP_LEVEL_VIEW_ONLY     = b'\x00\x00'
QSP_LEVEL_BASIC         = b'\x10\x00'
QSP_LEVEL_EXPERT        = b'\x20\x00'
QSP_LEVEL_INSTALLER     = b'\x30\x00'
QSP_LEVEL_QSP           = b'\x40\x00'


### operating modes (11016)
MODE_NIGHT      = ValueTuple(0, "MODE_NIGHT")
MODE_STARTUP    = ValueTuple(1, "MODE_STARTUP")
MODE_CHARGER    = ValueTuple(3, "MODE_CHARGER")
MODE_SECURITY   = ValueTuple(5, "MODE_SECURITY")
MODE_OFF        = ValueTuple(6, "MODE_OFF")
MODE_CHARGE     = ValueTuple(8, "MODE_CHARGE")
MODE_CHARGE_V   = ValueTuple(9, "MODE_CHARGE_V")
MODE_CHARGE_I   = ValueTuple(10, "MODE_CHARGE_I")
MODE_CHARGE_T   = ValueTuple(11, "MODE_CHARGE_T")

MODE_CHARGING = (
    MODE_CHARGE,
    MODE_CHARGE_V,
    MODE_CHARGE_I,
    MODE_CHARGE_T
)

### battey cycle phase (11038)
PHASE_BULK      = ValueTuple(0, "PHASE_BULK")
PHASE_ABSORPT   = ValueTuple(1, "PHASE_ABSORPT")
PHASE_EQUALIZE  = ValueTuple(2, "PHASE_EQUALIZE")
PHASE_FLOATING  = ValueTuple(3, "PHASE_FLOATING")
PHASE_R_FLOAT   = ValueTuple(6, "PHASE_R_FLOAT")
PHASE_PER_ABS   = ValueTuple(7, "PHASE_PER_ABS")


### error codes
ERROR_CODES = {
    b'\x01\x00': "INVALID_FRAME",
    b'\x02\x00': "DEVICE_NOT_FOUND",
    b'\x03\x00': "RESPONSE_TIMEOUT",
    b'\x11\x00': "SERVICE_NOT_SUPPORTED",
    b'\x12\x00': "INVALID_SERVICE_ARGUMENT",
    b'\x13\x00': "SCOM_ERROR_GATEWAY_BUSY",
    b'\x21\x00': "TYPE_NOT_SUPPORTED",
    b'\x22\x00': "OBJECT_ID_NOT_FOUND",
    b'\x23\x00': "PROPERTY_NOT_SUPPORTED",
    b'\x24\x00': "INVALID_DATA_LENGTH",
    b'\x25\x00': "PROPERTY_IS_READ_ONLY",
    b'\x26\x00': "INVALID_DATA",
    b'\x27\x00': "DATA_TOO_SMALL",
    b'\x28\x00': "DATA_TOO_BIG",
    b'\x29\x00': "WRITE_PROPERTY_FAILED",
    b'\x2A\x00': "READ_PROPERTY_FAILED",
    b'\x2B\x00': "ACCESS_DENIED",
    b'\x2C\x00': "SCOM_ERROR_OBJECT_NOT_SUPPORTED",
    b'\x2D\x00': "SCOM_ERROR_MULTICAST_READ_NOT_SUPPORTED",
    b'\x2E\x00': "OBJECT_PROPERTY_INVALID",
    b'\x2F\x00': "FILE_OR_DIR_NOT_PRESENT",
    b'\x30\x00': "FILE_CORRUPTED",
    b'\x81\x00': "INVALID_SHELL_ARG",
}

### main parameters

class Dataset:

    # Xtender parameters (Writable)
    MAX_CURR_AC_SOURCE = Datapoint(1107, "MAX_CURR_AC_SOURCE", TYPE_FLOAT)
    SMART_BOOST_ALLOWED = Datapoint(1126, "SMART_BOOST_ALLOWED", TYPE_BOOL)
    BATTERY_CHARGE_CURR = Datapoint(1138, "BATTERY_CHARGE_CURR", TYPE_FLOAT)
    MAX_GRID_FEEDING_CURR = Datapoint(1523, "MAX_GRID_FEEDING_CURR", TYPE_FLOAT)
    SMART_BOOST_LIMIT = Datapoint(1607, "SMART_BOOST_LIMIT", TYPE_FLOAT)
    
    # Nouveaux paramètres Xtender (Writable)
    BATT_CHARGE_CURRENT = Datapoint(1138, "BATT_CHARGE_CURRENT", TYPE_FLOAT)
    BATT_ABSORPTION_VOLTAGE = Datapoint(1156, "BATT_ABSORPTION_VOLTAGE", TYPE_FLOAT)
    BATT_FLOATING_VOLTAGE = Datapoint(1140, "BATT_FLOATING_VOLTAGE", TYPE_FLOAT)
    BATT_EQUALIZATION_VOLTAGE = Datapoint(1143, "BATT_EQUALIZATION_VOLTAGE", TYPE_FLOAT)
    BATT_UNDERVOLTAGE = Datapoint(1108, "BATT_UNDERVOLTAGE", TYPE_FLOAT)
    BATT_TEMP_COMPENSATION = Datapoint(1139, "BATT_TEMP_COMPENSATION", TYPE_FLOAT)
    INVERTER_OUTPUT_VOLTAGE = Datapoint(1286, "INVERTER_OUTPUT_VOLTAGE", TYPE_FLOAT)
    INVERTER_OUTPUT_FREQUENCY = Datapoint(1112, "INVERTER_OUTPUT_FREQUENCY", TYPE_FLOAT)
    ECO_MODE_ENABLED = Datapoint(1517, "ECO_MODE_ENABLED", TYPE_BOOL)
    GRID_FEEDING_ALLOWED = Datapoint(1127, "GRID_FEEDING_ALLOWED", TYPE_BOOL)
    GRID_FEEDING_POWER_LIMIT = Datapoint(1524, "GRID_FEEDING_POWER_LIMIT", TYPE_FLOAT)
    TRANSFER_RELAY_ENABLED = Datapoint(1128, "TRANSFER_RELAY_ENABLED", TYPE_BOOL)

    PARAMS_SAVED_IN_FLASH = Datapoint(1550, "PARAMS_SAVED_IN_FLASH", TYPE_BOOL)

    # RCC / Xcom-232i parameters (Not SCOM accessible, do not use)
    USER_LEVEL = Datapoint(5012, "USER_LEVEL", TYPE_SHORT_ENUM)

    # Xtender infos (Read only)
    AC_ENERGY_IN_CURR_DAY = Datapoint(3081, "AC_POWER_IN_CURR_DAY", TYPE_FLOAT, "kWh")
    AC_ENERGY_IN_PREV_DAY = Datapoint(3080, "AC_POWER_IN_PREV_DAY", TYPE_FLOAT, "kWh")
    AC_ENERGY_OUT_CURR_DAY = Datapoint(3083, "AC_ENERGY_OUT_CURR_DAY", TYPE_FLOAT, "kWh")
    AC_ENERGY_OUT_PREV_DAY = Datapoint(3082, "AC_ENERGY_OUT_PREV_DAY", TYPE_FLOAT, "kWh")
    AC_FREQ_IN = Datapoint(3084, "AC_FREQ_IN", TYPE_FLOAT, "Hz")
    AC_FREQ_OUT = Datapoint(3085, "AC_FREQ_OUT", TYPE_FLOAT, "Hz")
    AC_POWER_IN = Datapoint(3137, "AC_POWER_IN", TYPE_FLOAT, "kW")
    AC_POWER_OUT = Datapoint(3136, "AC_POWER_OUT", TYPE_FLOAT, "kW")
    AC_VOLTAGE_IN = Datapoint(3011, "AC_VOLTAGE_IN", TYPE_FLOAT, "V")
    AC_VOLTAGE_OUT = Datapoint(3021, "AC_VOLTAGE_OUT", TYPE_FLOAT, "V")
    AC_CURRENT_IN = Datapoint(3012, "AC_CURRENT_IN", TYPE_FLOAT, "A")
    AC_CURRENT_OUT = Datapoint(3022, "AC_CURRENT_OUT", TYPE_FLOAT, "A")
    
    # Nouveaux paramètres Xtender (Read only)
    SYSTEM_STATE = Datapoint(3049, "SYSTEM_STATE", TYPE_SHORT_ENUM)
    OPERATING_MODE = Datapoint(3048, "OPERATING_MODE", TYPE_SHORT_ENUM)
    INPUT_ACTIVE = Datapoint(3020, "INPUT_ACTIVE", TYPE_BOOL)
    TRANSFER_RELAY_STATE = Datapoint(3049, "TRANSFER_RELAY_STATE", TYPE_BOOL)
    GRID_FEEDING_ACTIVE = Datapoint(3119, "GRID_FEEDING_ACTIVE", TYPE_BOOL)
    AUXILIARY_RELAY_1_STATE = Datapoint(3031, "AUXILIARY_RELAY_1_STATE", TYPE_BOOL)
    AUXILIARY_RELAY_2_STATE = Datapoint(3032, "AUXILIARY_RELAY_2_STATE", TYPE_BOOL)
    RUNNING_TIME = Datapoint(3089, "RUNNING_TIME", TYPE_FLOAT, "h")
    ENERGY_AC_IN_TOTAL = Datapoint(3085, "ENERGY_AC_IN_TOTAL", TYPE_FLOAT, "kWh")
    ENERGY_AC_OUT_TOTAL = Datapoint(3086, "ENERGY_AC_OUT_TOTAL", TYPE_FLOAT, "kWh")
    NUM_BATTERY_UNDERVOLTAGES = Datapoint(3088, "NUM_BATTERY_UNDERVOLTAGES", TYPE_SINT)
    NUM_BATTERY_CRITICALS = Datapoint(3089, "NUM_BATTERY_CRITICALS", TYPE_SINT)
    NUM_BATTERY_LOW = Datapoint(3090, "NUM_BATTERY_LOW", TYPE_SINT)
    
    BATT_CYCLE_PHASE_XT = Datapoint(3010, "BATT_CYCLE_PHASE_XT", TYPE_SHORT_ENUM)
    BATT_VOLTAGE = Datapoint(3092, "BATT_VOLTAGE", TYPE_FLOAT, "V")

    # Xcom-CAN BMS parameters (Writable)
    SOC_LEVEL_FOR_BACKUP = Datapoint(6062, "SOC_LEVEL_FOR_BACKUP", TYPE_FLOAT)
    SOC_LEVEL_FOR_GRID_FEEDING = Datapoint(6063, "SOC_LEVEL_FOR_GRID_FEEDING", TYPE_FLOAT)

    # BSP infos (Read only)
    BATT_VOLTAGE = Datapoint(7000, "BATT_VOLTAGE", TYPE_FLOAT, "V")
    BATT_CURRENT = Datapoint(7001, "BATT_CURRENT", TYPE_FLOAT, "A")
    BATT_SOC = Datapoint(7032, "BATT_SOC", TYPE_FLOAT, "%")
    BATT_TEMP = Datapoint(7029, "BATT_TEMP", TYPE_FLOAT, "°C")
    BATT_CYCLE_PHASE = Datapoint(11038, "BATT_CYCLE_PHASE", TYPE_SHORT_ENUM)
    BATT_POWER = Datapoint(7003, "BATT_POWER", TYPE_FLOAT, "W")
    BATT_CHARGE = Datapoint(7007, "BATT_CHARGE", TYPE_FLOAT, "Ah")
    BATT_DISCHARGE = Datapoint(7008, "BATT_DISCHARGE", TYPE_FLOAT, "Ah")
    BATT_CHARGE_PREV_DAY = Datapoint(7009, "BATT_CHARGE_PREV_DAY", TYPE_FLOAT, "Ah")
    BATT_DISCHARGE_PREV_DAY = Datapoint(7010, "BATT_DISCHARGE_PREV_DAY", TYPE_FLOAT, "Ah")
    
    # Nouveaux paramètres BSP (Read only)
    BATT_STATE_OF_HEALTH = Datapoint(7033, "BATT_STATE_OF_HEALTH", TYPE_FLOAT, "%")
    BATT_REMAINING_AUTONOMY = Datapoint(7034, "BATT_REMAINING_AUTONOMY", TYPE_FLOAT, "h")
    BATT_REMAINING_CAPACITY = Datapoint(7035, "BATT_REMAINING_CAPACITY", TYPE_FLOAT, "Ah")
    BATT_NUM_CYCLES = Datapoint(7036, "BATT_NUM_CYCLES", TYPE_SINT)
    BATT_HISTORY_DEEPEST_DISCHARGE = Datapoint(7037, "BATT_HISTORY_DEEPEST_DISCHARGE", TYPE_FLOAT, "Ah")
    BATT_HISTORY_MAX_VOLTAGE = Datapoint(7038, "BATT_HISTORY_MAX_VOLTAGE", TYPE_FLOAT, "V")
    BATT_HISTORY_MIN_VOLTAGE = Datapoint(7039, "BATT_HISTORY_MIN_VOLTAGE", TYPE_FLOAT, "V")
    BATT_HISTORY_TOTAL_AH_CHARGED = Datapoint(7040, "BATT_HISTORY_TOTAL_AH_CHARGED", TYPE_FLOAT, "Ah")
    BATT_HISTORY_TOTAL_AH_DISCHARGED = Datapoint(7041, "BATT_HISTORY_TOTAL_AH_DISCHARGED", TYPE_FLOAT, "Ah")

    # VarioTrack infos (Read only)
    PV_VOLTAGE = Datapoint(11041 ,"PV_VOLTAGE", TYPE_FLOAT, "V")
    PV_POWER = Datapoint(11043, "PV_POWER", TYPE_FLOAT, "W")
    PV_ENERGY_CURR_DAY = Datapoint(11007, "PV_ENERGY_CURR_DAY", TYPE_FLOAT, "kWh")
    PV_ENERGY_PREV_DAY = Datapoint(11011, "PV_ENERGY_PREV_DAY", TYPE_FLOAT, "kWh")
    PV_ENERGY_TOTAL = Datapoint(11009, "PV_ENERGY_TOTAL", TYPE_FLOAT, "MWh")
    PV_SUN_HOURS_CURR_DAY = Datapoint(11025, "PV_SUN_HOURS_CURR_DAY", TYPE_FLOAT, "h")
    PV_SUN_HOURS_PREV_DAY = Datapoint(11026, "PV_SUN_HOURS_PREV_DAY", TYPE_FLOAT, "h")
    
    # Nouveaux paramètres VarioTrack (Read only)
    PV_CURRENT = Datapoint(11042, "PV_CURRENT", TYPE_FLOAT, "A")
    PV_OPERATING_MODE = Datapoint(11016, "PV_OPERATING_MODE", TYPE_SHORT_ENUM)
    PV_CHARGING_CURRENT = Datapoint(11044, "PV_CHARGING_CURRENT", TYPE_FLOAT, "A")
    PV_CHARGING_POWER = Datapoint(11045, "PV_CHARGING_POWER", TYPE_FLOAT, "W")
    PV_INPUT_POWER_REDUCTION = Datapoint(11046, "PV_INPUT_POWER_REDUCTION", TYPE_FLOAT, "%")
    PV_TEMPERATURE_INTERNAL = Datapoint(11047, "PV_TEMPERATURE_INTERNAL", TYPE_FLOAT, "°C")
    PV_TEMPERATURE_MAX_24H = Datapoint(11048, "PV_TEMPERATURE_MAX_24H", TYPE_FLOAT, "°C")
    PV_TEMPERATURE_MAX_TOTAL = Datapoint(11049, "PV_TEMPERATURE_MAX_TOTAL", TYPE_FLOAT, "°C")
    PV_NUM_OVERTEMP_TODAY = Datapoint(11050, "PV_NUM_OVERTEMP_TODAY", TYPE_SINT)
    PV_NUM_OVERTEMP_TOTAL = Datapoint(11051, "PV_NUM_OVERTEMP_TOTAL", TYPE_SINT)

    PV_OPERATION_MODE = Datapoint(11016, "PV_OPERATION_MODE", TYPE_SHORT_ENUM)
    PV_NEXT_EQUAL = Datapoint(11037, "PV_NEXT_EQUAL", TYPE_FLOAT, "d")

    # VarioTrack parameters (Writable)
    FORCE_NEW_CYCLE = Datapoint(10029, "FORCE_NEW_CYCLE", TYPE_SINT)

    # VarioString infos (Read only)
    VS_PV_POWER = Datapoint(15010, "VS_PV_POWER", TYPE_FLOAT, "kW")
    VS_PV_PROD = Datapoint(15017, "VS_PV_PROD", TYPE_FLOAT, "kWh")
    VS_PV_ENERGY_PREV_DAY = Datapoint(15027, "VS_PV_ENERGY_PREV_DAY", TYPE_FLOAT, "kWh")
    
    # Nouveaux paramètres VarioString (Read only)
    VS_PV_VOLTAGE = Datapoint(15011, "VS_PV_VOLTAGE", TYPE_FLOAT, "V")
    VS_PV_CURRENT = Datapoint(15012, "VS_PV_CURRENT", TYPE_FLOAT, "A")
    VS_BATT_VOLTAGE = Datapoint(15013, "VS_BATT_VOLTAGE", TYPE_FLOAT, "V")
    VS_BATT_CURRENT = Datapoint(15014, "VS_BATT_CURRENT", TYPE_FLOAT, "A")
    VS_OPERATING_MODE = Datapoint(15015, "VS_OPERATING_MODE", TYPE_SHORT_ENUM)
    VS_TEMPERATURE_INTERNAL = Datapoint(15016, "VS_TEMPERATURE_INTERNAL", TYPE_FLOAT, "°C")
    VS_ENERGY_TODAY = Datapoint(15018, "VS_ENERGY_TODAY", TYPE_FLOAT, "kWh")
    VS_NUM_ERRORS_TODAY = Datapoint(15019, "VS_NUM_ERRORS_TODAY", TYPE_SINT)
    VS_NUM_ERRORS_TOTAL = Datapoint(15020, "VS_NUM_ERRORS_TOTAL", TYPE_SINT)

    @staticmethod
    def getParamByID(id: int) -> Datapoint:
        for point in Dataset._getDatapoints():
            if point == id:
                return point

        raise UnknownDatapointException(id)

    @staticmethod
    def _getDatapoints() -> list[Datapoint]:
        points = list()
        for val in Dataset.__dict__.values():
            if type(val) is Datapoint:
                points.append(val)

        return points
