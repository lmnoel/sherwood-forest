import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Scanner;

public class McDonaldAnalyzer2 {
	
	private static ArrayList<String> negPosWords;
	
	private static List<String> positiveWords;
	private static List<String> negativeWords;
	
	private static ArrayList<String> punctuationMarks;
	
	private static HashMap<Integer,Double> dateMultipliers;

	McDonaldAnalyzer2() {//constructor
		punctuationMarks = new ArrayList<String>();
		punctuationMarks.add(".");
		punctuationMarks.add(",");
		punctuationMarks.add("?");
		punctuationMarks.add("!");
		
		negPosWords = new ArrayList<String>();
		positiveWords = new ArrayList<String>();
		negativeWords = new ArrayList<String>();
		
		readInput("negative.txt", negPosWords);
		readInput("positive.txt", negPosWords);
		readInput("negative.txt", negativeWords);
		readInput("positive.txt", positiveWords);
		
		
	}//constructor
	
	public static void main(String[] args) {
		McDonaldAnalyzer2 analyzer = new McDonaldAnalyzer2();
		analyzer.processNYT();
	}
	
	
	
	public void processNYT() {
		SpyAnalyzer marketAnalyzer = new SpyAnalyzer();
		marketAnalyzer.collectData();
		dateMultipliers = marketAnalyzer.dateMultiplier;
		
		//clean newspaperCodings directory
		File cleanDirectory = new File ("newspaperCodings");
		File[] deleteFiles = cleanDirectory.listFiles();
		for (File deleteFile : deleteFiles) {
			deleteFile.delete();
		}
		
		
		File[] files = new File("newspaperdata").listFiles();
		fileRecurse(files);
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
				
				String dateMapFormat = elements[0];
				dateMapFormat += elements[1];
				dateMapFormat += elements[2];

				if (dateMultipliers.get(Integer.parseInt(dateMapFormat))==null) continue;
				double currMultiple = dateMultipliers.get(Integer.parseInt(dateMapFormat));
				
				McDonaldAnalyzer2.analyzeAndStore(articles[i+1], currMultiple);
				
				
				System.out.println(elements[0]+" "+elements[1]+" "+elements[2]);
			}
		}
	}
	
	//analyzes a nyt article and stores it in a file
	//the file's first line contains the positive word count followed by 
	//the negative word count, separated by a comma.
	//the file's second line contains the instances of each word in negPosWords,
	//also separated by commas
	public static void analyzeAndStore(String text, double currMultiple) {
		
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
		
		//initialize wordCounts double[] and fill with 0s
		int[] wordCounts = new int[negPosWords.size()];
		for (int i=0; i<wordCounts.length;++i) {
			wordCounts[i]=0;
		}
		
		
		for (String word : words) {
			for (int i=0; i<negPosWords.size();++i) {
				if (word.equals(negPosWords.get(i))) {
					wordCounts[i]++;
				}
			}
			for (String posWord : positiveWords) {
				if (word.equals(posWord)) posWordCount++;
			}
			for (String negWord : negativeWords) {
				if (word.equals(negWord)) negWordCount++;
			}
		}
		
		for (int i=0; i<wordCounts.length;++i) {
		}
		
		
		String filename = "newspaperCodings/article";
		File file = new File(filename.concat(Long.toString(System.currentTimeMillis()) +".txt"));
		
		BufferedWriter bw = null;
		FileWriter fw = null;
		try {

			fw = new FileWriter(file);
			bw = new BufferedWriter(fw);
			
			//on first line, write positive word count, comma, negative word count
			bw.write(Integer.toString(posWordCount)+","+Integer.toString(negWordCount));
			bw.newLine();
			
			
			//on second line, write contents of wordCounts separated by commas
			for (int i=0; i<wordCounts.length;++i) {
				if(i!=0) bw.write(",");
				bw.write(Integer.toString(wordCounts[i]));
			}
			bw.newLine();
			
			
			//on third line, write close/open multiple from market of day
			bw.write(Double.toString(currMultiple));

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
		
		
		
		
		
		
	}//analyzeAndStore()
	
	
	
	
	
	
	
	
	
	
	//used to read in positive.txt and negative.txt
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
	
	//close file readers
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
