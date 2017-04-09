import java.util.ArrayList;
import java.util.Map;
import java.util.Map.Entry;

public class TextProcessor {

	TextProcessor() {}

	private static int counter = 0;

	private static boolean[] negations;
	private static boolean[] punctuations;

	private static boolean negate = false;
	
	private static boolean capitalTitle = false;
	
	private static String classifiersFile = "categories.txt";
	private static String inputFile = "input.txt";

	public static void main(String[] args) {
		long startTime = System.currentTimeMillis();//temp
		FileParser.readClassifiers(classifiersFile);
		FileParser.readInput(inputFile);
		
		
		read(Constants.input);
		
		//temp
		long endTime   = System.currentTimeMillis();
		long totalTime = endTime - startTime;
		System.out.println("Runtime: " + totalTime + "ms");
	}

	static void read(String input) {
		
		if (capitalTitle(input)) {
			capitalTitle = true;
		}
		

		// make word array
		String[] words = input.split(" ");

		negations = new boolean[words.length];
		punctuations = new boolean[words.length];
		for (boolean b : punctuations) {
			b = false;
		}
		for (boolean b : negations) {
			b = false;
		}

		// remove punctuation
		for (int i = 0; i < words.length; i++) {
			words[i] = words[i].toLowerCase();

			for (String punctuation : Constants.punctuationMarks) {
				if (words[i].contains(punctuation)) {
					words[i] = words[i].replace(punctuation, "");
					punctuations[i] = true;
				}
			}
			if (words[i].contains("n't") || words[i].equals("not")) {
				negations[i] = true;
			}
		}

		// *** DETERMINE CATEGORY ***

		// tally up each category
		for (String word : words) {
			for (Category category : Constants.categories) {
				for (Map.Entry<String, Integer> indicator : category.indicators.entrySet()) {
					if (word.toLowerCase().equals(indicator.getKey())) {
						category.increaseBy(indicator.getValue());
					}
				}
			}
		}
		for (Category category : Constants.categories) {
			category.score /= category.indicators.size();
		}

		// pick best category
		float maxCategoryRating = 0;
		Category maxCategory = null;
		for (Category category : Constants.categories) { // find max category
			if (category.score > maxCategoryRating) {
				maxCategoryRating = category.score;
				maxCategory = category;
			}
			System.out.println(category.name + ": " + category.score);//TEMP
		}

		if (maxCategory == null) {
			System.out.println("Unable to detect category");
			return;
		}
		
		
		System.out.println("Category: " + maxCategory.name);

		// *** DETERMINE POSITIVITY/NEGATIVITY ***

		// determine rating
		float rating = 0f;
		for (int i = 0; i < words.length; i++) {

			// general classifiers
			rating = rate(words[i], rating, i, Constants.generalClassifiers);

			// specific classifiers
			rating = rate(words[i], rating, i, maxCategory.classifiers);

		}
		rating /= counter;
		
		
		System.out.println("Rating: " + rating);

	}

	private static float rate(String word, float rating, int index, Map<String, Float> map) {

		for (Entry<String, Float> entry : map.entrySet()) {
			if (word.equals(entry.getKey())) {
				counter++;
				float value = entry.getValue();
				
				//update score accounting for negation
				if (!negate) rating += value;
				else {
					rating -= value;
				}
			}
			
			
			//check for negations or punctuation and update negate accordingly
			if (negations[index]) {
				negate = true;
			}
			if (punctuations[index]) {
				negate = false;
			}
			
		}

		return rating;
	}
	private static boolean capitalTitle(String text) {
		int capitalsCounter = 0;
		int lowercaseCounter = 0;
		
		for (int i=0; i<text.length(); i++) {
			
			if (text.charAt(i) == '-') {
				break;
			}
			
			if (Character.isUpperCase(text.charAt(i))) {
				capitalsCounter++;
			}
			else lowercaseCounter++;
		}
		
		if (capitalsCounter > lowercaseCounter) {
			return true;
		}
		else return false;
		
	}
	
	private static void printCategories() { //for testing
		
		System.out.println("Immigration Indicators:");
		for (Map.Entry<String, Integer> indicator : Constants.immigrationIndicators.entrySet()) {
			System.out.println(indicator.getKey() + " : " + indicator.getValue());
		}
		
		System.out.println("Trade Indicators:");
		for (Map.Entry<String, Integer> indicator : Constants.tradeIndicators.entrySet()) {
			System.out.println(indicator.getKey() + " : " + indicator.getValue());
		}
		
		System.out.println("Energy Indicators:");
		for (Map.Entry<String, Integer> indicator : Constants.energyIndicators.entrySet()) {
			System.out.println(indicator.getKey() + " : " + indicator.getValue());
		}
		
		System.out.println("Finance Indicators:");
		for (Map.Entry<String, Integer> indicator : Constants.financeIndicators.entrySet()) {
			System.out.println(indicator.getKey() + " : " + indicator.getValue());
		}
		
		System.out.println("Infrastructure Indicators:");
		for (Map.Entry<String, Integer> indicator : Constants.infrastructureIndicators.entrySet()) {
			System.out.println(indicator.getKey() + " : " + indicator.getValue());
		}
		
		System.out.println("General Classifiers:");
		for (Map.Entry<String, Float> indicator : Constants.generalClassifiers.entrySet()) {
			System.out.println(indicator.getKey() + " : " + indicator.getValue());
		}
		
		System.out.println("Immigration Classifiers:");
		for (Map.Entry<String, Float> indicator : Constants.immigrationClassifiers.entrySet()) {
			System.out.println(indicator.getKey() + " : " + indicator.getValue());
		}
		
		System.out.println("Trade Classifiers:");
		for (Map.Entry<String, Float> indicator : Constants.tradeClassifiers.entrySet()) {
			System.out.println(indicator.getKey() + " : " + indicator.getValue());
		}
		
		System.out.println("Energy Classifiers:");
		for (Map.Entry<String, Float> indicator : Constants.energyClassifiers.entrySet()) {
			System.out.println(indicator.getKey() + " : " + indicator.getValue());
		}
		
		System.out.println("Finance Classifiers:");
		for (Map.Entry<String, Float> indicator : Constants.financeClassifiers.entrySet()) {
			System.out.println(indicator.getKey() + " : " + indicator.getValue());
		}
		
		System.out.println("Infrastructure Classifiers:");
		for (Map.Entry<String, Float> indicator : Constants.infrastructureClassifiers.entrySet()) {
			System.out.println(indicator.getKey() + " : " + indicator.getValue());
		}
	}
}
