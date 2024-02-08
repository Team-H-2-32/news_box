import wikipedia as w


def search_wikipedia(lg, keyword):
    w.set_lang(lg)
    result = w.summary(keyword)
    return result
