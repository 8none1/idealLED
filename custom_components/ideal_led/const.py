from enum import Enum

DOMAIN = "ideal_led"
CONF_RESET = "reset"
CONF_DELAY = "delay"

COMMAND_BYTES = {
    "TYPE1" : {
        "turn_on_bytes"  : bytearray.fromhex("06 4C 45 44 4F 4E 00 00 00 00 00 00 00 00 00 00"),
        "turn_off_bytes" : bytearray.fromhex("06 4C 45 44 4F 46 46 00 00 00 00 00 00 00 00 00"),
        "rgb_bytes" :      bytearray.fromhex("07 43 4F 4C 4F 00 FF 00 00 00 00 00 00 00 00 00"),
        "red_offset" :     6,
        "green_offset" :   5,
        "blue_offset" :    7,
        "effects_bytes" :  bytearray.fromhex("06 4C 49 47 48 54 0C 00 00 00 00 00 00 00 00 00"),
        "effect_offset" :  5,
    },
    "TYPE2" : {
        "turn_on_bytes"  : bytearray.fromhex("05 54 55 52 4E 01 00 00 00 00 00 00 00 00 00 00"),
        "turn_off_bytes" : bytearray.fromhex("05 54 55 52 4E 00 00 00 00 00 00 00 00 00 00 00"),
        "rgb_bytes" :      bytearray.fromhex("0F 53 47 4C 53 00 00 64 50 1F 00 00 1F 00 00 32"),
        "red_offset" :     9,
        "green_offset" :   10,
        "blue_offset" :    11,
        "effects_bytes" :  bytearray.fromhex("0A 4D 55 4C 54 08 00 64 50 07 32 00 00 00 00 00"),
        "effect_offset" :  5,
    }
}

COMMAND_LOOKUP = {
    "TYPE1" : ['R002-15', 'R004-01', 'R003-01'],
    "TYPE2" : ['R012-01']
}
