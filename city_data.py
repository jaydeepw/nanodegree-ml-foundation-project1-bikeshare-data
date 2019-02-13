import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITY_CODES_NAMES = { 'ch': 'Chicago',
              'ny': 'New York City',
              'wd': 'Washington' }

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # print(df.head())
    # print(df.info())
    # print(df.describe())

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    # print(list(df.columns.values))
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    # get the locale based name of the week.
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).weekday_name
    # print(df['day_of_week'].head(2))

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)
        print("month {}".format(month))

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        # use .title() to bring them both on same level
        df = df.loc[df['day_of_week'] == day.title()]
        # print(df.head(5))
    
    return df

def get_male_sharer_percentage(df):
    """
    Get the approx. percentage of Male participants in the total bike sharing.
    """
    try:
        valueCounts = df['Gender'].value_counts(dropna=True)
    except KeyError:
        print("Sorry, gender data not available for this city")
        return 0

    #print(valueCounts)
    genderDict = valueCounts.to_dict()
    #print(genderDict)
    maleSharers = genderDict['Male']
    totalSharers = maleSharers + genderDict['Female']
    # print(totalSharers)
    percentage = float((maleSharers*100 / totalSharers))
    return percentage

def popular_hour_of_the_day(df):
    """
    Get the hour of the day which sharing was at peak
    """
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    count = df['hour'].value_counts().to_dict()[17]
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    return popular_hour, count

def trip_duration(df):
    """
    Get the total trip duration and average trip duration
    """
    totalDuration = df['Trip Duration'].sum()
    numRows = df['Trip Duration'].count()
    averageDuration = totalDuration / numRows
    return totalDuration, averageDuration

def show_head_data_conditionally(response, df):
    if response == "no":
        return
    
    print(df.head())

# df = load_data('washington', 'all', 'Friday')
# trip_duration(df)

while True:

    while True:
        print("Which city you want to get data for?")
        cityCodes = CITY_CODES_NAMES.keys()
        cityNames = CITY_CODES_NAMES.values()
        for item in range(len(CITY_CODES_NAMES)):
            print("Enter {} for {}".format(cityCodes[item], cityNames[item]))
        
        cityCode = raw_input()

        if (cityCode in CITY_CODES_NAMES.keys()):
            print("Alright, you want to know about {}".format(CITY_CODES_NAMES[cityCode]))
            break
        else:
            print("====> Invalid input for city name. Pleas try again")

    while True:
        print("Which month you want to get data for?")
        print("Please enter index number.")
        monthIndex = raw_input("\
    1. Jan \n\
    2. Feb \n\
    3. March \n\
    4. April \n\
    5. May \n\
    6. June \n")

        """
        print("monthIndex {}".format(monthIndex))
        print("in range {}".format(monthIndex in range(1, 7)))
        print(monthIndex >= 1)
        print(monthIndex < 7)
        """

        #todo: This is currently not working. fix it.
        if monthIndex in range(1, 7):
            print("Month is in range")
            break
        else:
            print("====> Invalid input for month")
            #todo remove this break once above if block start working
            break

        # todo: check invalid input
        print("My month is {} {}".format(monthIndex, cityName))

    while True:
        print("Which day you want to get data for?")
        print("Please enter index number.")
        dayIndex = raw_input("    0. Mon \n\
        1. Tuesday \n\
        2. Wednesday \n\
        3. Thursday \n\
        4. Friday \n\
        5. Saturday \n\
        6. Sunday\n")

        #todo: This is currently not working. fix it.
        if dayIndex in range(0, 7):
            print("Day is in range")
            break
        else:
            print("====> Invalid input for day")
            #todo remove this break once above if block start working
            break

        # todo: check invalid input
        print("My city: {} \n month {} \n dayIndex {}".format(cityCode, monthIndex, dayIndex))

    # calculate the statistics
    print("Counting stats....")
    cityName = CITY_CODES_NAMES[cityCode].lower()
    df = load_data(cityName, 'all', 'Thursday')

    # Print the statistics
    print("Printing analysis")

    # Print percentage if male sharers
    percentage = get_male_sharer_percentage(df)

    if percentage > 0:
        print("Approximately {} percent of the total particiapnt are Male".format(percentage))

    # Print most popular hour and its count
    popular_hour, count = popular_hour_of_the_day(df)

    print("Most popular hour of the day was {}".format(popular_hour))
    print("{} sharings happened during this hour".format(count))

    # Print duration stats
    totalDuration, averageDuration = trip_duration(df)
    print("Riders from this city spent a total of {} seconds riding".format(totalDuration))
    print("Average duration of the riders has been {} seconds".format(averageDuration))

    show_head_data_conditionally(raw_input("See 5 lines of raw data? Enter yes/no \n"), df)

    # Outermost big loop counting here
    print("Do you want more analysis of other cities, months or days?")
    more_analysis = raw_input("yes/no \n")
    if more_analysis == "no":
        # break top-most while loop
        print("Thank you for using this tool")
        break
