from re import sub
from transliterate import translit, exceptions


def make_url(title):
    url = 'default_url'
    try:
        url = sub(r'_| |!|\?|\.|,|\'|\"|;|:', '-', translit(title, reversed=True).lower())
    except exceptions.LanguageDetectionError:
        url = sub(r'_| |!|\?|\.|,|\'|\"|;|:', '-', title.lower())
    return url
