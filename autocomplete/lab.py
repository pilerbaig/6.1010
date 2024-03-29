"""
6.1010 Spring '23 Lab 9: Autocomplete
"""

# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

class PrefixTree:
    """
    Initialize an instance of the PrefixTree class.
    """
    def __init__(self):
        self.value = None
        self.children = {}

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the prefix tree,
        or reassign the associated value if it is already present.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError
        if not key:
            self.value = value
        else:
            if key[:1] not in self.children:
                self.children[key[0]] = PrefixTree()
            self.children[key[0]].__setitem__(key[1:], value)

    def __gettree__(self, key):
        """
        Return the subtree for the specified prefix.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError
        if not key:
            return (self, self.value)
        if key[0] not in self.children:
            raise KeyError
        else:
            return self.children[key[0]].__gettree__(key[1:])

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        return self.__gettree__(key)[1]
                

    def __delitem__(self, key):
        """
        Delete the given key from the prefix tree if it exists.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError
        if not key:
            if self.value is None:
                raise KeyError
            else:
                self.value = None
        elif key[0] not in self.children:
            raise KeyError
        else:
            self.children[key[0]].__delitem__(key[1:])
        

    def has(self, key):
        """
        Is key a key in the prefix tree? Does the key have a node in the
        prefix tree? Returns a tuple of two bools, True or False for each.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError
        if not key:
            if self.value is None:
                return (False, True)
            else:
                return (True, True)
        if key[0] not in self.children:
            return (False, False)
        else:
            return self.children[key[0]].has(key[1:])

    def __contains__(self, key):
        """
        Is key a key in the prefix tree?  Return True or False.
        Raise a TypeError if the given key is not a string.
        """
        return self.has(key)[0]

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this prefix tree
        and its children.  Must be a generator!
        """
        if self.value is not None:
            yield ("", self.value)
        for key, tree in self.children.items():
            for (subkey, subvalue) in tree.__iter__():
                yield (key + subkey, subvalue)
            



def word_frequencies(text):
    """
    Given a piece of text as a single string, create a prefix tree whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.
    """
    tree = PrefixTree()
    all_words = []
    word_freq = {}
    sentences = tokenize_sentences(text)
    for sentence in sentences:
        all_words.extend(sentence.split())
    for word in all_words:
        word_freq[word] = word_freq.setdefault(word, 0) + 1
    for word, freq in word_freq.items():
        tree[word] = freq
    return tree


def autocomplete(tree, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is not a string.
    """
    if not isinstance(prefix, str):
        raise TypeError
    if not tree.has(prefix)[1]:
        return []
    running_dict = {}
    freq_list = []
    prefix_tree = tree.__gettree__(prefix)[0]
    for key, val in prefix_tree:
        running_dict.setdefault(val, []).append(prefix + key)
    for freq in range(max(running_dict.keys()), 0, -1):
        if freq in running_dict:
            if max_count is not None and len(freq_list) >= max_count:
                break
            for word in running_dict[freq]:
                if max_count is not None and len(freq_list) >= max_count:
                    break
                freq_list.append(word)
    return freq_list


def edits_list(prefix):
    """
    Given a prefix, return a list of all possible edits to the prefix
    by insertion, deletion, replacement, and transposition.
    """
    insert_list = []
    delete_list = []
    replace_list = []
    transpose_list = []
    for i, _ in enumerate(prefix):
        delete_list.append(prefix[:i] + prefix[i+1:])
        # for j in range(i+1, len(prefix)):
        if i < len(prefix) - 1:
            transpose_list.append(prefix[:i] + prefix[i+1] \
                                + prefix[i] + prefix[i+2:])
        for letter in ALPHABET:
            insert_list.append(prefix[:i] + letter + prefix[i:])
            replace_list.append(prefix[:i] + letter + prefix[i+1:])
    edit_list = []
    [edit_list.extend(edit) for edit in \
        [insert_list, delete_list, replace_list, transpose_list]]

    return edit_list

def sort_list_to_dict(input_list, tree):
    running_dict = {}
    running_dict_sorted = {}
    for word in input_list:
        if word in tree:
            running_dict[word] = \
                running_dict.setdefault(word, 0) + tree[word]
            
    for freq in range(max(running_dict.values()), 0, -1):
        for word, word_freq in running_dict.items():
            if word_freq == freq:
                running_dict_sorted.setdefault(freq, []).append(word)
    
    return running_dict_sorted

def autocorrect(tree, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    freq_list = autocomplete(tree, prefix, max_count)
    if max_count is not None and len(freq_list) == max_count:
        return freq_list
    if max_count is not None:
        max_count_edit = max_count - len(freq_list)
    else:
        max_count_edit = None
    
    edit_list = edits_list(prefix)

    freq_list_edit = []
    running_dict_sorted = sort_list_to_dict(edit_list, tree)

    for freq in range(max(running_dict_sorted.keys()), 0, -1):
        if freq in running_dict_sorted:
            if max_count_edit is not None and len(freq_list_edit) >= max_count_edit:
                break
            for word in running_dict_sorted[freq]:
                if max_count_edit is not None and len(freq_list_edit) >= max_count_edit:
                    break
                if word not in freq_list:
                    freq_list_edit.append(word)

    freq_list_total = []
    freq_list_total.extend(freq_list)
    freq_list_total.extend(freq_list_edit)
    return freq_list_total



def word_filter(tree, pattern, curr_key=None):
    """
    Return list of (word, freq) for all words in the given prefix tree that
    match pattern.  pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    pattern_words = []
    if curr_key is None:
        curr_key = ""

    if not pattern:
        if tree.value is not None:
            return [(curr_key, tree.value)]
    
    elif pattern[0] == "?":
        if tree.children.items():
            for key, child in tree.children.items():
                pattern_words.extend(word_filter(child, pattern[1:], curr_key + key))
    
    elif pattern[0] == "*":
        if tree.children.items():
            for key, child in tree.children.items():
                pattern_words.extend(word_filter(child, pattern, curr_key + key))
        pattern_words.extend(word_filter(tree, pattern[1:], curr_key))

    else:
        if pattern[0] in tree.children:
            pattern_words.extend(word_filter(tree.children[pattern[0]], pattern[1:], curr_key + pattern[0]))
    
    return list(set(pattern_words))
    


# you can include test cases of your own in the block below.
if __name__ == "__main__":
    #doctest.testmod()
    # t = PrefixTree()
    # t.value = 2
    # t.__setitem__("bar", 3)
    # t.__setitem__("bad", 8)
    # t.__setitem__("b", 4)
    # print(t.__contains__("ba"))
    # for i in t:
    #     print(i)
    # texty = "b ba bar bad bard bardy. bardy bar bard. bardy!!! bardye bardyep!"
    # all_words = []
    # word_freq = {}
    # words = tokenize_sentences(texty)
    # for sentence in words:
    #     all_words.extend(sentence.split())
    # print(all_words)
    # for word in all_words:
    #     word_freq[word] = word_freq.setdefault(word, 0) + 1
    # print(word_freq)
    # t = word_frequencies(texty)
    # freqs = freq_tree.__getitem__("hi")
    ##print(autocomplete(freq_tree, "bar", 2))
    #t = word_frequencies("man mat mattress map me met a man a a a map man met")
    #result = autocorrect(t, 'ma', 10)
    # result = autocorrect(t, "ba", 10)
    # print(result)
    #assert set(result) == {"man", "map", "met"}
    # with open("Metamorphosis.txt", encoding="utf-8") as f:
    #     text = f.read()
    with open("Dracula.txt", encoding="utf-8") as f:
        text = f.read()
    freqs = word_frequencies(text)
    # print(autocorrect(freqs, "gre", 6))
    # print(word_filter(freqs, "c*h"))
    # print(word_filter(freqs, "r?c*t"))
    # print(autocorrect(freqs, "hear"))
    all_wordies = word_filter(freqs, "*")
    # print(len(all_wordies))
    all_words = []
    word_freq = {}
    sentences = tokenize_sentences(text)
    for sentence in sentences:
        all_words.extend(sentence.split())
    print(len(all_words))

