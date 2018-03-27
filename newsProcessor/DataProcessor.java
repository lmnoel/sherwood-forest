import java.io.*;

import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Random;


class DataProcessor {
	
	private static int numPositiveWords = 354;
	private static int numNegativeWords = 2355;
	
	private static int networkInputSize = 1;
	private static final int networkHiddenSize = 3;
	private static final int networkOutputSize = 1;
	
	private Network network;
	private McDonaldAnalyzer newsAnalyzer;
	private SpyAnalyzer marketAnalyzer;
	
	private ArrayList<DateScore> dateScores;
	private HashMap<Integer, Double> dateMultipliers;
	
	private ArrayList<DataChunk> data;
	
	private ArrayList<DataChunk> trainData;
	private ArrayList<DataChunk> testData;
	
	private ArrayList<File> trainFiles;
	private ArrayList<File> testFiles;

	public DataProcessor() {
		newsAnalyzer = new McDonaldAnalyzer();
		marketAnalyzer = new SpyAnalyzer();
	}

	public static void main(String[] args) {
		DataProcessor processor = new DataProcessor();
		processor.createTrainAndTestNetwork();
		// processor.makePredictions();
	}

	// this one uses the more advanced training data from McDonaldAnalyzer2
	private void createTrainAndTestNetwork() {
		int networkInputSize = 2711;
		// int networkInputSize = 2;
		int networkHiddenSize = 100;
		int networkOutputSize = 1;
		int polarizationFilter = 10;
		int trainIterations = 5;

		network = new Network(networkInputSize, networkHiddenSize, networkOutputSize, 0.1, 0.6);

		NumberFormat percentFormat = NumberFormat.getPercentInstance();
		percentFormat.setMinimumFractionDigits(4);

		File dir = new File("newspaperCodings");
		File[] directoryListing = dir.listFiles();
		int trial = 0;

		testFiles = new ArrayList<File>(Arrays.asList(directoryListing));
		trainFiles = new ArrayList<File>();

		Random rand = new Random();
		double trainFileFraction = 5.0 / 6.0;
		for (int i = 0; i < (int) (trainFileFraction * testFiles.size()); ++i) {
			int randomIndex = rand.nextInt(testFiles.size());
			trainFiles.add(testFiles.get(randomIndex));
			testFiles.remove(randomIndex);
		}

		for (int j = 0; j < trainIterations; ++j) {

			for (File trainFile : trainFiles) {
				FileReader fr = null;
				BufferedReader br = null;

				double[] networkInput = new double[networkInputSize];
				double[] networkOutput = new double[networkOutputSize];

				try {
					fr = new FileReader(trainFile);
					br = new BufferedReader(fr);

					String line1 = br.readLine();
					String[] line1elements = line1.split(",");
					networkInput[0] = Double.parseDouble(line1elements[0])/numPositiveWords;
					networkInput[1] = Double.parseDouble(line1elements[1])/numNegativeWords;

					// this line filters out articles that contain less than x polarizing words
					if (Double.parseDouble(line1elements[0]) + Double.parseDouble(line1elements[1]) < polarizationFilter)
						continue;

					String line2 = br.readLine();
					String[] line2elements = line2.split(",");
					for (int i = 2; i < networkInput.length; ++i) {
						networkInput[i] = Double.parseDouble(line2elements[i - 2]);
					}

					String line3 = br.readLine();
					if (Double.parseDouble(line3)<1) {
						networkOutput[0] = 0;
						System.out.println("negative");
					}
					else {
						networkOutput[0] = 1;
						System.out.println("positive");
					}

				} catch (FileNotFoundException fnfe) {
					System.out.println(fnfe.getMessage());
				} catch (IOException ioe) {
					System.out.println(ioe.getMessage());
				} finally {
					closeReaders(br, fr);
				}
				
				
				network.computeOutputs(networkInput);
				network.calcError(networkOutput);
				network.learn();

				System.out.println(
						"Trial #" + trial + ",Error:" + percentFormat.format(network.getError(networkInput.length)));
				trial++;
			}

		}

		BufferedWriter bw = null;
		FileWriter fw = null;

		try {

			fw = new FileWriter("predictions.txt");
			bw = new BufferedWriter(fw);

			// for csv for Logan
			bw.write("predictedRatio,actualRatio,positiveWordCount,negativeWordCount");
			bw.newLine();

			for (File testFile : testFiles) {
				FileReader fr = null;
				BufferedReader br = null;

				double[] networkInput = new double[networkInputSize];
				double[] networkOutput = new double[networkOutputSize];

				try {
					fr = new FileReader(testFile);
					br = new BufferedReader(fr);

					String line1 = br.readLine();
					String[] line1elements = line1.split(",");
					networkInput[0] = Double.parseDouble(line1elements[0])/numPositiveWords;
					networkInput[1] = Double.parseDouble(line1elements[1])/numNegativeWords;

					// this line filters out articles that contain less than x polarizing words
					if (Double.parseDouble(line1elements[0]) + Double.parseDouble(line1elements[1]) < polarizationFilter)
						continue;

					String line2 = br.readLine();
					String[] line2elements = line2.split(",");
					for (int i = 2; i < networkInput.length; ++i) {
						networkInput[i] = Double.parseDouble(line2elements[i - 2]);
					}

					String line3 = br.readLine();
					if (Double.parseDouble(line3)<1) {
						networkOutput[0] = 0;
					}
					else networkOutput[0] = 1;

				} catch (FileNotFoundException fnfe) {
					System.out.println(fnfe.getMessage());
				} catch (IOException ioe) {
					System.out.println(ioe.getMessage());
				} finally {
					closeReaders(br, fr);
				}

				// predictions.txt writing
				double prediction = network.computeOutputs(networkInput)[0];

				// plain multiplier predictions
				// bw.write(Double.toString(prediction));

				// for csv for Logan
				bw.write(Double.toString(prediction));
				bw.write("," + networkOutput[0]);
				bw.write("," + networkInput[0] + "," + networkInput[1]);

				// differenceBetweenPredictedAndActual,positivity-negativity
				// bw.write(Double.toString(networkOutput[0] - prediction));
				// bw.write("," + (networkInput[0]-networkInput[1]));

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
		} // finally

		System.out.println("Predictions made");

	}

	private void trainNetwork() {
		data = new ArrayList<DataChunk>();
		testData = new ArrayList<DataChunk>();
		trainData = new ArrayList<DataChunk>();

		newsAnalyzer.load();
		marketAnalyzer.collectData();

		dateScores = newsAnalyzer.dateScores;
		dateMultipliers = marketAnalyzer.dateMultiplier;

		// MAKE SURE THIS WORKS CORRECTLY YOU WERE TIRED AND THIS IS SUPER IMPORTANT AND
		// HARD TO CHECK
		// this v important part combines all news article scores with the multiplier
		// from its day
		for (DateScore dateScore : dateScores) {
			String date = Integer.toString(dateScore.year);
			date += Integer.toString(dateScore.month);
			date += Integer.toString(dateScore.day);

			double currScore = dateScore.score;
			if (dateMultipliers.get(Integer.parseInt(date)) == null)
				continue;
			double currMultiple = dateMultipliers.get(Integer.parseInt(date));
			// System.out.println(dateScore.year+" " + dateScore.month+" " +dateScore.day);
			data.add(new DataChunk(currScore, currMultiple, dateScore.year, dateScore.month, dateScore.day));
		}

		// OPTIONAL
		// filters out non-polar articles
		data.removeIf(dataChunk -> Math.abs(dataChunk.newsRating) < 30);

		// select random elements 3/4 the size of array, and put into trainData
		Random rand = new Random();
		int testDataSetSize = (int) ((double) data.size() * (3.0 / 4.0));
		for (int i = 0; i < testDataSetSize; ++i) {
			int randomIndex = rand.nextInt(data.size());
			trainData.add(data.get(randomIndex));
			data.remove(randomIndex);
		}

		// make testData the remaining elements still in data
		testData = data;

		System.out.println("training data size: " + trainData.size());
		System.out.println("test data size: " + testData.size());

		NumberFormat percentFormat = NumberFormat.getPercentInstance();
		percentFormat.setMinimumFractionDigits(4);

		// now we train the network
		int i = 0;
		for (DataChunk dataChunk : trainData) {
			double[] input = { dataChunk.newsRating };
			double[] output = { dataChunk.priceMultiplier };
			network.computeOutputs(input);
			network.calcError(output);
			network.learn();
			// System.out.println("Trial #" + i + ",Error:" +
			// percentFormat.format(network.getError(input.length)));
			i++;
		}

	}

	private void makePredictions() {
		BufferedWriter bw = null;
		FileWriter fw = null;

		try {

			fw = new FileWriter("predictions.txt");
			bw = new BufferedWriter(fw);

			// write predictions
			for (DataChunk dataChunk : testData) {
				double[] input = { dataChunk.newsRating };
				double prediction = network.computeOutputs(input)[0];
				double successDifference = dataChunk.priceMultiplier - prediction;
				// System.out.println(dataChunk.year+" " + dataChunk.month+" " +dataChunk.day);
				// bw.write(Integer.toString(dataChunk.year) + ":" + dataChunk.month + ":" +
				// dataChunk.day + ":");
				// bw.write(Double.toString(prediction));
				bw.write("" + Double.toString(successDifference));
				bw.write("," + Double.toString(dataChunk.newsRating));
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
		} // finally

		System.out.println("Predictions made");
	}// makePredictions()

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

	// a data chunk is one news article with its day's price differential
	class DataChunk {
		public double newsRating;
		public double priceMultiplier;
		public int year;
		public int month;
		public int day;

		DataChunk(double newsRating, double priceMultiplier, int year, int month, int day) {
			this.newsRating = newsRating;
			this.priceMultiplier = priceMultiplier;
			this.year = year;
			this.month = month;
			this.day = day;
		}
	}// class DataChunk

}// class DataProcessor
