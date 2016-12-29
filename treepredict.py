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

 
#---------t4--------
def unique_counts(part): 
    return collections.Counter(row[-1] for row in part)


#---------t5--------
def gini_impurity(part):
    total = float(len(part))
    results = unique_counts(part)
    addSquare = 0 
    for item in results:
        div = results[item]/total 
        addSquare = addSquare + (div*div)
    
    return 1 - addSquare

#-------------t7----------------
def divideset(part, column, value):
    split_fn = lambda x: x[column] == value
    if isinstance(value, (int, float)):
        split_fn = lambda x: x[column] >= value
    
    set1, set2 = [], []
    
    for row in part:
        s = set1 if split_fn(row) else set2
        s.append(row)

    return set1, set2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('prototypes_file', type=str, help="hola que tal")
    parser.add_argument('-ifl', '--ignore_first_line', action='store_true',
        help='Soy un flag')
    parser.add_argument('-ds', '--data-sep', required=False, default=',',                help="")
    opts = parser.parse_args()
    data = read_file(opts.prototypes_file, data_sep=opts.data_sep, ignore_first_line=opts.ignore_first_line)

    sett, setf = divideset(data, 3, 20)
    print "Gini True:", gini_impurity(sett)
    print "Gini False:", gini_impurity(setf) 
