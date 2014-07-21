# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
import json, os, sys
from collections import defaultdict
### ------------ color convert utility ------------ ###

_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}
LOWERCASE, UPPERCASE = 'x', 'X'

def rgb(triplet):
	try:
		rbg_code = _HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]
		return rbg_code
	except KeyError:
		return False

def triplet(rgb, lettercase=LOWERCASE):
	return format(rgb[0]<<16 | rgb[1]<<8 | rgb[2], '06'+lettercase)

### -------------------- end  -------------------- ###

### ------------ pattern ------------ ###
import pymongo
mc = pymongo.MongoClient('doraemon.iis.sinica.edu.tw')

# emotion_colors = [ (str(e),rgb(c[1:])) for e, c in json.load(open('color.order.json'))]

co_color_order = mc['feelit']['color.order']
co_color_map = mc['feelit']['color.map']
co_lexicon = mc['LJ40K']['lexicon.nested']
co_pats = mc['LJ40K']['pats']
co_patscore = mc['LJ40K']['patscore.normal']

# emo_list = co_color_order.find_one({ 'order': 'group-maxis' })['emotion']

## get ordered emotion list
emo_list = co_color_order.find_one({ 'order': 'group-maxis' })['emotion']
white = (255,255,255)

## get theme color mapping
mapping = co_color_map.find_one({'theme': 'default'})['map']

def build_color_db():

	emotion_colors = [ (str(e),rgb(c[1:])) for e, c in json.load(open('color.order.json'))]

	# co_color_order.insert( { 'order': 'default', 'emotion': sorted([x[0] for x in emotion_colors]) } )
	# co_color_order.insert( { 'order': 'group-maxis', 'emotion': [x[0] for x in emotion_colors] } )

	# mapping = {str(emo) : {'hex': str(c_hex[1:]), 'rgb': rgb(c_hex[1:])} for emo, c_hex in json.load(open('color.order.json'))}

	# co_color_map.insert({ 'theme': 'default', 'map': mapping })
	return None

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

def get_pats_colors(pat, percent=0.5):

	# if not emo_list: emo_list = co_color_order.find_one({ 'order': 'group-maxis' })['emotion']

	global emo_list, mapping

	mdoc = co_lexicon.find_one({'pattern': pat})

	white = (255,255,255)

	render_colors = { e: white for e in emo_list}
	if mdoc:
		counts = mdoc['count']
		E = accumulate_threshold(count=counts, percentage=percent)

		for e in E:
			render_colors[e] = tuple(mapping[e]['rgb'])

	order_render_colors = [(e,render_colors[e]) for e in emo_list]

	return order_render_colors


def build_doc_colors(vectors):

	global emo_list

	white = (255,255,255)
	render_colors = { e: white for e in emo_list}

	for dist in vectors:

		E = accumulate_threshold(count=counts, percentage=percent)

		for e in E:
			render_colors[e] = tuple(mapping[e]['rgb'])

		order_render_colors = [(e,render_colors[e]) for e in emo_list]



## input: udocID
## output: <dict> usentID: <list>(pattern, weight)
def list_doc_patterns(udocID):

	global emo_list # ordered emotion list

	## fetch
	mdocs = co_pats.find({'udocID': udocID}, {'_id':0, 'pattern':1, 'usentID': 1, 'weight':1})

	## group by sent
	Sent2Pats = defaultdict(list)
	for mdoc in mdocs:
		Sent2Pats[mdoc['usentID']].append( (mdoc['pattern'], mdoc['weight']) )

	return dict(Sent2Pats)


def get_pat_dists(udocID, weighted=False, scoring=False, base='pattern'):

	Sent2Pats = list_doc_patterns(udocID)

	# lookup distribution
	dists = defaultdict(list)

	for usentID in Sent2Pats:

		for pat, weight in Sent2Pats[usentID]:

			pat = pat.lower()

			mdoc = co_lexicon.find_one({'pattern': pat}) if not scoring else co_patscore.find_one({'pattern': pat})

			if not mdoc: continue

			dist = mdoc['count'] if not scoring else mdoc['score'] 

			w = weight if weighted else 1.0

			vector = {}
			for e in emo_list:
				if e not in dist: dist[e] = 0.0
				vector[e] = dist[e]*w

			dists[usentID].append( vector )

	## sentence base
	
	# print dict(dists)


	vectors = []

	if not dists.values():
		return vectors
	else:
		if base.startswith('sent'):

			## aggregate by sentence
			for usentID in dists:
				aggregated_vector = {}
				for vector in dists[usentID]:
					if aggregated_vector:
						for e in aggregated_vector: aggregated_vector[e] += vector[e]
					else:
						aggregated_vector = dict(vector)
				vectors.append( aggregated_vector )

		## pattern base
		else:
			vectors = reduce(lambda x,y:x+y, dists.values())

	return vectors

## input: dists of a document
## output: matrix
def generate_matrix(dists, percent):

	global emo_list, mapping

	matrix = []
	for dist in dists:

		## clear render color
		render_colors = { e: white for e in emo_list}

		E = accumulate_threshold(count=dist, percentage=percent)

		for e in E: render_colors[e] = tuple(mapping[e]['rgb'])

		order_render_colors = [(e,render_colors[e]) for e in emo_list]
		
		row = []
		for emotion, color in order_render_colors:
			row.append(color)
		matrix.append(row)

	return matrix


def draw_image(matrix, output_path, w=5, h=5, rows='auto'):


	img_width = w*len(matrix[0])
	img_height = h*len(matrix) if type(rows) == str and rows.lower() == 'auto' else rows*h

	im = Image.new('RGB', (img_width, img_height))

	## draw a rectangle
	draw = ImageDraw.Draw(im)

	for row in range(len(matrix)):
		for col in range(len(matrix[row])):

			x0, x1 = col*h, (col+1)*h
			y0, y1 = row*w, (row+1)*w
			
			c = matrix[row][col]
			draw.rectangle(xy=[(x0,y0),(x1,y1)], fill=c)
		
	im.save(output_path)

def run(options):

	##########################
	##		read config		##
	##########################
	weighted = options['weighted']
	scoring = options['scoring']
	base = options['base']
	percent = options['percent']

	output_root = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'imgs', base)
	if not os.path.exists(output_root): os.mkdir(output_root)

	# imgs/<group-by>/<emotions>/<udocID>
	# imgs/pattern/sleep/38000
	# imgs/sentence/sleep/38000

	docs = [ (x['udocID'], x['emotion']) for x in mc['LJ40K']['docs'].find()]

	docs = sorted( docs, key=lambda x:x[0] )
	
	Matrixs = []
	MatrixLength = []

	for udocID, emotion in docs:

		output_folder = '/'.join(['emotion-imgs-%dx%d' % (options['w'],options['h']), base, emotion])
		if not os.path.exists(output_folder): os.makedirs(output_folder)

		fn = str(udocID)+'.png'
		output_path = os.path.join(output_folder, fn)

		if os.path.exists(output_path): 
			print 'existed', udocID, '\t', round(udocID/float(len(docs))*100, 3), '\r',
			sys.stdout.flush()			
			continue


		dists = get_pat_dists(udocID, weighted, scoring, base)

		matrix = generate_matrix(dists, percent)

		# [str(udocID), str(emotion)]
		if not matrix: 
			print 'no matrix', udocID, '\t', round(udocID/float(len(docs))*100, 3), '\r',
			sys.stdout.flush()			
			continue

		draw_image(matrix, output_path, w=options['w'], h=options['h'], rows='auto')

		print 'processing', udocID, '\t', round(udocID/float(len(docs))*100, 3), '\r',
		sys.stdout.flush()

		# break
	print 'all done'

if __name__ == '__main__':

	options = { 
		'w':1, 
		'h':1,
		'weighted': False,
		'scoring': False,
		'base': 'pattern',
		'percent': 0.5
	}

	run(options)
