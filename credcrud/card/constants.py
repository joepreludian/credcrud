from enum import IntEnum


class CardConstants(IntEnum):
    HOLDER_MIN_SIZE = 2
    HOLDER_MAX_SIZE = 128

    CARD_NUMBER_SIZE = 16

    CVV_MIN_SIZE = 3
    CVV_MAX_SIZE = 4
