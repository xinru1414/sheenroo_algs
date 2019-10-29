from allennlp import pretrained
from functools import lru_cache
from typing import Dict, List


@lru_cache(maxsize=1)
def get_coref_model():
    return pretrained.neural_coreference_resolution_lee_2017()


def coref(file):
    model = get_coref_model()
    results = model.predict(document=file)
    return results


def char_sent(coref: Dict[str, List], parse: List[Dict]) -> Dict:
    sents_indicies = dict()
    for item in max(coref['clusters'], key=len):
        if item[0] == item[1]:
            token = coref['document'][item[0]]
            for i, sent in enumerate(parse):
                if token in parse[i]['tokens']:
                    if token in sents_indicies:
                        if i not in sents_indicies[token]:
                            sents_indicies[token].append(i)
                    else:
                        sents_indicies[token] = [i]
        else:
            token_begin = coref['document'][item[0]]
            token_end = coref['document'][item[1]]
            for i, sent in enumerate(parse):
                if token_begin in parse[i]['tokens'] and token_end in parse[i]['tokens']:
                    if token_end in sents_indicies:
                        if i not in sents_indicies[token_end]:
                            sents_indicies[token_end].append(i)
                        else:
                            sents_indicies[token_end] = [i]
    return sents_indicies