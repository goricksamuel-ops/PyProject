import pandas as pd
import numpy as np


def check_column_type_consistency (df, column_name, expected_type, sample_size = None):
    """ Takes Inputs of column_name and expected data type and then checks all referenced columns in the dataframe are of the type required
        Users can provide a sample size to check excessively large dataframes
    """

    if sample_size is None:
        sample_size = len(df)
    else:
    # Prevent user Inputting Sample Size Larger than the Dataframe    
        sample_size = min(len(df), sample_size)

    sampled_df = df.sample(n=sample_size)

    if column_name not in df.columns:
        return "Error: Provided Column Does Not Exist In Data Frame"
    else:
        return "Column Exists"



def check_record_dupes (df, column_name, output_file_path,output_to_file = False):
    """ Checks a specified column within a specified data frame for duplicate values. Users can choose to export these duplicate values to a file
    """

    if df[column_name].is_unique:
        return "Field Contains Unique Values"
    else:
        
        if output_to_file:
            duplicates = df[df[column_name].duplicated(keep="first")][column_name]  
            np.savetxt(
                output_file_path,
                duplicates.values,
                fmt="%s"
            )

        return "Field Contains Duplicated Values"

