from flask import Flask
from flask import render_template
from flask import request
import datasets
import transformers

app = Flask(__name__)
summarizer = transformers.pipeline("summarization", model = "t5-small")

def summarize(s, length_percentage): # make this an actual summarize function
    len_of_data = len(s.split(" "))
    output = summarizer(s, min_length = 1, max_length = int(len_of_data*length_percentage/100))
    return output[0]['summary_text']

@app.route('/', methods = ["GET", "POST"]) #
def index():
    if request.method == 'GET':
        return render_template(r'index.html', data="", prefill="")
    else:
        print(request, " - - Get Request detected")
        data = request.form['transcript']
        length= int(request.form['length'])
        print(length)
        return render_template(r'index.html', data=summarize(str(data), length), prefill=data, size=length)
        # return text from the webpage




app.run()