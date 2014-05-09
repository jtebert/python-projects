[Requires matplotlib]

This Python program is designed to calculate word usage statistics on a text
document:
- Total words in the file
- Number of unique words in the file
- Most commonly used words in the file, including instances and frequency
- Plot the distribution of word frequency (bar graph)

To run the program:
    python Word_counter $TEXTFILE [$NUMWORDS]
$TEXTFILE is the name and location of the text file to analyze
$NUMWORDS is the number of top most-used words to list.  If not specified,
defaults to 25.

For your convenience a sample text file is provided to use with the program:
    iliad.txt
    
Future goals:
- Show distribution of where a specific word occurs in the text (like that Kindle feature)
- Various ways to compare two different texts
- Using a dictionary API to assess word part of speech
