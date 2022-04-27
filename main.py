import sys
import csv, os

from attr import frozen


def load_csv(dataset_name):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '{}'.format(dataset_name)),
              newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')

        data = []
        for row in datareader:
            data.append(set(row))
        # print("Finished data loading.")
        return data


def get_frequency_set(data, min_sup):
    L_frequent_item = []
    support_data = dict()
    sorted_supp = []
    L_k = [frozenset()]

    items = set().union(*data)  # All elements in data which don't repeat

    # Generate deeper (k-1) frequency itemsets until we can't find more L_k
    n = 0
    while len(L_k) > 0:
        n = n + 1
        if n == 1:
            L_candidates = [frozenset([item]) for item in items]
            final_candi = [frozenset([item]) for item in items]
        else:
            L_candidates = set()
            final_candi = set()
            for L_1 in L_k:
                for L_2 in L_k:
                    for item in L_2:
                        diff_ele = L_2.difference(set([item]))  # Return elements in L_2 but not in item
                        if diff_ele.issubset(L_1):  # If L_1 has these elements
                            r = frozenset(L_1.union(set([item])))
                            if r not in L_candidates:
                                L_candidates.add(r)

            # Use pruning to remove the candidates that are not in L_k
            for candidate in set(L_candidates):
                prune_flage = 0
                subsets = [candidate.difference([elem]) for elem in candidate]
                for item in subsets:
                    if item not in L_k:
                        prune_flage = 1
                        break
                if prune_flage == 0:
                    final_candi.add(candidate)

<<<<<<< HEAD
        # Initialize candidate:frequency dictionary (f = 0)
        candidates_freqs = dict()
        for candidate in final_candi:
            candidates_freqs[candidate] = 0
        # Update each candidate's frequency
=======
        candidates_freqs = {candidate: 0 for candidate in list(final_candi)}
>>>>>>> 291523c174adb70252d5862a9b8643b038a02db4
        for item in data:
            for candidate in final_candi:
                if candidate.issubset(item):
                    candidates_freqs[candidate] = candidates_freqs[candidate] + 1
<<<<<<< HEAD
        candidates_support = {candidate:(candidates_freqs[candidate]/len(data)) for candidate in final_candi}
=======

        candidates_support = {candidate: (candidates_freqs[candidate] / len(data)) for candidate in final_candi}
>>>>>>> 291523c174adb70252d5862a9b8643b038a02db4

        # Keep the candidate frequency sets whose support value >= min_sup
        L_k = [candidate for candidate in final_candi if candidates_support[candidate] >= min_sup]
        # L_frequent = L_frequent.union(L_k)
        support_data.update({k: v for k, v in candidates_support.items() if k in set(L_k)})

    L_sorted = sorted(support_data.items(), key=lambda item: item[1], reverse=True)
    L_frequent_item = []
    sorted_supp = []
    for s in L_sorted:
        flag = 0
        temp_list = []
        frozen_set = s[0]
        for i in frozen_set:
            if i == '':
                flag = 1
                break
            temp_list.append(i)
        if flag == 0:
            L_frequent_item.append(temp_list)
            sorted_supp.append(s[1])
<<<<<<< HEAD
    return L_frequent_item, sorted_supp, support_data

def get_association_rules(L_frequent_item, support_data, min_supp, min_conf):
    rules = []
    for item in L_frequent_item:
        # print("L_f: ", L_frequent_item)
        item = set(item)
        sub_sets = [(item.difference([elem]), set([elem])) for elem in item]
        # print("subs: ", subs)
        if set() not in sub_sets[0]:
            for s in sub_sets: # Each subset
                rule_left = s[0]
                rule_right = s[1]
                supp_left = support_data[frozenset(rule_left)]
                supp_whole = support_data[frozenset(item)]
                conf = supp_whole / supp_left
                if conf > min_conf:
                    rules.append([rule_left, rule_right, conf, supp_whole])
    print(rules)

    return rules
    
=======
    return L_frequent_item, sorted_supp


>>>>>>> 291523c174adb70252d5862a9b8643b038a02db4
def main():
    # Input arguments format: <target dataset> <min_sup> <min_conf>
    dataset = sys.argv[1]  # Expected input: 'INTEGRATED-DATASET.csv'
    min_sup, min_conf = float(sys.argv[2]), float(sys.argv[3])  # Expected input: 0.01, 0.5

    # Load data from target dataset
    data = load_csv(dataset)
    print(data)

    # 1. Get sorted frequent itemsets by Apriori algorithm
    L_frequent_item, sorted_supp, support_data = get_frequency_set(data, min_sup)

    # 2. Output frequent itemsets as required format
<<<<<<< HEAD
    print("==Frequent itemsets (min_sup="+str(min_sup*100)+"%)")
    for idx, item in enumerate(L_frequent_item):
        supp = sorted_supp[idx]
        print( str(item) + ', ' + str(int(supp*100)) +"%)")

    # TODO: Get association rules
    # 3. Get and print association rules by Apriori algorithm
    rules = get_association_rules(L_frequent_item, support_data, min_sup, min_conf)
    print("==High-confidence association rules (min_conf="+str(min_conf*100)+"%)")
    for rule in rules:
        print(list(rule[0]), '=>', list(rule[1]), '(Conf: ', str(int(rule[2]*100)), '%, Supp :', str(int(rule[3]*100)), '%)')

=======
    print("==Frequent itemsets (min_sup=" + str(min_sup * 100) + "%)\n")
    for idx, item in enumerate(L_frequent_item):
        supp = sorted_supp[idx]
        print(str(item) + ', ' + str(int(supp * 100)) + "%)\n")

    # TODO: Get association rules
    # 3. Get and print association rules by Apriori algorithm
    print("==High-confidence association rules (min_conf=" + str(min_conf * 100) + "%)\n")
>>>>>>> 291523c174adb70252d5862a9b8643b038a02db4


if __name__ == '__main__':
    main()
