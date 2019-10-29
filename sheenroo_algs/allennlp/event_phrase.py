from allennlp.predictors.predictor import Predictor
from typing import Dict, List, NamedTuple
from functools import lru_cache

from sheenroo_algs.allennlp.tree import filter_tree_with_path, filter_tree, get_all_text_for_dep_tree, \
    get_shortened_text_for_dep_tree
from sheenroo_algs.allennlp.verbs import is_verb


class PairFlags(NamedTuple):
    negative: bool = False
    passive: bool = False


@lru_cache(maxsize=1)
def get_dep_predictor() -> Predictor:
    return Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/biaffine-dependency-parser-ptb-2018.08.23.tar.gz")


@lru_cache(maxsize=1)
def get_con_predictor() -> Predictor:
    return Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/elmo-constituency-parser-2018.03.14.tar.gz")


def dependency_parse(doc: List[str]) -> List[Dict]:
    predictor = get_dep_predictor()
    results = []
    for sent in doc:
        result = predictor.predict(sentence=sent)
        results.append(result)
    assert len(results) == len(doc)
    return results


def constituency_parse(doc: List[str]) -> List[Dict]:
    """
    parameter: List[str] for each doc
    return: List[Dict] for each doc
    """
    predictor = get_con_predictor()
    results = []
    for sent in doc:
        result = predictor.predict(sentence=sent)
        results.append(result)
    assert len(results) == len(doc)
    return results


def is_node_verb(node):
    return is_verb(node['attributes'][0])


def is_node_conj(node):
    return node['nodeType'] == 'conj'


def is_node_xcomp(node):
    return node['nodeType'] == 'xcomp'


def is_node_dobj(node):
    return node['nodeType'] == 'dobj'


def is_node_prt(node):
    return node['nodeType'] == 'prt'


def is_node_prep(node):
    return node['nodeType'] == 'prep'


def is_node_neg(node):
    return node['nodeType'] == 'neg'


def is_node_pas(node):
    return 'pass' in node['nodeType']


def has_nsubj(node, include_pass=True, max_depth=1):
    node_types = {'nsubj'} | ({'nsubjpass'} if include_pass else set())
    return len(filter_tree(node, lambda x: x['nodeType'] in node_types, max_depth=max_depth)) > 0


def get_dobj(node, details=False):
    dobj = filter_tree(node, lambda x: is_node_dobj(x), max_depth=1)
    if dobj:
        assert len(dobj) >= 1
        if details:
            return get_all_text_for_dep_tree(dobj[0])
        return dobj[0]['word']
    return None


def get_verb_phrase(node):
    verb = node['word']
    prt = filter_tree(node, lambda x: is_node_prt(x), max_depth=1)
    if prt:
        assert len(prt) == 1
        prt = prt[0]['word']
        return f'{verb} {prt}'
    prep = filter_tree(node, lambda x: is_node_prep(x), max_depth=1)
    if prep:
        if len(prep) == 1:
            prep = prep[0]['word']
            return f'{verb} {prep}'
        else:
            return verb
        # assert len(prep) == 1
        # prep = prep[0]['word']
        # return f'{verb} {prep}'
    return verb


def make_pair(subj, verb):
    subj_phrase = get_shortened_text_for_dep_tree(subj, {'nsubj', 'nsubjpass', 'det', 'poss', 'cc', 'conj'})
    vp = get_verb_phrase(verb)
    dobj = get_dobj(verb, details=True)
    negs = filter_tree(verb, is_node_neg, max_depth=1)
    assert len(negs) < 2, f'We don\'t allow double negatives. Found {negs}'
    neg = len(negs) > 0
    passes = filter_tree(verb, is_node_pas, max_depth=1)
    pas = len(passes) > 0
    return subj_phrase, vp, dobj, PairFlags(negative=neg, passive=pas)


def get_svo_detail_pairs_sent(sent):
    dep_parsed_sent = dependency_parse([sent])[0]
    root = dep_parsed_sent['hierplane_tree']['root']
    results = filter_tree_with_path(root, lambda x: x['nodeType'].startswith('nsubj'))
    pairs = set()
    for subj, path in results:
        verbs = []
        parent = path[0]
        if is_node_verb(parent):
            verbs = [parent]
        seen = []
        while verbs:
            verb = verbs.pop()
            if verb in seen:
                continue
            seen += [verb]
            pairs.add(make_pair(subj, verb))
            verbs += filter_tree(verb, lambda x: is_node_conj(x) and is_node_verb(x) and not has_nsubj(x),
                                     max_depth=1)
            verbs += filter_tree(verb, lambda x: is_node_xcomp(x) and is_node_verb(x) and not has_nsubj(x),
                                      max_depth=1)
    return pairs
