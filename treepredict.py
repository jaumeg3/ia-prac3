import argparse
import collections
import itertools
import sys
import time


def read_file(file_path, data_sep=' ', ignore_first_line=False):
    with open(file_path, 'r') as f:
        return read_stream(f, data_sep, ignore_first_line)


def read_stream(stream, data_sep=' ', ignore_first_line=False):
    strip_reader = (l.strip() for l in stream)
    filtered_reader = (l for l in strip_reader if l)
    start_at = 1 if ignore_first_line else 0

    prototypes = []
    for line in itertools.islice(filtered_reader, start_at, None):
        tokens = itertools.imap(str.strip, line.split(data_sep))
        prototypes.append(map(filter_token, tokens))

    return prototypes


def filter_token(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
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
    # split_function = None
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row: row[column] >= value
    else:
        split_function = lambda row: row[column] == value

    set1 = [row for row in part if split_function(row)]
    set2 = [row for row in part if not split_function(row)]
    return set1, set2


def entropy(rows):
    from math import log
    log2 = lambda x: log(x) / log(2)
    results = unique_counts(rows)
    imp = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        imp = imp - p * log2(p)
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

    attributes = len(part[0]) - 1

    for col in range(0, attributes):
        values = {}
        for row in part:
            values[row[col]] = 1
        for value in values.keys():
            (set1, set2) = divideset(part, col, value)
            p = float(len(set1)) / len(part)
            gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)
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
# def buildtree_iterative(part, scoref=entropy, beta=0):


# ---- t11 ----
def printtree(tree, indent=''):
    # Is this a leaf node?
    if tree.results is not None:
        print(str(tree.results))
    else:
        # Print the criteria
        print(str(tree.col) + ':' + str(tree.value) + '? ')
        # Print the branches
        print(indent + 'T->', printtree(tree.tb, indent + ' '))
        print(indent + 'F->', printtree(tree.fb, indent + ' '))


#---- t12 ----
def classify(obj, tree):
    if tree.results is not None:
        return tree.results
    else:
        v = obj[tree.col]
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        else:
            if v == tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        return classify(obj, branch)


# ---- t13 ----
#def test_performance(testset, trainingset):
#    read_file()


# ---- t15 ----
# Suggest other solutions

# ---- t16 ----
def prune(tree, threshold):
    # If the branches aren't leaves, then prune them
    if tree.tb.results is None:
        prune(tree.tb, threshold)
    if tree.fb.results is None:
        prune(tree.fb, threshold)

    if tree.tb.results is not None and tree.fb.results is not None:
        tb, fb = [], []
        for v, c in tree.tb.results.items():
            tb += [[v]] * c
        for v, c in tree.fb.results.items():
            fb += [[v]] * c

        delta = entropy(tb + fb) - (entropy(tb) + entropy(fb) / 2)

        if delta < threshold:
            tree.tb, tree.fb = None, None
            tree.results = unique_counts(tb + fb)


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
    print("Gini True:", gini_impurity(sett))
    print("Gini False:", gini_impurity(setf))
    protos = read_file(opts.prototypes_file, opts.data_sep)
    for p in protos:
        print(p)
    print(unique_counts(protos))
    tree = buildtree(protos)

    print(" ")
    printtree(tree)
