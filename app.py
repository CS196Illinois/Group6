from flask import Flask
from flask import render_template
from flask import request
import datasets
from transformers import pipeline

app = Flask(__name__)

def summarize(s): # make this an actual summarize function
    summarization = pipeline("summarization")
    summary_text = summarization(s)[0]['summary_text']
    return summary_text


@app.route('/', methods = ["GET", "POST"]) #
def index():
    if request.method == 'GET':
        return render_template(r'index.html', data="")
    else:
        print(request, " - - Get Request detected")
        data = request.form['transcript']
        return render_template(r'index.html', data=summarize(str(data)))
        # return text from the webpage




app.run()
