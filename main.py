import sys
import csv, os

def load_csv(dataset_name):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '{}'.format(dataset_name)), newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        next(datareader)

        data = []
        for row in datareader:
            data.append(set(row))
        return data

def get_frequency_set(data, min_sup):

    items = set().union(*data)
    L_frequent = set()
    support_data = dict()
    L_k = [frozenset()]

    # Generate deeper (k-1) frequency itemsets until we can't find more L_k
    while len(L_k) != 0:
        if L_k == [frozenset()]:
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

    return L_frequent, support_data

def main():
    
    # Input arguments format: <target dataset> <min_sup> <min_conf>
    dataset = sys.argv[1] # Expected input: 'INTEGRATED-DATASET.csv'
    min_sup, min_conf = float(sys.argv[2]), float(sys.argv[3]) # Expected input: 0.01, 0.5

    # Load data from target dataset
    data = load_csv(dataset)

    # 1. Get and print frequent itemsets by Apriori algorithm
    print("==Frequent itemsets (min_sup="+str(min_sup*100)+"%)\n")

    L_frequent, support_data = get_frequency_set(data, min_sup)
    L_frequent = sorted(L_frequent, key=lambda x: support_data[x], reverse=True)
    for item in L_frequent.items():
        print(item + ', ' + str(support_data[item]*100) +"%)\n")

    # TODO: Get association rules
    # 2. Get and print association rules by Apriori algorithm
    print("==High-confidence association rules (min_conf="+str(min_conf*100)+"%)\n")


if __name__ == '__main__':
    main()