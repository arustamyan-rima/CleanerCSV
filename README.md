# CSV File Cleaner and Profiler

This project involves reading a CSV file, cleaning it according to specific rules provided in a JSON configuration file, and then saving the cleaned data to a new CSV file. Additionally, it generates a profiling report for the cleaned data in the form of an HTML file.

The script is structured around a class named `CleanerCSV` that encapsulates various methods for file manipulation and data cleaning.

### Project Structure

- The main script is named `data_cleaner.py`.
- The input CSV file and the JSON configuration file are loaded using the class methods.
- The script includes methods for cleaning the CSV file based on rules defined in the JSON configuration file.
- Data profiling is conducted using the `ydata_profiling` library, generating an HTML report for the cleaned data.

### Usage

Ensure you have the necessary libraries installed to run the code. You can run the script using Python.

The cleaned data will be saved to a new CSV file as specified in the JSON configuration file, and a profiling report will be generated as an HTML file.

### Functions
The CleanerCSV class includes the following methods:  

open_file: Opens the JSON configuration file.  
open_csv: Opens and reads the specified CSV file.  
clean_csv: Cleans the CSV data based on rules defined in the JSON configuration file.  
save_data: Saves the cleaned data to a new CSV file and conducts data profiling, generating an HTML report.  
