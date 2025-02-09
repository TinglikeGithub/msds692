# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from htable import *
from words import get_text, words


def myhtable_create_index(files):
    """
    Build an index from word to set of document indexes
    This does the exact same thing as create_index() except that it uses
    your htable.  As a number of htable buckets, use 4011.
    Returns a list-of-buckets hashtable representation.
    """
    table = htable(4011)

    for doc_id, file in enumerate(files):
        word = words(get_text(file))
        for w in word:
            table_index = hashcode(w) % len(table)
            bucket = table[table_index]
            found = False
            for item in bucket:
                if item[0] == w:
                    item[1].add(doc_id)
                    found = True
                    break
            if not found:
                table[table_index].append([w, {doc_id}])
    return table

def myhtable_index_search(files, index, terms):
    """
    This does the exact same thing as index_search() except that it uses your htable.
    I.e., use htable_get(index, w) not index[w].
    Given an index and a list of fully-qualified filenames, return a list of
    filenames whose file contents has all words in terms parameter as normalized
    by your words() function. 
    """
    # terms = ['very', 'luxurious']
    # index: [[('very', {0}), ('with', {0}), ('hotel', {0}), ('ocean', {0}), ('luxurious', {0, 1}), ('rooms', {0}), ('facing', {0}), ('hong', {1}), ('some', {1}), ('world', {1}), ('has', {1})], [('and', {0}), ('most', {0, 1}), ('bathrooms', {0}), ('large', {0}), ('the', {0, 1}), ('kong', {1}), ('recommended', {1}), ('hotels', {1})]]
    # we wanna intersection of {0,1} and {0}
    inter = htable_get(index, terms[0])
    if htable_get(index, terms[0]) is not None:
        for term in terms[1:]:
            inter &= htable_get(index, term)
        return [files[i] for i in inter]
    else:
        return []



# rootdir = os.path.expanduser("~/data/berlitz1")
# files = filelist(rootdir)
# index = myhtable_create_index(files)
# terms="hawaii travel"
# terms = words(terms)
# index_docs = myhtable_index_search(files, index, terms)
# print(index_docs)
