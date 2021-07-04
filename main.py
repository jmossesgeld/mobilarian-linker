from flask import Flask, render_template, redirect, url_for, flash, abort
from flask.globals import request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired
import re

##WTForm
class PasteLinkForm(FlaskForm):
    title = TextAreaField("Paste Text Here", validators=[DataRequired()])
    submit = SubmitField("Submit")

app = Flask(__name__)
app.config['SECRET_KEY'] = "MOBILARIAN LINKER"
ckeditor = CKEditor(app)
Bootstrap(app)

def FindLinks(string):  
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '.', data)

@app.route('/', methods=["POST", "GET"])
def home():
    form = PasteLinkForm()
    results = [""]
    if form.validate_on_submit():
        text = str(form.title.data).replace(" ","")
        results = FindLinks(remove_emojis(text))
        for i in range(len(results)):
            print(results[i][:4])
            if results[i][:4] != "http":
                results[i] = f"https://{results[i]}"
                print(results[i])
        print(results)
        form.title.data = ""
        return render_template("index.html", results=results, form=form)

    return render_template("index.html", results=[], form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)