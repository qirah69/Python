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

def load_data(command_list, data):
    """Placeholder for load operation.

    Actual file I/O is intentionally performed in the UI loop so that
    the computational functions remain side-effect-free.
    """
    # File reading is handled in the UI loop; keep this as a no-op placeholder to avoid breaking references.
    return data

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


if __name__ == "__main__":
    option = ''
    data = []
    while True:
        option = input("Enter an option: ")
        command_list = option.split()
        
        # Check if the list isn't empty before looking inside
        if len(command_list) > 0:
            match command_list[0]:
                # UI: list CSV files in the current directory
                case 'print':
                    files = print_data(command_list, data)
                    for file in files:
                        print(file)
                
                # UI: load CSV file into memory (performs I/O)
                case 'load':
                    try:
                        if len(command_list) < 2:
                            raise MissingArgumentError("Please provide a filename (e.g., 'load penguins_data.csv')")
                        data = []
                        with open(command_list[1], 'r') as file:
                            reader = csv.reader(file)
                            next(reader)
                            for row in reader:
                                data.append(row)
                        print(f"Loaded {len(data)} penguins successfully!")
                    except FileNotFoundError:
                        print(FileMissingError("Could not find that file. Check the spelling!"))
                    except PenguinError as e:
                        print(str(e))

                # UI: filter data and optionally save results (I/O performed in UI)
                case 'filter':
                    try:
                        filtered = filter_data(command_list, data)
                        save_choice = input("Would you like to save the filtered data? (y/n): ").strip().lower()
                        if save_choice == 'y':
                            filename = input("Enter a filename to save to (e.g., results.csv): ")
                            if not filename.endswith(".csv"):
                                filename += ".csv"
                            with open(filename, 'w') as file:
                                writer = csv.writer(file)
                                writer.writerows(filtered)
                            print(f"Successfully saved to {filename}")
                        elif save_choice == 'n':
                            print(f"Found {len(filtered)} matching penguins:")
                            for row in filtered[:5]:
                                print(row)
                    except PenguinError as e:
                        print(str(e))

                # UI: compute and print descriptive stats (I/O in UI)
                case 'describe':
                    try:
                        res = describe_data(command_list, data)
                        if res is not None:
                            minimum, maximum, average = res
                            print(f"Description for {command_list[1]}:")
                            print(f"  Min: {minimum}")
                            print(f"  Max: {maximum}")
                            print(f"  Average: {average:.2f}")
                    except PenguinError as e:
                        print(str(e))

                # UI: print unique value counts for a column
                case 'unique':
                    try:
                        uniq = unique_data(command_list, data)
                        print(f"Unique values for {command_list[1]}:")
                        for value, count in uniq.items():
                            print(f"  {value}: {count}")
                    except PenguinError as e:
                        print(str(e))

                # UI: sort dataset and log timing (I/O performed in UI)
                case 'sort':
                    try:
                        sorted_data, elapsed = sort_data(command_list, data)
                        data = sorted_data
                        now = datetime.now()
                        date_str = now.strftime("%Y-%m-%d")
                        time_str = now.strftime("%H:%M:%S")
                        with open('sorting_log.txt', 'a') as log_file:
                            log_file.write(f"{date_str},{time_str},{len(sorted_data)},Merge Sort,{elapsed:.6f}\n")
                        print(f"Successfully sorted by {command_list[1]} ({command_list[2]}).")
                    except PenguinError as e:
                        print(str(e))

                # UI: augment dataset (writes augmented_data.csv)
                case 'augment':
                    try:
                        new_data, num_added, action = augment_data(command_list, data)
                        data = new_data
                        if action == 'duplicate':
                            print(f"Successfully duplicated {num_added} penguins.")
                        else:
                            print(f"Successfully created {num_added} new penguins.")
                        with open('augmented_data.csv', 'w') as file:
                            writer = csv.writer(file)
                            augmented_headers = list(headers.keys())
                            writer.writerow(augmented_headers)
                            writer.writerows(data)
                    except PenguinError as e:
                        print(str(e))

                # UI: prepare and display scatter plot (plotting done here in UI)
                case 'scatter':
                    try:
                        x_vals, y_vals = scatter_data(command_list, data)
                        plt.scatter(x_vals, y_vals)
                        plt.xlabel(command_list[1])
                        plt.ylabel(command_list[2])
                        plt.title(f"Scatter Plot of {command_list[1]} vs {command_list[2]}")
                        plt.show()
                    except PenguinError as e:
                        print(str(e))

                # UI: prepare and display histogram (plotting done here in UI)
                case 'hist':
                    try:
                        values, bins = hist_data(command_list, data)
                        plt.hist(values, bins=bins)
                        plt.title(f"Histogram of {command_list[1]}")
                        plt.grid(True)
                        plt.show()
                    except PenguinError as e:
                        print(str(e))
                                    
                # UI: prepare and display boxplot (plotting done here in UI)
                case 'boxplot':
                    try:
                        groups = boxplot_data(command_list, data)
                        plt.boxplot(groups.values(), tick_labels=groups.keys())
                        plt.title(f"Boxplot of {command_list[2]} by {command_list[1]}")
                        plt.xlabel(command_list[1])
                        plt.ylabel(command_list[2])
                        plt.grid(True)
                        plt.show()
                    except PenguinError as e:
                        print(str(e))

                case 'help':
                    print("Available commands:")
                    print("  print                           - List all CSV files in the current directory")
                    print("  load <filename>                 - Load a CSV file")
                    print("  filter <column> <value>        - Filter data by column and value")
                    print("  describe <column>               - Show min, max, and average for a numeric column")
                    print("  unique <column>                 - Show unique values and their counts for a column")
                    print("  sort <column> <asc|desc>       - Sort data by column in ascending or descending order")
                    print("  augment <percentage> <option>   - Augment data by duplicating or creating new entries")
                    print("  scatter <x_column> <y_column> - Create a scatter plot of two numeric columns")
                    print("  hist <column> <bin_count>         - Create a histogram of a numeric column")
                    print("  boxplot <category_column> <numeric_column> - Create a boxplot of a numeric column grouped by a categorical column")
                    print("  help                            - Show this help message")
                    print("  quit                            - Exit the program")

                case 'quit':
                    print("Exiting the program. Goodbye!")
                    break

                case _ :
                    print("Unknown command.")