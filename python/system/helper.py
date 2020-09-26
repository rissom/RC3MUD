

def i18n(playerlanguage, iobject):
    if playerlanguage in iobject:
        return iobject[playerlanguage]
    if 'en' in iobject:
        return iobject['en']
    if 'de' in iobject:
        return iobject['de']
    return "$$ Ooops, no text available $$"