import sys
import csv, os
from operator import itemgetter


def load_csv(dataset_name):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '{}'.format(dataset_name)),
              newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        data = []
        for row in datareader:
            data.append(set(row))
        # print("Finished data loading.")
        return data


def get_frequency_set(data):
    support_data = dict()
    L_k = [frozenset()]
    data_size = len(data)

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
                    if not set(L_2).issubset(L_1):
                        r = frozenset(set(L_2).union(L_1))
                        if r not in L_candidates:
                            L_candidates.add(r)

            # Use pruning to remove the candidates that are not in L_k
            for candidate in set(L_candidates):
                subsets = [candidate.difference([elem]) for elem in candidate]
                if not any(item not in L_k for item in subsets):
                    final_candi.add(candidate)

        # Initialize candidate:frequency dictionary (f = 0)
        candi_freq = dict()
        for candidate in final_candi:
            candi_freq[candidate] = 0

        # Update each candidate's frequency
        for item in data:
            for candidate in final_candi:
                if candidate.issubset(item):
                    candi_freq[candidate] = candi_freq[candidate] + 1

        candidates_support = {candidate: (candi_freq[candidate] / data_size) for candidate in final_candi}

        # Keep the candidate frequency sets whose support value >= min_sup
        L_k = [candidate for candidate in final_candi if candidates_support[candidate] >= min_sup]
        support_data.update({k: v for k, v in candidates_support.items() if k in set(L_k)})

    # Get frequent itemsets with their sorted support in decreasing order
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

    return L_frequent_item, sorted_supp, support_data


def get_association_rules(L_frequent_item, support_data):
    rules = []
    for item in L_frequent_item:
        item = set(item)
        sub_sets = [(item.difference([elem]), set([elem])) for elem in item]
        if set() not in sub_sets[0]:
            for s in sub_sets:  # Each subset
                rule_left = s[0]
                rule_right = s[1]
                supp_left = support_data[frozenset(rule_left)]
                supp_whole = support_data[frozenset(item)]
                conf = supp_whole / supp_left
                if conf > min_conf:
                    rules.append([rule_left, rule_right, conf, supp_whole])
    # print(rules)
    rules.sort(key=itemgetter(2), reverse=True)
    return rules


def main():
    # Input arguments format: <target dataset> <min_sup> <min_conf>
    dataset = sys.argv[1]  # Expected input: 'INTEGRATED-DATASET.csv'
    global min_sup, min_conf
    min_sup, min_conf = float(sys.argv[2]), float(sys.argv[3])  # Expected input: 0.01, 0.5

    # Load data from target dataset
    data = load_csv(dataset)

    # 1. Get sorted frequent itemsets by Apriori algorithm
    L_frequent_item, sorted_supp, support_data = get_frequency_set(data)

    # 2. Get association rules by Apriori algorithm
    rules = get_association_rules(L_frequent_item, support_data)

    # 3. Output frequent itemsets and high-confidence association rules to output.txt
    with open('output.txt', 'w') as file:
        file.write("==Frequent itemsets (min_sup=" + str(min_sup * 100) + "%)\n")
        for idx, item in enumerate(L_frequent_item):
            supp = sorted_supp[idx]
            file.write(str(item) + ', ' + str(int(supp * 100)) + "%\n")

        file.write("==High-confidence association rules (min_conf=" + str(min_conf * 100) + "%)\n")
        for rule in rules:
            file.write('{0} => {1} (Conf: {2}%, Supp: {3}%)\n'.format(str(list(rule[0])), str(list(rule[1])),
                                                                      str(int(rule[2] * 100)), str(int(rule[3] * 100))))


if __name__ == '__main__':
    main()
