from flask import Flask, render_template, url_for, make_response, Response, jsonify, request
import sys, json, os
import fetch_mongo
import confusion_matrix as matrix
from pprint import pprint
from datetime import datetime
import svm_wrap

app = Flask(__name__)

cache_folder_name = 'feelit-data'
cache_folder_root = os.path.join(os.getcwd(), cache_folder_name)

@app.route('/')
def hello():
	return render_template( 'index.html' )

@app.route("/browse")
@app.route("/browse/")
def list_emotions():
	emotions = fetch_mongo.get_emotion_list()
	return render_template( 'emotions.html', emotions=emotions )

@app.route("/browse/<emotion>/")
def list_docIDs(emotion):
	return render_template( 'docids.html', emotion=emotion )

@app.route('/browse/<emotion>/<int:ldocID>/')
def list_sents(emotion, ldocID):
	sp_pairs = fetch_mongo.get_sp_pairs(emotion, ldocID)
	docscore_categories = fetch_mongo.get_docscore_categories()
	return render_template( 'sents.html', emotion=emotion, ldocID=ldocID, sp_pairs=sp_pairs, docscore_categories=docscore_categories )

@app.route('/chart')
@app.route('/chart/')
def plot():
	return render_template( 'chart.html' )


@app.route('/scoring')
@app.route('/scoring/')
def show_scoring():
	pats_stat = fetch_mongo.get_pats_stat(digit=3)
	return render_template( 'scoring.html', data=pats_stat )


caching = True

@app.route('/matrix')
@app.route('/matrix/')
def show_matrix():

	settings = fetch_mongo.get_all_settings()
	# setting_id='537b00e33681df445d93d57e', svm_param='c9r2t1'
	args = request.args

	if not os.path.exists(cache_folder_root):
		print >> sys.stderr, '[warning] cache desternation is not existed'
		try:
			os.mkdir(cache_folder_root)
			print >> sys.stderr, '[cache] cache root created'
		except:
			print >> sys.stderr, '[error] failed to create cache folder on'
			print >> sys.stderr, '\t', cache_folder_root, 'check the permission'
			print >> sys.stderr, '\t','in the meanwhile, the program cahce will be disabled.'

	if not request.args:
		data = {}
		## list availabel matrix
		# matrix.list_all()

	elif request.args['setting_id'] and request.args['svm_param']:
		if caching:
			cache_fn   = '.'.join([args['setting_id'], args['svm_param'], 'json'])
			cache_path = os.path.join(cache_folder_root, cache_fn)

		## found in cache
		if caching and os.path.exists(cache_path):
			data = json.load(open(cache_path, 'r'))
			print >> sys.stderr, '[cache] load', cache_fn
		## cannot find in cache
		else:
			matrix.setting_id = args['setting_id']
			matrix.svm_param = args['svm_param']
			## set default search path
			# matrix.external_search = external_search
			# matrix.internal_search = internal_search

			print >> sys.stderr, '[call] [server.py] matrix.load_data()'
			matrix.load_data()

			print >> sys.stderr, '[call] [server.py] matrix.generate()'
			data = matrix.generate()

			if caching and data:
				## cache it
				json.dump(data, open(cache_path, 'w'))
				print >> sys.stderr, '[cache] dump', cache_fn
	else:
		data = {}
	# print settings
	return render_template( 'matrix.html', matrix=data, settings=settings, args=args, order=list( enumerate(sorted(data.keys())) ) )

@app.route('/results')
@app.route('/results/')
def show_results():
	R = fetch_mongo.get_all_results()
	return render_template( 'results.html', results=R, emotions=sorted(R[0]['accuracy'].keys()) )

TFIDF_model = ('538bcfaad4388c59136665df', 'c2g0.001t2')
models = svm_wrap.load_models(setting=TFIDF_model)
eid_map = svm_wrap.get_emotion_map()

@app.route('/predict')
@app.route('/predict/')
def predict_article():
	

	## extract feature
	doc_feature = ( [1], [{0:0.363567605836,1:0.411922192345,6:0.120659868742,7:0.181609213725,8:0.0142126256871,16:0.771638306031,18:0.228594185937,19:0.212155938635,20:0.102642384771,25:1.28001663688,27:0.131812046956,28:0.444717277835,32:1.31986666171,34:0.0158454523278,37:0.160168166454,39:0.0320417106863,45:0.397828777013,53:0.831755117548,62:0.0,64:0.435231504778,67:0.0545741066013,70:0.031651240684,75:0.158647058187,79:0.243868012116,102:2.1282956994,110:1.60072703366,112:0.596714691253,123:1.09495258653,130:0.250525575223,142:0.337866522042,160:0.589590342359,175:0.215473900157,178:1.16033515062,179:0.476411602727,188:0.140955727686,203:2.440195405,209:0.782047322706,226:2.88080889342,243:1.59831685845,252:1.6693800869,259:4.29609910968,273:1.59318640799,274:2.31001902743,286:2.70161948567,300:2.77944957458,303:0.974249169436,309:2.80107774577,318:0.718780555785,321:2.61901415471,354:1.11557417582,356:1.66506036879,400:1.9265961001,403:1.44043216565,429:1.4701859512,452:0.626452725549,471:1.01752569439,473:1.1510323544,486:1.75483380015,495:0.724961349958,523:1.93639542854,524:2.16893648683,599:1.31270565703,600:3.00776916238,601:1.38652697123,623:3.3718657122,681:1.45374128672,797:2.61341173784,815:2.44766326749,852:1.66377916886,864:3.23374103641,916:4.32921488488,926:2.70520009382,990:2.5309591509,1040:2.07124187963,1177:2.44486598488,1301:2.7859004779,1377:3.23820872106,1430:1.90441002863,1519:2.35128351305,1547:2.09204435409,1583:2.46298457875,1606:3.63703825713,1838:3.14688641646,1840:4.71332154698,1921:2.62984488824,2034:4.30975803316,2040:2.86371586073,2091:5.33958159622,2159:5.16956557753,2180:2.69297922338,2665:3.399821646,3283:3.61286627068,3338:6.14047589947,3436:4.06585145261,3488:3.3674897564,4114:2.64367852098,4884:3.88576215569,5640:4.77570349526,5830:5.05485870084,6245:4.72762850178,8149:4.59641821299,11080:4.75355070406,12036:6.12193662827,12690:6.08590433443,12707:4.82161341975,13366:5.81124204286,17276:5.54657714596,20425:6.44686012782,22087:6.17867069133,30781:5.98531217578,36670:8.84546499714,116835:9.89435680391}] )
	
	global models
	p_vals = svm_wrap.predict(models, doc_feature)
	print 'p_vals:',p_vals

	global eid_map
	labels = svm_wrap.emit(eid_map, p_vals)
	print 'labels:',labels

	return render_template( 'demo.html', prediction=labels)

## -------------------- APIs -------------------- ##

@app.route('/api/pat_distribution/<pat>')
@app.route('/api/pat_distribution/<pat>/')
def showplot(pat):
	print >> sys.stderr, '[info] get pattern "'+pat+'"'
	pat_data = fetch_mongo.get_pat_dist(pat)
	print >> sys.stderr, '[info] data length:', len(pat_data)

	ip = request.remote_addr
	now = datetime.now()

	mdoc = {
		'time': {
			'year': now.year,
			'month': now.month,
			'day': now.day,
			'weekday': now.weekday(),
			'hour': now.hour,
			'minute': now.minute,
			'second': now.second
		},
		'ip': ip,
		'pattern': pat
	}
	fetch_mongo.insert_log(mdoc)


	if type(pat_data) == list and len(pat_data) == 0:
		return Response(status=204)
	elif type(pat_data) == list and len(pat_data) > 0:
		return Response(json.dumps(pat_data), mimetype="application/json", status=200)
	else:
		return Response(status=500)

@app.route('/api/pat_sentences/<pat>')

@app.route('/api/pat_sentences/<pat>/<emo>/')
def showsents(pat, emo=None):
	return fetch_mongo.get_sents_by_pat(pat, emo)

@app.route('/api/docscore/<udocID>/<docscore_category>')
def showdocscore():
	return fetch_mongo.get_docscores(udocID, docscore_category)


@app.route('/api/settings')
@app.route('/api/settings/')
def show_settings():
	settings = fetch_mongo.get_all_settings()
	return json.dumps(settings)
	# return Response(json.dumps(settings), mimetype="application/json", status=200)


if __name__ == "__main__":
	import getopt, sys

	_port = 5000
	app.debug = False

	try:
		opts, args = getopt.getopt(sys.argv[1:],'p:d',['port=', 'debug'])
	except getopt.GetoptError:
		exit(2)

	for opt, arg in opts:
		if opt in ('-p', '--port'): _port = int(arg.strip())
		elif opt in ('-d','--debug'): app.debug = True

	app.run(host='0.0.0.0', port=_port)
