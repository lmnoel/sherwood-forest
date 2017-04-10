import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class FileParser {

	public static void readInput(String filename) {
		FileReader fr = null;
		BufferedReader br = null;

		try {
			fr = new FileReader(filename);
			br = new BufferedReader(fr);

			StringBuffer fileData = new StringBuffer();
			char[] buf = new char[1024];
			int numRead = 0;
			while ((numRead = br.read(buf)) != -1) {
				String readData = String.valueOf(buf, 0, numRead);
				fileData.append(readData);
			}
			Constants.input = fileData.toString();
/*
			while (true) {
				String line = br.readLine();
				if (line == null)
					break;

				Constants.input.concat(line);
			}
*/
		} catch (FileNotFoundException fnfe) {
			System.out.println(fnfe.getMessage());
		} catch (IOException ioe) {
			System.out.println(ioe.getMessage());
		} finally {
			closeReaders(br, fr);
		}

	}

	public static void readClassifiers(String filename) {

		FileReader fr = null;
		BufferedReader br = null;

		try {
			fr = new FileReader(filename);
			br = new BufferedReader(fr);

			while (true) {
				String line = br.readLine();
				
				line = line.toLowerCase();
				
				if (line.equals("categories")) break;
				
				

				String[] words = line.split(":");
				if (words.length != 3)
					continue;

				if (words[0].equals("immigration")) {
					Constants.immigrationIndicators.put(words[1], Integer.parseInt(words[2]));
				}
				if (words[0].equals("trade")) {
					Constants.tradeIndicators.put(words[1], Integer.parseInt(words[2]));
				}
				if (words[0].equals("energy")) {
					Constants.energyIndicators.put(words[1], Integer.parseInt(words[2]));
				}
				if (words[0].equals("finance")) {
					Constants.financeIndicators.put(words[1], Integer.parseInt(words[2]));
				}
				if (words[0].equals("infrastructure")) {
					Constants.infrastructureIndicators.put(words[1], Integer.parseInt(words[2]));
				}

			}
			String currLine;
			while (true) {
				String line = br.readLine();
				if (line == null) break;
				
				line = line.toLowerCase();

				String[] words = line.split(":");
				if (words.length != 3)
					continue;

				if (words[0].equals("general")) {
					Constants.generalClassifiers.put(words[1], Float.parseFloat(words[2]));
				}
				if (words[0].equals("immigration")) {
					Constants.immigrationClassifiers.put(words[1], Float.parseFloat(words[2]));
				}
				if (words[0].equals("trade")) {
					Constants.tradeClassifiers.put(words[1], Float.parseFloat(words[2]));
				}
				if (words[0].equals("energy")) {
					Constants.energyClassifiers.put(words[1], Float.parseFloat(words[2]));
				}
				if (words[0].equals("finance")) {
					Constants.financeClassifiers.put(words[1], Float.parseFloat(words[2]));
				}
				if (words[0].equals("infrastructure")) {
					Constants.infrastructureClassifiers.put(words[1], Float.parseFloat(words[2]));
				}

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
