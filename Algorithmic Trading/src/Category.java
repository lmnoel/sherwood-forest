import java.util.HashMap;
import java.util.Map;

public class Category {
	
	public float score = 0;
	public String name;
	public Map<String, Float> classifiers;
	
	public Map<String, Integer> indicators = new HashMap<String, Integer>(){
		private static final long serialVersionUID = 1L;
		};
	
	Category(Map<String, Integer> indicators, String categoryName, Map<String,Float> classifiers) {
		this.indicators = indicators;
		this.name = categoryName;
		this.classifiers = classifiers;
	}
	
	public void increaseBy(int value) {
		score += value;
	}
	
}
