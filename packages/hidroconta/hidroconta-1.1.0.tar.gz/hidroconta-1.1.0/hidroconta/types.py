class AnalogInputHist:
    subtype = 4
    subcode = 0

class CounterGlobalHist:
    subtype = 2
    subcode = 2

class Element(enumerate):
    ANALOG_INPUT = 'analogInputs'
    COUNTER = 'counters'
    RTU = 'rtus'
    IRIS = 'iris'
    HYDRANT = 'hydrants'
    VALVE = 'valves'
    DIGITAL_INPUT = 'digitalInputs'
    DIGITAL_OUTPUT = 'digitalOutputs'
    CENTINEL = 'centinels'
    WMBUS_COUNTER = 'wmbusCounters'
    CENTAURUS = 'centaurus'

class Status(enumerate):
    ENABLED = 'enabled'
    DISABLED = 'disabled'
    ALL = 'all'
