import pytest

from sheenroo_algs.allennlp.verbs import is_verb


@pytest.mark.parametrize('label, is_label_verb', [
    ('VB', True),
    ('VBD', True),
    ('VBZ', True),
    ('VBP', True),
    ('VBN', True),
    ('VBG', True),
    ('VP', False),
    ('NP', False),
])
def test_is_verb(label, is_label_verb):
    if is_label_verb:
        assert is_verb(label)
    else:
        assert not is_verb(label)
