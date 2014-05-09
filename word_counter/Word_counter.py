import re
import sys

class Word_counter:
    def __init__(self, input_file, num_common_words):
        self.input_file = input_file
        sit = String_iterator(input_file)
        self.word_map = self.build_map(sit)
        self.num_common_words = num_common_words
        self.num_strings = len(sit.words)
    
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
        #print self.words
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
#Print the results
print "Total words in file: " + str(counter.num_strings)
print "Unique words in file: " + str(len(counter.word_map))

print "Finished."


