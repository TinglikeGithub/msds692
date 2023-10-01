from collections import defaultdict  # https://docs.python.org/2/library/collections.html
import os
from words import get_text, words


def create_index(files):
    """
    Given a list of fully-qualified filenames, build an index from word
    to set of document IDs. A document ID is just the index into the
    files parameter (indexed from 0) to get the file name. Make sure that
    you are mapping a word to a set of doc IDs, not a list.
    For each word w in file i, add i to the set of document IDs containing w
    Return a dict object mapping a word to a set of doc IDs.
    """
    index = {}
    for file in files:
        file_word = words(get_text(file))
        for word in file_word:
            value=set()
            if word in index.keys():
                index[word].add(files.index(file))
            else:
                value.add(files.index(file))
                index[word] = value
    return index
# output: {'word': {0,1}, 'a': {0}}


def index_search(files, index, terms):
    """
    Given an index and a list of fully-qualified filenames, return a list of
    filenames whose file contents has all words in terms parameter as normalized
    by your words() function.  Parameter terms is a list of strings.
    You can only use the index to find matching files; you cannot open the files
    and look inside.
    """
    # terms = ['word', 'a'], index={'word': {0,1}, 'a': {0}}
    # we wanna intersection of {0,1} and {0}
    
    if terms[0] in index.keys():
        inter = index[terms[0]]
        print(inter)
        for term in terms[1:]:
            inter &= index.get(term, set())
        return [files[i] for i in inter]
    else:
        return []
    