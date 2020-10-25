from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

def summarize(s): # make this an actual summarize function
    return s[::2]

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