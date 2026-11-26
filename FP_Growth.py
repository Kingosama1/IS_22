from itertools import combinations
from FP_Tree import *

def getPrefixes(target, hdr):
    paths_list = []
    curr = hdr[target]['head']
    while curr is not None:
        anc = []
        up_node = curr.parent
        while up_node is not None and up_node.item is not None:
            anc.append(up_node.item)
            up_node = up_node.parent
        anc.reverse()
        if len(anc) > 0: paths_list.append((anc, curr.count))
        curr = curr.node_link
    return paths_list

def make_subtree(paths_list, min_cnt):
    cnts={}
    for p, w in paths_list:
        for k in p: cnts[k] = cnts.get(k, 0) + w

    keptItems = {k: c for k, c in cnts.items() if c >= min_cnt}
    if not keptItems: return None, None

    ordered = sorted(keptItems, key=lambda x: (-keptItems[x], str(x)))
    ordMap = {k: i for i, k in enumerate(ordered)}

    sRoot = FPNode(None)
    s_hdr = {}
    for k in ordered: s_hdr[k] = {"support": keptItems[k], "head": None, "tail": None}

    for p, w in paths_list:
        trimmed = [k for k in p if k in keptItems]
        trimmed.sort(key=lambda x: ordMap[x])
        if trimmed: addBasket(sRoot, trimmed, s_hdr, w)
    return sRoot, s_hdr

def mineTree(hdr, min_cnt, prefix=None, out=None):
    if prefix is None: prefix = []
    if out is None: out = {}

    # bottom up
    skus = sorted(hdr, key=lambda x: (hdr[x]["support"], str(x)))
    for k in skus:
        cand_list = prefix + [k]
        out[tuple(sorted(cand_list))] = hdr[k]['support']

        paths_list = getPrefixes(k, hdr)
        sRoot, s_hdr = make_subtree(paths_list, min_cnt)
        if s_hdr: mineTree(s_hdr, min_cnt, cand_list, out)
    return out

# task 5
def get_rules(patterns, total):
    rulesList = []
    if total <= 0: return rulesList

    for bundle, b_hits in patterns.items():
        if len(bundle) < 2: continue
        for sz in range(1, len(bundle)):
            for lhs in combinations(bundle, sz):
                rhs = tuple([x for x in bundle if x not in lhs])
                lHits = patterns[tuple(sorted(lhs))]
                r_hits = patterns[tuple(sorted(rhs))]

                sup = b_hits / total
                conf = b_hits / lHits
                rSup = r_hits / total
                lift = conf / rSup if rSup > 0 else 0.0
                rulesList.append((lhs, rhs, sup, conf, lift))
    return rulesList