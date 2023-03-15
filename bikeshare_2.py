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

    # User input option-lists
    list_cities = ["chicago", "new york", "washington"]
    list_month_options = ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    list_day_options = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    #Variables
    city=""
    month=""
    day=""

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while (city.lower() not in list_cities):
        city = input("Would you like to see data for Chicago, New York, or Washington? Please enter one of the three City names: ")
        if (city.lower() not in list_cities):
            print("Your entry is outside the options. Please try again:")

    # get user input for month (all, january, february, ... , june)
    while (month.lower() not in list_month_options):
        month = input("Which month would you like to filter? Type in one specific month or 'all' to filter for all month:")
        if (month.lower() not in list_month_options):
            print("Your entry is outside the options. Please try again:")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while (day.lower() not in list_day_options):
        day = input("Which day do you want to see? Type in one specific day or 'all' to filter for all days: )")
        if (day.lower() not in list_day_options):
            print("Your entry is outside the options. Please try again:")


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
    #Variables
    df=pd.DataFrame

    # file selection
    if city.lower() == "chicago":
        df=pd.read_csv("chicago.csv")
    elif city.lower() == "new york":
        df=pd.read_csv("new_york_city.csv")
    elif city.lower() == "washington":
        df=pd.read_csv("washington.csv")
    else: 
        print("error at file selection")


    ## filter by Month and day if applicable
    # Declarations Months
    list_index_months = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    list_month_options = ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    dict_months = dict(zip(list_month_options,list_index_months))
    # Declarations Days
    list_index_days = [0,1,2,3,4,5,6,7]
    list_day_options = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    dict_days = dict(zip(list_day_options,list_index_days))

    #colums year, month, day, weekday, start hour
    df["star_year"]=pd.DatetimeIndex(df["Start Time"]).year
    df["start_month"]=pd.DatetimeIndex(df["Start Time"]).month
    df["start_day"]=pd.DatetimeIndex(df["Start Time"]).day
    df["start_weekday"]=pd.DatetimeIndex(df["Start Time"]).weekday
    df["start_hour"]=pd.DatetimeIndex(df["Start Time"]).hour
    
    #query month
    str_filter_month = (dict_months[month.lower()])
    if month.lower() != "all": # No Filterin needed in this case
        df=df.query("start_month == @str_filter_month")
    #query day
    str_filter_day = (dict_days[day.lower()]-1)
    if day.lower() != "all": # No Filterin needed in this case
        df=df.query("start_weekday == @str_filter_day")

    #print(df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #months
    list_index_months = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    list_month_options = ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    series_month_options = pd.Series(data=list_month_options, index=list_index_months)
    #days
    list_index_days = [0,1,2,3,4,5,6]
    list_weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    series_day_options = pd.Series(data=list_weekdays, index=list_index_days)
    #variables
    df_time=pd.DataFrame
    max_month_pos=0
    max_day_pos=0
    max_hour_pos=0
    max_month=0
    max_day=0
    max_hour=0
    max_value=0

    # display the most common month
    print("--------------")
    print("view count of rentals in each month:\n")
    df_time=df.groupby(["start_month"]).size().reset_index(name="counts")
    print (df_time) #print View
    print("\n")
    max_value=df_time["counts"].max()
    max_month_pos=(df_time["counts"].idxmax())
    max_month=df_time.iloc[max_month_pos,0]
    print("Most common month:")
    print(series_month_options[max_month])
    print("number of bookings this month:")
    print(max_value)
    print("\n")

    # display the most common day of week
    print("--------------")
    print("view count of rentals in each day:\n")
    df_time=df.groupby(["start_weekday"]).size().reset_index(name="counts")
    print (df_time) #print View
    print("\n")
    max_value=df_time["counts"].max()
    max_day_pos=(df_time["counts"].idxmax())
    max_day=df_time.iloc[max_day_pos,0]
    print("Most common day:")
    print(series_day_options[max_day])
    print("number of bookings this day:")
    print(max_value)
    print("\n")

    # display the most common start hour
    print("--------------")
    print("view count of rentals in each hour:\n")
    df_time=df.groupby(["start_hour"]).size().reset_index(name="counts")
    print (df_time) #print View
    print("\n")
    max_value=df_time["counts"].max()
    max_hour_pos=(df_time["counts"].idxmax())
    max_hour=df_time.iloc[max_hour_pos,0]
    print("Most common hour:")
    print(max_hour)
    print("number of bookings this hour:")
    print(max_value)
    print("\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    #variables
    df_station=pd.DataFrame
    max_value=0
    max_station_pos=0
    max_station=0


    # display most commonly used start station
    print("view start stations and counts:\n")
    df_station=df.groupby(["Start Station"]).size().reset_index(name="counts")
    print(df_station)
    max_value=df_station["counts"].max()
    max_station_pos=(df_station["counts"].idxmax())
    max_station=df_station.iloc[max_station_pos,0]
    print("Most common Start-Station:")
    print(max_station)
    print("number of bookings:")
    print(max_value)
    print("\n")

    # display most commonly used end station
    print("view end stations and counts:\n")
    df_station=df.groupby(["End Station"]).size().reset_index(name="counts")
    print(df_station)
    max_value=df_station["counts"].max()
    max_station_pos=(df_station["counts"].idxmax())
    max_station=df_station.iloc[max_station_pos,0]
    print("Most common End-Station:")
    print(max_station)
    print("number of bookings:")
    print(max_value)
    print("\n")

    # display most frequent combination of start station and end station trip
    print("view combination of stations and counts:\n")
    df_station=df.groupby(["Start Station","End Station"]).size().reset_index(name="counts")
    print(df_station)
    max_value=df_station["counts"].max()
    max_station_pos=(df_station["counts"].idxmax())
    max_start_station=df_station.iloc[max_station_pos,0]
    max_end_station=df_station.iloc[max_station_pos,1]
    print("Most common combination:")
    print("Start Station: " + max_start_station)
    print("End Station: " + max_end_station)
    print("number of bookings:")
    print(max_value)
    print("\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration=str(df["Trip Duration"].sum())
    print("Total Duration " + duration + " seconds")

    # display mean travel time
    AVG=str(df["Trip Duration"].mean())
    print("AVG Duration " + AVG + " seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    df_userstats=pd.DataFrame

    # Display counts of user types
    print("view usertypes and counts:\n")
    df_userstats=df.groupby(["User Type"]).size().reset_index(name="counts")
    print(df_userstats)
    print("\n")
    max_value=df_userstats["counts"].max()
    max_user_pos=(df_userstats["counts"].idxmax())
    max_user=df_userstats.iloc[max_user_pos,0]
    print("Most common usertype:")
    print(max_user)
    print("number of bookings:")
    print(max_value)
    print("\n")

    
    if city.lower() != "washington":
        # Display counts of gender
        print("view gender and counts:\n")
        df_userstats=df.groupby(["Gender"]).size().reset_index(name="counts")
        print(df_userstats)
        print("\n")
        max_value=df_userstats["counts"].max()
        max_user_pos=(df_userstats["counts"].idxmax())
        max_user=df_userstats.iloc[max_user_pos,0]
        print("Most common Gender:")
        print(max_user)
        print("number of bookings:")
        print(max_value)
        print("\n")

        # Display earliest, most recent, and most common year of birth
        print("Customer birth year: view birth year and counts:\n")
        df_userstats=df.groupby(["Birth Year"]).size().reset_index(name="counts")
        print(df_userstats)
        print("\n")
        max_value=df_userstats["counts"].max()
        max_user_pos=(df_userstats["counts"].idxmax())
        max_user=df_userstats.iloc[max_user_pos,0]
        print("Most common Birth Year:")
        print(max_user)
        print("number of bookings:")
        print(max_value)
        print("\n")

        #earlies Birth Year
        print("earlies Birth Year:")
        earliest_BY = df_userstats["Birth Year"].max()
        print(earliest_BY)
        print("\n")
        #most recent Birth Year
        print("most recent Birth Year:")
        recent_BY = df_userstats["Birth Year"].min()
        print(recent_BY)
        print("\n")

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print("No User Data for Birth year and Gender for selection washington")
    



def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while (view_data != "no"):
        print(df.iloc[start_loc:(start_loc + 5)])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

