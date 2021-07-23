from enum import Enum
from googletrans import Translator

_translator = Translator()

class Language(Enum):
    english = "en"
    spanish = "es"


def translate(message: str, language: Language):
    lan_code = language.value
    trans = _translator.translate(message, dest=lan_code)
    return trans.text