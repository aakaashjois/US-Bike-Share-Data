import calendar
import datetime
import time

import numpy as np
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input('Enter a city. {chicago, new york city or washington}.').strip()
        if city in CITY_DATA.keys():
            print(f'The chosen city is {city}.')
            break
        else:
            print('Unknown city. Please try again.')

    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                    'november', 'december']
    while True:
        month = input('Enter a month. Leave blank to select all months.').strip()
        if month in valid_months:
            print(f'The chosen month is {month}.')
            break
        elif month == '':
            month = 'all'
            break
        else:
            print('Unknown month. Please try again.')

    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('Enter a day. Leave blank to select all days.').strip()
        if day in valid_days:
            print(f'The chosen day is {day}.')
            break
        elif day == '':
            day = 'all'
            break
        else:
            print('Unknown day. Please try again.')
    print('-' * 40)
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
    return pd.read_csv('./data/' + CITY_DATA[city])


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    start_month = pd.DatetimeIndex(df['Start Time']).month
    end_month = pd.DatetimeIndex(df['End Time']).month
    common_month = start_month[np.where(np.equal(start_month, end_month) == True)]
    most_common_month = calendar.month_abbr[common_month.unique()[0]]
    print(f'{most_common_month} is the most common month')
    # display the most common day of week
    start_day = pd.DatetimeIndex(df['Start Time']).dayofweek
    end_day = pd.DatetimeIndex(df['End Time']).dayofweek
    common_day = start_day[np.where(np.equal(start_day, end_day) == True)]
    most_common_day = calendar.day_abbr[common_day.unique()[0]]
    print(f'{most_common_day} is the most common day')
    # display the most common start hour
    common_hour = pd.DatetimeIndex(df['Start Time']).hour
    most_common_hour = common_hour.unique()[0]
    print(f'{most_common_hour} is the most common start hour')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(df['Start Station'].unique()[0] + ' is the most commonly used start station')
    # display most commonly used end station
    print(df['End Station'].unique()[0] + ' is the most commonly used end station')
    # display most frequent combination of start station and end station trip
    print(str(pd.DataFrame(df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)).index[0])
          + ' is the most frequent combination of start station and end station trip')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    seconds = np.sum(list((pd.DatetimeIndex(df['End Time']) - pd.DatetimeIndex(df['Start Time'])).seconds))
    print(str(datetime.timedelta(seconds=int(seconds))) + ' is the total travel time')

    # display mean travel time
    seconds = np.mean(list((pd.DatetimeIndex(df['End Time']) - pd.DatetimeIndex(df['Start Time'])).seconds))
    print(str(datetime.timedelta(seconds=int(seconds))) + ' is the mean travel time')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User type count: ')
    print(df['User Type'].value_counts())

    # Display counts of gender
    print('User gender count: ')
    print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    print(str(df['Birth Year'].sort_values().dropna().values[0]) + ' is the earliest year of birth')
    print(str(df['Birth Year'].sort_values().dropna().values[-1]) + ' is the most recent year of birth')
    print(str(df['Birth Year'].value_counts().index[0]) + ' is the most common year of birth')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
