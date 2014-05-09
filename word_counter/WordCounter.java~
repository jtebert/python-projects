import java.util.*;
import java.math.*;

public class WordCounter {
    
    // Fields
    String inputFile;
    TreeMap<String, Integer> wordMap;
    int numCommonWords;
    int numStrings;
    
    // Constructor
    WordCounter(String inputFile, int numCommonWords) {
        this.inputFile = inputFile;
        this.wordMap = buildMap(new StringIterator(inputFile));
        this.numCommonWords = numCommonWords;
        this.numStrings = this.numStrings();
    }
    
    public static void main(String[] args) {
        int numWords;
        if (args.length < 2) {
            numWords = 25;
        } else {
            numWords = Integer.parseInt(args[1]);
        }
        WordCounter counter = new WordCounter(args[0], numWords);
        System.out.println(counter.inputFile + ": ");
        System.out.println("Total words in file: " + counter.numStrings);
        System.out.println("Unique words in file: " + counter.wordMap.size());
        System.out.println(counter.numCommonWords + " most used word" +
            counter.addS() + ":");
        Map<String, Integer> commonWords = 
            counter.commonestWords(counter.numCommonWords);
        for (Map.Entry<String, Integer> entry : commonWords.entrySet()) {
            System.out.println("\t" + entry.getKey() + "\t" + entry.getValue() +
                 "\t(" + counter.getPercent(entry.getValue()) + "%)");
        }
    }
    
    // Build a map of words and # of occurrences from the input file
    TreeMap<String, Integer> buildMap(Iterator<String> sit) {
        String currentKey = "";
        TreeMap<String, Integer> map = new TreeMap<String, Integer>();
        while (sit.hasNext()) {
            currentKey = sit.next();
            if (map.containsKey(currentKey)) {
                map.put(currentKey, map.get(currentKey) + 1);
            }
            else {
                map.put(currentKey, 1);
            }
        }
        return map;
    }
    
    // Return number of words in document:
    int numStrings() {
        int numString = 0;
        Iterator<String> sit = new StringIterator(inputFile);
        while (sit.hasNext()) {
            numString++;
            sit.next();
        }
        return numString;
    }
    
    // Get the k highest values from the word/occurences map
    ArrayList<Integer> getMaximumValues(int k) {
        ArrayList<Integer> values = new ArrayList<Integer>(wordMap.values());
        Collections.sort(values);
        int numVals = values.size();
        ArrayList<Integer> maxima =
            new ArrayList<Integer>(values.subList(numVals - k, numVals));
        return maxima;
    }
    
    // Get the keys with the maximum values (k most common words)
    Map<String, Integer> commonestWords(int k) {
        ArrayList<Integer> maxOccurrences = getMaximumValues(k);
        Map<String, Integer> commonWords = new HashMap<String, Integer>();
        for (Map.Entry<String, Integer> entry : wordMap.entrySet()) {
            if (maxOccurrences.contains(entry.getValue())) {
                commonWords.put(entry.getKey(), entry.getValue());
            }
        }
        Map<String, Integer> sortedByNum = WordCounter.sortByValue(commonWords);
        //Collections.sort(commonWords);
        return sortedByNum;
    }
    
    public static Map<String, Integer> sortByValue(Map<String, Integer> map) {
        List<Map.Entry<String, Integer>> list =
            new LinkedList<Map.Entry<String, Integer>>(map.entrySet());
        Collections.sort(list,
            new Comparator<Map.Entry<String, Integer>>() {
                public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
                    return (o2.getValue()).compareTo( o1.getValue() );
            }
        } );
        Map<String, Integer> result = new LinkedHashMap<String, Integer>();
        for (Map.Entry<String, Integer> entry : list) {
            result.put( entry.getKey(), entry.getValue() );
        }
        return result;
    }
    
    // Add an "s" if numCommonWords > 1
    String addS() {
        String s = "";
        if (numCommonWords != 1) { s = "s";}
        return s;
    }
    
    // Get percent of 2 ints
    Double getPercent(int numWords) {
        return round(numWords * 100.0 / numStrings, 2);
    }
    
    public static double round(double value, int places) {
        if (places < 0) throw new IllegalArgumentException();
        BigDecimal bd = new BigDecimal(value);
        bd = bd.setScale(places, RoundingMode.HALF_UP);
        return bd.doubleValue();
    }
    
}
