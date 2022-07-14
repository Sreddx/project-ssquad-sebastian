import os
from flask import Flask, render_template, request, url_for, flash, redirect
from dotenv import load_dotenv
from peewee import *



load_dotenv()
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)

#Initialize DB
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

#Import endpoints from timeline
from . timeline import timeline, post_timeline_post, load_timeline_post, get_timeline_posts, delete_post

#Website routes
@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

#Sebastian's Functions
@app.route('/aboutSebas')
def sebasProfile():
    return render_template('aboutMe.html')

@app.endpoint("sebasWork")
def sebasWork():
    return render_template('workExperience.html')


@app.endpoint("sebasHobbies")
def sebasHobbies():
    return render_template('hobbiesSection.html')


@app.endpoint("sebasEducation")
def sebasEducation():
    return render_template('educationSection.html')

@app.endpoint("sebasTravel")
def sebasTravel():
    return render_template('travelSection.html')

@app.endpoint("moreAboutSebas")
def moreAboutSebas():
    return render_template('moreAboutSection.html', extra_hobbies="Hobbies", hobby_list=["Going to the beach","Surfing","Reading manga"],
    extra_work="Work experiences", work_list=["Freelance web page dev","Video editor"], 
    extra_education="Education",education_list=["Harkness Highscool", "MLH Fellowship"])

@app.route('/jinjaTest')
def jinjTest():
    return render_template('extraTemplate.html', url=os.getenv("URL"), my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


#Endpoints for views
app.add_url_rule("/aboutSebas-work", endpoint="sebasWork")
app.add_url_rule("/aboutSebas-hobbies", endpoint="sebasHobbies")
app.add_url_rule("/aboutSebas-education", endpoint="sebasEducation")
app.add_url_rule("/aboutSebas-more", endpoint="moreAboutSebas")
app.add_url_rule("/aboutSebas-travel", endpoint="sebasTravel")


#Timeline section--------

#Endpoints for timeline
#Render timeline page
app.add_url_rule('/timeline', view_func=timeline, methods=['GET'])
#Post to timeline 
app.add_url_rule('/api/newPost', view_func=post_timeline_post, methods=['POST'])
#Retrieve all timeline and return list of posts
app.add_url_rule('/api/load_timeline_post', view_func=load_timeline_post, methods=['GET'])
#Retrieve all timeline posts ordered by created_at descending
app.add_url_rule('/api/timeline_post', view_func=get_timeline_posts, methods=['GET'])
#Delete timeline post
app.add_url_rule('/api/delete_post/<int:id>', view_func=delete_post, methods=['POST'])



