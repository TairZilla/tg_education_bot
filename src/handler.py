import re

def remove_ending(word:str):
    endings = ['а', 'я', 'о', 'е', 'ь', 'и', 'ы', 'ую', 'ю', 'ей', 'ой', 'ем', 'ом', 'ам', 'им', 'ым', 'ых', 'их', 'ого', 'его', 'ому', 'ему', 'ую', 'юю', 'ая', 'яя', 'ое', 'ее', 'ые', 'ие', 'ий', 'ый', 'ой', 'ей']
    endings.sort(key=len, reverse=True)
    for ending in endings:
        if word.endswith(ending):
            return word[:-len(ending)]
    return word

def find_in_dict(data, keywords, border, path=''):
    results = []
    keywords = [remove_ending(word) for word in keywords]
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}|{key}" if path else key
            results.extend(find_in_dict(value, keywords, border, new_path))
    elif isinstance(data, str):
        found_keywords = sum(bool(re.search(keyword, data, re.IGNORECASE)) for keyword in keywords)
        if found_keywords >= border:
            results.append(path)
    return results