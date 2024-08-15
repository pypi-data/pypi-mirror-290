import json

class Code:
    def __init__(self, system, code, display, synonyms = []):
        self.system = system
        self.code = code
        self.display = display
        self.synonyms = synonyms

    def to_json(self):
        return json.dumps({
            'system': self.system,
            'code': self.code,
            'display': self.display,
            'synonyms': self.synonyms
        }, indent=4)

