
public class DateScore {
		int year;
		int month;
		int day;
		double score;
		
		DateScore(int year, int month, int day, double score) {
			this.year = year;
			this.month = month;
			this.day = day;
			this.score = score;
		}
		
		public void printDateScore() {
			System.out.println("Year: " + this.year);
			System.out.println("Month: " + this.month);
			System.out.println("Day: " + this.day);
			System.out.println("Score: " + this.score);
			System.out.println();
		}
		
	}