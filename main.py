import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

#Import and display the dataframe.
daily_activity = pd.read_csv('/Users/ice50l/Downloads/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv')
calories = pd.read_csv('/Users/ice50l/Downloads/Fitabase Data 4.12.16-5.12.16/dailyCalories_merged.csv')
heart_rate = pd.read_csv('/Users/ice50l/Downloads/Fitabase Data 4.12.16-5.12.16/heartrate_seconds_merged.csv')
sleep_day = pd.read_csv('/Users/ice50l/Downloads/Fitabase Data 4.12.16-5.12.16/sleepDay_merged.csv')
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 25)
print(daily_activity.head(10))

#Find if there are any missing values.
missing = daily_activity.isnull().sum()
print(missing[:])
heart_rateM = heart_rate.isnull().sum()
print(heart_rateM[:])

#Remove time from sleep_day
def new_activity(row):
    row.SleepDay = row.SleepDay[:9]
    return row
sleep_day=sleep_day.apply(new_activity, axis="columns").rename(columns={"SleepDay":"ActivityDate"})

#Merging 2 datasets on Id and Activity Date
left = daily_activity.set_index(['Id','ActivityDate'])
right = sleep_day.set_index(['Id','ActivityDate'])
daily_activityS = left.join(right)
daily_activityS = daily_activityS.drop_duplicates(keep='first',inplace=False).reset_index()
stepsnsleep = daily_activityS[['TotalSteps','TotalMinutesAsleep']].dropna(subset=['TotalMinutesAsleep'])
stepsnsleep.to_csv("stepsnsleep.csv")

#Find the number of unqiue values we have in the ID column.
unique = daily_activity['Id'].nunique()
print('We have', unique, 'unique values.')

#Check the data type.
daily_activity.info()

#Change Date from Object to Date format.
daily_activity["ActivityDate"] = pd.to_datetime(daily_activity["ActivityDate"], format="%m/%d/%Y")

daily_activity.info()

#Make a new column for days of the week and add the day name.
daily_activity.insert(3,'Week_Day', " ")
daily_activity["Week_Day"] = daily_activity["ActivityDate"].dt.day_name()
print(daily_activity.head(10))

#Find total minutes walked per log.
daily_activity['total_min'] = daily_activity['VeryActiveMinutes'] + daily_activity['FairlyActiveMinutes'] + daily_activity['LightlyActiveMinutes'] + daily_activity['SedentaryMinutes']
print(daily_activity['total_min'].head(5))

#Merge Activity and SleepDay
DS = pd.merge(daily_activity, sleep_day, on = 'Id', how = 'inner')
print(DS.head(10))

#Analysis
print(daily_activity.describe())

# plotting histogram
plt.style.use("default")
plt.figure(figsize=(6,4)) # specify size of the chart
plt.hist(daily_activity.Week_Day, bins = 7,
         width = 0.6, color = "lightskyblue", edgecolor = "black")

# adding annotations and visuals
plt.xlabel("Day of the week")
plt.ylabel("Frequency")
plt.title("No. of times users logged in app across the week")
plt.grid(True)
plt.show()

sb.barplot(data=daily_activity, x="Week_Day", y="total_min")
plt.show()

#Pie chart
very_active_mins = daily_activity["VeryActiveMinutes"].sum()
fairly_active_mins = daily_activity["FairlyActiveMinutes"].sum()
lightly_active_mins = daily_activity["LightlyActiveMinutes"].sum()
sedentary_mins = daily_activity["SedentaryMinutes"].sum()

slices = [very_active_mins, fairly_active_mins, lightly_active_mins, sedentary_mins]
labels = ["Very active minutes", "Fairly active minutes", "Lightly active minutes", "Sedentary minutes"]
colours = ["lightcoral", "yellowgreen", "lightskyblue", "darkorange"]
explode = [0, 0, 0, 0.1]
plt.style.use("default")
plt.pie(slices, labels = labels,
        colors = colours, wedgeprops = {"edgecolor": "black"},
        explode = explode, autopct = "%1.1f%%")
plt.title("Percentage of Activity in Minutes")
plt.tight_layout()
plt.show()

#Scatterplot of min and calories
sb.scatterplot(data = daily_activity, x = 'Calories', y = 'SedentaryMinutes', color='#f22a51')
plt.title('Sedentary Minutes vs Calories')
plt.xlabel('Calories')
plt.ylabel('Sedentary Minutes')
plt.show()

#Scatterplot of Total Steps and Calories Burnt
sb.scatterplot(data = daily_activity, x = 'Calories', y = 'TotalSteps')
plt.title('Total Steps Vs. Calories Burnt')
plt.xlabel('Calories')
plt.ylabel('Total Steps')
plt.show()





