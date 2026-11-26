def getFreqs(trans):
    if not trans: return {}
    freqs={}
    for row in trans:
        # clean empty cells
        items = {str(x).strip() for x in row if x and str(x).strip()}
        for k in items: freqs[k] = freqs.get(k, 0) + 1
    return freqs

def filter_items(freqMap, min_cnt):
    res1 = {}
    for k in freqMap:
        val = freqMap[k]
        if val >= min_cnt: res1[k] = val
    return res1

def rankItems(valid_items):
    pairs_list = list(valid_items.items())
    # sort desc
    pairs_list.sort(key=lambda e: (-e[1], str(e[0])))
    return dict(pairs_list)

def prep_baskets(baskets, ranked):
    rankMap = {k: i for i, k in enumerate(ranked)}
    outlist = []
    for row in baskets:
        tmp_arr = []
        seenSet = set()
        for raw in row:
            s = str(raw).strip() if raw else ""
            if s in rankMap and s not in seenSet:
                tmp_arr.append(s)
                seenSet.add(s)
        tmp_arr.sort(key=lambda x: rankMap[x])
        outlist.append(tmp_arr)
    return outlist

class FPNode:
    def __init__(self, item, parent=None):
        self.item = item
        self.count = 0
        self.parent = parent
        self.children = {}
        self.node_link = None



def addBasket(tRoot, basket, hdr, w=1):
    curr = tRoot
    for k in basket:
        if k in curr.children:
            node = curr.children[k]
            node.count += w
        else:
            node = FPNode(k, curr)
            node.count = w
            curr.children[k] = node
            # link nodes
            if hdr[k]['head'] is None:
                hdr[k]['head'] = node; hdr[k]['tail'] = node
            else:
                hdr[k]['tail'].node_link = node; hdr[k]['tail'] = node
        curr = node

def build_tree(baskets, ranked):
    tRoot = FPNode(None)
    hdr={}
    for k, sup in ranked.items(): hdr[k] = {"support": sup, "head": None, "tail": None}

    for b in baskets:
        if len(b) > 0: addBasket(tRoot, b, hdr)
    return tRoot, hdr

def printTree(node, depth=0):
    if node is None: return
    for ch in node.children.values():
        pad_str = "  " * depth
        print("%s%s: %d" % (pad_str, ch.item, ch.count))
        printTree(ch, depth + 1)