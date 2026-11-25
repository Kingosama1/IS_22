from math import ceil

from data_loader import load_transactions_from_excel
from FP_Tree import *
from FP_Growth import *


experiments = [
    
    (0.40, 0.60),
    (0.60, 0.80)
    (0.80, 0.90)
]

def main():
    # read excel
    try:
        baskets, receiptIds = load_transactions_from_excel()
    except FileNotFoundError:
        print("Excel file missing.")
        return
    except Exception as e:
        print("Error reading sheet: %s" % e)
        return

    if not baskets or len(baskets) != len(receiptIds):
        print("Data mismatch or empty.")
        return

    freqs = getFreqs(baskets)  
          
    print("Transactions:", baskets)
    print("\nTransaction IDs:", receiptIds)

    # task 3
    #print("\nSupport Counts:", freqs)

    for exp_no, (MIN_SUP, min_conf) in enumerate(experiments, 1):

        print("\nExperiment:", exp_no)
        print("MinSup:", MIN_SUP)
        print("MinCon:", min_conf)

        min_cnt = ceil(MIN_SUP * len(baskets))

        
        valid_items = filter_items(freqs, min_cnt)
        print("\nFrequent Items (min sup = %d/%d):" % (min_cnt, len(baskets)))
        print(valid_items)

        ranked = rankItems(valid_items)
        print("\nSorted Frequent Items:", ranked)

        cleaned = prep_baskets(baskets, ranked)

        print("\nRearranged Transactions (top 5):")
        for i in range(min(5, len(cleaned))):
            print("[%s] -> %s" % (receiptIds[i], cleaned[i]))

        tRoot, hdr = build_tree(cleaned, ranked)

        print("\nFP-Tree:\nRoot")
        printTree(tRoot)

        patterns = mineTree(hdr, min_cnt)

        print("\nFrequent Itemsets:")
        # group by size
        sizes = sorted({len(b) for b in patterns})
        for sz in sizes:
            print("\nL%d:" % sz)
            for bundle, hits in patterns.items():
                if len(bundle) == sz: print("  %s -> count: %d" % (bundle, hits))

        rules = get_rules(patterns, len(baskets))

        print("\nAssociation Rules:")
        if not rules:
            print("No rules found.")
        else:
            for lhs, rhs, sup, conf, lift in rules:
                flag_str = " [STRONG]" if conf >= min_conf else ""
                print("%s -> %s | Support: %.2f | Confidence: %.2f | Lift: %.2f%s" % (lhs, rhs, sup, conf, lift, flag_str))
        print("\nStrong Association Rules:")
        found_strong = False

        for lhs, rhs, sup, conf, lift in rules:
            if conf >= min_conf:
                print(
                    "%s -> %s | Support: %.2f | Confidence: %.2f | Lift: %.2f"
                    % (lhs, rhs, sup, conf, lift)
                )
                found_strong = True
        if not found_strong:
            print("No strong rules found.")

#----------------------------------------------------------------------------    
if __name__ == "__main__":
    main()