import pandas as pd
import numpy as np
import json

import os
from pathlib import Path
from ydata_profiling import ProfileReport

os.chdir(Path(__file__).parent)

class CleanerCSV():
    def __init__(self):
        pass
    
    def open_file(self, filename = "default_specs.json"):
        self.filename = Path(__file__).parent / filename
        with open(self.filename) as file:
            json_file = json.load(file)
        self.json_file = json_file

    def open_csv(self):
        # assigning the CSV file with its path to a variable using json specification info
        csv_file = Path(__file__).parent / self.json_file["input_file"]

        # reading the CSV file, assigning no header to later remove header dupes treating it as a regular row
        original_df = pd.read_csv(csv_file, header = None)

        #making a copy of the original csv file
        df = original_df.copy()

        # saving the dataframe to the constructor
        self.df = df
    
    def clean_csv(self):
        
        def del_dupe():

            #dropping all dupe rows, keeping the first ones from the copies
            self.df = self.df.drop_duplicates(keep = "first")

            #after deleting all dupes, immediately assigning columns from first row to have it as a header
            self.df.columns = self.df.iloc[0]

            #reassigning the dataframe from 1st row on to not repeat the header row
            self.df = self.df[1:]

       
        def del_na():

            #deleting all rows where there is any NA value
            self.df = self.df.dropna(axis = "rows", how = "any")

            #deleting all columns where the whole column is only NA values
            self.df = self.df.dropna(axis = "columns", how = "all")
            

        def strip_str():

            # for string columns we take info about which ones those are from the json specs file 
            str_col = self.json_file["str_col"]

            # we loop through all column names in the above list to use the strip function on all of them
            for item in str_col:
                self.df[item] = self.df[item].str.strip()
            
        
        def replace_char():

            # using json specs info to find out which charachters are to be replaced
            # in this case its a dictionary, where key is replacee and value is replacement
            charachters= self.json_file["replace_row_char_details"]["change"]

            # using json specs to find out in which column the replacement should be applied
            replaced_col = self.json_file["replace_row_char_details"]["col"]

            # as replacee we take 'characters' dictionary's key and turn it to a list to then access its first [0] element
            char1 = list(charachters.keys())[0]

            # as replacement we access the 'characters' dictionary's value using the key defined above
            char2 = charachters[char1]

            # we loop over all items of the list of columns and apply the replacement
            for items in replaced_col:
                self.df[items] = self.df[items].str.replace(char1,char2)
            

        def data_type_check():

            # we assign variables columns where data types should be reassinged
            # we take the info about which columns those are from the json specs file
            numeric_col = self.json_file["numeric_col"]
            datetime_col = self.json_file["datetime_col"]
            str_col = self.json_file["str_col"]

            # we loop over every item of the lists we get from the json file,
            # and apply the reassignment of datatypes

            for item in str_col:
                self.df[item] = self.df[item].astype(str)

            for item in numeric_col:
                self.df[item] = pd.to_numeric(self.df[item])

            for item in datetime_col:
                self.df[item] = pd.to_datetime(self.df[item])

        # we call all the above functions so they can run once the main function is called
        del_dupe()
        del_na()
        strip_str()
        replace_char()
        data_type_check()


    def save_data(self):
        # we define the output file name using info from json specs file
        output_file = self.json_file["output_file"]

        # we define delimiter type using json specs file info
        sep = self.json_file["delimiter"]

        # we export the dataframe to a csv file, using the name and separator defined above
        self.df.to_csv(output_file, sep, index = False)

test = CleanerCSV()
test.open_file("specs.json")
test.open_csv()
test.clean_csv()
test.save_data()

# we do data profiling after the file has been cleaned
# first, we read the cleaned file data and save it in a dataframe
dframe = pd.read_csv("./my_data_clean1.csv")

# we create a profile from the dataframe where read file is stored
profile = ProfileReport(dframe)

# we save the profile into an html file, where we get infos about it
profile.to_file(output_file = "./profile_cleaned.html")
