from flask import Flask


# creates an application object
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello Everyone!</h1>'

# add dynamic pages
@app.route('/<name>')
def index_name(name):
    ls = ['T', 'Z', 'X', 'W']
    if name[0].upper() in ls:
        return '<h1> {}!You are a winer!</h1>'.format(name)
    else:
        return f'<h1> {name}!try again!</h1>'


# if you are running the script 
if __name__ == '__main__':
    app.run()