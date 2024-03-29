def word_filter(trie, pattern, key=''):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    #gets rid of duplicates
    total = word_filter_helper(trie,pattern,key)
    total = set(total)
    return list(total)


def word_filter_helper(trie,pattern,key):
    total = []
    #base cases
    if len(pattern)==0:
        if trie.value!=None:
            return [(key, trie.value)]
        if trie.value==None:
            return []
    #iterates through children and recurses on each child
    if pattern[0]=='?':
        for child in trie.children:
            total.extend(word_filter(trie.children[child], pattern[1:], key+child))
    #recurses with a ? (no letters) and without a ? (1 or more letters)
    elif pattern[0]=='*':
        total.extend(word_filter(trie, pattern[1:], key))
        total.extend(word_filter(trie, '?'+'*'+pattern[1:], key))
    #only recurses if the given character that's a letter matches at least one of the children.
    else:
        if pattern[0] in trie.children:
            total.extend(word_filter(trie.children[pattern[0]], pattern[1:], key+pattern[0]))
    

    return total