from app import mydb
from peewee import *
from flask import Flask, render_template, request, url_for, flash, redirect
import datetime
import re
from playhouse.shortcuts import model_to_dict

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

# Regex for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def timeline():
    #Retrieve existing posts on page load
    timeline_posts = TimelinePost.select()
    posts = []
    for post in timeline_posts:
        posts.append(model_to_dict(post))
 
    return render_template('timeline.html', posts=posts)

#Post to timeline 
#@app.route('/api/newPost',methods=['POST'])
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
#@app.route('/api/load_timeline_post',methods=['GET'])
def load_timeline_post():
    timeline_posts = TimelinePost.select()
    posts_list = []
    for timeline_post in timeline_posts:
        posts_list.append(model_to_dict(timeline_post))
    return posts_list
    
#Retrieve all timeline posts ordered by created_at descending
#@app.route('/api/timeline_post',methods=['GET'])
def get_timeline_posts():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

#Delete timeline post
#@app.route('/api/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    try:
        qry = TimelinePost.delete().where (TimelinePost.id==id)
        qry.execute()
        return redirect('/timeline')
    except Exception as e:
        return e