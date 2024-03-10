import learning

def search_in_json(*keywords):
    data:dict=learning.LEARNING_DATA
    results = []

    def search_dict(d):
        for key, value in d.items():
            if isinstance(value, dict):
                search_dict(value)
            elif isinstance(value, str):
                if any(keyword in value.lower() for keyword in keywords):
                    results.append(value)

    search_dict(data)
    return results
          

