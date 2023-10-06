import sys
import re
import string
import os
import numpy as np
import codecs
import pickle
import spacy

# From scikit learn that got words from:
# http://ir.dcs.gla.ac.uk/resources/linguistic_utils/stop_words
ENGLISH_STOP_WORDS = frozenset([
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves"])


def load_glove(filename):
    """
    Read all lines from the indicated file and return a dictionary
    mapping word:vector where vectors are of numpy `array` type.
    GloVe file lines are of the form:

    the 0.418 0.24968 -0.41242 0.1217 ...

    So split each line on spaces into a list; the first element is the word
    and the remaining elements represent factor components. The length of the vector
    should not matter; read vectors of any length.

    ignore stopwords
    """
    # filename = "test_glove.txt"
    ## YOUR CODE HERE
    glove_dict = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().split(' ')
            title = line[0]
            if title in ENGLISH_STOP_WORDS:
                continue
            vector = np.array(line[1:], dtype='float32')
            glove_dict[title]=vector
    return glove_dict
# output: {',': np.array([1.5,0,0]), 'sunny':np.array([1.5,0,0])}

def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""
    allfiles = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            allfiles.append(os.path.join(path, name))
    return allfiles


def get_text(filename):
    """
    Load and return the text of a text file, assuming latin-1 encoding as that
    is what the BBC corpus uses.  Use codecs.open() function not open().
    """
    f = codecs.open(filename, encoding='latin-1', mode='r')
    s = f.read()
    f.close()
    return s


def words(text):
    """
    Given a string, return a list of words normalized as follows.
    
        1. Lowercase all words
        2. Use re.sub function and string.punctuation + '0-9\\r\\t\\n]'
            to replace all those char with a space character.
        3. Split on space to get word list.
        4. Ignore words < 3 char long.
        5. Remove English stop words
    Don't use Spacy.
    """
    text = text.lower()
    text = re.sub("[" + string.punctuation + '0-9\\r\\t\\n]', ' ', text)
    ## YOUR CODE HERE 
    text = text.split(" ")
    text = [word for word in text if len(word)>2]
    words = [word for word in text if word.lower() not in ENGLISH_STOP_WORDS]
    return words


def split_title(text):
    """
    Given text returns title and the rest of the article.

    Split the test by "\n" and assume that the first element is the title
    """
    ## YOUR CODE HERE
    lines = text.strip().split("\n")
    title = lines[0]
    body = lines[1:]
    body =' '.join(body)
    return title, body


def load_articles(articles_dirname, gloves):
    """
    Load all .txt files under articles_dirname and return a table (list of lists/tuples)
    where each record is a list of:

      [filename, title, article-text-minus-title, wordvec-centroid-for-article-text]

    We use gloves parameter to compute the word vectors and centroid.

    The filename is fully-qualified name of the text file including
    the path to the root of the corpus passed in on the command line.

    When computing the vector for each document, use just the text, not the text and title.
    """
    ## YOUR CODE HERE
    # articles_dirname = ~/data/bbc
    # gloves = {',': np.array([1.5,0,0]), 'sunny':np.array([1.5,0,0])}
    files_name = filelist(articles_dirname)
    table = []
    for filename in files_name:
        file_text = get_text(filename)
        title, body = split_title(file_text)
        centroid = doc2vec(body, gloves)
        record = [filename, title, body, centroid]
        table.append(record)
    return table



def doc2vec(text, gloves):
    """
    Return the word vector centroid for the text. Sum the word vectors
    for each word and then divide by the number of words. Ignore words
    not in gloves.
    """
    word_list = words(text)
    word_sum = 0
    word_in_gloves = 0
    for word in word_list:
        if word in gloves.keys():
            word_in_gloves += 1
            word_sum += gloves[word]

    if word_in_gloves != 0:
        vector_centroid = word_sum / word_in_gloves
    else:
        vector_centroid =0
    return vector_centroid
  # output: 300-dimension array


def distances(article, articles):
    """
    Compute the euclidean distance from article to every other article.

    Inputs:
        article = [filename, title, text-minus-title, wordvec-centroid]
        article = ["tech/1.txt", "title", "", np.array([0,0,0])]
        articles is a list of [filename, title, text-minus-title, wordvec-centroid] [filename, title, body, centroid]
        articles = [["tech/384.txt", "tech", "", np.array([1.5,0,0])],
                    ["tech/4.txt", "more tech", "", np.array([0,0,2])],
                    ["tech/3.txt", "mas tech", "", np.array([0,0,1])],

    Output:
        list of (distance, a) for a in articles 
        where a is list of [filename, title, text-minus-title, wordvec-centroid]
    [(distance, [filename2, title, text-minus-title, wordvec-centroid]),(distance, [filename3, title, text-minus-title, wordvec-centroid])]
    """
    ## YOUR CODE HERE
    # related articles should have centroids that are close in the 300-dimensional space
    distances = []
    for item in articles:
        distance = np.linalg.norm(article[3] - item[3])
        t =(distance,item)
        distances.append(t)
    return distances
# output: [(distance, [filename2, title, text, centroid]),(distance, [filename3, title, text-minus-title, wordvec-centroid])]


def recommended(article, articles, n):
    """ Return top n articles closest to article.

    Inputs:
        article: list [filename, title, text-minus-title, wordvec-centroid]
        articles: list of list [filename, title, text-minus-title, wordvec-centroid]

    Output:
         list of [topic, filename, title]
    """
    ## YOUR CODE HERE
    distance_ls = distances(article, articles)
    sorted_ls = sorted(distance_ls, key=lambda x: x[0])
    output = []
    for i in range(n):
        filepath = sorted_ls[i+1][1][0]
        filename = filepath.split('/')[-1]
        title = sorted_ls[i+1][1][1]
        topic = filepath.split('/')[-2]
        mid = [topic, filename, title]
        output.append(mid)
    return output
# output =[['tech', '3.txt', title],[topic, '384.txt', title],[topic, '384.txt', title]]


def main():
    glove_filename = sys.argv[1] #~/data/glove.6B.300d.tx
    articles_dirname = sys.argv[2] #~/data/bbc

    gloves = load_glove(glove_filename)  #  {',': ['-0.25539', '-0.25723', '0.13169'], 'sunny':['-0.25539', '-0.25723', '0.13169']}
    articles = load_articles(articles_dirname, gloves) # [[fully-qualified_filename, title, body, centroid],[filename, title, body, centroid]]
    #python doc2vec.py ~/data/glove.6B.300d.txt ~/data/bbc
    # articles_dirname = ~/data/bbc
   
    # save a articles.pkl a list with the following information about articles
    # [[topic, filename, title, text], ...]
    ## YOUR CODE HERE
    info = []
    for item in articles[2:]:
        filepath = item[0]
        filename = filepath.split('/')[-1]
        topic = filepath.split('/')[-2]
        title = item[1]
        text = item[2]
        mid = [topic, filename, title, text]
        info.append(mid)

    with open("articles.pkl", "wb") as file:
        pickle.dump(info, file)

    # save in recommended.pkl a dictionary with top 5 recommendations for each article. 
    # given an article use (topic, filename) as the key
    # the recomendations are a list of [topic, filename, title] for the top 5 closest articles
    # you may want to also add the title and text of the current article
    ## YOUR CODE HERE
    rec_dict = dict()
    for article in articles[2:]: #article=[filename, title, text-minus-title, wordvec-centroid]
        recommend = recommended(article, articles, 5) # output =[['tech', '3.txt', title],[topic, filename, title],[topic, '384.txt', title]]
        key = (article[0].split('/')[-2], article[0].split('/')[-1])
        rec_dict[key] = recommend
    
    with open("recommended.pkl", "wb") as file:
        pickle.dump(rec_dict, file)

if __name__ == '__main__':    
    main()

