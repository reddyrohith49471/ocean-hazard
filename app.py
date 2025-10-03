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
import os
nltk.download('stopwords')
nltk.download('wordnet')





mongo_uri = os.environ.get("MONGO_URI")
client = pymongo.MongoClient(mongo_uri)

try:
    client.admin.command("ping")
    print("Connected successfully to MongoDB Atlas!")
except Exception as e:
    print("Connection failed:", e)

db = client['Ocean_Hazard_DB']
collection = db['Hazard_posts']



def translation(text):
    translated = GoogleTranslator(source='auto',target='en').translate(text)
    return translated

def emoji_removed(text):
    return (emoji.replace_emoji(text,replace=" "))

def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    text = re.sub('^a-zA-Z0-9'," ",text)
    text = emoji.replace_emoji(text, replace='')
    text = text.lower()
    text = text.split()
    text = [lemmatizer.lemmatize(word) for word in text if word not in stopwords.words('english')]
    text = " ".join(text)
    return text

def checking(text):
    with open('ocean_hazard_model1.pkl','rb') as f:
        vectorizer, model = pickle.load(f)
    text = preprocess(text)
    text = vectorizer.transform([text])
    return model.predict(text)

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

def input_details():
    valid_extensions = ('.svg','.jpg','.jpeg')
    while True:
        post = input('Enter the post Path:-')
        if post.lower().endswith(valid_extensions):
            break
        print("Enter Valid File Path")

    while True:
        description = input('Enter the Description:-')

        # Translate description to english
        translate_description = translation(description)

        # Remove Emojis for clean Text
        description_after_emojis = emoji_removed(translate_description)

        # Check Wether the message is warning message or not
        message_check = checking(description_after_emojis)

        # if message is too big then summarize text
        if message_check == 1:
            words = len(description_after_emojis.split())
            summarized_message = summarizing_message(description_after_emojis,words)
            break
        print("Invalid Description")


    while True:
        location = input('Enter the Location:-')
        # Check wether the location name is correct or not if wrong then auto correct
        # This location is from india or not
        is_india, latitude, longitude = get_indian_location_details(location)
        if is_india:
            break
        print("Invalid Location")


    while True:
        date = input('Enter the Date:-')
        # Accept any kind of date formats
        # Allow only 1 week past from present day
        date = validate_date(date)
        if date!=None:
            break
        print("Invalid Date")

    while True:
        time = input('Enter the time:-')
        # It should be 24 hrs time format
        time = validate_time(time)
        if time!=None:
            break
        print("Invalid Time")



    return {
            "post":post,
            "Description":description_after_emojis,
            "Summarized_Message":summarized_message,
            "Location":location,
            "Latitude":latitude,
            "Longitude":longitude,
            "Date":date,
            "Time":time
        }



if __name__== "__main__":
  while True:
    print("1. Add New Post")
    print("2. View All Posts")
    print("3. Exit")
    choice = int(input("Enter your choice:-"))
    if choice==1:
      details = input_details()
      if isinstance(details['Date'], datetime):
        pass
      else:
        details['Date'] = datetime.combine(details['Date'], datetime.min.time())
      collection.insert_one(details)
      print("Details Added Successfully")
    elif choice==2:
      post = list(collection.find({},{"_id":0}))
      if not post:
        print("Posts Not found")
      else:
        df = pd.DataFrame(post)
        print(df)
    elif choice==3:
      break
    else:
      print("Invalid Choice")
