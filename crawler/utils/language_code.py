def get_language_code(language):
    if language == 'Chinese' or language == 'chinese':
        return 'zh'
    elif language == 'English' or language == 'english':
        return 'en'
    elif language == 'korean' or language == 'korean':
        return 'ko'
    elif language == 'Japanese' or language == 'japanese':
        return 'ja'
    else:
        return language
