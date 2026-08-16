import pandas as pd
import numpy as np
import re
from codefiles.definitions.definitions import *
from random import sample



def check_column_type_consistency(df, variable_definitions, sample_size = None):
    """ Takes Inputs of column_name and expected data type and then checks all referenced columns in the dataframe are of the type required
        Users can provide a sample size to check excessively large dataframes
        Will Output any columns that exist in the data frame that are not found in the variable definitions, and thus are not checked
    """
# Dont allow users to input a sample size larger than the dataframe
    if sample_size is None:
        df_sample = df
    else:
        try:
            sample_size = int(sample_size)
            df_sample = sample(df,min(sample_size,len(df)))
        except ValueError:    
                print("Please Enter Valid Sample Size")

# Intialise Table To Track Any columns that are missing, to allow the user to amend the names in the dataframe   

    count = 0
    missing_columns = {}

    for column, definitions in variable_definitions:

        if column in df.columns:

            valid_values = definitions.keys()

            invalid_values = df[~df[column].astype(str).isin(valid_values)][column].unique()

            if len(invalid_values) == 0:
                print(f"{column}: All values valid")
            else:
                print(f"{column}: Invalid values found: {invalid_values}")
        else:
            print("Column " + column + " Not Found")
            missing_columns[count] = column
            count = count + 1

    return missing_columns


def check_record_dupes (df, column_name, output_file_path = "",output_to_file = False):
    """ Checks a specified column within a specified data frame for duplicate values. Users can choose to export these duplicate values to a file
    """

    if df[column_name].is_unique:
        return "Field Contains Unique Values"
    else:
        
        if output_to_file:
            # Create Exceptions File With List of Duplicate Values
            duplicates = df[df[column_name].duplicated(keep=False)][column_name]  
            np.savetxt(
                output_file_path,
                duplicates.values,
                fmt="%s"
            )

            # Clean Dataset 
            df.drop_duplicates(subset=[column_name],keep="first")


        return "Field Contains Duplicated Values"


import re

import re

def regex_column_rename(column_dictionary, df):
    """Compare column names from a dictionary against DataFrame columns.
    Column names are normalised before comparison by:
    - Converting to lowercase
    - Removing spaces
    - Removing underscores
    """

    def normalise_name(name):
        return re.sub(r"[\s_]+", "", str(name)).lower()

    for expected_column in column_dictionary.values():

        for actual_column in df.columns:

            if normalise_name(expected_column) == normalise_name(actual_column):

                # Don't ask if they already have exactly the same name
                if expected_column == actual_column:
                    continue

                print("Potential match found:")
                print(f"Expected: {expected_column}")
                print(f"DataFrame: {actual_column}")

                confirmation = input(
                    f"Rename '{actual_column}' to '{expected_column}'? (y/n): "
                )

                if confirmation.lower() == "y":

                    df.rename(
                        columns={actual_column: expected_column},
                        inplace=True
                    )

                    print(
                        f"Renamed '{actual_column}' to '{expected_column}'"
                    )

    return df