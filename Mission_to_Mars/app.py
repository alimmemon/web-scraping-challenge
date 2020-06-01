# import necessary libraries
from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo

# create instance of Flask app
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scrape_app")


# create route that renders index.html template
@app.route("/")
def echo():

    # Find one record of data from the mongo database
    mars_facts = mongo.db.collection.find_one()
    
    # Return template and data
    print(mars_facts)
    return render_template("index.html", mars=mars_facts)



#Scraping function
@app.route("/scrape")
def scrape():
    
    # Run the scrape function
    mars_facts_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_facts_data, upsert=True)

    # Redirect back to home page
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
