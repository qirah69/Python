import csv
import matplotlib.pyplot as plt
import os
from datetime import datetime
import random
import time


headers = {
    "species": 0,
    "flipper_length_mm": 1,
    "culmen_length_mm": 2,
    "culmen_depth_mm": 3,
    "body_mass_g": 4,
    "island": 5,
    "sex": 6
}
numeric_indices = [1, 2, 3, 4]
# Custom exceptions
class PenguinError(Exception):
    """Base class for penguin app errors."""
    pass

class ColumnNotFoundError(PenguinError):
    pass

class MissingArgumentError(PenguinError):
    pass

class InvalidNumberError(PenguinError):
    pass

class NotNumericColumnError(PenguinError):
    pass

class InvalidOrderError(PenguinError):
    pass

class InvalidOptionError(PenguinError):
    pass

class FileMissingError(PenguinError):
    pass

class PlotError(PenguinError):
    pass

def merge(left,right,attribute_index, reverse=False):
    """Merge two sorted lists into one sorted list by the given attribute index.

    Handles numeric and non-numeric attributes and respects the `reverse` flag.
    Returns a new merged list without modifying the contract of the callers.
    """
    if len(left) == 0:
        return right
    if len(right) == 0:
        return left

    merged = []
    while left and right:
        if attribute_index in numeric_indices:
            val_left = float(left[0][attribute_index])
            val_right = float(right[0][attribute_index])
            if (not reverse and float(val_left) <= float(val_right)) or (reverse and float(val_left) >= float(val_right)):
                merged.append(left.pop(0))
            else:
                merged.append(right.pop(0))
        else:
            if (not reverse and left[0][attribute_index] <= right[0][attribute_index]) or (reverse and left[0][attribute_index] >= right[0][attribute_index]):
                merged.append(left.pop(0))
            else:
                merged.append(right.pop(0))
    return merged + left + right
            
def merge_sort(data, attribute_index, reverse=False):
    """Sort `data` using merge sort by the field at `attribute_index`.

    `reverse` controls ascending/descending order. Returns a new sorted list.
    """
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid], attribute_index, reverse)
    right = merge_sort(data[mid:], attribute_index, reverse)

    return merge(left, right, attribute_index, reverse)

def print_data(command_list, data):
    """Return a list of CSV filenames in the current directory.

    This function does not perform any printing; the UI is responsible for
    presenting the returned filenames to the user.
    """
    files = []
    for file in os.listdir('.'):
        if file.endswith('.csv'):
            files.append(file)
    return files

def load_file_content(filename):
    """Reads the CSV and returns the list of rows."""
    new_data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader) # Skip header
        for row in reader:
            new_data.append(row)
    return new_data

def filter_data(command_list, data):
    """Return rows from `data` matching the filter specified in `command_list`.

    Expects `command_list` like: ['filter', '<column>', '<value>'] and returns a list
    of matching rows. Raises custom PenguinError subclasses for invalid input.

    Time complexity: O(n) where n is the number of rows (substring checks may
    add additional cost proportional to field lengths).
    Space complexity: O(k) where k is the number of matching rows (worst-case O(n)).
    """
    # Validate arguments
    if len(command_list) < 3:
        raise MissingArgumentError("Please provide a column and value to filter by (e.g., 'filter species Adelie')")
    if command_list[1] not in headers:
        raise ColumnNotFoundError("That column does not exist. Try again.")
    col_index = headers[command_list[1]]
    target_value = command_list[2]
    filtered_data = []

    for row in data:
        if col_index in numeric_indices:
            try:
                if float(row[col_index]) > float(target_value):
                    filtered_data.append(row)
            except ValueError:
                # signal invalid numeric filter to UI
                raise InvalidNumberError("Please provide a valid number for filtering.")
        else:
            if target_value in row[col_index]:
                filtered_data.append(row)
    return filtered_data

def describe_data(command_list, data):
    """Return (min, max, average) for a numeric column specified in `command_list`.

    Returns None if no valid numeric values are present. Raises custom exceptions
    for missing or non-numeric columns.

    Time complexity: O(n) where n is the number of rows scanned.
    Space complexity: O(m) where m is the number of numeric values collected
    (worst-case O(n)).
    """
    if len(command_list) < 2:
        raise MissingArgumentError("Please provide a column to describe (e.g., 'describe body_mass_g')")
    if command_list[1] not in headers:
        raise ColumnNotFoundError("That column does not exist. Try again.")
    col_index = headers[command_list[1]]
    if col_index not in numeric_indices:
        raise NotNumericColumnError("Description is only available for numeric columns.")
    values = []
    for row in data:
        try:
            values.append(float(row[col_index]))
        except ValueError:
            continue
    if not values:
        return None
    minimum = min(values)
    maximum = max(values)
    average = sum(values) / len(values)
    return minimum, maximum, average

def unique_data(command_list, data):
    """Return a dict of value -> count for the specified column.

    Raises a PenguinError subclass if the column is missing.

    Time complexity: O(n) where n is the number of rows.
    Space complexity: O(u) where u is the number of unique values (<= n).
    """
    if len(command_list) < 2:
        raise MissingArgumentError("Please provide a column to check uniqueness for (e.g., 'unique species')")
    if command_list[1] not in headers:
        raise ColumnNotFoundError("That column does not exist. Try again.")
    col_index = headers[command_list[1]]
    unique_values = {}
    for row in data:
        value = row[col_index]
        unique_values[value] = unique_values.get(value, 0) + 1
    return unique_values

def sort_data(command_list, data):
    """Return (sorted_data, elapsed_seconds) after sorting by the specified column.

    Validates arguments and raises custom exceptions for missing column or invalid order.
    """
    if len(command_list) < 2:
        raise MissingArgumentError("Please provide a column and order to sort by (e.g., 'sort body_mass_g asc')")
    if command_list[1] not in headers:
        raise ColumnNotFoundError("That column does not exist. Try again.")
    if len(command_list) <= 2 or command_list[2] not in ('asc', 'desc'):
        raise InvalidOrderError("Please specify 'asc' or 'desc' for sorting order.")
    col_index = headers[command_list[1]]
    is_reverse = (command_list[2] == 'desc')
    start_time = time.time()
    sorted_data = merge_sort(data, col_index, is_reverse)
    end_time = time.time()
    elapsed = end_time - start_time
    return sorted_data, elapsed

def augment_data(command_list, data):
    """Augment dataset either by duplicating existing rows or creating synthetic ones.

    Returns (data, num_added, action). Raises PenguinError subclasses for invalid input.
    """
    if len(command_list) < 3:
        raise MissingArgumentError("Please enter one of the following options: duplicate or create")
    action = command_list[2]
    try:
        percent = int(command_list[1])
    except Exception:
        raise InvalidNumberError("Please provide a valid percentage.")
    num_to_add = int(len(data) * (percent / 100))

    if action == 'duplicate':
        for _ in range(num_to_add):
            data.append(random.choice(data))
        return data, num_to_add, 'duplicate'
    elif action == 'create':
        blueprint = {}
        for header in range(len(headers)):
            if header in numeric_indices:
                blueprint[header] = [float('inf'), float('-inf')]
            else:
                blueprint[header] = set()
        for row in data:
            for header in range(len(headers)):
                if header in numeric_indices:
                    blueprint[header][0] = min(blueprint[header][0], float(row[header]))
                    blueprint[header][1] = max(blueprint[header][1], float(row[header]))
                else:
                    blueprint[header].add(row[header])
        for _ in range(num_to_add):
            new_row = []
            for header in range(len(headers)):
                if header in numeric_indices:
                    min_val, max_val = blueprint[header]
                    new_value = random.uniform(min_val, max_val)
                    new_row.append(new_value)
                else:
                    new_value = random.choice(list(blueprint[header]))
                    new_row.append(new_value)
            data.append(new_row)
        return data, num_to_add, 'create'
    else:
        raise InvalidOptionError("Unknown augment option. Please use 'duplicate' or 'create'.")

def scatter_data(command_list, data):
    """Return two lists (x_values, y_values) prepared for plotting.

    Validates arguments and raises appropriate PenguinError exceptions on error.
    """
    if len(command_list) < 3:
        raise MissingArgumentError("Please provide two numeric columns to plot (e.g., 'scatter flipper_length_mm body_mass_g').")
    if command_list[1] not in headers or command_list[2] not in headers:
        raise ColumnNotFoundError("One or both of the specified columns do not exist.")
    if headers[command_list[1]] not in numeric_indices or headers[command_list[2]] not in numeric_indices:
        raise NotNumericColumnError("Both columns must be numeric to create a scatter plot.")
    idx = headers[command_list[1]]
    idy = headers[command_list[2]]
    x_values = []
    y_values = []
    for row in data:
        try:
            x_val = float(row[idx])
            y_val = float(row[idy])
            x_values.append(x_val)
            y_values.append(y_val)
        except ValueError:
            continue
    return x_values, y_values

def hist_data(command_list, data):
    """Return values and bin count for a histogram.

    Validates the input and raises PenguinError subclasses for invalid arguments.
    """
    if len(command_list) < 3:
        raise MissingArgumentError("Please provide two numeric columns to plot (e.g., 'hist flipper_length_mm body_mass_g').")
    if command_list[1] not in headers:
        raise ColumnNotFoundError("One or both of the specified columns do not exist.")
    if headers[command_list[1]] not in numeric_indices:
        raise NotNumericColumnError("Both columns must be numeric to create a histogram.")
    if not command_list[2].isdigit():
        raise InvalidNumberError("Bin count must be an integer.")
    values = []
    for row in data:
        try:
            val = float(row[headers[command_list[1]]])
            values.append(val)
        except ValueError:
            continue
    bins = int(command_list[2])
    return values, bins

def boxplot_data(command_list, data):
    """Prepare grouped numeric values for a categorical boxplot.

    Returns a dict mapping category label -> list of numeric values. Raises
    PenguinError subclasses for invalid input.
    """
    if len(command_list) < 3:
        raise MissingArgumentError("Please provide a categorical column and a numeric column to plot (e.g., 'boxplot species body_mass_g').")
    if command_list[1] not in headers:
        raise ColumnNotFoundError("The specified column does not exist.")
    if command_list[2] not in headers:
        raise ColumnNotFoundError("The specified column does not exist.")
    if headers[command_list[2]] not in numeric_indices:
        raise NotNumericColumnError("The column must be numeric to create a boxplot.")
    groups = {}
    for row in data:
        try:
            value = float(row[headers[command_list[2]]])
            label = row[headers[command_list[1]]]
            groups.setdefault(label, []).append(value)
        except ValueError:
            continue
    return groups

def generate_penguin_ascii():
    """Return a random penguin ASCII art string."""
    return """
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠉⠁⠀⠀⠀⠀⠉⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⣤⡈⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠒⠢⡀⠀⠀⠀⠀⠀⠀⠐⠒⢄⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⡔⠉⠉⢢⠈⠀⠀⠀⢠⠚⠉⠉⠓⡄⠑⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⢠⣾⢿⣄⡇⠀⠀⠀⡇⣰⡾⢿⣷⡘⡄⠀⠀⠀⠀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⡿⠁⠀⢻⡃⢀⡀⢠⣷⡏⠀⠀⢹⣷⡇⠀⠀⠀⠀⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⡇⠀⠀⣼⠓⢉⣈⡚⠻⢇⠀⠀⢨⣿⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢿⡤⢈⣴⣞⣽⣷⣬⣿⣤⣅⡐⢾⠋⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢠⠊⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡦⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠐⠰⣯⣿⣿⣿⣿⣿⣿⣿⠟⣡⣿⣿⠅⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢰⡀⢠⣉⣉⣉⣉⣭⣤⣾⡿⣋⣥⣦⠀⠀⠀⠘⣦⡀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⣸⣿⣦⡉⠟⠻⠛⠻⢉⣴⣾⣿⣿⣿⣧⠀⠀⠀⠘⠃⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⡿⢱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⢀⡀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⣰⠀⠀⢿⠿⠟⢛⣉⣩⣭⡥⢁⣴⣶⣶⣶⣶⣤⣤⣤⣬⣉⣙⠛⠀⠀⠈⠛⣆⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⡼⠁⠀⣠⣴⣾⣿⣿⣿⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠈⢆⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⡼⠁⠀⣼⣿⣿⣿⣿⣿⣿⣿⠇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠘⣆⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⡴⠃⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠸⡄⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣸⠁⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡇⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⡇⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⣰⡇⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢀⡿⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⢱⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⡼⠃⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⡆⢀⣀⣀⠀⢧⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⣀⡼⠛⠛⠻⠶⣄⡀⠀⢰⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⡟⣰⣿⣿⣿⣷⡄⠉⠻⢿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣴⣦⣅⠋⠀⠀⠀⠀⠀⢠⡇⢀⠾⢿⣿⣿⣿⣿⣿
            ⣿⡿⢟⣀⣩⣩⢉⡰⣵⣿⣿⣿⣿⣿⣆⠀⠀⠙⠿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢽⣿⡿⠀⠀⠀⠀⠀⠀⠈⢠⣾⣿⠆⣿⣿⣿⣿⣿
            ⣿⠱⣾⣿⣯⣿⣾⣷⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢘⣿⣷⣂⡀⠀⠀⠀⣀⣴⣾⣿⣿⡆⣿⣿⣿⣿⣿
            ⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⣿⣳⡽⣎⡷⣯⢿⣿⣿⣿⣿⣷⣌⠻⣿⣿⣿
            ⣿⣌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣬⡛⢿
            ⣿⣇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡤⢤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠠⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡨
            ⡟⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⢐⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⣟⠿⡩⠆⣱
            ⢰⡹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣀⠀⠉⠛⠛⠛⠻⠟⠛⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⢌⡿⣿⣿⣿⣿⣿⣿⣿⡿⢿⡹⢎⠱⠃⣌⣠⣴⣿⣿
            ⣤⡉⠧⢛⡜⢯⣛⢿⡻⢿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡱⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⠞⡿⣿⢿⡟⡿⣏⠷⡩⢃⠐⣠⣶⣾⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣶⣤⣬⣆⣉⠣⠙⠲⢩⠛⣽⢻⡟⡿⡝⠶⡉⠄⢠⣶⣾⣶⣿⣿⣿⣿⣷⣾⣶⣶⣶⣤⣤⣤⣀⡀⠀⠨⠑⡍⢎⡙⠲⢉⠂⢁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣬⣀⡡⠘⠁⠉⠐⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣀⠀⠀⠀⠀⠁⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"""

def get_random_fact():
    """Returns a random interesting fact about penguins."""
    facts = [
        "Penguins are flightless birds.",
        "The Emperor Penguin is the tallest species, standing nearly 4 feet tall.",
        "Penguins have a gland above their eye that converts saltwater into freshwater.",
        "Gentoo penguins are the fastest swimmers, reaching speeds of 22 mph.",
        "Penguins modify their vision to see clearly both in and out of water.",
        "Penguins undergo 'catastrophic molt', losing all their feathers at once.",
        "The smallest species is the Little Blue Penguin, which is only about 16 inches tall.",
        "Their black and white color is called countershading; it camouflages them from predators above and below.",
        "Male Adélie and Gentoo penguins offer pebbles to females as a proposal for mating.",
        "Emperor penguin males incubate the egg for two months in the freezing cold while the female hunts.",
        "King Penguin chicks look so different from adults they were once thought to be a different species called 'Woolly Penguins'.",
        "Penguins spend about 75% of their lives in the water.",
        "Penguins do not have teeth; instead, they have backward-facing fleshy spines lining their throats.",
        "Almost all penguin species live in the Southern Hemisphere.",
        "The Galápagos Penguin is the only species found north of the equator."
    ]
    return random.choice(facts)