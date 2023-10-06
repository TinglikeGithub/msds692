# Launch with
#
# python app.py

from flask import Flask, render_template
import sys
import pickle

app = Flask(__name__)


@app.route("/")
def articles_func():
    """Show a list of article titles"""
    ## YOUR CODE HERE
    return render_template('articles.html', articles = articles)


@app.route("/article/<topic>/<filename>")
def article(topic, filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    # YOUR CODE HERE
    for art in articles:
        if art[0] == topic and art[1] == filename:
            selected_article = art
            break
    
    if (topic, filename) in recommended:
        rec = recommended[(topic, filename)]
    else:
        rec = []

    return render_template('article.html', article=selected_article, recommend=rec)


f = open('articles.pkl', 'rb')
articles = pickle.load(f)
f.close()


f = open('recommended.pkl', 'rb')
recommended = pickle.load(f)
f.close()

# you may need more code here or not


# for local debug
if __name__ == '__main__':
    app.run(debug=True)