import csv
import os
from datetime import datetime
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

def merge(left,right,attribute_index, reverse=False):
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
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid], attribute_index, reverse)
    right = merge_sort(data[mid:], attribute_index, reverse)

    return merge(left, right, attribute_index, reverse)

option = ''
while True:
    option = input("Enter an option: ")
    command_list = option.split()
    
    # Check if the list isn't empty before looking inside
    if len(command_list) > 0:
        match command_list[0]:
            case 'print':
                try:
                    files = os.listdir(".")
                    for file in files:
                        if file.endswith(".csv"):
                            print(file)
                except Exception as e:
                    print(f"An error occurred: {e}")
            case 'load':
                try:
                    data = []
                    # command_list[1] is the filename the user typed
                    with open(command_list[1], 'r') as file:
                        reader = csv.reader(file)
                        
                        # Skip the header row so we don't load text into our data
                        next(reader) 
                        
                        # Add every other row to our main list
                        for row in reader:
                            data.append(row)
                            
                    print(f"Loaded {len(data)} penguins successfully!")
                    
                except FileNotFoundError:
                    print("Could not find that file. Check the spelling!")
                except IndexError:
                    print("Please provide a filename (e.g., 'load penguins_data.csv')")

            case 'filter':
                try:
                    col_index = headers[command_list[1]]  # e.g., gets 0 for "species"
                    target_value = command_list[2]        # e.g., gets "Adelie"
                    filtered_data = []

                    for row in data:
                        if col_index in numeric_indices:
                            try:
                                if float(row[col_index]) > float(target_value):
                                    filtered_data.append(row)
                            except ValueError:
                                print("Please provide a valid number for filtering.")
                                break
                        else:
                            if target_value in row[col_index]:
                                filtered_data.append(row)

                    save_choice = input("Would you like to save the filtered data? (y/n): ").strip().lower()
                    if save_choice == 'y':
                        filename = input("Enter a filename to save to (e.g., results.csv): ")
                        if not filename.endswith(".csv"):
                            filename += ".csv"
                        with open(filename, 'w') as file:
                            writer = csv.writer(file)
                            writer.writerows(filtered_data)
                        print(f"Successfully saved to {filename}")
                        
                    elif save_choice == 'n':
                        print(f"Found {len(filtered_data)} matching penguins:")
                        for row in filtered_data[:5]:
                            print(row)
                
                except KeyError:
                    print("That column does not exist. Try again.")
                except IndexError:
                    print("Please provide a column and value to filter by (e.g., 'filter species Adelie')")

            case 'describe':
                try:
                    col_index = headers[command_list[1]]
                    if col_index in numeric_indices:
                        values = []
                        for row in data:
                            try:
                                values.append(float(row[col_index]))
                            except ValueError:
                                continue
                        if values:
                            minimum = min(values)
                            maximum = max(values)
                            average = sum(values) / len(values)
                            print(f"Description for {command_list[1]}:")
                            print(f"  Min: {minimum}")
                            print(f"  Max: {maximum}")
                            print(f"  Average: {average:.2f}")
                    else:
                        print("Description is only available for numeric columns.")
                except KeyError:
                    print("That column does not exist. Try again.")

            case 'unique':
                try:
                    col_index = headers[command_list[1]]
                    unique_values = dict()
                    for row in data:
                        value = row[col_index]
                        if value not in unique_values:
                            unique_values[value] = 0
                        unique_values[value] += 1

                    print(f"Unique values for {command_list[1]}:")  
                    for value, count in unique_values.items():
                        print(f"  {value}: {count}")

                except KeyError:
                    print("That column does not exist. Try again.")

            case 'sort':
                try:
                    col_index = headers[command_list[1]]
                    
                    if command_list[2] == 'asc':
                        is_reverse = False
                    elif command_list[2] == 'desc':
                        is_reverse = True
                    else:
                        print("Please specify 'asc' or 'desc' for sorting order.")
                        continue 
                    
                    start_time = time.time()
                    
                    sorted_data = merge_sort(data, col_index, is_reverse)
                    end_time = time.time()
                   
                    data = sorted_data

                    now = datetime.now()
                    date_str = now.strftime("%Y-%m-%d")
                    time_str = now.strftime("%H:%M:%S")
                    
                    with open('sorting_log.txt', 'a') as log_file:
                        log_file.write(f"{date_str},{time_str},{len(sorted_data)},Merge Sort,{end_time-start_time:.6f}\n")
                    
                    print(f"Successfully sorted by {command_list[1]} ({command_list[2]}).")

                except KeyError:
                    print("That column does not exist. Try again.")
                except IndexError:
                    print("Please provide a column and order to sort by (e.g., 'sort body_mass_g asc')")

            case 'quit':
                print("Exiting the program. Goodbye!")
                break

            case _ :
                print("Unknown command.")