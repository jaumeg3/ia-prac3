import argparse
import itertools
import random
import sys
import time

import Stack


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
        imp -= p * log2(p)
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

    if best_gain > beta:
        true_branch = buildtree(best_sets[0])
        false_branch = buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0], value=best_criteria[1],
                            tb=true_branch, fb=false_branch)
    else:
        return decisionnode(results=unique_counts(part))


# ---- t10 ----
def build_tree_iterative(part, scoref=entropy, beta=0):
    node = decisionnode()
    warehouse = Stack.Stack()

    warehouse.push(part, node)

    while warehouse.isEmpty() is False:
        column, parent = warehouse.pop()
        current_score = scoref(column)
        best_gain = 0
        best_criteria = None
        best_sets = None
        best_col = -1

        attributes = len(column[0]) - 1
        for col in range(0, attributes):
            values = {}
            for row in column:
                values[row[col]] = 1
            for value in values.keys():
                (set1, set2) = divideset(column, col, value)
                p = float(len(set1)) / len(column)
                gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)
                if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                    best_gain = gain
                    best_criteria = value
                    best_sets = (set1, set2)
                    best_col = col

        if best_gain > beta:
            parent.tb = decisionnode()
            parent.fb = decisionnode()
            parent.value = best_criteria
            parent.col = best_col
            warehouse.push(best_sets[0], parent.tb)
            warehouse.push(best_sets[1], parent.fb)
        else:
            parent.results = unique_counts(column)
    return node


# ---- t11 ----
def printtree(tree, indent=''):
    # Is this a leaf node?

    if tree.results != None:
        print str(tree.results)
    else:
        # Print the criteria
        print str(tree.col) + ':' + str(tree.value) + '? '

        # Print the branches
        print indent + 'T->',
        printtree(tree.tb, indent + ' ')
        print indent + 'F->',
        printtree(tree.fb, indent + ' ')


# ---- t12 ----
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
def test_performance(testset, trainingset):
    trained = buildtree(trainingset)
    good = 0.0
    for x in testset:
        result = classify(x, trained)
        if result.get(str(x[-1])) is not None:
            good += 1.0
    return str(good/len(testset)*100)


# ---- t15 ----
"""
Another solution that we can do is:
    - Discard instances: Simply discarding instances with missing values.
    -
"""


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


# -- Auxiliary Functions --

def create_sets(tan):
    if not 0.0 < tan < 1.0:
        print "Error: The percentage must be a number between 0.0 and 1.0"
        sys.exit(-1)
    else:
        random.seed(options.seed)
        random.shuffle(data)
        percentage = int(len(data)*tan)
        return data[:percentage], data[percentage:]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="---- DESCRIPTION HERE ----",
        epilog="---- EPILOG HERE ----")

    parser.add_argument('prototypes_file', type=argparse.FileType('r'),
                        help="File filled with prototypes (one per line)")

    parser.add_argument('-ifl', '--ignore_first_line', action='store_true',
                        help="Ignores the first line of the prototypes file")

    parser.add_argument('-ds', '--data_sep', required=False, default=',',
                        help="Prototypes data fields separation mark")

    parser.add_argument('-s', '--seed', default=int(time.time()), type=int,
                        help="Random number generator seed.")

    parser.add_argument('-p', '--percentage', default=0.75, type=float,
                        help="Percentage of Training Test sets.")

    options = parser.parse_args()

    # Example code
    data = read_stream(options.prototypes_file, options.data_sep, options.ignore_first_line)
    tree = buildtree(data)
    #tree2 = build_tree_iterative(data)
    #print (" ")
    #printtree(tree)
    #print (" ")
    #printtree(tree2)
    training_set, test_set = create_sets(options.percentage)
    print test_performance(test_set, training_set)

