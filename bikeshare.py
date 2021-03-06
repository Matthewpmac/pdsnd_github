import time
import pandas as pd
import numpy as np

pd.set_option('display.max_columns',20)

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
    cities = list(CITY_DATA.keys())
    while city not in cities:
        city= input('Not an appropriate choice. Please select new choice of city: \n').lower()

    # get user input for month (all, january, february, ... , june)

    month = input("Which month? January, February, March, April, May, June or all\n").lower()
    months = ['january','february','march','april','may','june','all']
    while month not in months:
        month = input('Not an appropriate choice. Please select another choice of month: \n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all\n').lower()
    days = ['monday','tuesday','wednesday','thursday','friday','saturday', 'sunday', 'all']
    while day not in days:
       day = input('Not an appropriate choice. Please select another choice of day: \n').lower()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of city to analyze
        (str) month - name of month to filter by, or "all" to apply no month filter
        (str) day - name of day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month: ', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of week: ', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most common start station: ', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most common end station: ', common_end)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " TO " + df['End Station']
    common_trip = df['trip'].mode()[0]
    print ('Most frequent combination of start and end station: ', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Travel Time'] = df['End Time'] - df['Start Time']

    # display total travel time
    print('Total Travel Time: ', df['Travel Time'].sum())

    # display mean travel time
    print('Mean Travel Time: ', df['Travel Time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of user types:\n')
    print(user_types)



    if city != 'washington':
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print('Count of gender:\n')
        print(gender)

        # Display earliest, most recent, and most common year of birth
        min_birth = df['Birth Year'].min()
        max_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]

        print('Earliest Birth Year: ', min_birth)
        print('Most Recent Birth Year: ', max_birth)
        print('Most Common Birth Year: ', common_birth)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays 5 lines of raw data upon user request"""

    start_loc = 0
    end_loc = 5

    show_data = input("Do you want to see 5 lines of raw data? \n").lower()
    if show_data == 'yes':
        while end_loc <= df.shape[0] - 1:
            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5
            continue_show = input("Do you want a further 5 lines? \n").lower()
            if continue_show == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
