import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
        print(df.head(5))
    
    return df
    
# df = load_data('chicago', 'all', 'Thursday')

while True:
    inputResponse = raw_input("\nWhich city you want to get data for? \
    Chicago, Washington, NY \
            \nEnter ch, wd or ny \
            \nExter X to exit")

    if inputResponse == "y":
        print("My name is Jaydeep")
    elif inputResponse == "x":
        break
    else:
        print("====> Invalid input")