import re


# VBD past tense verb claimed
# VBZ 3rd person singular present tense verb is
# VBP non-3rd person singular present tense verb have
# VBN past participle found
# VB	Verb, base form
# VBG	Verb, gerund or present participle
def is_verb(label):
    if re.match(r'^VB.?$', label):
        return True
    return False


assert is_verb('VB')
assert is_verb('VBD')
assert is_verb('VBZ')
assert is_verb('VBP')
assert is_verb('VBN')
assert is_verb('VBG')
assert not is_verb('VP')
assert not is_verb('NP')