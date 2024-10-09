class StoryException(Exception):
    def __init__(self, name: str):
        self.name = name

class TermsViolationException(Exception):
    def __init__(self, detail: str):
        self.detail = detail