import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Scanner;


import java.io.*;

/*
 * 
 * THIS ANALYZE FUNCTION OF THIS CLASS RETURNS (positiveWords-negativeWords)/totalWords
 * 
 */


public class McDonaldAnalyzer {
	
	public ArrayList<DateScore> dateScores;

	public HashMap<Integer, Double> formatDateScores;

	private static List<String> positiveWords;
	private static List<String> negativeWords;
	
	private static ArrayList<String> punctuationMarks;

	McDonaldAnalyzer() {//constructor
		punctuationMarks = new ArrayList<String>();
		punctuationMarks.add(".");
		punctuationMarks.add(",");
		punctuationMarks.add("?");
		punctuationMarks.add("!");
		
		positiveWords = new ArrayList<String>();
		negativeWords = new ArrayList<String>();
		
		readInput("negative.txt", negativeWords);
		readInput("positive.txt", positiveWords);
		
		
	}//constructor
	
	
	public static double analyze(String text) {
		int posWordCount = 0;
		int negWordCount = 0;
		String[] words = text.split(" ");
		
		for (int i = 0; i < words.length; i++) {
			
			words[i] = words[i].toLowerCase();

			for (String punctuation : punctuationMarks) {
				if (words[i].contains(punctuation)) {
					words[i] = words[i].replace(punctuation, "");
				}
			}
			
		}
		
		for (String word : words) {
			
			for (String posWord : positiveWords) {
				if (word.equals(posWord)) posWordCount++;
			}
			for (String negWord : negativeWords) {
				if (word.equals(negWord)) negWordCount++;
			}
		}
		
		//TEMP
		//System.out.println("posWordCount: " + posWordCount);
		//System.out.println("negWordCount: " + negWordCount);
		
		//return (double)(((double)posWordCount - (double)negWordCount)/(double)words.length);
		return (double)((double)posWordCount - (double)negWordCount);
		
	}
	
	//TEMP FOR TESTING
	public static void main(String[] args) {
		
		McDonaldAnalyzer analyzer = new McDonaldAnalyzer();
		analyzer.processNYT();
		//analyzer.load();

		
		analyzer.createMap();
	}
	
	public void createMap() {
		formatDateScores = new HashMap<Integer, Double>();
		
		for (DateScore dateScore : dateScores) {
			String dateFormat = Integer.toString(dateScore.year);
			dateFormat += Integer.toString(dateScore.month);
			dateFormat += Integer.toString(dateScore.day);
			
			
			formatDateScores.put(Integer.parseInt(dateFormat), dateScore.score);
			
	    }
	}
	
	public void load() {
		dateScores = new ArrayList<DateScore>();
		FileReader fr = null;
		BufferedReader br = null;

		try {
			fr = new FileReader("nytDateScore.txt");
			br = new BufferedReader(fr);

			while (true) {
				String line = br.readLine();
				if (line == null)
					break;
				//else
				String[] elements = line.split(":");
				dateScores.add(new DateScore(Integer.parseInt(elements[0]),
						Integer.parseInt(elements[1]),
						Integer.parseInt(elements[2]),
						Double.parseDouble(elements[3])));
				
				
			}

		} catch (FileNotFoundException fnfe) {
			System.out.println(fnfe.getMessage());
		} catch (IOException ioe) {
			System.out.println(ioe.getMessage());
		} finally {
			closeReaders(br, fr);
		}
	}
	
	
	//one use of this function processes the entire NYT folder into nytDateScore
	public void processNYT() {
		dateScores = new ArrayList<DateScore>();
		File[] files = new File("newspaperdata").listFiles();
		fileRecurse(files);
		
		String filename = "nytDateScore.txt";
		BufferedWriter bw = null;
		FileWriter fw = null;

		try {

			fw = new FileWriter(filename);
			bw = new BufferedWriter(fw);
			
			
			//record inputCount, hiddenCount, outputCount, learnRate, and momentum
			for (DateScore dateScore : dateScores) {
				bw.write(Integer.toString(dateScore.year) + ":" + 
						Integer.toString(dateScore.month) + ":" + 
						Integer.toString(dateScore.day) + ":");
				bw.write(Double.toString(dateScore.score));
				bw.newLine();
			}
			


		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (bw != null)
					bw.close();
				if (fw != null)
					fw.close();
			} catch (IOException ex) {
				ex.printStackTrace();
			}
		}
		
		
	}
	
	private void fileRecurse(File[] files) {
	    for (File file : files) {
	        if (file.isDirectory()) {
	        		if (Integer.parseInt(file.getName().split("_")[0]) > 1994) {
	        			System.out.println(file.getName());
	        		}
	            fileRecurse(file.listFiles()); // Calls same method again.
	        } else {
	            if (file.getName().equals("nyt_business.txt")) {
	            		String text = null;
	            		Scanner scanner = null;
	            		try {
	            			scanner = new Scanner( file );
	            			text = scanner.useDelimiter("\\A").next();
	            			readNYT(text);
	            		} catch (FileNotFoundException e) {
	            			e.printStackTrace();
	            		} finally {
	            			scanner.close();
	            		}
	            		
	            }
	        }
	    }
	}
	
	
	//this function reads a single NYT txt file named nyt_business.txt
	private void readNYT(String text) {
		
		String[] articles = text.split("\\r?\\n-----\\r?\\n");
		for (int i=0; i<articles.length;++i) {
			if (i==0) continue;
			if (i%2==1) {
				if (i==articles.length-1) break;
				String date = articles[i].split("T")[0];
				date = date.replaceAll(Character.toString((char)10), "");
				String[] elements = date.split("-");
				double currScore = McDonaldAnalyzer.analyze(articles[i+1]);
				System.out.println(elements[0]+" "+elements[1]+" "+elements[2]);
				dateScores.add(new DateScore(Integer.parseInt(elements[0]),
						Integer.parseInt(elements[1]),
						Integer.parseInt(elements[2]),
						currScore));
			}
		}
	}
	

	public static void readInput(String filename, List<String> list) {

		FileReader fr = null;
		BufferedReader br = null;

		try {
			fr = new FileReader(filename);
			br = new BufferedReader(fr);

			while (true) {
				String line = br.readLine();
				if (line == null)
					break;
				//else
				line = line.toLowerCase();
				list.add(line);
			}

		} catch (FileNotFoundException fnfe) {
			System.out.println(fnfe.getMessage());
		} catch (IOException ioe) {
			System.out.println(ioe.getMessage());
		} finally {
			closeReaders(br, fr);
		}
	}
	
	public static void closeReaders(BufferedReader br, FileReader fr) {
		if (br != null) {
			try {
				br.close();
			} catch (IOException ioe) {
				System.out.print(ioe.getMessage());
			}
		}
		if (fr != null)
			try {
				fr.close();
			} catch (IOException ioe) {
				System.out.print(ioe.getMessage());
			}
	}
	
	
}
