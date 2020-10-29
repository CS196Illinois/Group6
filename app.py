from flask import Flask
from flask import render_template
from flask import request
import datasets
import transformers

app = Flask(__name__)
summarizer = transformers.pipeline("summarization", model = "t5-small")

def summarize(s): # make this an actual summarize function
    output = summarizer(s, min_length = 1, max_length = 200) 
    return output[0]['summary_text']

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