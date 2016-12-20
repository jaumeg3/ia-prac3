#! /usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import re
# import math


# ---- t1 ----
def getwords(document):
    splitter = re.compile(r'\W*')
    words = filter(lambda x: 2 < len(x) < 20, splitter.split(document))
    return {w.lower() for w in words}


# ---- t2 ----
class classifier(object):

    def __init__(self, get_features):
        self.fc = {}  # feature/category combinations
        self.cc = {}  # documents in each category
        self.get_features = get_features

    # ---- t3 ----
    def incf(self, feature, category):
        self.fc.setdefault(feature, {})
        self.fc[feature].setdefault(category, 0)
        self.fc[feature][category] += 1

    def incc(self, category):
        self.cc.setdefault(category, 0)
        self.cc[category] += 1

    def fcount(self, feature, category):
        if feature in self.fc and category in self.fc[feature]:
            return float(self.fc[feature][category])
        return 0.0

    def catcount(self, category):
        return float(self.cc[category]) if category in self.cc else 0.0

    def totalcount(self):
        total = 0
        for f in self.fc:
            for c in self.fc[f]:
                total += self.fc[f][c]
        return total

    def categories(self):
        return self.cc.keys()

    # ---- t4 ----
    def train(self, item, category):
        feature = self.get_features(item)
        for f in feature:
            self.incf(f, category)
        self.incc(category)

    # ---- t6 ----
    def fprob(self, feature, category):
        return self.fcount(feature, category) / self.catcount(category) \
            if self.catcount(category) != 0.0 else 0.0

    # ---- t8 ----
    def weightedprob(self, feature, category, prf, weight=1.0, ap=0.5):
        basicprob = prf(feature, category)
        count = sum(self.fcount(feature, c) for c in self.cc)
        return (weight * ap + count * basicprob) / (count + weight)


# ---- t5 ----
def sample_train(cl):
    cl.train("Nobody owns the water", 'good')
    cl.train("the quick rabbit jumps fences", 'good')
    cl.train("buy pharmaceuticals now", 'bad')
    cl.train("make quick money at the online casino", 'bad')
    cl.train("the quick brown fox jumbs", 'good')


# ---- t9 ----
class NaiveBayes(classifier):
    # ---- t13 ----
    def __init__(self, get_features):
        super(NaiveBayes, self).__init__(get_features)
        self.thresholds = collections.defaultdict(lambda: 1.0)


# Falta tarea 10, 11 i 14
'''
classify(item, default) --> Bayes' Theorem: Maximo A Posteriori (MAP) sin P(D)
Problema:
	p(good | item) --> p(good | item) = p(item | good) * (p(good)/p(item)) --> p(item | good)

	Como tenemos que calcular qual es mayor, p(good | item) i p(bad | item), nos ahorramos el p(item)
	en nuestro caso.


THRESHOLDS:

'''
