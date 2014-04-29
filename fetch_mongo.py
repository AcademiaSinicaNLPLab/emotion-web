import pymongo, json
from pprint import pprint
# emotion = "crazy"
# ldocID = 0
# output = [(sent, pats), ...]

mc = pymongo.Connection('doraemon.iis.sinica.edu.tw')
db = mc['LJ40K']

co_emotions = db['emotions']
co_docmap = db['docs']
co_sents = db['sents']
co_pats = db['pats']
co_lexicon = db['lexicon']

emo_list = None


def emotion_list():
	emotions = list( co_emotions.find( {'label': 'LJ40K'} ) )
	return sorted( [x['emotion'] for x in emotions] )


def sp_pairs(emotion, ldocID):
	udocID = co_docmap.find_one( {'emotion': emotion, 'ldocID': ldocID} )['udocID']
	pairs = []
	sents = sorted( list( co_sents.find( {'udocID': udocID} ) ), key=lambda x:x['usentID'] )
	for sent in sents:
		words = [(x, 0) for x in sent['sent'].split(' ')]
		pats = [ (x['pattern'], x['anchor_idx']) for x in sorted( list( co_pats.find( {'usentID': sent['usentID']} ) ), key=lambda x:x['anchor_idx'] )]

		pairs.append( (sent['sent'], [x[0] for x in pats]) )
	return pairs


def get_pat_dist(pat, percent=True):

	global emo_list

	if not emo_list:
		emo_list = emotion_list()

	fetch = list(co_lexicon.find({'pattern': pat}))

	if len(fetch) > 0: 

		D = dict([(x['emotion'],x['count']) for x in fetch])

		C = {}
		for x in emo_list:
			if x in D:
				C[x] = D[x]
			else:
				C[x] = 0.0

		# print C

		S = 1 if not percent else float(sum([x['count'] for x in fetch]))

		if S == 0:
			data = []
		else:
			data = [ {'key':x, 'val':C[x]/S} for x in C]

		data.sort(key=lambda x:x['val'], reverse=True)
	else:
		data = []

	return json.dumps(data)

def get_sents_by_pat(pat):
	fetch = list(co_pats.find({'pattern':pat}))

	fetch = [x if co_docs.find_one({'udocID':x['udocID']})['ldocID'] < 800 for x in fetch]

	sents = x['usentID'] for x in fetch


if __name__ == '__main__':
	
	print get_pat_dist('i am pissed')
	# emotion = "crazy"
	# ldocID = 0
	# pairs = sent_pat_pairs(emotion, ldocID)

