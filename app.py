import gridfs
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)
app.config['MONGO_DBNAME'] = "BRICS" # name of database on mongo
app.config["MONGO_URI"] = "mongodb+srv://team01:team01@bankdata.elcja.mongodb.net/BRICS?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/')
def home():
    results = list()
    query = request.form.get("query")
    return render_template("index.html")

@app.route('/results', methods=["GET", "POST"])
def display_description():
    """
    Serve anchor links to pet documents whose description matches the query
    :return: HTML page with Links to pet documents
    """
    if request.method == 'POST':
        results = list()
        try:
            country = request.form.getlist("country")
            SeriesName = request.form.get("SeriesName")
            year = int(request.form.get("year"))
            query_results = mongo.db.BRICS.find({"CountryName":  { "$in" : country}, "Year": year,"SeriesName":{"$regex": SeriesName,"$options": "i"}})
            for query_result in query_results:
                results.append([query_result['_id'],query_result['CountryCode'], query_result['SeriesCode'],query_result['SeriesName'],query_result['Year'],round(query_result['Value'], 2)])
            query_results = mongo.db.BRICS.find({"CountryName":  { "$in" : country}, "Year": year,"SeriesName": SeriesName})
            for query_result in query_results:
                results.append([query_result['_id'],query_result['CountryCode'], query_result['SeriesCode'],query_result['SeriesName'],query_result['Year'],round(query_result['Value'], 2)])

            if( len(results) > 0):
                return render_template("link_to_results.html", items=results,count=len(results))
            else:
                return render_template("error.html")
        except:
            return render_template("error.html")


@app.route('/dashboard',methods=["GET", "POST"])
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upcoming_features')
def upcoming_features():
    return render_template('upcoming_features.html')

@app.route('/Contact',methods=['GET','POST'])
def Contact():
        return render_template('contact.html')

@app.route('/feedback',methods=['GET','POST'])
def feedback():
            return render_template('feedback.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, threaded=True)