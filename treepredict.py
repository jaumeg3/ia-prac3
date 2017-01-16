import sys
import collections
import pprint
import argparse


def read_file(file_path, data_sep=' ', ignore_first_line=False):
    with open(file_path, 'r') as f:
        return read_stream(f, data_sep, ignore_first_line)


def read_stream(stream, data_sep=' ', ignore_first_line=False):
    rows = []
    reader = (l for l in (ll.strip() for ll in stream) if l)
    for line in reader:
        values = []
        if ignore_first_line:
            ignore_first_line = False
        else:
            for val in line.split(data_sep):
                values.append(filter_token(val.strip()))
            if values:
                rows.append(values)
    return rows        
            

def filter_token(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            pass
    return token

 
# ---------t4--------
def unique_counts(part): 
    # return collections.Counter(row[-1] for row in part)
    counts = {}
    for row in part:
        counts[row[-1]] = counts.get(row[-1], 0) + 1
    return counts

# ---------t5--------
def gini_impurity(part):
    total = float(len(part))
    counts = unique_counts(part)
    probs = (v / total for v in counts.itervalues())
    return 1 - sum((p * p for p in probs))


# -------------t7----------------
def divideset(part, column, value):
    split_fn = lambda x: x[column] == value
    if isinstance(value, (int, float)):
        split_fn = lambda x: x[column] >= value
    set1, set2 = [], []
    for row in part:
        s = set1 if split_fn(row) else set2
        s.append(row)
    return set1, set2


def entropy(rows):
    from math import log
    log2 = lambda x: log(x) / log(2)
    results = unique_counts(rows)
    imp = 0.0
    for x in results:
        imp += -(log2 * x/int(len(results)))
    return imp


# ---- t8 ----
class decisionnode:
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb


# ---- t9 ----
def buildtree(part, scoref=entropy, beta=0):
    if len(part) == 0: return decisionnode()
    current_score = scoref(part)
    # Set up some variables to track the best criteria
    best_gain = 0
    best_criteria = None
    best_sets = None

    atributes = len(part[0])-1

    for col in range(0, atributes):
        values = {}
        for row in part:
            atributes[row[col]] = 1
        for value in values.keys():
            (set1, set2) = divideset(part, col, value)
            p = float(len(set1))/len(part)
            gain = current_score-p*scoref(set1)-(1-p)*scoref(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)
    if best_gain > 0:
        true_branch = buildtree(best_sets[0])
        false_branch = buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0], value=best_criteria[1],
                            tb=true_branch, fb=false_branch)
    else:
        return decisionnode(-1, None, unique_counts(part), None, None)


# ---- t10 ----
#def buildtree_iterative(part, scoref=entropy, beta=0):


# ---- t11 ----
def printtree(tree, indent=''):
    # Is this a leaf node?
    if tree.results != None:
        print str(tree.results)
    else:
        # Print the criteria
        print str(tree.col) + ':' + str(tree.value) + '? '
        # Print the branches
        print indent +'T->', printtree(tree.tb, indent + ' ')
        print indent +'F->', printtree(tree.fb, indent + ' ')


# ---- t12 ----
def classify(obj, tree):
    if tree.results is not None:
        return tree.results
    else:
        v = obj[tree.col]
        if isinstance(v, int) or isinstance(v, float):
            branch = tree.tb if v >= tree.value else branch=tree.fb
        else:
            branch = tree.tb if v == tree.value else branch = tree.fb
    return classify(obj, branch)


# ---- t13 ----
def test_performance(testset, trainingset):
    read_file()

# ---- t15 ----
# Suggest other solutions

# ---- t16 ----
def prune(tree, threshold):

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('prototypes_file', type=str, help="hola que tal")
    parser.add_argument('-ifl', '--ignore_first_line', action='store_true',
                        help='Soy un flag')
    parser.add_argument('-ds', '--data-sep', required=False, default=',',
                        help="")
    opts = parser.parse_args()
    data = read_file(opts.prototypes_file, data_sep=opts.data_sep,
                     ignore_first_line=opts.ignore_first_line)

    sett, setf = divideset(data, 3, 20)
    print "Gini True:", gini_impurity(sett)
    print "Gini False:", gini_impurity(setf)