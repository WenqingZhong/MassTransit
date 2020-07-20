import crowdingtools.getTurnstileEntries;
import crowdingtools.getTrainsCount;
import crowdingtools.getDelayTime;
import crowdingtools.getLargeCrowd;

public class Crowd {

	private String station;
	private String trainline;
	private String date;
	private String time;
	
	public Crowd(String station, String trainline, String date, String time) {
	
		this.station = station;
		this.trainline = trainline;
		this.date = date;
		this.time = time;
	
# The user specifies as inputs the station, 	#
# the train line, the time, and the date.	#

# The first step is to prepare the correct	#
# data based on the user's inputs.		#

# Based on the layout of the turnstile data 	#
# spreadsheet, the csv should be	 	#
# processed in the following order: 		#
# 1. STATION					#
# 2. LINENAME					#
# 3. DATE					#
# 4. TIME					#
# When the csv is filtered in that order,	#
# the remaining items should have everything	#
# in common except C/A, SCP, ENTRIES, and	#
# EXITS.					#

# We'll assign the job of converting the 	#
# string inputs into the necessary form	#
# to other functions. 				#

# We'll also assign the job of getting	#
# the necessary information from the 		#
# sorted entries to other functions, and	#
# here we will call those functions.		#

		new int turnstileEntries = getTurnstileEntries(station,trainline,date,time);
		# This function brings in the sum of the turnstile entries from the 	#
		# turnstiles belonging to the relevant unit during the four hour 	#
		# period corresponding to the time specified by the user on the 	#
		# latest date with the same weekday as the date specified.		#
		
		new int trainsCount = getTrainsCount(station,trainline,date,time);
		# This function brings in the number of trains that stopped at	#
		# the platforms accessible to the UNIT during the same four-hour	#
		# interval on the same date that is used to sum the turnstile	#
		# entries in the previous function.					#
		
		new int delayTime = getDelayTime(station,trainline,date,time);
		# This function produces an estimate of the amount of minutes 		#
		# a delay typically might have. I am not sure how to calculate it	#
		# yet, but here is where we will use it.				#
		
		new int totalMinutes = 60 * 4;
		# The number of minutes in a four hour interval.			#
		
		new int avgTimeSpacing = totalMinutes / trainsCount;
		# This gives the average time spacing between trains in minutes.	#
		
		new int crowd = turnstileEntries * (avgTimeSpacing / totalMinutes);
		# The crowd that would accumulate based on equal time spacing	#
		# and uniform arrival rate without delays accounted.			#
		
		new int delayedCrowd = turnstileEntries * (delayTime / totalMinutes);
		# This calculates the extra crowd that would accumulate based on our	#
		# estimate of a delay. 						#
		
		new int largeCrowd = getLargeCrowd(station,trainline,date,time);
		# This function brings in a personcount corresponding to a large 	#
		# crowd at that particular platform, which we could compute with	#
		# a function that computes a crowd in the same way but with 		#
		# the largest turnstile count it can find at that particular 	#
		# station from an arbitrary csv of pre-covid data.			#
		
		new double crowdLevel = crowd / largeCrowd;
		new double dCrowdLevel = (crowd + delayedCrowd) / largeCrowd;
		
		# The above functions should produce a floating point number between	#
		# zero and one that indicate the crowd level.				#
		
		public  double getCrowdLevel() { return crowdLevel; }
		public double getDelayedCrowdLevel() { return dCrowdLevel; }
		
		# This was written in Java but we could easily translate to python.	#
		# In java the way we would call it is by creating a crowd object	#
			# Crowd crowd = new Crowd(station,trainline,date,time);		#
		# and then calling the methods to get the crowd calculations for it	#
			# return crowd.getCrowdLevel();					#
			
		
		
		
		

