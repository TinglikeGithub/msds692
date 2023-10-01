import os
import re
import string
from jinja2 import Template


def filelist(root): 
    """Return a fully-qualified list of filenames under root directory"""
    # rootdir = '/Users/tingpan/data/berlitz1'
    return [os.path.join(root, filename) for filename in os.listdir(root)]

# output :['/Users/tingpan/data/berlitz1/HandRLasVegas.txt','/Users/tingpan/data/berlitz1/IntroMalaysia.txt']


def get_text(fileName):
    f = open(fileName, encoding='latin-1')
    s = f.read()
    f.close()
    return s


def words(text):
    """
    Given a string, return a list of words normalized as follows.
    Split the string to make words first by using regex compile() function
    and string.punctuation + '0-9\\r\\t\\n]' to replace all those
    char with a space character.
    Split on space to get word list.
    Ignore words < 3 char long.
    Lowercase all words
    """
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = nopunct.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    # print words
    return words


def results(docs, terms):
    """
    Given a list of fully-qualifed filenames, return an HTML file
    that displays the results and up to 2 lines from the file
    that have at least one of the search terms.
    Return at most 100 results.  Arg terms is a list of string terms.
    """
    # docs = index_search(files, index, terms) or docs = linear_search(files, terms)
    # ['/Users/tingpan/data/berlitz1/WhereToGreek.txt', '/Users/tingpan/data/berlitz1/WhereToIndia.txt', 
    #  '/Users/tingpan/data/berlitz1/WhereToItaly.txt', '/Users/tingpan/data/berlitz1/HistoryGreek.txt'] 
    # we need: term, file path, len of files, contains
    length = len(docs)
    # create html
    template_str = '''
    <html>
        <body>
            <h2>Search results for <b>{{terms}}</b> in {{lenght}} files</h2>
            <p> <a href={{herf}}>{{file_text}}</a><br>
            {{lines}}<br><br>
        </body>
    </html>
    '''
    template = Template(template_str)

    rendered_html = template.render(
            terms = terms
            length = len(docs)
            herf = 
            file_text = 
    )




def filenames(docs):
    """Return just the filenames from list of fully-qualified filenames"""
    if docs is None:
        return []
    return [os.path.basename(d) for d in docs]
