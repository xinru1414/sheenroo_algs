from typing import Set


def map_tree(root, func, max_depth=9999999):
    results = []
    kids = [(root, 0)]
    while kids:
        node, depth = kids.pop()
        results += [func(node)]
        if depth < max_depth:
            kids += [(c, depth+1) for c in node.get('children', [])]
    return results


def filter_tree(root, func, max_depth=9999999):
    results = []
    kids = [(root, 0)]
    while kids:
        node, depth = kids.pop()
        if func(node):
            results += [node]
        if depth < max_depth:
            kids += [(c, depth+1) for c in node.get('children', [])]
    return results


def filter_tree_with_path(root, func, max_depth=9999999):
    results = []
    kids = [(root, [])]
    while kids:
        kid, path = kids.pop()
        if func(kid):
            results += [(kid, path)]
        if len(path) < max_depth:
            kids += [(x, [kid] + path) for x in kid.get('children', [])]
    return results


def get_all_text_for_dep_tree(tree):
    l = map_tree(tree, lambda n: (n.get('spans')[0]['start'], n.get('word', '')))
    return ' '.join(x[1] for x in sorted(l))


def get_shortened_text_for_dep_tree(tree, attributes: Set[str], max_depth=1):
    mapped_l = map_tree(tree, lambda n: (n.get('spans')[0]['start'], n.get('word', ''), n.get('nodeType', '')), max_depth=max_depth)
    filtered_l = filter(lambda x: x[2] in attributes, mapped_l)
    return ' '.join(x[1] for x in sorted(filtered_l))
