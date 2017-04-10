import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Constants {

	Constants() {}
	
	public static String input = "";
	
	static final ArrayList<String> punctuationMarks = new ArrayList<String>() {
		private static final long serialVersionUID = 1L;

		{
			add(".");
			add(",");
			add("?");
			add("!");
		}
	};

	
	// *** INDICATORS ***

	public static Map<String, Integer> immigrationIndicators = new HashMap<String, Integer>() {
		private static final long serialVersionUID = 1L;
	};
	public static Map<String, Integer> tradeIndicators = new HashMap<String, Integer>() {
		private static final long serialVersionUID = 1L;
	};
	public static Map<String, Integer> energyIndicators = new HashMap<String, Integer>() {
		private static final long serialVersionUID = 1L;
	};
	public static Map<String, Integer> financeIndicators = new HashMap<String, Integer>() {
		private static final long serialVersionUID = 1L;
	};
	public static Map<String, Integer> infrastructureIndicators = new HashMap<String, Integer>() {
		private static final long serialVersionUID = 1L;
	};
	
	
	
	// *** CLASSIFIERS ***
	
	public static Map<String, Float> generalClassifiers = new HashMap<String, Float>() {
		private static final long serialVersionUID = 1L;
	};
	
	public static Map<String, Float> immigrationClassifiers = new HashMap<String, Float>() {
		private static final long serialVersionUID = 1L;
	};
	public static Map<String, Float> tradeClassifiers = new HashMap<String, Float>() {
		private static final long serialVersionUID = 1L;
	};
	public static Map<String, Float> energyClassifiers = new HashMap<String, Float>() {
		private static final long serialVersionUID = 1L;
	};
	public static Map<String, Float> financeClassifiers = new HashMap<String, Float>() {
		private static final long serialVersionUID = 1L;
	};
	public static Map<String, Float> infrastructureClassifiers = new HashMap<String, Float>() {
		private static final long serialVersionUID = 1L;
	};
	
	
	// *** CATEGORIES ***
	
	public static final ArrayList<Category> categories = new ArrayList<Category>() {
		private static final long serialVersionUID = 1L;

		{
			add(new Category(immigrationIndicators, "Immigration", immigrationClassifiers));
			add(new Category(tradeIndicators, "Trade", tradeClassifiers));
			add(new Category(energyIndicators, "Energy", energyClassifiers));
			add(new Category(financeIndicators, "Finance", financeClassifiers));
			add(new Category(infrastructureIndicators, "Infrastructure", infrastructureClassifiers));
		}
	};
	
}
	


