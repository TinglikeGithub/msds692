from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    some_name = "Ting"
    letters = list(some_name)
    return render_template('basic_3.html', name=some_name, letters=letters)

if __name__ == "__main__":
    app.run(debug=True)


