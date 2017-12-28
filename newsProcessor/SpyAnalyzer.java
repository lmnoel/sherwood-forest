import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class SpyAnalyzer {

	public ArrayList<MarketData> marketData;
	public HashMap<Integer, Double> dateMultiplier;
	
	public SpyAnalyzer() {
		marketData = new ArrayList<MarketData>();
		dateMultiplier = new HashMap<Integer, Double>();
	}
	
	
	public void collectData() {
		String csvFile = "spy_historical.csv";
		String cvsSplitBy = ",";
		
		try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
			
			br.readLine();
			String line = null;
			
			while ((line = br.readLine()) != null) {
				String[] words = line.split(cvsSplitBy);
				String[] date = words[0].split("-");
				double open = Double.parseDouble(words[1]);
				double close = Double.parseDouble(words[4]);
				
				marketData.add(new MarketData(
						Integer.parseInt(date[0]), 
						Integer.parseInt(date[1]), 
						Integer.parseInt(date[2]), 
						close/open));
				
			}
		} catch (IOException e) {
            e.printStackTrace();
        }
		
		for (MarketData marketData : marketData) {
			String dateFormat = Integer.toString(marketData.year);
			dateFormat += Integer.toString(marketData.month);
			dateFormat += Integer.toString(marketData.day);
			
			
			dateMultiplier.put(Integer.parseInt(dateFormat), marketData.openCloseMultiple);
			
		}
		
		
		
		
	}//collectData()
	
	
	
	public static void main(String[] args) {
		SpyAnalyzer analyzer = new SpyAnalyzer();
		analyzer.collectData();
		analyzer.printMarketData();
	}
	
	
	private void printMarketData() {
		for (MarketData marketData: marketData) {
			System.out.println(marketData.year+" "+
							marketData.month+" "+
							marketData.day+" "+
							marketData.openCloseMultiple);
		}
	}
	
	
	class MarketData {
		public int year;
		public int month;
		public int day;
		public double openCloseMultiple;
		
		public MarketData(int year, int month, int day, double multiple) {
			this.year = year;
			this.month = month;
			this.day = day;
			this.openCloseMultiple = multiple;
		}
	}

}
