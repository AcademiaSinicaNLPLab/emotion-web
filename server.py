from flask import Flask, render_template
import fetch_mongo
app = Flask(__name__)

@app.route("/")
def home():
	return "Home!!"

@app.route("/test/")
def test_page():
	return "XD"

@app.route("/index/")
def emotion_index():
	return render_template( 'emotion_index.html', emotions=fetch_mongo.emotion_list() )

@app.route("/<emotion>/")
def docID_index(emotion):
	return render_template( 'docID_index.html', emotion=emotion )

@app.route('/<emotion>/<int:ldocID>/')
def document(emotion, ldocID):
	return render_template( 'document.html', emotion=emotion, ldocID=ldocID, data=fetch_mongo.sp_pairs(emotion, ldocID) )


if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0')