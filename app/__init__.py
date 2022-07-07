import os
from flask import Flask, render_template, request, url_for, flash, redirect
from dotenv import load_dotenv
from peewee import *
import datetime
import re
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = MySQLDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

# Regex for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

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
    return render_template('moreAboutSection.html', extra_hobbies="Hobbies", hobby_list=["Going to the beach","Surfing","Reading"],
    extra_work="Work experiences", work_list=["Freelance web page dev","Indoor cycling staff"], 
    extra_education="Education",education_list=["Harkness Highscool", "MLH Fellowship"])

@app.route('/jinjaTest')
def jinjTest():
    return render_template('extraTemplate.html', url=os.getenv("URL"), my_string="Wheeeee!", my_list=[0,1,2,3,4,5])

#Timeline section
@app.route('/timeline')
def timeline():
    timeline_posts = TimelinePost.select()
    posts = []
    for timeline_post in timeline_posts:
        posts.append(model_to_dict(timeline_post))
 
    return render_template('timeline.html', posts=posts)

#Endpoints
app.add_url_rule("/aboutSebas-work", endpoint="sebasWork")
app.add_url_rule("/aboutSebas-hobbies", endpoint="sebasHobbies")
app.add_url_rule("/aboutSebas-education", endpoint="sebasEducation")
app.add_url_rule("/aboutSebas-more", endpoint="moreAboutSebas")
app.add_url_rule("/aboutSebas-travel", endpoint="sebasTravel")





#Post new timeline 
@app.route('/api/timeline_post',methods=['POST'])
def post_timeline_post():
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    content = request.form.get('content', None)
    error=None
    #Verify form content
    if name is None or name == '':
        error = 'Name is required.'
    elif email is None or email == '':
        error = 'Email is required.'
    elif content is None or content == '':
        error = 'Content is required.'
    
    #Verify valid email format with regex
    if not (re.fullmatch(regex, email)):
        error = "Invalid email"

    if error is not None:
        return error, 400
    else:
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(timeline_post)
        

#Retrieve all timeline and return list of posts
@app.route('/api/load_timeline_post',methods=['GET'])
def load_timeline_post():
    timeline_posts = TimelinePost.select()
    posts_list = []
    for timeline_post in timeline_posts:
        posts_list.append(model_to_dict(timeline_post))
    return posts_list
    
#Retrieve all timeline posts ordered by created_at descending
@app.route('/api/timeline_post',methods=['GET'])
def get_timeline_posts():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

#Delete timeline post
@app.route('/api/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    try:
        qry = TimelinePost.delete().where (TimelinePost.id==id)
        qry.execute()
        return redirect('/timeline')
    except Exception as e:
        return e
