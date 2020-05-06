import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

# use input() function to get user input! Cast it to string, and force lower casing.
# use the .get() function on the CITY_DATA dict to get the data set corresponding to the input.



    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = ""
    month = True
    day = True
    while city not in CITY_DATA:
        city = str(input("What City shall be analysed? Chicago, New York City or Washington?: \n")).lower()
    else:
        print("lets see what we can find...")

    # TO DO: get user input for month (all, january, february, ... , june)
    while month not in ['all','january', 'february', 'march', 'april', 'may', 'june']:
        month = input("\nWhat month shall be analysed? We have data for Janauary to June. If you want to see all months\n type 'all' otherwise write the name of the respective month: \n").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = str(input("\nIf you want a specific day to be analysed choose Monday, Tuesday, Thursday, Friday, Saturday or Sunday.\n If not type 'all':  \n")).lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
    	print("Please enter a correct option: 'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'")
    	day = input().lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    que_stat = True
    df = pd.DataFrame(pd.read_csv(CITY_DATA.get(city)))
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month == True:
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day == True:
        df = df[df['day_of_week'] == day.title()]


    while que_stat == "yes":
        que_stat = str(input("Do you want to see 5 random lines of raw data based on your criterias? Enter 'Yes' or 'No': ")).lower()
        if que_stat == "yes":
            print(df.sample(5))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]

    # TO DO: display the most common day of week
    df['day'] = df['Start Time'].dt.dayofweek
    most_common_day = df['day'].mode()[0]

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]

    print("\nMost people bike in month {}, on day {}, and at {} o'clock.\n".format(most_common_month, most_common_day, most_common_start_hour))

    print('This took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("\nThe most popular Start Station is:\n{}\n".format(start_station))
#     TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("\nThe most popular End Station is \n{}\n".format(end_station))
    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print("\nThe most popular trip is between\n{}!\n".format(popular_trip))
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    average_travel_time = df['Trip Duration'].mean()

    print('\nThe total travel time is around {} hours and the average travel time is {} min!\n'.format(int(total_travel_time / 360), int(average_travel_time / 60)))

    print('This took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nDistribution of users types:\n", user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print("\nGender distribution:\n", gender, "\n")

   # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        youngest = int(df['Birth Year'].min())
        oldest = int(df['Birth Year'].max())
        most_common_yob = int(df['Birth Year'].mode()[0])
        print("\nThe earliest Year of Birth is {}, the latest YoB is {} and the most common YoB is {} \n".format(youngest, oldest, most_common_yob))

    print('This took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() == 'yes':
    	main()
    else:
    	print("Thanks for analyzing! Good Bye :)")

if __name__ == "__main__":
	main()
