# coding: utf-8
from transliterate import translit, get_available_language_codes

from stuff import try_translit

assert translit("Привет мир 2012 すべての人間は", reversed=True, strict=True) == "Privet mir 2012 すべての人間は"
assert try_translit(" Привет мир 2012 ") == "privetmir2012"


