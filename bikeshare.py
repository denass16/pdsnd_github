import time
import pandas as pd
import numpy as np

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
    city = ''    #initiatize city
    month = 0    #initialize month
    day = 0      #initialize day

    msgcity1 = 'Would you like to see data from Chicago, New York City or Washington? '
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        city = input(msgcity1).lower()
        if city == 'new york':
            city = 'new york city'
        msgcity1 = 'Invalid entry. You can only enter Chicago, New York or Washington. Try again...'

    # TO DO: get user input for month (all, january, february, ... , june)
    filt_option_month = input('would you like to filter by month? (Y/N): ').lower()
    if filt_option_month == 'y':
        msgmonth1 = 'Which month will you like to filter by? Enter month number 1 - 6: '
        while month<1 or month>6:
            try:
                month = int(input(msgmonth1))
                msgmonth1 = msgmonth2
            except ValueError:
                msgmonth1 = 'Invalid entry. Enter month number 1 - 6: '
                continue
    else:
        if filt_option_month.lower() != 'n':
            print('Invalid entry. Exiting....')
            exit()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    filt_option_day = input('would you like to filter by day? (Y/N): ').lower()
    if filt_option_day == 'y':
        msgday1 = 'Which day will you like to filter by? Enter Monday, Tuesday,..Sunday: '
        while True:
            day = input(msgday1).lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            msgday1 = 'Invalid entry. Try again: '

    print('-'*40)
    return city, month, day, filt_option_month, filt_option_day


def load_data(city, month, day, filt_option_month, filt_option_day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if filt_option_month == 'y':
        df = df[df['month'] == month]
    if filt_option_day == 'y':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\nNote that if filter is applied, the following results only apply to the  filtered result.\n')
    start_time = time.time()

    # TO DO: display the most common month
    months_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    print('Most frequent month of travel is: ', months_dict[(pd.Series(df['month']).mode()[0])])

    # TO DO: display the most common day of week
    print('\nMost frequent day of travel is: ', pd.Series(df['day_of_week']).mode()[0])

    # TO DO: display the most common start hour

    df['Start Hour'] = (df['Start Time']).dt.hour
    print('\nMost frequent hour of travel is: {}:00hrs '.format(pd.Series(df['Start Hour']).mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station is: ', pd.Series(df['Start Station']).mode()[0])


    # TO DO: display most commonly used end station
    print('\nThe most commonly used end station is: ', pd.Series(df['End Station']).mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['start_stop_station'] = df['Start Station'] + ' and ' + df['End Station']
    print('\nThe most frequent combination of start and end station trip are: ', pd.Series(df['start_stop_station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time is {} hours'.format(df['Trip Duration'].sum()/(60*60)))


    # TO DO: display mean travel time
    print('\nThe mean travel time is {} hours'.format(df['Trip Duration'].mean(axis=0)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of user types\n',df['User Type'].value_counts())


    # TO DO: Display counts of gender
    if city.lower() == 'chicago' or city.lower() == 'new york city':
        print('\nCounts of user gender\n',df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_yob = int(pd.Series(df['Birth Year']).min())
        most_recent_yob = int(pd.Series(df['Birth Year']).max())
        most_common_yob = int(pd.Series(df['Birth Year']).mode())
        print('\nEarliest year of birth: {}\nMost common year of birth is: {}\nMost common year of birth is: {}'.format(earliest_yob, most_recent_yob, most_common_yob))
    else:
        print('\nNo available data on Gender and Birth Year for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_raw(df):
    """Display 5 rows of raw data"""
    begin_view = 0
    end_view = 5
    view = 'y'      #initialize
    msg_view1 = "Would you like to view 5 lines of raw data? (Y/N)..."
    while view.lower() == 'y':
        view = input(msg_view1)
        if view.lower() == "y":
            print(df.iloc[begin_view:end_view, :])
            begin_view +=5
            end_view +=5
            msg_view1 = "Would you like to view the next 5 lines of raw data? (Y/N)..."
        else:
            break


def main():
    while True:
        city, month, day, filt_option_month, filt_option_day = get_filters()
        df = load_data(city, month, day, filt_option_month, filt_option_day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_raw(df)

        restart = input('\nWould you like to restart? Enter Y/N.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
