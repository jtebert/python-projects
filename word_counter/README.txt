[ There is currently also a fully functional Java implementation here, but my
  goal is to convert the project completely to Python. Mostly for practice. ]

This Python program is designed to calculate word usage statistics on a text
document:
- Total words in the file
- Number of unique words in the file
- Most commonly used words in the file, including instances and frequency

To run the program:
    python Word_counter $TEXTFILE [$NUMWORDS]
$TEXTFILE is the name and location of the text file to analyze
$NUMWORDS is the number of top most-used words to list.  If not specified,
defaults to 25.

For your convenience a sample text file is provided to use with the program:
    iliad.txt
    
Future goals:
- Plot distribution of word usage
- Using a dictionary API to assess word part of speech
