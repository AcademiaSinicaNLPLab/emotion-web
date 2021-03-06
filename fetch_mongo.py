import pymongo, json
from pprint import pprint
from collections import defaultdict
# emotion = "crazy"
# ldocID = 0
# output = [(sent, pats), ...]

mc = pymongo.Connection('doraemon.iis.sinica.edu.tw')
db = mc['LJ40K']
logdb = mc['logs']

co_emotions = db['emotions']
co_docmap = db['docs']
co_sents = db['sents']
co_pats = db['pats']
co_lexicon = db['lexicon.nested']
co_docs = db['docs']
co_feature_setting = db['features.settings']
co_svm_eval = db['svm.eval']

co_stat_pats = db['stat.pats']

co_logs = logdb['feelit']

emo_list = None

docscore_categories = [
	'docscore_d0_g3_l0_p2_s0', 
	'docscore_d0_g3_l0_p2_s1', 
	'docscore_d0_g3_l3_p2_s0'
	'docscore_d0_g3_l5_p2_s0'
]

def insert_log(mdoc):
	co_logs.insert(mdoc)
	return True

def get_emotion_list():
	emotions = list( co_emotions.find( {'label': 'LJ40K'} ) )
	return sorted( [x['emotion'] for x in emotions] )

def get_pats_stat(limit=100, digit=None):
	import re
	pats_stat = []
	for mdoc in co_stat_pats.find({}, {'_id':0}):

		
		if re.findall(r'<[a-z]+', mdoc['pattern']):
			continue
		# <html>
		# <a href=....
		# <td > <font >

		if digit:
			mdoc_new = {}
			for k in mdoc:
				if type(mdoc[k]) == float:
					val = round(mdoc[k], digit)
				else:
					val = mdoc[k]
				mdoc_new[k] = val
			mdoc = mdoc_new
		mdoc['p_len'] = len(mdoc['pattern'])
		pats_stat.append(mdoc)
		if limit > 0 and len(pats_stat) >= limit:
			break
	return pats_stat



def get_docscore_categories(): 
	return docscore_categories

### get sentence_pattern pairs

def get_udocID(emotion, ldocID):
	udocID = co_docmap.find_one( {'emotion': emotion, 'ldocID': ldocID} )['udocID']
	return udocID

def get_doc_info(udocID):
	return co_docmap.find_one({ 'udocID': udocID })

def get_sp_pairs(udocID):
	pairs = []
	sents = sorted( list( co_sents.find( {'udocID': udocID} ) ), key=lambda x:x['usentID'] )
	for sent in sents:
		words = [(x, 0) for x in sent['sent'].split(' ')]
		pats = [ (x['pattern'], x['anchor_idx']) for x in sorted( list( co_pats.find( {'usentID': sent['usentID']} ) ), key=lambda x:x['anchor_idx'] )]

		pairs.append( (sent['sent'], [x[0] for x in pats]) )
	return pairs



def accumulate_threshold(count, percentage):
	## temp_dict -> { 0.3: ['happy', 'angry'], 0.8: ['sleepy'], ... }
	## (count)	    { 2:   ['bouncy', 'sleepy', 'hungry', 'creative'], 3: ['cheerful']}
	temp_dict = defaultdict( list ) 
	for e in count:
		temp_dict[count[e]].append(e)
	
	## temp_list -> [ (0.8, ['sleepy']), (0.3, ['happy', 'angry']), ... ] ((sorted))
	## (count)	    [ (3, ['cheerful']), (2,   ['bouncy', 'sleepy', 'hungry', 'creative'])]
	temp_list = temp_dict.items()
	temp_list.sort(reverse=True)

	th = percentage * sum( count.values() )
	current_sum = 0
	selected_emotions = []

	while current_sum < th:
		top = temp_list.pop(0)
		selected_emotions.extend( top[1] )
		current_sum += top[0] * len(top[1])

	return dict( zip(selected_emotions, [1]*len(selected_emotions)) )

colors = json.load(open('feelit-data/colors.json'))
def get_pats_colors(pat, percent=0.5, return_format=dict, emotion_label=True):
	global emo_list, colors
	if not emo_list:
		emo_list = get_emotion_list()

	mdoc = co_lexicon.find_one({'pattern': pat})

	render_colors = { e:'none' for e in emo_list}
	if mdoc:
		counts = mdoc['count']
		E = accumulate_threshold(count=counts, percentage=percent)

		for e in E:
			render_colors[e] = colors[e]

	if return_format == tuple or return_format == list:
		if emotion_label:
			return [(e, render_colors[e]) for e in emo_list]
		else:
			return [render_colors[e] for e in emo_list]
	else:
		if emotion_label:
			return render_colors
		else:
			return [render_colors[e] for e in emo_list]

def get_pat_dist(pat, percent=True):

	global emo_list

	if not emo_list:
		emo_list = get_emotion_list()

	mdoc = co_lexicon.find_one({'pattern': pat})

	return_data = []

	if mdoc:
		counts = mdoc['count']

		C = dict( [ (e, 0.0 if e not in counts else counts[e]) for e in emo_list] )

		Sum = 1 if not percent else float( sum(C.values()) )

		return_data = [] if Sum == 0 else [ {'key':x, 'val':C[x]/Sum} for x in C]

		return_data.sort(key=lambda x:x['val'], reverse=True)

	return return_data


def get_sents_by_pat(pat, emo):
	 
	D = defaultdict(list)

	if not emo:
		pat_mdoc_list = list(co_pats.find({'pattern':pat }))
	else:
		pat_mdoc_list = list(co_pats.find({'pattern':pat, 'emotion':emo}))

	for pat_mdoc in pat_mdoc_list:

		if co_docs.find_one({'udocID': pat_mdoc['udocID']})['ldocID'] < 800: 

			sent_mdoc = co_sents.find_one({'usentID': pat_mdoc['usentID']})
			D[sent_mdoc['emotion']].append(sent_mdoc['sent'])
	
	data = [{'emotion': emotion, 'sentences': D[emotion]} for emotion in sorted(D, key=lambda x:len(D[x]), reverse=True)]

	return json.dumps(data)


def get_docscores(udocID, docscore_category):
	## type(scores)=dictionary
	scores = db[docscore_category].findOne({'udocID': udocID})['scores']
	data = [scores['emotion'] for emotion in sorted(scores, key=lambda x:scores[x], reverse=True)]
	return json.dumps(data)

def get_all_settings():
	FS = defaultdict(list)
	for mdoc in co_feature_setting.find():
		mdoc['_id'] = str(mdoc['_id'])
		FS[mdoc['feature_name']].append( mdoc )
	return dict(FS)

# {
# 	sid:,
# 	feature_name:,
# 	detail:,
# 	accuracy:,
# 	avg_accuracy:
# }

def get_all_results():

	# R = defaultdict(dict)
	details = { str(mdoc['_id']):mdoc for mdoc in co_feature_setting.find() }
	R = []

	for mdoc in co_svm_eval.find():
		if mdoc['setting'] not in details:
			continue
		rdoc = {
			'sid': mdoc['setting'],
			'param': mdoc['param'],
			'avg_accuracy': mdoc['avg_accuracy'],
			'accuracy': mdoc['accuracy'],
			'feature_name':details[mdoc['setting']]['feature_name'],
			'detail': details[mdoc['setting']]
		}
		R.append(rdoc)

	R.sort(key=lambda x:x['feature_name'], reverse=True)

	return R


if __name__ == '__main__':
	
	print get_pat_dist('i am pissed')

	# print get_all_results()
	# emotion = "crazy"
	# ldocID = 0
	# pairs = sent_pat_pairs(emotion, ldocID)

	# print get_sents_by_pat('she wants nothing')

