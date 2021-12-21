from enum import Enum, EnumMeta


class MyEnumMeta(EnumMeta):
    def __contains__(cls, item):
        return item in [k for k in cls.__members__.keys()]


class SequencerStatus(Enum, metaclass=MyEnumMeta):
    NOT_RECEIVED = False, 404
    ACCEPTED_ON_L2 = True, 200
