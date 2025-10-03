from flask import Flask,render_template,request,redirect,url_for,flash,jsonify
from werkzeug.utils import secure_filename
import os
import pandas as pd
import numpy as np
import pymongo
from deep_translator import GoogleTranslator
import re
import emoji
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline
import requests
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('stopwords')
nltk.download('wordnet')





client = pymongo.MongoClient("mongodb+srv://reddyrohith20061902_db_user:12345@cluster0.h7s3hox.mongodb.net/")

try:
    client.admin.command("ping")
    print("Connected successfully to MongoDB Atlas!")
except Exception as e:
    print("Connection failed:", e)

db = client['Ocean_Hazard_DB']
collection = db['Hazard_posts']

app = Flask(__name__)
app.secret_key = "ocean_secret"

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # create folder if not exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

with open('ocean_hazard_model1.pkl','rb') as f:
        vectorizer, model = pickle.load(f)

def translation(text):
    translated = GoogleTranslator(source='auto',target='en').translate(text)
    return translated

def emoji_removed(text):
    return (emoji.replace_emoji(text,replace=" "))

def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    text = re.sub(r'[^a-zA-Z0-9]', " ", text)
    text = emoji.replace_emoji(text, replace='')
    text = text.lower()
    text = text.split()
    text = [lemmatizer.lemmatize(word) for word in text if word not in stopwords.words('english')]
    text = " ".join(text)
    return text

def checking(text):
    text = preprocess(text)
    text = vectorizer.transform([text])
    return model.predict(text)[0]

def summarizing_message(text,words):
    pipe = pipeline("summarization",model = "facebook/bart-large-cnn")
    minimum = max(5, int(words * 0.3))
    maximum = max(10, int(words * 0.7))
    summarizer = pipe(text, min_length = minimum, max_length = maximum, do_sample=True)
    return summarizer[0]['summary_text']

def get_indian_location_details(location: str):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q":location,
        "format":"json",
        "addressdetails":1,
        "limit":1
    }
    headers = {
        "User-Agent" : "location-checker-app"
    }

    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()

    if not data:
        print("Result Not Found")
        return False,None,None
    country = data[0]['address'].get("country", "").lower()
    lat = data[0].get("lat")
    lon = data[0].get("lon")

    return country == 'india',lat,lon


def validate_date(date: str):
    if not date or not date.strip():
        return None
    try:
        dt = date_parser.parse(date, fuzzy=True, dayfirst=True)

        # If year missing, set current year
        if dt.year == 1900:
            dt = dt.replace(year=datetime.now().year)

        dt = dt.date()
    except Exception:
        return None
    today = datetime.now().date()
    seven_days = today - timedelta(days=7)

    if dt>=seven_days:
        return dt
    return None

def validate_time(time:str):
    if not time or not time.strip():
        return None
    try:
        time = datetime.strptime(time.strip(),'%H:%M')
        return time.strftime("%H:%M")
    except Exception:
        return None


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add",methods=["POST"])
def add_post():
    files = request.files["post"]
    if files:
        filename = secure_filename(files.filename)
        if not filename.lower().endswith(('.jpg','.jpeg','.svg','.png')):
            flash("Invalid Format! The file format must be in .jpg .jpeg .svg .png")
            return redirect(url_for("home"))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        files.save(filepath)
        post_path = filepath
    else:
        flash("No File Selected")
        return redirect(url_for("home"))
        
    
    post = post_path    
    description = request.form.get("description")
    location = request.form.get("location")
    date = request.form.get("date")
    time = request.form.get("time")

    translate_description = translation(description)
    description_after_emojis = emoji_removed(translate_description)
    message_check = checking(description_after_emojis)

    if message_check != 1:
        flash("Description not valid. Please enter a proper hazard warning.")
        return redirect(url_for("home"))
    
    words = len(description_after_emojis.split())
    summarized_message = summarizing_message(description_after_emojis,words)

    is_india, latitude, longitude = get_indian_location_details(location)

    if not is_india:
        flash("Invalid Location")
        return redirect(url_for("home"))
    
    date = validate_date(date)
    if date == None:
        flash("Invalid Date")
        return redirect(url_for("home"))
    
    time = validate_time(time)
    if time == None:
        flash("Invalid Time: 24 hours Format HH:MM")
        return redirect(url_for("home"))

    details = {
    "post": post,
    "Description": description_after_emojis,
    "Summarized_Message": summarized_message,
    "Location": location,
    "Latitude": latitude,
    "Longitude": longitude,
    "Date": date.strftime("%Y-%m-%d"),  # convert to string
    "Time": time
}
    
    collection.insert_one(details)
    flash("post added Successfully")
    return redirect(url_for("home"))

@app.route("/posts")
def view_posts():
    post = list(collection.find({},{"_id":0}))
    if not post:
        return render_template("posts.html", posts=None)
    df = pd.DataFrame(post)
    table_html = df.to_html(classes="table table-bordered table-striped", index=False)
    
    return render_template("posts.html", posts=post, tables=[table_html])

@app.route("/map")
def show_map():
    return render_template("map.html")

@app.route("/map_data")
def map_data():
    # Fetch only posts with valid latitude and longitude
    posts = list(collection.find({"Latitude": {"$ne": None}, "Longitude": {"$ne": None}}, {"_id":0, "Latitude":1, "Longitude":1, "Location":1}))
    
    # Convert strings to float
    for p in posts:
        p['Latitude'] = float(p['Latitude'])
        p['Longitude'] = float(p['Longitude'])
        # p['Location'] = str(p['Location'])
    
    return jsonify(posts)


if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))