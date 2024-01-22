import techgram
from techgram.types import InlineKeyboardButton


class BuildButton:
    def build_button(self: 'techgram.Client', buttons):
        keyb = []
        for btn in buttons:
            if btn[2] and keyb:
                keyb[-1].append(InlineKeyboardButton(btn[0], url=btn[1]))
            else:
                keyb.append([InlineKeyboardButton(btn[0], url=btn[1])])
        return keyb
