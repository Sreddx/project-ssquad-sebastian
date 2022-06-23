import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

#Sebastian's Functions
@app.route('/aboutSebas')
def sebasProfile():
    return render_template('sebastian.html', extra_hobbies="Hobbies", hobby_list=["Going to the beach","Surfing","Reading"],
    extra_work="Work experiences", work_list=["Freelance web page dev","Indoor cycling staff"], 
    extra_education="Education",education_list=["Harkness Highscool", "MLH Fellowship"])

@app.endpoint("sebasWork")
def sebasWork():
    return render_template('sebastian.html', scrollToAnchor='work', extra_hobbies="Hobbies", hobby_list=["Going to the beach","Surfing","Reading"],
    extra_work="Work experiences", work_list=["Freelance web page dev","Indoor cycling staff"], 
    extra_education="Education",education_list=["Harkness Highscool", "MLH Fellowship"])

@app.endpoint("sebasHobbies")
def sebasHobbies():
    return render_template('sebastian.html', scrollToAnchor='hobbies', extra_hobbies="Hobbies", hobby_list=["Going to the beach","Surfing","Reading"],
    extra_work="Work experiences", work_list=["Freelance web page dev","Indoor cycling staff"], 
    extra_education="Education",education_list=["Harkness Highscool", "MLH Fellowship"])

@app.endpoint("sebasEducation")
def sebasEducation():
    return render_template('sebastian.html', scrollToAnchor='education', extra_hobbies="Hobbies", hobby_list=["Going to the beach","Surfing","Reading"],
    extra_work="Work experiences", work_list=["Freelance web page dev","Indoor cycling staff"], 
    extra_education="Education",education_list=["Harkness Highscool", "MLH Fellowship"])

@app.endpoint("sebasTravel")
def sebasTravel():
    return render_template('sebastian.html', scrollToAnchor='travel', extra_hobbies="Hobbies", hobby_list=["Going to the beach","Surfing","Reading"],
    extra_work="Work experiences", work_list=["Freelance web page dev","Indoor cycling staff"], 
    extra_education="Education",education_list=["Harkness Highscool", "MLH Fellowship"])

@app.route('/jinjaTest')
def jinjTest():
    return render_template('extraTemplate.html', url=os.getenv("URL"), my_string="Wheeeee!", my_list=[0,1,2,3,4,5])

#Endpoints
app.add_url_rule("/aboutSebas-work", endpoint="sebasWork")
app.add_url_rule("/aboutSebas-hobbies", endpoint="sebasHobbies")
app.add_url_rule("/aboutSebas-education", endpoint="sebasEducation")
app.add_url_rule("/aboutSebas-travel", endpoint="sebasTravel")


