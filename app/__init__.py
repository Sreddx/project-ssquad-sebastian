import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

print(mydb)

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
    posts=load_timeline_post()
    return render_template('timeline.html', posts=posts)

#Endpoints
app.add_url_rule("/aboutSebas-work", endpoint="sebasWork")
app.add_url_rule("/aboutSebas-hobbies", endpoint="sebasHobbies")
app.add_url_rule("/aboutSebas-education", endpoint="sebasEducation")
app.add_url_rule("/aboutSebas-more", endpoint="moreAboutSebas")
app.add_url_rule("/aboutSebas-travel", endpoint="sebasTravel")







#Post new timeline post
@app.route('/api/timeline_post',methods=['POST'])
def post_timeline_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return "Post created"

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
@app.route('/api/timeline_post',methods=['DELETE'])
def delete_timeline_post_by_name():
    try:
        name = request.form['name']
        qry = TimelinePost.delete().where (TimelinePost.name==name)
        qry.execute()
        return "Post deleted"
    except Exception as e:
        return e
