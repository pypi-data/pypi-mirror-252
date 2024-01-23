# All the packages that we need to import
import numpy as np               # for linear algebra
import pandas as pd              # for tabular output
from scipy.stats import rankdata # for ranking the candidates
import sys

# The given data encoded into vectors and matrices

if __name__ == "__main__":
    # Check if a filename is provided in the command line arguments
    if len(sys.argv) != 5:
        print("File not found")
        sys.exit(1)

    # Get the datafile from the command line arguments
    data = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    result = sys.argv[4]

    values = [int(value) for value in weights.split(',')]
    impact = [1 if char == '+' else -1 for char in impacts.split(',')]

    # Convert the list of integers to a NumPy array
    weights = np.array(values)
    impacts = np.array(impact)
    # impacts = sys.argv[3]

    attributes = np.array(["P1","P2","P3","P4","P5"])
    candidates = np.array(["0","1","2","3","4","5","6","7"])
    data = pd.read_excel(data)
    data.to_csv ("102153030-data.csv",  index = None,header=True) 
    raw_data = pd.read_csv('102153030-data.csv')
    # read csv file and convert  
    # into a dataframe object 


    # raw_data = np.array([
    #     [0.88,	0.77,	3.3,	50,	13.74],
    #     [0.93,	0.86,	5.9,	44.8,	13.12],
    #     [0.73,	0.53,	3.2,	45.2,	12.42],
    #     [0.75,	0.56,	4.6,	64.3,	17.55],
    #     [0.73,	0.53,	4.6,	36.7,	10.64],
    #     [0.67,	0.45,	3.8,	34.7,	9.91],
    #     [0.9,	0.81,	4,	49.5,	13.8],
    #     [0.81,	0.66,	4.2,	58.4,	16.02],
    # ])

    df=raw_data.drop(columns=['Fund Name'])
    raw_data=df.to_numpy()
    print(raw_data)
    # weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

    # The indices of the attributes (zero-based) that are considered beneficial.
    # Those indices not mentioned are assumed to be cost attributes.
    benefit_attributes = set([0, 1, 2, 3, 4])

    # Display the raw data we have
    pd.DataFrame(data=raw_data, index=candidates, columns=attributes)

    m = len(raw_data)
    n = len(attributes)
    divisors = np.empty(n)
    for j in range(n):
        column = raw_data[:,j]
        divisors[j] = np.sqrt(column @ column)

    raw_data /= divisors

    columns = ["$X_{%d}$" % j for j in range(n)]
    pd.DataFrame(data=raw_data, index=candidates, columns=columns)

    raw_data *= (weights*impacts)
    pd.DataFrame(data=raw_data, index=candidates, columns=columns)

    a_pos = np.zeros(n)
    a_neg = np.zeros(n)
    for j in range(n):
        column = raw_data[:,j]
        max_val = np.max(column)
        min_val = np.min(column)
        
        # See if we want to maximize benefit or minimize cost (for PIS)
        if j in benefit_attributes:
            a_pos[j] = max_val
            a_neg[j] = min_val
        else:
            a_pos[j] = min_val
            a_neg[j] = max_val

    pd.DataFrame(data=[a_pos, a_neg], index=["$A^*$", "$A^-$"], columns=columns)

    sp = np.zeros(m)
    sn = np.zeros(m)
    cs = np.zeros(m)

    for i in range(m):
        diff_pos = raw_data[i] - a_pos
        diff_neg = raw_data[i] - a_neg
        sp[i] = np.sqrt(diff_pos @ diff_pos)
        sn[i] = np.sqrt(diff_neg @ diff_neg)
        cs[i] = sn[i] / (sp[i] + sn[i])

    pd.DataFrame(data=zip(sp, sn, cs), index=candidates, columns=["$S^*$", "$S^-$", "$C^*$"])

    def rank_according_to(data):
        ranks = rankdata(data).astype(int)
        ranks -= 1
        return candidates[ranks][::-1]

    cs_order = rank_according_to(cs)
    sp_order = rank_according_to(sp)
    sn_order = rank_according_to(sn)

    pd.DataFrame(data=zip(cs_order, sp_order, sn_order), index=range(1, m + 1), columns=["$C^*$", "$S^*$", "$S^-$"])

    print("The best candidate/alternative according to C* is " + cs_order[0])
    print("The preferences in descending order are " + ", ".join(cs_order) + ".")

    ranks = [int(rank) for rank in cs_order]
    order = []
    for i in range (0,len(ranks)):
        for j in range (0,len(ranks)):
            if ranks[j]==i :
                order.append(j+1)

    df = data.assign(Rank=[int(rank) for rank in order])
    df.to_csv(result)
    