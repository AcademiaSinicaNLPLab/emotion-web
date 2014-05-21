# -*- coding: utf-8 -*-
# import config
# import sys, pymongo, color

from collections import defaultdict, Counter
import json, sys, os, re, color

### input
# file 1: gold		e.g., gold.txt
# file 2: answer	e.g., svm .out

### output
# matrix (std.out or file)

# data_folder_name = 'feelit-data'
# data_folder_root = os.path.join(os.getcwd(), data_folder_name)

# path_to_answer = '../tmp/0.out'
# path_to_gold = '../tmp/gold.txt'

path_to_gold = None
path_to_out  = None

answers = []
golds = []
labels = {}

### default path setting
external_search = '../emotion-detection-modules/tmp'
internal_search = 'tmp'

setting_id = '537b00e33681df445d93d57e'
svm_param = 'c9r2t1'

def search_files():
	global internal_search, external_search, setting_id, svm_param
	# search .out and .gold.txt
	## search internal
	out_path = os.path.join(internal_search, '.'.join([setting_id, svm_param, 'out']))
	gold_path = os.path.join(internal_search, '.'.join([setting_id, 'gold', 'txt']))



	found_out = os.path.exists(out_path)
	found_gold = os.path.exists(gold_path)
	## search external
	if not found_out:
		out_path = os.path.join(external_search, '.'.join([setting_id, svm_param, 'out']))
		found_out = os.path.exists(out_path)
	if not found_gold:
		gold_path = os.path.join(external_search, '.'.join([setting_id, 'gold', 'txt']))
		found_gold = os.path.exists(gold_path)
	

	print "out_path:",out_path
	print "gold_path:",gold_path
	print 

	if found_out and found_gold:
		return {'out': out_path, 'gold': gold_path}
	else:
		return False

# def list_all():
# 	## list external
# 	fns = [x for x in os.listdir(external_search) if re.match(r'^[0-9a-z]{24}', x)]

# 	fns

# 	os.listdir(external_search)


	pass

def load_data():
	global answers, golds, labels

	paths = search_files()

	if paths:
		print >> sys.stderr, '[path] [confusion_matrix.py] path for out:', paths['out']
		print >> sys.stderr, '[path] [confusion_matrix.py] path for gold:',paths['gold']		
		answers = [line.strip().split('\t')[0] for line in open(paths['out'])]
		golds = [line.strip().split('\t')[0] for line in open(paths['gold'])]
		labels = { line.strip().split('\t')[0]:line.strip().split('\t')[-1] for line in open(paths['gold']) }		
	else:
		print >> sys.stderr, color.render('[erorr] [confusion_matrix.py] cannot find the files.', 'r')


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
	