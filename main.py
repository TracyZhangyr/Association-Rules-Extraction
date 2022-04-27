import sys
import csv, os

def load_csv(dataset_name):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '{}'.format(dataset_name)), newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        next(datareader)

        data = []
        for row in datareader:
            data.append(set(row))
        # print("Finished data loading.")
        return data

def get_frequency_set(data, min_sup):
    items = set().union(*data) # All elements in data which don't repeat
    L_frequent = set()
    L_frequent_item = []
    support_data = dict()
    sorted_supp = []
    L_k = [frozenset()]

    # Generate deeper (k-1) frequency itemsets until we can't find more L_k
    n = 0
    while len(L_k) > 0:
        # L_k.remove(frozenset({''}))
        n = n + 1
        # if L_k == [frozenset()]:
        if n == 1:
            L_candidates = [frozenset([item]) for item in items]
        else: 
            L_candidates = set()
            for L_1 in L_k:
                for L_2 in L_k:
                    for item in L_2:
                        diff_ele = L_2.difference(set([item]))
                        if diff_ele.issubset(L_1):
                            r = frozenset(L_1.union(set([item])))
                            if r not in L_candidates:
                                L_candidates.add(r)
            for candidate in set(L_candidates):
                subsets = [candidate.difference([elem]) for elem in candidate]
                for item in subsets:
                    if item not in L_k:
                        L_candidates.remove(candidate)
                        break
 
        candidates_freqs = {candidate:0 for candidate in list(L_candidates)}
        for item in data:
            for candidate in L_candidates:
                if candidate.issubset(item):
                    candidates_freqs[candidate] = candidates_freqs[candidate] + 1

        candidates_support = {candidate:(candidates_freqs[candidate]/len(data)) for candidate in L_candidates}

        # Keep the candidate frequency sets whose support value >= min_sup
        L_k = [candidate for candidate in L_candidates if candidates_support[candidate] >= min_sup]
        L_frequent = L_frequent.union(L_k)
        support_data.update({k:v for k, v in candidates_support.items() if k in set(L_k)})
    
    L_sorted = sorted(support_data.items(), key=lambda item:item[1], reverse=True)
    L_frequent_item = []
    sorted_supp = []
    for s in L_sorted:
        flag = 0
        temp_list = []
        frozen_set = s[0]
        for i in frozen_set:
            print(i)
            if i == '':
                flag = 1
                break
            temp_list.append(i)
        if flag == 0:
            L_frequent_item.append(temp_list)
            sorted_supp.append(s[1])
    return L_frequent_item, sorted_supp

def main():
    
    # Input arguments format: <target dataset> <min_sup> <min_conf>
    # dataset = sys.argv[1] # Expected input: 'INTEGRATED-DATASET.csv'
    dataset = 'INTEGRATED-DATASET.csv'
    # min_sup, min_conf = float(sys.argv[2]), float(sys.argv[3]) # Expected input: 0.01, 0.5
    min_sup = 0.2
    min_conf = 0.5

    # Load data from target dataset
    data = load_csv(dataset)

    # 1. Get sorted frequent itemsets by Apriori algorithm
    L_frequent_item, sorted_supp = get_frequency_set(data, min_sup)

    # 2. Output frequent itemsets as required format
    print("==Frequent itemsets (min_sup="+str(min_sup*100)+"%)\n")
    for idx, item in enumerate(L_frequent_item):
        supp = sorted_supp[idx]
        print( str(item) + ', ' + str(int(supp*100)) +"%)\n")

    # TODO: Get association rules
    # 3. Get and print association rules by Apriori algorithm
    print("==High-confidence association rules (min_conf="+str(min_conf*100)+"%)\n")


if __name__ == '__main__':
    main()