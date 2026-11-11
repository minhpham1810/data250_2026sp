# -*- coding: utf-8 -*-
"""
data.py
This python file will be used in Project 1 for DATA 250. 
Details on your tasks can be found in the Project 1 Jupyter notebook.
"""
import numpy as np
import csv
import math
import matplotlib.pyplot as plt
class phase0:
    """
    This class is only relevant to phase 0, and is a "proof of concept"
    """
    
    def __init__(self, filepath=None):
        """
        Parameters
        ----------
        filepath : Path to a csv file

        TODO:
            1. Open and read the .csv file using csv.reader
            2. Store JUST the first row as self.data
        
        """
        if filepath is not None:
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                self.data = next(reader)
            
    def showrow(self):
        """
        Return self.data -- this is one line :)
        """        
        return self.data
        
        


class Data:
    def __init__(self, filepath=None):
        """
        Parameters
        ----------
        filepath : str or None.  Path to data .csv file.  The .csv file should
        be formatted with a first header row giving column names, a second row
        giving the type of data (Categorical or Numerical), and all remaining rows data.
        
        Create a data object declaring the following attributes.  Initialize them
        as None. Use the EXACT attribute names below (e.g. use self.n, not self._n, not
        self.num_points, etc).
                                                     
 
            - m: the number of columns
            - n: the number of data samples
            - headers: a Python list of Strings that correspond to the variable names 
            from the csv (from the first row of the csv)
            - data: a Python list of lists.  data[i][j] should correspond to the
            ith sample and jth column.  
            - header2col is a Python dictionary mapping each categorical variable header
            (a string) too its column index
            
        If filepath is not None, use the read method to properly initialize them.
        """
        if filepath is not None:
            self.read(filepath)
        else:
            self.m = None
            self.n = None
            self.headers = None
            self.data = None
            self.header2col = None
        
    def read(self, filepath):
        """

        Parameters
        ----------
        filepath : Path to data .csv file

        Reads in a csv and uses basic Python (no pandas/numpy) to load the data.
        
        TODO:
            1. Open and read the .csv file using csv.reader.
            2. Based on the csv file, update/set self.m, self.n, self.headers,
            self.data, and self.header2col as defined in the __init__ method.
            
            Numerical data should be stored as floats.
            
            Categorical data should be stored as strings.
            
            3. If any data is missing, assign it to be np.nan (if numerical)
            or the string "missing" (if categorical)

        """
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            self.headers = next(reader)
            self.m = len(self.headers)
            types = next(reader)
            
            self.data = []
            self.header2col = {header: i for i, header in enumerate(self.headers)}
            
            for row in reader:
                processed_row = []
                for i, value in enumerate(row):
                    if value.strip() == "":
                        if types[i].lower() == "numerical":
                            processed_row.append(np.nan)
                        else:
                            processed_row.append("missing")
                    else:
                        if types[i].lower() == "numerical":
                            processed_row.append(float(value))
                        else:
                            processed_row.append(value)
                self.data.append(processed_row)
            
            self.n = len(self.data)



    def __str__(self):
        """
        Returns:
        -----------
        s: A nicely formatted string representation of the data in this Data object.
           If the data has more than 5 rows, only show the first 5 rows
           See the test code at the end of this file for example output.

        """
        if self.data is None:
            return "Data object is empty"

        # Build header line
        header_line = "  ".join(f"{h:<20}" for h in self.headers)

        # Determine number of rows to show
        num_rows = min(5, self.n)
        show_truncated = self.n > 5

        # Build data lines
        data_lines = []
        for i in range(num_rows):
            row_str = "  ".join(f"{str(val):<20}" for val in self.data[i])
            data_lines.append(row_str)

        # Build final string
        result = f"Data: {self.n} samples, {self.m} features.\n"
        result += header_line + "\n"
        result += "-" * 31 + "\n"

        if show_truncated:
            result += f"Showing first {num_rows}/{self.n} rows.\n"

        result += "\n".join(data_lines) + "\n"
        result += "-" * 31

        return result
    
    def head(self):
        """

        Returns the first 5 data samples as a list.  
        If there are less than 5 samples, return them all.
        
        -------
        """
        return self.data[:min(5, self.n)]
        
    def tail(self):
        """

        Returns the last  5 data samples as a list.  
        If there are less than 5 samples, return them all.
        
        -------
        """
        return self.data[-min(5, self.n):]
    
    def get_max(self, col):
        """
        
        Parameters
        ----------
        col : A column name for your data set (col will be a string, not integer)

        Returns
        -------
        The maximum value in that column, skipping any nans
        If col is not in self.headers or that data is categorical, return np.nan
        
        NOTE: You MUST do this "from scratch" by looping through the relevan column.
        You can NOT use any numpy/pandas commands, and should not even use
        python's "max" command
        """
        
        if col not in self.headers:
            return np.nan

        col_idx = self.header2col[col]
        col_data = [self.data[i][col_idx] for i in range(self.n)]

        # Check if categorical
        if any(isinstance(val, str) and val != "missing" for val in col_data if not (isinstance(val, float) and math.isnan(val))):
            return np.nan

        max_val = None
        for val in col_data:
            if isinstance(val, float) and math.isnan(val):
                continue
            if max_val is None or val > max_val:
                max_val = val

        return max_val if max_val is not None else np.nan

    
    
    
    def get_min(self, col):
        """
        
        Parameters
        ----------
        col : A column name for your data set (col will be a string, not integer)

        Returns
        -------
        The minimum value in that column, skipping any nans
        If col is not in self.headers or that data is categorical, return np.nan
        
        NOTE: You MUST do this "from scratch" by looping, as with get_max.  
        You can NOT use any numpy/pandas commands.
        
        This is the last method for phase 1, but you can of course get ahead and 
        complete more!
        """
        
        if col not in self.headers:
            return np.nan

        col_idx = self.header2col[col]
        col_data = [self.data[i][col_idx] for i in range(self.n)]

        # Check if categorical
        if any(isinstance(val, str) and val != "missing" for val in col_data if not (isinstance(val, float) and math.isnan(val))):
            return np.nan

        min_val = None
        for val in col_data:
            if isinstance(val, float) and math.isnan(val):
                continue
            if min_val is None or val < min_val:
                min_val = val

        return min_val if min_val is not None else np.nan
    
    def get_sum(self, col):       
        """
        
        Parameters
        ----------
        col : A column name for your data set (col will be a string, not integer)

        Returns
        -------
        The sum of all entries in that column, skipping any nans
        If col is not in self.headers or that data is categorical, return np.nan
        
        NOTE: You MUST do this "from scratch" by looping.  You can NOT use any numpy/pandas
        commands.
    
        """       
        if col not in self.headers:
            return np.nan
        col_idx = self.header2col[col]
        col_data = [self.data[i][col_idx] for i in range(self.n)]

        for val in col_data:
            if isinstance(val, str):
                return np.nan

        sum = 0
        for i in col_data:
            if math.isnan(i):
                continue
            else:
                sum += i
        return sum

    
    def count_entries(self, col):     
        """
        
        Parameters
        ----------
        col : A column name for your data set (col will be a string, not integer)

        Returns
        -------
        The count of non-nan entries in that column
        If col is not in self.headers or that data is categorical, return np.nan

        """           
        if col not in self.headers:
            return np.nan
        col_idx = self.header2col[col]
        col_data = [self.data[i][col_idx] for i in range(self.n)]
        sum = 0
        for i in col_data:
            if math.isnan(i):
                continue
            sum += 1
        return sum    
    
    def get_mean(self, col):       
        """
        
        Parameters
        ----------
        col : A column name for your data set (col will be a string, not integer)

        Returns
        -------
        The mean of all entries in that column, skipping any nans.  
        For instance, if a column has 3 entries (2, 4, np.nan), the mean would be 6/2=3,
        the mean of non-nan entries.
        
        If col is not in self.headers or that data is categorical, return np.nan
        
        You can assume there is at least one non-nan entry in the column.
        
        NOTE: You can NOT use any numpy/pandas commands.
        """     
        if col not in self.headers:
            return np.nan
        

        return self.get_sum(col) / self.count_entries(col)
    
    def get_stddev(self, col):       
        """
        
        Parameters
        ----------
        col : A column name for your data set (col will be a string, not integer)

        Returns
        -------
        The (sample) standard deviation of all entries in that column, skipping any nans.  
        
        The formula for standard deviation is in the Project Jupyter notebook.
        
        If col is not in self.headers or that data is categorical, return np.nan.
        
        If count_entries(col)<2, also return np.nan (to avoid a divide-by-0 error)
        
        
        NOTE: You MUST do this "from scratch".  You can NOT use any numpy/pandas
        commands.
        """       
        
        if col not in self.headers or self.count_entries(col) < 2:
            return np.nan
        
        col_idx = self.header2col[col]
        col_data = [self.data[i][col_idx] for i in range(self.n)]
        
        # Filter out NaN values
        valid_data = []
        for val in col_data:
            if not (isinstance(val, float) and math.isnan(val)):
                valid_data.append(val)
        
        # Compute mean of valid data
        mean = sum(valid_data) / len(valid_data)
        
        # Compute squared differences 
        diff_squared = [(val - mean)**2 for val in valid_data]

        # Stddev formula
        return math.sqrt(sum(diff_squared) / (len(valid_data) - 1))
    
    
    def describe(self, col):       
        """
        
        Parameters
        ----------
        col : A column name for your data set (col will be a string, not integer)

        Returns
        -------
        A (nicely formatted) string summarizing the min, mean, max, and standard deviation
        of the data in col.  It should also include the number of data points and number
        of missing entries.  
        
        If col is not in self.headers or that data is categorical, return the strung
        "Error: Non-numerical or missing data".
        
        Please emulate the formatting in the Project 1 notebook exactly.
        
        NOTE: You can NOT use any numpy/pandas commands.  Use your earlier work.
        """       
        if col not in self.headers:
            return "Error: Non-numerical or missing data"

        col_idx = self.header2col[col]
        col_data = [self.data[i][col_idx] for i in range(self.n)]

        # Check if categorical
        if any(isinstance(val, str) and val != "missing" for val in col_data if not (isinstance(val, float) and math.isnan(val))):
            return "Error: Non-numerical or missing data"

        count = self.count_entries(col)
        if count == 0 or self.get_min(col) is np.nan:
            return "Error: Non-numerical or missing data"

        missing_count = self.n - count

        result = f"Variable: {col}\n"
        result += f"{self.n} samples, {missing_count} of which has missing data\n"
        result += f"Min: {self.get_min(col)}\n"
        result += f"Max: {self.get_max(col)}\n"
        result += f"Mean: {self.get_mean(col)}\n"
        result += f"Standard Deviation: {self.get_stddev(col)}"

        return result

    
    
    def describe_at_level(self, col, cat, level):       
        """
        
        Parameters
        ----------
        col : A column name for your data set (col will be a string, not integer) containing numerical data
        cat: A column name for your data set containing categorical data
        level: A level of cat

        Returns
        -------
        A (nicely formatted) string summarizing the count, min, mean, max, and standard deviation
        of the data in col, only accounting for entries whose value in column cat is level.
        
        Example: Suppose your CSV looked like
            category, value
            Categorical,	Numerical
            A, 1
            B, 2
            A, 3
            A, 4
            B, 5
            C, 6
            
        If you call describe_at_level(value, category, "A"), it should return a string
        giving the count, min, mean, max, and standard deviation of [1, 3, 4] (the
        entries who have category A).  
        
        Note: You can assume that col correctly consists of numerical data and that
        cat correctly consists of categorical data.  You should not, however, assume
        that level occurs within cat (i.e. it's possible to have count 0').  If the
        count is 0, the min, mean, max, and standard deviation should all be np.nan.
        If the count is 1, the min, mean, and max are all defined, but the standard deviation
        should be np.nan
        
        Please emulate the formatting in the Project 1 notebook exactly.
        
        NOTE: You can NOT use any numpy/pandas commands.  
        
        NOTE2: You probably want to add some helper functions here, like a
        mean_at_level method.
        
        """       
        col_idx = self.header2col[col]
        cat_idx = self.header2col[cat]
            
        # Filter data for the specified level
        filtered_data = []
        for i in range(self.n):
            if self.data[i][cat_idx] == level:
                val = self.data[i][col_idx]
                if not (isinstance(val, float) and math.isnan(val)):
                    filtered_data.append(val)
        
        count = len(filtered_data)
        
        if count == 0:
            result = f"Variable: {col}\n"
            result += f"Restricted to level {level} of variable {cat}\n"
            result += f"Count: {count}\n"
            result += f"Min: nan\n"
            result += f"Max: nan\n"
            result += f"Mean: nan\n"
            result += f"Standard Deviation: nan"
            return result
        
        min_val = min(filtered_data)
        max_val = max(filtered_data)
        mean_val = sum(filtered_data) / count
        
        if count == 1:
            stddev_val = np.nan
        else:
            diff_squared = [(val - mean_val)**2 for val in filtered_data]
            stddev_val = math.sqrt(sum(diff_squared) / (count - 1))
        
        result = f"Variable: {col}\n"
        result += f"Restricted to level {level} of variable {cat}\n"
        result += f"Count: {count}\n"
        result += f"Min: {min_val}\n"
        result += f"Max: {max_val}\n"
        result += f"Mean: {mean_val}\n"
        result += f"Standard Deviation: {stddev_val}"
        
        return result
            
    def plot_scatter(self, col_x, col_y, color='pink', alpha=0.6, title=None):
        """
        Parameters
        ----------
        col_x : Column name for x-axis (must be numerical)
        col_y : Column name for y-axis (must be numerical)
        color : Color for the points (default 'purple')
        alpha : Transparency level (default 0.6)
        title : Title for the plot. If None, uses default title.

        Creates a scatter plot of two numerical columns.
        
        Returns
        -------
        None (displays a plot)
        
        If columns are not in self.headers or data is categorical, prints error message.
        """
        if col_x not in self.headers or col_y not in self.headers:
            print("Error: One or both columns not found")
            return
        
        col_x_idx = self.header2col[col_x]
        col_y_idx = self.header2col[col_y]
        
        # Extract data and check if numerical
        x_data = []
        y_data = []
        
        for i in range(self.n):
            x_val = self.data[i][col_x_idx]
            y_val = self.data[i][col_y_idx]
            
            # Check if categorical
            if isinstance(x_val, str) or isinstance(y_val, str):
                print("Error: One or both columns are categorical")
                return
            
            # Only include if both values are not NaN
            if not (isinstance(x_val, float) and math.isnan(x_val)) and \
            not (isinstance(y_val, float) and math.isnan(y_val)):
                x_data.append(x_val)
                y_data.append(y_val)
        
        if len(x_data) == 0:
            print("Error: No valid data to plot")
            return
            # Create scatter plot
        plt.figure(figsize=(10, 6))
        plt.scatter(x_data, y_data, color=color, alpha=alpha, edgecolors='black', linewidth=0.5)
        
        if title is None:
            title = f'{col_y} vs {col_x}'
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(col_x, fontsize=12)
        plt.ylabel(col_y, fontsize=12)
        plt.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    def get_median(self, col):
        """
        Parameters
        ----------
        col : A column name for your data set (col will be a string, not integer)

        Returns
        -------
        The median value in that column, skipping any nans
        If col is not in self.headers or that data is categorical, return np.nan
        
        """
        if col not in self.headers:
            return np.nan
        
        col_idx = self.header2col[col]
        col_data = [self.data[i][col_idx] for i in range(self.n)]
        
        # Check if categorical
        for val in col_data:
            if isinstance(val, str):
                return np.nan
            
        # Filter out NaN values
        valid_data = []
        for val in col_data:
            if not (isinstance(val, float) and math.isnan(val)):
                valid_data.append(val)
        
        if len(valid_data) == 0:
            return np.nan
        
        # Sort the data
        sorted_data = sorted(valid_data)
        n = len(sorted_data)
        
        # Find median
        if n % 2 == 1:
            # Odd number of elements
            return sorted_data[n // 2]
        else:
            # Even number of elements - average the two middle values
            return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
        
    def filter_data(self, col, condition, value):
        """
        Create a new Data object containing only rows that meet a condition.
        
        Parameters
        ----------
        col : Column to filter on
        condition : One of '==', '!=', '>', '<', '>=', '<='
        value : Value to compare against
        
        Returns
        -------
        New Data object with filtered rows
        
        Example: nba.filter_data('Position', '==', 'PG') returns only point guards
        """
        if col not in self.headers:
            print("Error: Column not found")
            return None
        
        col_idx = self.header2col[col]
        filtered_rows = []
        
        for i in range(self.n):
            val = self.data[i][col_idx]
            
            # Handle NaN
            if isinstance(val, float) and math.isnan(val):
                continue
            
            # Apply condition
            keep = False
            if condition == '==':
                keep = (val == value)
            elif condition == '!=':
                keep = (val != value)
            elif condition == '>':
                if not isinstance(val, str):
                    keep = (val > value)
            elif condition == '<':
                if not isinstance(val, str):
                    keep = (val < value)
            elif condition == '>=':
                if not isinstance(val, str):
                    keep = (val >= value)
            elif condition == '<=':
                if not isinstance(val, str):
                    keep = (val <= value)
            
            if keep:
                filtered_rows.append(self.data[i])
        
        # Create new Data object
        new_data = Data()
        new_data.headers = self.headers.copy()
        new_data.m = self.m
        new_data.n = len(filtered_rows)
        new_data.data = filtered_rows
        new_data.header2col = self.header2col.copy()
        
        return new_data

if __name__ == "__main__":
    print("---------\nTesting read method and constructor on Simple Data\n---------")
    test = Data("simpletest.csv")
    print("n correct?: ", test.n==2)
    print("m correct?: ", test.m==3)
    print("Checking data[1][2]: ", test.data[1][2]==77.9)
    print("Checking headers: ", test.headers[1]=="Starbucks")
    print("Checking header2col: ", test.header2col["Starbucks"] == 1)

    
    
    print("---------\nTesting read method and constructor on Missing Data\n---------")
    test.read("missingdata.csv")
    print("Proper Nan in missingdata?: ", np.isnan(test.data[1][2]))
    print("Other entries still floats?: ", not np.isnan(test.data[0][2]))
  
    
    print("---------\nTesting String Method on Small Dataset\n---------")
    print("You should see something that looks like this: ")
    template_str = """
Data: 2 samples, 3 features.
Taco Bell     Starbucks     overall lifespan     
-------------------------------
2.8     1.8     74.9     
2.1     6.6     77.9     
-------------------------------
    """
    print("\n" + template_str)
    
    
    print("Your solution: \n")
    
    test = Data("simpletest.csv") 
    
    print(test)
    
        
    print("---------\nTesting String Method on Large Dataset\n---------")
    test = Data("foodandlifespan.csv") 
    print("You should see something that looks like this: ")
    template_str = """
Data: 50 samples, 4 features.
State     Taco Bell     Starbucks     overall lifespan     
-------------------------------
Showing first 5/50 rows.
AL     2.8     1.8     74.9     
AK     2.1     6.6     77.9     
AZ     2.5     7.3     79.2     
AR     3.5     2.0     75.4     
CA     2.1     7.4     81.0     
-------------------------------
    """
    print("\n" + template_str)
    
    
    print("Your solution: \n")
    
    
    print(test)

    print("---------\nTesting head\n---------")        
    
    h=test.head()
    print("Length should be 5: ", len(h)==5)
    print("Last element should begin with CA: ", h[-1][0]=="CA")
    
    test = Data("simpletest.csv") 
    h=test.head()
    print("Length should be 2: ", len(h)==2)
    print("Last element should begin with 2.1: ", h[-1][0]==2.1)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        