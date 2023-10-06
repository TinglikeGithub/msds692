# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs
import os
from words import get_text, words


def linear_search(files, terms):
    """
    Given a list of fully-qualified filenames, return a list of them
    whose file contents has all words in terms as normalized by your words() function.
    Parameter terms is a list of strings.
    Perform a linear search, looking at each file one after the other.
    """
    output = []
    for file in files:
        file_word = words(get_text(file))
        count = 0
        for term in terms:
            if term in file_word:
                count += 1
        if count == len(terms):
            output.append(file)

    return output
