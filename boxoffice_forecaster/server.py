from flask import Flask, request, render_template, jsonify
from joblib import load
import datetime
from afinn import Afinn
import numpy as np
import pandas as pd

afinn = Afinn(language='en')

app = Flask(__name__)

clf = load('saved_model/boModel.joblib') 

@app.route("/", methods=["GET"])
def home():
	return render_template("home.html")

@app.route('/getprediction', methods=['POST'])
def predict():
	data = request.form

	title = str(data["title"]).lower()
	duration = int(data["duration"])
	genres = str(data["genre"]).capitalize()
	actors = str(data["actor"]).lower()
	directors = str(data["director"]).lower()
	companies = str(data["company"]).lower()
	date = data["date"]
	description = str(data['desc'])
	continent = str(data['continent'])

	top_actors = ['robert downey, jr.', 'samuel l. jackson', 'scarlett johansson', 'chris hemsworth', 'chris evans', 'zoe saldana', 'chris pratt', 'tom hanks', 'bradley cooper', 'johnny depp', 'tom cruise', 'vin diesel', 'mark ruffalo', 'emma watson', 'dwayne johnson', 'don cheadle', 'jeremy renner', 'will smith', 'daniel radcliffe', 'harrison ford', 'rupert grint', 'tom holland', 'karen gillan', 'chadwick boseman', 'elizabeth olsen', 'benedict cumberbatch', 'josh brolin', 'sebastian stan', 'leonardo dicaprio', 'matt damon', 'tom hiddleston', 'paul bettany', 'dave bautista', 'eddie murphy', 'brad pitt', 'liam neeson', 'bruce willis', 'ben stiller', 'hugh jackman', 'ian mckellen', 'steve carell', 'letitia wright', 'danai gurira', 'gwyneth paltrow', 'jennifer lawrence', 'nicolas cage', 'cameron diaz', 'pom klementieff', 'ewan mcgregor', 'benedict wong', 'josh gad', 'adam sandler', 'julia roberts', 'jim carrey', 'sandra bullock', 'jack black', 'ben affleck', 'robert de niro', 'idris elba', 'daisy ridley', 'natalie portman', 'jason statham', 'john boyega', 'sylvester stallone', 'christian bale', 'robin williams', 'ralph fiennes', 'orlando bloom', 'paul rudd', 'mel gibson', 'adam driver', 'morgan freeman', 'owen wilson', 'ryan reynolds', 'brie larson', 'george clooney', 'simon pegg', 'arnold schwarzenegger', 'shia labeouf', 'kevin hart', 'martin freeman', 'anthony mackie', 'mark wahlberg', 'keanu reeves', 'meryl streep', 'jon favreau', 'mark hamill', 'denzel washington', 'keegan-michael key', 'keira knightley', 'tim allen', 'geoffrey rush', 'anthony hopkins', 'sam worthington', 'daniel craig', 'mike myers', 'paul walker', 'kristen stewart', 'john travolta', 'evangeline lilly']
	top_directors = ['steven spielberg', 'anthony russo', 'joe russo', 'peter jackson', 'michael bay', 'james cameron', 'david yates', 'christopher nolan', 'j.j. abrams', 'tim burton', 'robert zemeckis', 'jon favreau', 'ron howard', 'ridley scott', 'chris columbus', 'roland emmerich', 'bryan singer', 'pierre coffin', 'gore verbinski', 'james wan', 'george lucas', 'brad bird', 'francis lawrence', 'clint eastwood', 'sam raimi', 'chris renaud', 'todd phillips', 'zack snyder', 'sam mendes', 'carlos saldanha', 'bill condon', 'm. night shyamalan', 'joss whedon', 'andrew stanton', 'tom mcgrath', 'jennifer lee', 'chris buck', 'guy ritchie', 'andrew adamson', 'justin lin', 'john lasseter', 'eric darnell', 'barry sonnenfeld', 'conrad vernon', 'shawn levy', 'steven soderbergh', 'jon turteltaub', 'pete docter', 'f. gary gray', 'kyle balda', 'jake kasdan', 'brett ratner', 'martin scorsese', 'rob marshall', 'tony scott', 'david fincher', 'andy wachowski', 'james mangold', 'rich moore', 'martin campbell', 'jon watts', 'rob minkoff', 'quentin tarantino', 'richard donner', 'byron howard', 'raja gosnell', 'lee unkrich', 'chen sicheng', 'wolfgang petersen', 'rian johnson', 'ivan reitman', 'dennis dugan', 'jay roach', 'mike newell', 'garry marshall', 'ron clements', 'joe johnston', 'john musker', 'mike mitchell', 'peyton reed', 'christopher mcquarrie', 'ang lee', 'james gunn', 'colin trevorrow', 'rob letterman', 'joel schumacher', 'kenneth branagh', 'paul w.s. anderson', 'alfonso cuarã³n', 'david leitch', 'dean deblois', 'marc forster', 'gareth edwards', 'robert rodriguez', 'paul greengrass', 'peter berg', 'tom shadyac', 'marc webb', 'stephen sommers', 'ryan coogler']
	top_companies = ['warner bros.', 'universal pictures', 'columbia pictures', 'walt disney pictures', 'paramount pictures', 'marvel studios', '20th century fox', 'relativity media', 'new line cinema', 'dreamworks pictures', 'legendary pictures', 'dune entertainment', 'disney-pixar', 'amblin entertainment', 'regency enterprises', 'village roadshow productions', 'dreamworks animation', 'lucasfilm', 'lionsgate', 'metro-goldwyn-mayer pictures', 'touchstone pictures', 'ratpac entertainment', 'walt disney animation studios', 'heyday films', 'summit entertainment', 'jerry bruckheimer', 'bad robot', 'twentieth century fox', 'imagine entertainment', 'di bonaventura pictures', 'fox 2000 pictures', 'illumination entertainment', 'tsg entertainment', 'original film', '1492 pictures', 'blumhouse', 'the kennedy/marshall company', 'working title films', 'wingnut films', 'happy madison', 'perfect world pictures', 'spyglass entertainment', 'tri-star pictures', 'scott rudin productions', 'silver pictures', 'temple hill entertainment', 'skydance productions', 'syncopy', 'castle rock entertainment', 'pdi', 'screen gems', 'new regency', 'eon productions', 'chernin entertainment', 'donnersâ\x80\x99 company', 'revolution studios', 'color force', 'hasbro studios', 'sony pictures animation', 'overbrook entertainment', 'walden media', 'atlas entertainment', 'zancuk company', 'fairview entertainment', 'sunswept entertainment', 'chris meledandri', 'ingenious media', 'davis entertainment', 'scott free films', 'participant media', 'mandeville films', 'brian grazer productions', 'blue sky studios', 'vertigo entertainment', 'ingenious film partners', 'lstar capital', 'cruel and unusual films', 'roth films', 'fox searchlight pictures', 'focus features', 'weinstein company', 'kinberg genre', 'malpaso productions', 'canal plus', 'laura ziskin productions', 'plan b entertainment', 'gk films', 'centropolis entertainment', 'lightstorm entertainment', 'one race films', 'the safran company', 'dentsu inc.', 'parkes+macdonald productions', 'gary sanchez productions', 'alcon entertainment', 'cruise-wagner', 'united artists', 'platinum dunes', 'judd apatow', 'lakeshore entertainment']
	
	genre_list = ['Action', 'Adventure','Animation','Biography','Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy','Film-Noir','History' ,'Horror', 'Music','Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller','War','Western']
	continents_list = ['Africa','Asia',	'Australia','Europe','North America', 'South America', 'other']
	
	# input data for the model
	input_data = []

	# duration feature
	input_data.append(duration)

	# top actor feature
	top_actor = 0
	for actor in actors.split(','):
		if actor.strip() in top_actors:
			top_actor = 1
			break
	input_data.append(top_actor)

	# top director feature
	top_director = 0
	for director in directors.split(','):
		if director.strip() in top_directors:
			top_director = 1
			break
	input_data.append(top_director)

	# top director feature
	top_company = 0
	for company in companies.split(','):
		if company.strip() in top_companies:
			top_company = 1
			break
	input_data.append(top_company)

	# title length feature
	input_data.append(len(title))

	# genre count feature
	input_data.append(len(genres.split(',')))

	# actor count feature
	input_data.append(len(actors.split(',')))

	# month feature 
	year, month, day = (int(x) for x in date.split('-'))
	input_data.append(int(month))

	# week day feature
	day = datetime.date(year, month, day).weekday()
	input_data.append(day)

	# quarter feature
	if month >= 1 and month <= 3:
		input_data.append(1)
	elif month >= 4 and month <= 6:
		input_data.append(2)
	elif month >= 7 and month <= 9:
		input_data.append(3)
	else:
		input_data.append(4)
		
	# genre feature
	genres = [genre.capitalize() for genre in genres.split(',')]
	for genre in genre_list:
		if genre in genres:
			input_data.append(1)
		else:
			input_data.append(0)


	# sentiment score
	if afinn.score(description) > 0:
		input_data.append(0)
		input_data.append(0)
		input_data.append(1)
	elif afinn.score(description) < 0:
		input_data.append(1)
		input_data.append(0)
		input_data.append(0)
	else:
		input_data.append(0)
		input_data.append(1)
		input_data.append(0)
	
	# continent
	for continent_v in continents_list:
		if continent_v == continent:
			input_data.append(1)
		else:
			input_data.append(0)

	# converting to pandas dataframe
	inp_data = pd.DataFrame(np.array(input_data).reshape(-1, len(input_data)), columns = ['duration', 'top_actor', 'top_director', 'top_company', 'title_length',
       'genre_count', 'actor_count', 'published_month', 'published_weekday',
       'published_quarter', 'Action', 'Adventure', 'Animation', 'Biography',
       'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
       'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
       'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western', 'negative',
       'neutral', 'positive', 'Africa', 'Asia', 'Australia', 'Europe',
       'North America', 'South America', 'other'])
	

	prediction = clf.predict(inp_data)[0]
	
	# confidence level of the prediction
	print(clf.predict_proba(inp_data))
	confidence = clf.predict_proba(inp_data)[0][prediction]

	if prediction == 1:
		success="This movie will likely be successful !"
	else:
		success="Nah, this movie won't be as successful..."

	return render_template('prediction.html', title=title, success=success, confidence=confidence)

if __name__ == "__main__":
	app.run(port=5000, debug=True)