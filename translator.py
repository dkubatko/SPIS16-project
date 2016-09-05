from translate import Translator


langDict = {'english': "en",
            'spanish': "es",
            'russian': "ru",
            'chinese': "zh",
            'korean': "ko",
            'french': "fr",
            'gujarati': "gu",
            'indonesian': "in",
            'irish': "ga",
            'japanese': "ja",
            'punjabi': "pa",
            'tagalog': "tl",
            'urdu': "ur",
            'vietnamese': "vi"}
wordDict = {'english': u"English",
            'spanish': u"español",
            'russian': u"русский",
            'chinese': u"中文",
            'korean': u"한국어",
            'french': u"français",
            'gujarati': u"ગુજરાતી",
            'indonesian': u"bahasa Indonesia",
            'irish': u"Gaeilge",
            'japanese': u"日本語",
            'punjabi': u"ਪੰਜਾਬੀ ਦੇ",
            'tagalog': u"tagalog",
            'urdu': u"اردو",
            'vietnamese': u"Tiếng Việt"}
            
def transStr(language, phrase):
    for l in langDict:
        if language == l:
            translator = Translator(to_lang=langDict[language])
            transword = wordDict[l]
            translation = translator.translate(phrase)
            return translation + ' ' + transword + '!'
    return 'No language'
