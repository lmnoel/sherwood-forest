import java.io.*;

import java.text.NumberFormat;

public class Network {

	// The global error for the training.
	protected double globalError;

	// The number of input neurons.
	protected int inputCount;

	// The number of hidden neurons.
	protected int hiddenCount;

	// The number of output neurons
	protected int outputCount;

	// The total number of neurons in the network.
	protected int neuronCount;

	// The number of weights in the network.
	protected int weightCount;

	// The learning rate.
	protected double learnRate;

	// The outputs from the various levels.
	protected double fire[];

	// The weight matrix this, along with the thresholds can be
	// thought of as the "memory" of the neural network.
	protected double matrix[];

	// The errors from the last calculation.
	protected double error[];

	// Accumulates matrix delta's for training.
	protected double accMatrixDelta[];

	// The thresholds, this value, along with the weight matrix
	// can be thought of as the memory of the neural network.
	protected double thresholds[];

	// The changes that should be applied to the weight matrix.
	protected double matrixDelta[];

	// The accumulation of the threshold deltas.
	protected double accThresholdDelta[];

	// The threshold deltas.
	protected double thresholdDelta[];

	// The momentum for training.
	protected double momentum;

	// The changes in the errors.
	protected double errorDelta[];

	/**
	 * Construct the neural network.
	 *
	 * @param inputCount
	 *            The number of input neurons.
	 * @param hiddenCount
	 *            The number of hidden neurons
	 * @param outputCount
	 *            The number of output neurons
	 * @param learnRate
	 *            The learning rate to be used when training.
	 * @param momentum
	 *            The momentum to be used when training.
	 */
	public Network(int inputCount, int hiddenCount, int outputCount, double learnRate, double momentum) {

		this.learnRate = learnRate;
		this.momentum = momentum;

		this.inputCount = inputCount;
		this.hiddenCount = hiddenCount;
		this.outputCount = outputCount;
		neuronCount = inputCount + hiddenCount + outputCount;
		weightCount = (inputCount * hiddenCount) + (hiddenCount * outputCount);

		fire = new double[neuronCount];
		matrix = new double[weightCount];
		matrixDelta = new double[weightCount];
		thresholds = new double[neuronCount];
		errorDelta = new double[neuronCount];
		error = new double[neuronCount];
		accThresholdDelta = new double[neuronCount];
		accMatrixDelta = new double[weightCount];
		thresholdDelta = new double[neuronCount];
		
		reset();
	}
	
	//Second constructor for loading a previously saved network
	public Network() {

		loadMemory();
		
		neuronCount = inputCount + hiddenCount + outputCount;
		weightCount = (inputCount * hiddenCount) + (hiddenCount * outputCount);
		
		fire = new double[neuronCount];
		matrixDelta = new double[weightCount];
		errorDelta = new double[neuronCount];
		error = new double[neuronCount];
		accThresholdDelta = new double[neuronCount];
		accMatrixDelta = new double[weightCount];
		thresholdDelta = new double[neuronCount];
	}

	// Stores "memory learned", or matrix[] and thresholds[], in memory.txt
	// First line contains inputCount, hiddenCount, outputCount, learnRate, and momentum separated by spaces
	// Second line contains all values in matrix[] separated by spaces
	// Third line contains all values in thresholds[] separated by spaces
	public void saveMemory() {
		String filename = "memory.txt";
		BufferedWriter bw = null;
		FileWriter fw = null;

		try {

			fw = new FileWriter(filename);
			bw = new BufferedWriter(fw);
			
			
			//record inputCount, hiddenCount, outputCount, learnRate, and momentum
			bw.write(Integer.toString(inputCount));
			bw.write(" " + Integer.toString(hiddenCount));
			bw.write(" " + Integer.toString(outputCount));
			bw.write(" " + Double.toString(learnRate));
			bw.write(" " + Double.toString(momentum));
			

			//go to second line and record matrix[]
			bw.write("\n");
			for (int i=0; i<matrix.length; ++i) {
				if (i != 0) bw.write(" ");
				bw.write(Double.toString(matrix[i]));
			}
			
			//go to third line and record thresholds[]
			bw.write("\n");
			for (int i=0; i<thresholds.length; ++i) {
				if (i != 0) bw.write(" ");
				bw.write(Double.toString(thresholds[i]));
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
		
	}// saveMemory()

	// Loads memory into network from memory.txt
	public void loadMemory() {
		FileReader fr = null;
		BufferedReader br = null;

		try {
			fr = new FileReader("memory.txt");
			br = new BufferedReader(fr);

			//read in neuron counts, learnRate, and momentum
			String[] firstLine = br.readLine().split(" ");
			inputCount = Integer.parseInt(firstLine[0]);
			hiddenCount = Integer.parseInt(firstLine[1]);
			outputCount = Integer.parseInt(firstLine[2]);
			learnRate = Double.parseDouble(firstLine[3]);
			momentum = Double.parseDouble(firstLine[4]);
			
			//parse matrix[] on second line
			String[] secondLine = br.readLine().split(" ");
			matrix = new double[secondLine.length];
			for (int i=0; i<secondLine.length; ++i) {
				matrix[i] = Double.parseDouble(secondLine[i]);
			}
			
			//parse thresholds[] on third line
			String[] thirdLine = br.readLine().split(" ");
			thresholds = new double[thirdLine.length];
			for (int i=0; i<thirdLine.length; ++i) {
				thresholds[i] = Double.parseDouble(thirdLine[i]);
			}
			
		} catch (FileNotFoundException fnfe) {
			System.out.println(fnfe.getMessage());
		} catch (IOException ioe) {
			System.out.println(ioe.getMessage());
		} finally {
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

	// Returns the root mean square error for a complet training set.
	// @param len The length of a complete training set.
	// @return The current error for the neural network.
	public double getError(int len) {
		double err = Math.sqrt(globalError / (len * outputCount));
		globalError = 0; // clear the accumulator
		return err;
	}

	// Can override to provide other threshold methods
	// @param sum The activation from the neuron.
	// @return The activation applied to the threshold method.
	public double threshold(double sum) {
		return 1.0 / (1 + Math.exp(-1.0 * sum));
	}

	// Compute the output for a given input to the neural network.
	// @param input The input provide to the neural network.
	// @return The results from the output neurons.
	public double[] computeOutputs(double input[]) {
		int i, j;
		final int hiddenIndex = inputCount;
		final int outIndex = inputCount + hiddenCount;

		for (i = 0; i < inputCount; i++) {
			fire[i] = input[i];
		}

		// first layer
		int inx = 0;

		for (i = hiddenIndex; i < outIndex; i++) {
			double sum = thresholds[i];

			for (j = 0; j < inputCount; j++) {
				sum += fire[j] * matrix[inx++];
			}
			fire[i] = threshold(sum);
		}

		// hidden layer
		double result[] = new double[outputCount];

		for (i = outIndex; i < neuronCount; i++) {
			double sum = thresholds[i];

			for (j = hiddenIndex; j < outIndex; j++) {
				sum += fire[j] * matrix[inx++];
			}
			fire[i] = threshold(sum);
			result[i - outIndex] = fire[i];
		}

		return result;
	}// computeOutputs()

	// Calculate the error for the recogntion just done.
	// @param ideal What the output neurons should have yielded.
	public void calcError(double ideal[]) {
		int i, j;
		final int hiddenIndex = inputCount;
		final int outputIndex = inputCount + hiddenCount;

		// clear hidden layer errors
		for (i = inputCount; i < neuronCount; i++) {
			error[i] = 0;
		}

		// layer errors and deltas for output layer
		for (i = outputIndex; i < neuronCount; i++) {
			error[i] = ideal[i - outputIndex] - fire[i];
			globalError += error[i] * error[i];
			errorDelta[i] = error[i] * fire[i] * (1 - fire[i]);
		}

		// hidden layer errors
		int winx = inputCount * hiddenCount;

		for (i = outputIndex; i < neuronCount; i++) {
			for (j = hiddenIndex; j < outputIndex; j++) {
				accMatrixDelta[winx] += errorDelta[i] * fire[j];
				error[j] += matrix[winx] * errorDelta[i];
				winx++;
			}
			accThresholdDelta[i] += errorDelta[i];
		}

		// hidden layer deltas
		for (i = hiddenIndex; i < outputIndex; i++) {
			errorDelta[i] = error[i] * fire[i] * (1 - fire[i]);
		}

		// input layer errors
		winx = 0; // offset into weight array
		for (i = hiddenIndex; i < outputIndex; i++) {
			for (j = 0; j < hiddenIndex; j++) {
				accMatrixDelta[winx] += errorDelta[i] * fire[j];
				error[j] += matrix[winx] * errorDelta[i];
				winx++;
			}
			accThresholdDelta[i] += errorDelta[i];
		}
	}// calcError()

	// Modify the weight matrix and thresholds based on the last call to
	// calcError.
	public void learn() {
		int i;

		// process the matrix
		for (i = 0; i < matrix.length; i++) {
			matrixDelta[i] = (learnRate * accMatrixDelta[i]) + (momentum * matrixDelta[i]);
			matrix[i] += matrixDelta[i];
			accMatrixDelta[i] = 0;
		}

		// process the thresholds
		for (i = inputCount; i < neuronCount; i++) {
			thresholdDelta[i] = learnRate * accThresholdDelta[i] + (momentum * thresholdDelta[i]);
			thresholds[i] += thresholdDelta[i];
			accThresholdDelta[i] = 0;
		}
	}// learn()

	// Reset the weight matrix and the thresholds.
	public void reset() {
		int i;

		for (i = 0; i < neuronCount; i++) {
			thresholds[i] = 0.5 - (Math.random());
			thresholdDelta[i] = 0;
			accThresholdDelta[i] = 0;
		}
		for (i = 0; i < matrix.length; i++) {
			matrix[i] = 0.5 - (Math.random());
			matrixDelta[i] = 0;
			accMatrixDelta[i] = 0;
		}
	}// reset()

	public static void main(String args[]) {
		double xorInput[][] = { 
				{ 0.0, 0.0 }, 
				{ 1.0, 0.0 }, 
				{ 0.0, 1.0 }, 
				{ 1.0, 1.0 } 
				};
		
		double newInput[] = { 0.0, 0.5 };
		
		double xorIdeal[][] = { 
				{ 0.0 }, 
				{ 1.0 }, 
				{ 1.0 }, 
				{ 0.0 } 
				};

		System.out.println("Learn:");
		Network network = new Network(2, 3, 1, 0.7, 0.9);

		NumberFormat percentFormat = NumberFormat.getPercentInstance();
		percentFormat.setMinimumFractionDigits(4);
		
		for (int i = 0; i < 10000; i++) {
			for (int j = 0; j < xorInput.length; j++) {
				network.computeOutputs(xorInput[j]);
				network.calcError(xorIdeal[j]);
				network.learn();
			}
			System.out.println("Trial #" + i + ",Error:" + percentFormat.format(network.getError(xorInput.length)));
		}

		System.out.println("Recall:");

		for (int i = 0; i < xorInput.length; i++) {

			for (int j = 0; j < xorInput[0].length; j++) {
				System.out.print(xorInput[i][j] + ":");
			}

			double out[] = network.computeOutputs(xorInput[i]);
			System.out.println("=" + out[0]);
		}
		
		network.saveMemory();

		//System.out.println(network.computeOutputs(newInput)[0]);
		
		
	}//main()

}// class