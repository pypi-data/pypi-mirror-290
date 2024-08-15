import json

class Code:
    def __init__(self, **kwargs):
        self.prefix = None
        self.system = kwargs.get('system')
        self.code = kwargs.get('code')
        self.display = kwargs.get('display')
        self.synonyms = kwargs.get('synonyms')

    def to_json(self):
        return json.dumps({
            'system': self.system,
            'code': self.code,
            'full_code': self.full_code,
            'display': self.display,
            'synonyms': self.synonyms
        }, indent=4)

    @property
    def full_code(self):
        """ The code with the prefix. E.g. 'OPOR-3412' """
        return f"{self.prefix}-{self.code}"