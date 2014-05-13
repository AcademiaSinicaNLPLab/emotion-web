# -*- coding: utf-8 -*-
# import config
# import sys, pymongo, color

from collections import defaultdict, Counter
import json, sys, os

### input
# file 1: gold		e.g., gold.txt
# file 2: answer	e.g., svm .out

### output
# matrix (std.out or file)

path_to_answer = '../tmp/0.out'
path_to_gold = '../tmp/gold.txt'

answers = []
golds = []
labels = {}

print >> sys.stderr, '[path] [confusion_matrix.py]', os.getcwd()

def load_data():
	global answers, golds, labels

	print >> sys.stderr, '[path] [confusion_matrix.py] path_to_answer:',path_to_answer
	print >> sys.stderr, '[path] [confusion_matrix.py] path_to_gold:',path_to_gold

	answers = [line.strip().split('\t')[0] for line in open(path_to_answer)]
	golds = [line.strip().split('\t')[0] for line in open(path_to_gold)]
	labels = { line.strip().split('\t')[0]:line.strip().split('\t')[-1] for line in open(path_to_gold) }

def generate():
	global answers, golds, labels
	matrix = defaultdict(Counter)

	print >> sys.stderr, '[info] [confusion_matrix.py] generate() -> #init'
	# init
	for l1 in labels.values():
		for l2 in labels.values():
			matrix[l1][l2] = 0

	print >> sys.stderr, '[info] [confusion_matrix.py] generate() -> #generating'
	for gold ,answer in zip(golds, answers):
		gold_label = labels[gold]
		answer_label = labels[answer]
		matrix[gold_label][answer_label] += 1

	print >> sys.stderr, '[info] [confusion_matrix.py] get matrix with size:', len(matrix), 'x', len(matrix.values())

	return matrix

if __name__ == '__main__':
	for gold_label in sorted(matrix.keys()):
		# sum([x[1] for x in matrix[gold_label].items()])
		print gold_label, sorted(matrix[gold_label].items(), key=lambda x:x[1], reverse=True)
	