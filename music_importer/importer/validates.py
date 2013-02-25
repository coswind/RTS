import re, HTMLParser

def validate_meta(meta):
    for rule in RULES:
        if not rule().validate(meta):
            return False
    return True

class Rule(object):

    def validate(self, meta):
        return True

class EmptyNameRule(Rule):

    def validate(self, meta):
        return '' != meta['song']['name'] and '' != meta['album']['name'] and '' != meta['artist']['name']

RULES = [EmptyNameRule]
