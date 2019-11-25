
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def main():
    return render_template("main.html")

	
@app.route('/login')
def login():
	return "<H1> LOGIN </H1>"
	
	
if __name__ == '__main__':
	app.run(debug=True)