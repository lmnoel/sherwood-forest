import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class PredictionsAnalyzer {
	
	
	public static void main(String[] args) {
		analyzePredictions();
	}

	
	public static void analyzePredictions() {
	String csvFile = "predictions.txt";
	String cvsSplitBy = ",";
	
	int posCorrect = 0;
	int posIncorrect = 0;
	int negCorrect = 0;
	int negIncorrect = 0;
	
	int unsure = 0;

	try(
	BufferedReader br = new BufferedReader(new FileReader(csvFile)))
	{

		br.readLine();
		String line = null;
		
		double upperThreshold = 0.96;
		double lowerThreshold = 0.33;
		
		while ((line = br.readLine()) != null) {
			String[] values = line.split(cvsSplitBy);

			double predicted = Double.parseDouble(values[0]);
			double actual = Double.parseDouble(values[1]);
			
			if (predicted > upperThreshold && actual==1.0) {
				posCorrect++;
				System.out.println("found posCorrect");
			}
			if (predicted > upperThreshold && actual==0.0) {
				posIncorrect++;
				System.out.println("found posIncorrect");
			}
			if (predicted < lowerThreshold && actual==0.0) {
				negCorrect++;
				System.out.println("found negCorrect");
			}
			if (predicted < lowerThreshold && actual==1.0) {
				negIncorrect++;
				System.out.println("found negIncorrect");
			}
			else unsure++;
			

			
			
			
		}
	}catch(IOException e) {
		e.printStackTrace();
	}
	
	
	double posTotal = posCorrect + posIncorrect;
	double negTotal = negCorrect + negIncorrect;
	double posAccuracy = ((double)posCorrect) / posTotal;
	double negAccuracy = ((double)negCorrect) / negTotal;
	
	System.out.println(posCorrect + " " + posIncorrect);
	System.out.println(negCorrect + " " + negIncorrect);
	System.out.println(unsure);
	System.out.println("posAccuracy: " + posAccuracy);
	System.out.println("negAccuracy: " + negAccuracy);

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
