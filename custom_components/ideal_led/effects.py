# Perhaps these should be in const.py instead?

EFFECT_CMD = bytearray.fromhex("00 06 80 00 00 04 05 0b 38 01 32 64")

# The names given to the effects are just what I thought they looked like.  Updates are welcome.
EFFECT_1 = "Gold Ring"
EFFECT_2 = "Red Magenta Fade"
EFFECT_3 = "Yellow Magenta Fade"
EFFECT_4 = "Green Yellow Fade"
EFFECT_5 = "Green Blue Spin"
EFFECT_6 = "Blue Spin"
EFFECT_7 = "Purple Pink Spin"
EFFECT_8 = "Color Fade"
EFFECT_9 = "Red Blue Flash"
EFFECT_10 = "CMRGB Spin"
EFFECT_11 = "RGBYMC Follow"
EFFECT_12 = "CMYRGB Spin"
EFFECT_13 = "RGB Chase"
EFFECT_14 = "RGB Tri Reverse Spin"
EFFECT_15 = "Red Fade"
EFFECT_16 = "Blue Yellow Quad Static"
EFFECT_17 = "Red Green Quad Static"
EFFECT_18 = "Cyan Magenta Quad Static"
EFFECT_19 = "Red Green Reverse Chase"
EFFECT_20 = "Blue Yellow Reverse Chase"
EFFECT_21 = "Cyan Magenta Reverse Chase"
EFFECT_22 = "Yellow RGB Reverse Spin"
EFFECT_23 = "Cyan RGB Reverse Spin"
EFFECT_25 = "RGB Reverse Spin"
EFFECT_24 = "Magenta RGB Reverse Spin"
EFFECT_26 = "RGBY Reverse Spin"
EFFECT_27 = "Magenta RGBY Reverse Spin"
EFFECT_28 = "Cyan RGBYMC Reverse Spin"
EFFECT_29 = "White RGBYMC Reverse Spin"
EFFECT_30 = "Red Green Reverse Chase 2"
EFFECT_31 = "Blue Yellow Reverse Chase 2"
EFFECT_32 = "Cyan Pink Reverse Chase"
EFFECT_33 = "White Strobe"
EFFECT_34 = "White Strobe 2"
EFFECT_35 = "Warm White Strobe"
EFFECT_36 = "Smooth Color Fade"
EFFECT_37 = "White Static"
EFFECT_38 = "Pinks Fade"
EFFECT_39 = "Cyans Fade"
EFFECT_40 = "Cyan Magenta Slow Fade"
EFFECT_41 = "Green Yellow Fade 2"
EFFECT_42 = "RGBCMY Slow Fade"
EFFECT_43 = "Whites Fade"
EFFECT_44 = "Pink Purple Fade"
EFFECT_45 = "Cyan Magenta Fade"
EFFECT_46 = "Cyan Blue Fade"
EFFECT_47 = "Yellow Cyan Fade"
EFFECT_48 = "Red Yellow Fade"
EFFECT_49 = "RGBCMY Strobe"
EFFECT_50 = "Warm Cool White Strobe"
EFFECT_51 = "Magenta Strobe"
EFFECT_52 = "Cyan Strobe"
EFFECT_53 = "Yellow Strobe"
EFFECT_54 = "Magenta Cyan Strobe"
EFFECT_55 = "Cyan Yellow Strobe"
EFFECT_56 = "Cool White Strobe Random"
EFFECT_57 = "Warm White Strobe Random"
EFFECT_58 = "Light Green Strobe Random"
EFFECT_59 = "Magenta Strobe Random"
EFFECT_60 = "Cyan Strobe Random"
EFFECT_61 = "Oranges Ring"
EFFECT_62 = "Blue Ring"
EFFECT_63 = "RMBCGY Loop"
EFFECT_64 = "Cyan Magenta Follow"
EFFECT_65 = "Yellow Green Follow"
EFFECT_66 = "Pink Blue Follow"
EFFECT_67 = "BGP Pastels Loop"
EFFECT_68 = "CYM Follow"
EFFECT_69 = "Pink Purple Demi Spinner"
EFFECT_70 = "Blue Pink Spinner"
EFFECT_71 = "Green Spinner"
EFFECT_72 = "Blue Yellow Tri Spinner"
EFFECT_73 = "Red Yellow Tri Spinner"
EFFECT_74 = "Pink Green Tri Spinner"
EFFECT_75 = "Red Blue Demi Spinner"
EFFECT_76 = "Yellow Green Demi Spinner"
EFFECT_77 = "RGB Tri Spinner"
EFFECT_78 = "Red Magenta Demi Spinner"
EFFECT_79 = "Cyan Magenta Demi Spinner"
EFFECT_80 = "RCBM Quad Spinner"
EFFECT_81 = "RGBCMY Spinner"
EFFECT_82 = "RGB Spinner"
EFFECT_83 = "CMB Spinner"
EFFECT_84 = "Red Blue Demi Spinner"
EFFECT_85 = "Cyan Magenta Demi Spinner"
EFFECT_86 = "Yellow Orange Demi Spinner"
EFFECT_87 = "Red Blue Striped Spinner"
EFFECT_88 = "Green Yellow Striped Spinner"
EFFECT_89 = "Red Pink Yellow Striped Spinner"
EFFECT_90 = "Cyan Blue Magenta Striped Spinner"
EFFECT_91 = "Pastels Striped Spinner"
EFFECT_92 = "Rainbow Spin"
EFFECT_93 = "Red Pink Blue Spinner"
EFFECT_94 = "Cyan Magenta Spinner"
EFFECT_95 = "Green Cyan Spinner"
EFFECT_96 = "Yellow Red Spinner"
EFFECT_97 = "Rainbow Strobe"
EFFECT_98 = "Magenta Strobe"
EFFECT_99 = "Yellow Orange Demi Strobe"
EFFECT_100 = "Yellow Cyan Demi Flash"
EFFECT_101 = "White Lightening Strobe"
EFFECT_102 = "Purple Lightening Strobe"
EFFECT_103 = "Magenta Lightening Strobe"
EFFECT_104 = "Yellow Lightening Strobe"
EFFECT_105 = "Blue With Sparkles"
EFFECT_106 = "Red With Sparkles"
EFFECT_107 = "Blue With Sparkles"
EFFECT_108 = "Yellow Dissolve"
EFFECT_109 = "Magenta Dissolve"
EFFECT_110 = "Cyan Dissolve"
EFFECT_111 = "Red Green Dissolve"
EFFECT_112 = "RGB Dissolve"
EFFECT_113 = "RGBCYM Dissolve"
EFFECT_114 = "Nothing"
EFFECT_115 = "Nothing 2"
EFFECT_255 = "_Cycle Through All Modes"

EFFECT_MAP = {
    EFFECT_1: 0x01,
    EFFECT_2: 0x02,
    EFFECT_3: 0x03,
    EFFECT_4: 0x04,
    EFFECT_5: 0x05,
    EFFECT_6: 0x06,
    EFFECT_7: 0x07,
    EFFECT_8: 0x08,
    EFFECT_9: 0x09,
    EFFECT_10: 0x0A,
    EFFECT_11: 0x0B,
    EFFECT_12: 0x0C,
    EFFECT_13: 0x0D,
    EFFECT_14: 0x0E,
    EFFECT_15: 0x0F,
    EFFECT_16: 0x10,
    EFFECT_17: 0x11,
    EFFECT_18: 0x12,
    EFFECT_19: 0x13,
    EFFECT_20: 0x14,
    EFFECT_21: 0x15,
    EFFECT_22: 0x16,
    EFFECT_23: 0x17,
    EFFECT_24: 0x18,
    EFFECT_25: 0x19,
    EFFECT_26: 0x1A,
    EFFECT_27: 0x1B,
    EFFECT_28: 0x1C,
    EFFECT_29: 0x1D,
    EFFECT_30: 0x1E,
    EFFECT_31: 0x1F,
    EFFECT_32: 0x20,
    EFFECT_33: 0x21,
    EFFECT_34: 0x22,
    EFFECT_35: 0x23,
    EFFECT_36: 0x24,
    EFFECT_37: 0x25,
    EFFECT_38: 0x26,
    EFFECT_39: 0x27,
    EFFECT_40: 0x28,
    EFFECT_41: 0x29,
    EFFECT_42: 0x2A,
    EFFECT_43: 0x2B,
    EFFECT_44: 0x2C,
    EFFECT_45: 0x2D,
    EFFECT_46: 0x2E,
    EFFECT_47: 0x2F,
    EFFECT_48: 0x30,
    EFFECT_49: 0x31,
    EFFECT_50: 0x32,
    EFFECT_51: 0x33,
    EFFECT_52: 0x34,
    EFFECT_53: 0x35,
    EFFECT_54: 0x36,
    EFFECT_55: 0x37,
    EFFECT_56: 0x38,
    EFFECT_57: 0x39,
    EFFECT_58: 0x3A,
    EFFECT_59: 0x3B,
    EFFECT_60: 0x3C,
    EFFECT_61: 0x3D,
    EFFECT_62: 0x3E,
    EFFECT_63: 0x3F,
    EFFECT_64: 0x40,
    EFFECT_65: 0x41,
    EFFECT_66: 0x42,
    EFFECT_67: 0x43,
    EFFECT_68: 0x44,
    EFFECT_69: 0x45,
    EFFECT_70: 0x46,
    EFFECT_71: 0x47,
    EFFECT_72: 0x48,
    EFFECT_73: 0x49,
    EFFECT_74: 0x4A,
    EFFECT_75: 0x4B,
    EFFECT_76: 0x4C,
    EFFECT_77: 0x4D,
    EFFECT_78: 0x4E,
    EFFECT_79: 0x4F,
    EFFECT_80: 0x50,
    EFFECT_81: 0x51,
    EFFECT_82: 0x52,
    EFFECT_83: 0x53,
    EFFECT_84: 0x54,
    EFFECT_85: 0x55,
    EFFECT_86: 0x56,
    EFFECT_87: 0x57,
    EFFECT_88: 0x58,
    EFFECT_89: 0x59,
    EFFECT_90: 0x5A,
    EFFECT_91: 0x5B,
    EFFECT_92: 0x5C,
    EFFECT_93: 0x5D,
    EFFECT_94: 0x5E,
    EFFECT_95: 0x5F,
    EFFECT_96: 0x60,
    EFFECT_97: 0x61,
    EFFECT_98: 0x62,
    EFFECT_99: 0x63,
    EFFECT_100: 0x64,
    EFFECT_101: 0x65,
    EFFECT_102: 0x66,
    EFFECT_103: 0x67,
    EFFECT_104: 0x68,
    EFFECT_105: 0x69,
    EFFECT_106: 0x6A,
    EFFECT_107: 0x6B,
    EFFECT_108: 0x6C,
    EFFECT_109: 0x6D,
    EFFECT_110: 0x6E,
    EFFECT_111: 0x6F,
    EFFECT_112: 0x70,
    EFFECT_113: 0x71,
    EFFECT_114: 0x72,
    EFFECT_115: 0x73,
    EFFECT_255: 0xFF,
}

EFFECT_LIST = sorted(EFFECT_MAP)
EFFECT_ID_TO_NAME = {v: k for k, v in EFFECT_MAP.items()}
