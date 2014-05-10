[Requires matplotlib and numpy]

This Python program is designed to calculate word usage statistics on a text
document:
- Total words in the file
- Number of unique words in the file
- Most commonly used words in the file, including instances and frequency
- Plot the distribution of word frequency (bar graph)
- Show the distribution of appearances of a word through the text
  (To see why this is cool, search iliad.txt for "Patroclus" and you can see
  where he shows up in the story.)

To run the program:
    python Word_counter $TEXTFILE [$NUMWORDS $SEARCHWORD]
$TEXTFILE is the name and location of the text file to analyze
$NUMWORDS is the number of top most-used words to list.  If not specified,
defaults to 25.
$SEARCHWORD is a word to search the text file for to display its usage

For your convenience a sample text file is provided to use with the program:
    iliad.txt
    
Future goals:
- Various ways to compare two different texts
- Using a dictionary API to assess word part of speech
