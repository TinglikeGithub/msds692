"""
A hashtable represented as a list of lists with open hashing.
Each bucket is a list of (key,value) tuples
"""

def htable(nbuckets):
    """Return a list of nbuckets lists"""
    return [[] for i in range(nbuckets)]


def hashcode(o): # hashfuction to get the index for key
    """
    Return a hashcode for strings and integers; all others return None
    For integers, just return the integer value.
    For strings, perform operation h = h*31 + ord(c) for all characters in the string
    """
    h = 0
    if isinstance(o, int):
        h = o
    elif isinstance(o, str):
        for c in o:
            h = h*31 + ord(c)
    return h
# output = h = 90748680016
# # table =[90748680016, 2883905625, 2927376771, 93029210, 2623502345479838702]

def bucket_indexof(table, key):
    """
    You don't have to implement this, but I found it to be a handy function.
    Return the index of the element within a specific bucket; the bucket is:
    table[hashcode(key) % len(table)]. You have to linearly
    search the bucket to find the tuple containing key.
    """
    return hashcode(key) % len(table)


def htable_put(table, key, value):
    """
    Perform the equivalent of table[key] = value
    Find the appropriate bucket indicated by key and then append (key,value)
    to that bucket if the (key,value) pair doesn't exist yet in that bucket.
    If the bucket for key already has a (key,value) pair with that key,
    then replace the tuple with the new (key,value).
    Make sure that you are only adding (key,value) associations to the buckets.
    The type(value) can be anything. Could be a set, list, number, string, anything!
    """
    # table = [[], [], [], [], []]
    # key = 'carrots', value = [2, 99, 3942]
    bucket = table[bucket_indexof(table, key)]
    
    # Check if key already exists in the bucket
    for i, (k, v) in enumerate(bucket):
        if k == key:
            bucket[i] = (key, value)
            return table  # return early if key was found and value updated
    
    bucket.append((key, value))
    return table
 # output:[[], [('carrots', [2, 99, 3942])], [], [], []]

def htable_get(table, key):
    """
    Return the equivalent of table[key].
    Find the appropriate bucket indicated by the key and look for the
    association with the key. Return the value (not the key and not
    the association!). Return None if key not found.
    """
    # input: table =[[], [('carrots', [2, 99, 3942])], [], [], []]

    position = bucket_indexof(table, key)
    buckect = table[position]
    # buckect =[('carrots', [2, 99, 3942])]
    output = None
    for (k,v) in buckect:
        if key == k:
            output = v
    return output


def htable_buckets_str(table):
    """
    Return a string representing the various buckets of this table.
    The output looks like:
        0000->
        0001->
        0002->
        0003->parrt:99
        0004->
    where parrt:99 indicates an association of (parrt,99) in bucket 3.
    """
    output = ''
    for idx, pairs in enumerate(table):
        pairs_str = ', '.join(f"{k}:{v}" for k, v in pairs)
        output += f"{idx:04}->" + pairs_str + '\n'
    return output
    


def htable_str(table):
    """
    Return what str(table) would return for a regular Python dict
    such as {parrt:99}. The order should be in bucket order and then
    insertion order within each bucket. The insertion order is
    guaranteed when you append to the buckets in htable_put().
    """
    # input: table=[[(5, 5), (10, 10)], [(1, 1), (6, 6)], [(2, 2), (7, 7)], [(3, 3), (8, 8)], [(4, 4), (9, 9)]]
    # output: "{5:5, 10:10, 1:1, 6:6, 2:2, 7:7, 3:3, 8:8, 4:4, 9:9}"
    d = dict()
    for bucket in table:
        for (k,v) in bucket:
            d[k]=v
    output = "{" + ", ".join(f"{k}:{v}" for k, v in d.items()) + "}"
    return output

