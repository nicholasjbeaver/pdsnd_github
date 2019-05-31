import time
import pandas as pd
import numpy as np

# A dictionary of city names and csv files associated with them

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). Loop forever until the lowercase input is found in the city data dictionary. Tell the user      if they did something incorrectly

    while True:
        city = str(input('input one of these cities to see its bikeshare data - chicago, washington, new york city :'))
        city = city.lower()
        if city in CITY_DATA:
            break
        else:
           print('please enter one of the three valid city names')

    # get user input for month (all, january, february, ... , june). Loop forever until a valid month is chosen, remind user of inputs if incorrect
    while True:
        month = str(input('what month would you like to filter by? (If all months are desired, input "all"):'))
        month = month.title()
        if month in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
            break
        else:
            print('please choose a valid month to filter by or input "all" for all months')

    # get user input for day of week (all, monday, tuesday, ... sunday). Loop forever until valid day is chosen
    while True:
        day = str(input('what day of the week would you like to filter by? (If all days are desired, input "all"):'))
        day= day.title()
        if day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']:
            break
        else:
            print('please choose a valid day to filter by or input "all" for all days')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # loading the dataframe based on the variable city altered by get_filters()
    df = pd.read_csv(CITY_DATA[city])

    # making the start time in df a date time type, creating month and day columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filtering by month if neccesary
    if month != 'All':
        month = months.index(month) + 1
        df = df[df['month'] == month]


    # filtering by day if neccesary
    if day != 'All':
        df = df[df['day_of_week']== day]

    return df


def time_stats(df):
    """
    Calculates most common travel times.

    Parameters:
    df: the dataframe that is generated previously via user input/csv files

    Returns:
    most_common_month: most popular month in dataset based on mode
    most_common_day: most popular day of week based on mode
    most_common_hour: most popular rental hour based on mode

    """
    months = ['January', 'February', 'March', 'April', 'May', 'June']

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month (as a month name, take number output by df and use it as index in month array)
    most_common_month = months[df['month'].mode()[0]-1]
    print('Most common month: ',most_common_month)


    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most common day: ',most_common_day)

    # display the most common start hour
    most_common_hour = (df['Start Time'].dt.hour).mode()[0]
    print('Most common hour: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics for most popular stations and trips.

    Parameters:
    df: the dataframe that is generated previously via user input/csv files

    Returns:
    most_used_start: finds the most popular start station in the data based on mode
    most_used_end: finds the most popular end - similar to start station
    most_popular_combo: finds the most popular combination of start to end stations

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # creating pd series based on station name and how many times it is used
    start_station_counts = df['Start Station'].value_counts()
    # pd series using value counts defaults to descending order, first item in list will be max used
    most_used_start = start_station_counts.index[0]
    print('Most used start station: ', most_used_start, '-> Total uses: ', start_station_counts.max())

    # display most commonly used end station (same method as start station)
    end_station_counts = df['End Station'].value_counts()
    most_used_end = end_station_counts.index[0]
    print('Most used end station: ', most_used_end, '-> Total uses: ', end_station_counts.max())

    # display most frequent combination of start station and end station trip
    # create pd series of start and end stations
    start_stations = df['Start Station']
    end_stations = df['End Station']
    # concatenate the items in the series to make start>end combos as individual strings
    combined_string_list = start_stations+' to '+end_stations
    # count each time the string combos come up in the new list
    station_combo_counts = combined_string_list.value_counts()
    #compute statistics based on the value counts list of unique string combos
    how_many_trips = station_combo_counts.max()
    most_popular_combo = station_combo_counts.index[0]

    print('Most popular trip: ',most_popular_combo, '-> Total Trips: ', how_many_trips)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on trip duration.

    Parameters:
    df: the dataframe that is generated previously via user input/csv files

    Returns:
    total_travel_time: total time travelled among all users
    mean_travel_time: average trip duration for all users
    median_travel_time: median trip duration 

    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time among users: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time among users: ', mean_travel_time)

    # display median travel time
    median_travel_time = df['Trip Duration'].median()
    print('Median travel time among users: ', median_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """
    Displays user statistics and demographics.

    Parameters:
    df: the dataframe that is generated previously via user input/csv files
    city: the city passed into the dataframe, determines whether data is available

    Returns:
    Counts of each user type
    earliest_year: birth year of oldest user
    most_recent_year: birth date of youngest user
    most_common_year: most common birth year among users

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of each user type:\n', df['User Type'].value_counts())

    # Display counts of gender for only chicago and NYC
    if city != 'washington':
        print('\nCounts of gender among subscribers \n', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    # makes a sorted (ascending value) pd series based on users that have birth date values
        birth_year = (df['Birth Year'].sort_values()).dropna()
        earliest_year = birth_year.min()
        most_recent_year = birth_year.max()
        most_common_year = birth_year.mode()[0]

        print('\nEarliest birth date: ', earliest_year, '\n Most recent year: ', most_recent_year, '\n Most common birth year: ', most_common_year)
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print('Gender and birth year data not available for Washington\n')

def raw_data_prompt(city):
    """
    Shows the raw dataframe to the user when s/he asks for it.

    Data is shown 5 lines at a time. 5 more lines of data are shown every time the user answers 'yes'.
    Will not show more data if the the row number is outside of the dataframe. Program breaks if user
    inputs anything other than 'yes.'

    Parameters:
    df: the dataframe that is generated previously via user input/csv files

    Returns:
    most_used_start: finds the most popular start station in the data based on mode
    most_used_end: finds the most popular end - similar to start station
    most_popular_combo: finds the most popular combination of start to end stations

    """
    print('-'*40)
    # initialize x variable and total size of raw data to avoid overshooting it
    x = 5
    total_rows = pd.read_csv(CITY_DATA[city]).shape[0]
    # ask the user if they would like to see raw data, if answer is yes proceed until all data is explored
    while True:
        response = input('Would you like to see 5 lines of raw data? -type "yes" if yes, or enter anything else to exit: ').lower()
        if response == 'yes':
            # read the csv file for the city chosen in the beginning of the prompt down x lines (defaults to 5, increases by 5 each time)
            print(pd.read_csv(CITY_DATA[city], nrows=x))
            x += 5
            if x > total_rows:
                print('All data already shown')
                break
        else:
            break



def main():
    """Definition of main function"""

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data_prompt(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
