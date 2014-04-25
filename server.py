from flask import Flask, render_template, url_for
import fetch_mongo
app = Flask(__name__)

@app.route("/")
def list_emotions():
	return render_template( 'emotions.html', emotions=fetch_mongo.emotion_list() )

@app.route("/<emotion>/")
def list_docIDs(emotion):
	return render_template( 'docids.html', emotion=emotion )

@app.route('/<emotion>/<int:ldocID>/')
def list_sents(emotion, ldocID):
	return render_template( 'sents.html', emotion=emotion, ldocID=ldocID, data=fetch_mongo.sp_pairs(emotion, ldocID) )

@app.route('/chart')
@app.route('/chart/')
def plot():
	return render_template( 'chart.html' )

@app.route('/api/pat/<pat>')
def showplot(pat):
	print 'got',pat
	return fetch_mongo.get_pat_dist(pat)

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