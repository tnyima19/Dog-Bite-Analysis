"""
Name: Tenzing Nyima
Email: Tenzing.Nyima71@myhunter.cuny.edu
Resources: panda library and date and time, math
"""
from datetime import datetime
import pandas as pd

def capitalize(dog_name):
    """capitalize names of dogs if it is provieded,
    else return Name not provided"""
    dog_name = str(dog_name)
    if dog_name in ("nan", "NAME NOT PROVIDED"):
        return "Name not provided"
    return dog_name.title()

def make_dog_df(license_file, zipcode_file):
    """The function opens two inputted files, the first with
    god licensing information, and the second with zipcodes by boroughs.
    The function should do the follwing
    The names of hte dogs AnimalName sould be capitalized.
    The columns: 'License Expireddate', 'Extreact Year' should
    be dropped, the two  DataFrames sould be (left) merged on zipcoes
    Any reported gods not in NYC shoud be dropped."""
    df_license = pd.read_csv(license_file)
    df_license = df_license.drop(columns=['LicenseExpiredDate','Extract Year'])
    df_license['AnimalName'] = df_license['AnimalName'].apply(capitalize)
    #print(df_license)
    df_zipcode = pd.read_csv(zipcode_file)
    df_zipcode.rename(columns={'zip':'ZipCode'}, inplace=True)
    #print(df_zipcode)
    df_license = pd.merge(df_license, df_zipcode, how='left', on='ZipCode')
    #print(df_license)
    df_license = df_license.rename(columns={'borough':'Borough'})
    df_license = df_license.dropna(subset='Borough')
    df_license = df_license.drop(columns=['neighborhood', 'population', 'density', 'post_office'])
    return df_license

def make_bite_df(file_name):
    """This function takes one input:
    file name: the name of CSV file containing DOHMH Dog Bite DAta from POenData NYC.
    open csv file
    drop species column,
    return resulting dataframe
    """
    df = pd.read_csv(file_name)
    df = df.drop(columns=['Species'])
    return df

def clean_age(age_str):
    """If age_str ends in a y, return teh rest of the strings as number.
    For example, 3y represents 3 yrears and reutnr value is 3
    if age_str ends in a M, return teh rest of teh string as a number in years.
    For example, 6M represents 6monts and reutnr value is 0.5
    if age_str contains only a number , reutn it as number,
    Eg. 3 years and the return value is 3
    flr all other values return none"""
    #print(type(age_str))
    if type(age_str) is float:
        #print("i am here:")
        #print(age_str)
        return age_str
    else:
        if age_str.isdigit() is True:
            return float(age_str)
        if age_str[-1] == "Y":
            return float(age_str[0:len(age_str)-1])
        elif age_str[-1] == "M":
            return float(float(age_str[0: len(age_str)-1])/12)
        return None

def impute_age(df):
    """This function takes one input
    Your function shoudl replace any missing values in teh df['Age Num] column with
    the median of value of the column. The resulting Data Frame is returned"""
    median_age = df['Age Num'].median()
    df = df.replace({'Age Num': { "": median_age}})
    return df

def impute_zip(boro, zipcode):
    """if the zip code column is empyt, imput the value with zipcode of the
    post office based on value of boro: 10451 for bronx,
    11201 for Brooklyn, 10001 for Manhattan,
    11431 for Queens, 10341 for Staten island
    and none for other"""
    queens = "11431"
    brooklyn = "11201"
    manhattan = "10001"
    staten_island = "10341"
    bronx="10451"
    zipcode = str(zipcode)
    #print(type(zipcode), zipcode)
    if zipcode == "nan":
        if boro == "Queens":
            return queens
        elif boro == "Manhattan":
            return manhattan
        elif boro == "Brooklyn":
            return brooklyn
        elif boro == "Staten Island":
            return staten_island
        elif boro == "Bronx":
            return bronx
        return None
    return float(zipcode)

def clean_breed(breed_str):
    """Your function should return
    -> if breed empty, return "Unknown"
    else: return the string in title format with each word in string capitalized
    and all other letters lower case.
    Eg. if the input is BEAGLE MIXED, you should return Beagle Mixed.
    """
    breed_str = str(breed_str)

    if breed_str == "":
        return "Unknown"
    return breed_str.title()

def parse_datetime(df, column='LicenseIssuedDate'):
    """return df with 3 additional columns
    timestamp: contains the datetime object correspinding to
    the string stored in column. month: return the numb er correspinding
    to the month temestamp: 1 for january, 2 for feb 12 for Dec.
    day_of_week: returnthe number of correspondingt ot eh day of the week of timestap: 0
    for monday, 1 for tuesday, ...6 for Sunday.
    """
    #date_format_one = "%m/%d/%Y"
    #date_format_two = "%B %d %Y"
    df['timestamp']= pd.to_datetime(df[column])
    #print(dates)
    df['month'] = df['timestamp'].dt.month
    df['day_of_week'] = df['timestamp'].dt.day_of_week
    return df