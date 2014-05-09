#!/usr/bin/env python
import re
import sys
import operator
import numpy as np
import matplotlib.pyplot as plt

class Word_counter:
    def __init__(self, input_file, num_common_words):
        self.input_file = input_file
        text_it = String_iterator(input_file)
        self.text = text_it.words
        self.word_map = self.build_map(text_it)
        self.num_common_words = num_common_words
        self.num_strings = len(text_it.words)
    
    # Build a map/dictionary of the words and number of occurrences
    def build_map(self, sit):
        word_map = {}
        for word in sit:
            if word in word_map:
                word_map[word] = word_map[word] + 1
            else:
                word_map[word] = 1;
        return word_map
        
    # Get the k highest number of occurrences from the dict
    def get_max_occurs(self, k):
        occurs = self.word_map.values()
        occurs.sort()
        num_vals = len(occurs)
        maxima = occurs[num_vals - k : num_vals]
        return maxima
    
    # Return a list of tuples with the k most common words & num of occurrences
    def commonest_words(self, k):
        max_occurrences = self.get_max_occurs(k)
        common_words = {}
        for pair in self.word_map.items():
            if pair[1] in max_occurrences:
                common_words[pair[0]] = pair[1]
        common_words = \
            sorted(common_words.iteritems(), key=operator.itemgetter(1))
        common_words.reverse()
        return common_words
        
    # Print a String of info about the word from the tuple (word, occurrences)
    def print_word_info(self, pair):
        print "\t" + pair[0] + "\t" + str(pair[1]) + "\t(" + \
            str(self.get_percent(pair[1])) + "%)"
        
    # Plot the distribution of word frequency (for all words >.1% of total num)
    def plot_words_freq(self):
        thresh_num = self.num_strings * .1/100.0
        num_occurrences = self.word_map.values()
        num_occurrences.sort()
        num_occurrences.reverse()
        num_occurrences = filter(lambda x: x > thresh_num, num_occurrences)
        num_occurrences = [self.get_percent(x) for x in num_occurrences]
        ind = range(len(num_occurrences))
        fig, ax = plt.subplots()
        rects = ax.bar(ind, num_occurrences, width=1, color='b',edgecolor='none')
        #Add labels, etc.
        ax.set_title('Distribution of Word Commonality')
        ax.set_ylabel('Percentage of Use')
        ax.set_xlabel('Word Usage Order')
        ax.set_xlim(xmax=len(num_occurrences))
        plt.draw()
        
    # Plot distribution of a word in the text file (Like Kindle x-ray feature)
    # Current simple version: basically a histogram
    def word_xray(self, word):
        word = word.lower()
        num_text_divs = 500
        text_div_size = self.num_strings / num_text_divs
        #text_div_size = 100
        text_divs = range(0, self.num_strings, text_div_size)
        num_occurrences = []
        for i in text_divs:
            snippet = self.text[i:i + text_div_size]
            count = len(filter(lambda s: s == word, snippet))
            num_occurrences.append(count)
        occurred = [min(x, 1) for x in num_occurrences]
        # Create plot
        ind = np.linspace(0, 1, num=len(num_occurrences))
        width = ind[1]-ind[0]
        fig, ax = plt.subplots()
        rects = ax.bar(ind, occurred, width, color='r', edgecolor='none')
        ax.set_title('Distribution of "' + word + '" in text')
        ax.set_xlabel('Text Progression')
        ax.set_xlim((0, 1))
        ax.get_yaxis().set_visible(False)
        ax.set_aspect(.2)
        plt.draw()
        
    # Get percent of total words this numWords is
    def get_percent(self, num_words):
        percent = num_words * 100.0 / self.num_strings
        return int(percent * 100) / 100.0
    
    # Return an "s" or empty string if num_common_words =/!= 1
    def add_s(self):
        s = ""
        if self.num_common_words != 1:
            s = "s"
        return s

class String_iterator:
    def __init__(self, filename):
        self.words = []
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            self.words.extend(line.split(" "))
        for i in range(len(self.words)):
            self.words[i] = re.sub(r"[^a-zA-Z0-9_\-']", '', self.words[i])
        # This filter is changing the indexing and messing things up, I think
        self.words = filter(None, self.words)
        self.words = map(lambda x:x.lower(), self.words)
        self.ind = 0
        self.size = len(self.words)
        
    def __iter__(self):
        return self
    
    def next(self):
        try:
            result = self.words[self.ind]
        except IndexError:
            raise StopIteration
        self.ind += 1
        return result
            
# Get filename or raise exception
if len(sys.argv) < 2:
    raise IndexError('No filename provided')
else:
    filename = sys.argv[1]

# Get number of most common words to produce
if len(sys.argv) < 3:
    num_words = 25
else:
    num_words = int(sys.argv[2])

# Create the counter
counter = Word_counter(filename, num_words)

# Print the results
print "Total words in file: " + str(counter.num_strings)
print "Unique words in file: " + str(len(counter.word_map))
print str(counter.num_common_words) + " most used word" + counter.add_s() + ":"
for pair in counter.commonest_words(counter.num_common_words):
    counter.print_word_info(pair)

# Graphs:
counter.plot_words_freq()
if len(sys.argv) >= 4:
    counter.word_xray(sys.argv[3])
plt.show()
