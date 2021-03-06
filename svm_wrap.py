# -*- coding: utf-8 -*-
import sys
sys.path.append('/tools/libsvm/python/')

import os
from collections import defaultdict
from svmutil import *

from collections import defaultdict, Counter
import json, sys, os, re, color

import pymongo
import config
db = pymongo.Connection(config.mongo_addr)[config.db_name]

import pickle
emo_2_eid = pickle.load(open('feelit-data/featID.emotions.pkl'))

def load_models(setting, data_root='feelit-data'): 

	sid, param = setting
	root = os.path.join(data_root, 'model', sid)

	mpaths = [os.path.join(root, f) for f in os.listdir(root) if f.endswith(param+'.m')]

	model = dict()

	for mpath in mpaths:
		m = svm_load_model(mpath)
		sys.stderr.write('.')
		eid = int(mpath.split('/')[-1].split('.')[0])

		model[eid] = m

	sys.stderr.write('\n')
	return model

def predict(model, doc_feature):

	if type(doc_feature) == list or type(doc_feature) == tuple:
		y = doc_feature[0]
		x = doc_feature[1]
	elif type(doc_feature) == dict:
		y = [1]
		x = [doc_feature]
	else:
		return False
	
	p_vals = {}
	for eid in model:
		p_label, p_acc, p_val = svm_predict(y, x, model[eid], '-q')
		p_vals[eid] = p_val[0][0]

	return p_vals

def fusion_predict(models, weights, features):
	p_vals = {}
	for key in models:
		p_vals[key] = predict(models[key], features[key])

	fused = Counter()
	for key in p_vals:
		for eid in p_vals[key]:
			fused[eid] += p_vals[key][eid]*weights[key]
	return fused


def get_emotion_map(emo_2_eid):
	eid_2_emo = { emo_2_eid[e]: e for e in emo_2_eid }
	return eid_2_emo

def emit(eid_map, p_vals, sorting=False):
	labels = [ (eid_map[eid],prob) for eid, prob in p_vals.items() if prob > 0]
	if sorting:
		labels.sort(key=lambda x:x[1], reverse=True)
	return labels

if __name__ == '__main__':

	TFIDF_model =   ('538bcfaad4388c59136665df', 'c2g0.001t2')
	# pattern_model = ('53875eead4388c4eac581415', 'c2g0.001t2') # 50%
	pattern_model = ('53876645d4388c6f97360eb2', 'c2g0.001t2') # 100%

	doc_feature = ( [1], [{0:0.363567605836,1:0.411922192345,6:0.120659868742,7:0.181609213725,8:0.0142126256871,16:0.771638306031,18:0.228594185937,19:0.212155938635,20:0.102642384771,25:1.28001663688,27:0.131812046956,28:0.444717277835,32:1.31986666171,34:0.0158454523278,37:0.160168166454,39:0.0320417106863,45:0.397828777013,53:0.831755117548,62:0.0,64:0.435231504778,67:0.0545741066013,70:0.031651240684,75:0.158647058187,79:0.243868012116,102:2.1282956994,110:1.60072703366,112:0.596714691253,123:1.09495258653,130:0.250525575223,142:0.337866522042,160:0.589590342359,175:0.215473900157,178:1.16033515062,179:0.476411602727,188:0.140955727686,203:2.440195405,209:0.782047322706,226:2.88080889342,243:1.59831685845,252:1.6693800869,259:4.29609910968,273:1.59318640799,274:2.31001902743,286:2.70161948567,300:2.77944957458,303:0.974249169436,309:2.80107774577,318:0.718780555785,321:2.61901415471,354:1.11557417582,356:1.66506036879,400:1.9265961001,403:1.44043216565,429:1.4701859512,452:0.626452725549,471:1.01752569439,473:1.1510323544,486:1.75483380015,495:0.724961349958,523:1.93639542854,524:2.16893648683,599:1.31270565703,600:3.00776916238,601:1.38652697123,623:3.3718657122,681:1.45374128672,797:2.61341173784,815:2.44766326749,852:1.66377916886,864:3.23374103641,916:4.32921488488,926:2.70520009382,990:2.5309591509,1040:2.07124187963,1177:2.44486598488,1301:2.7859004779,1377:3.23820872106,1430:1.90441002863,1519:2.35128351305,1547:2.09204435409,1583:2.46298457875,1606:3.63703825713,1838:3.14688641646,1840:4.71332154698,1921:2.62984488824,2034:4.30975803316,2040:2.86371586073,2091:5.33958159622,2159:5.16956557753,2180:2.69297922338,2665:3.399821646,3283:3.61286627068,3338:6.14047589947,3436:4.06585145261,3488:3.3674897564,4114:2.64367852098,4884:3.88576215569,5640:4.77570349526,5830:5.05485870084,6245:4.72762850178,8149:4.59641821299,11080:4.75355070406,12036:6.12193662827,12690:6.08590433443,12707:4.82161341975,13366:5.81124204286,17276:5.54657714596,20425:6.44686012782,22087:6.17867069133,30781:5.98531217578,36670:8.84546499714,116835:9.89435680391}] )

	# models = load_models(setting=TFIDF_model)
	models = load_models(setting=pattern_model)

	p_vals = predict(models, doc_feature)

	## show label
	eid_map = get_emotion_map(emo_2_eid)

	labels = emit(eid_map, p_vals)
	# label = sorted([ (eid_map[eid],prob) for eid, prob in p_vals.items() if prob > 0], key=lambda x:x[1], reverse=True)

	print labels
