from domain import to_str
from service import (
    add_player,
    modify_player_info,
    remove_players_from_country,
    remove_players_by_points_interval,
    search_players_by_country_and_points_div_by_number,
    search_players_by_country_and_min_points,
    search_players_by_tournaments
)

def show_menu():
    print("Select an option:")
    print("1. Add player")
    print("2. Modify player")
    print("3. Remove player based on criteria" )
    print("4. List players based on criteria")
    print("0. Exit")

def run():
    player_list = []
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        try:
            match choice:
                case "0":
                    print("Exiting the program.")
                    break
                case "1":
                    name = input("Enter player name: ")
                    nationality = input("Enter player nationality: ")
                    try:
                        points = int(input("Enter player points: "))
                        tournaments = int(input("Enter number of tournaments played: "))
                    except ValueError:
                        print("Error: Points and tournaments must be integers.")
                        continue
                    try:
                        player_list = add_player(player_list, name, nationality, points, tournaments)
                        print("Player added successfully.")
                    except ValueError as ve:
                        print(f"Error: {ve}")
                case "2":
                    if not player_list:
                        print("No players available to modify.")
                        continue
                    name = input("Enter player name to modify: ")
                    try:
                        new_points = int(input("Enter new points: "))
                        new_tournaments = int(input("Enter new number of tournaments played: "))
                    except ValueError:
                        print("Error: Points and tournaments must be integers.")
                        continue
                    try:
                        player_list = modify_player_info(player_list, name, new_points, new_tournaments)
                        print("Player information updated successfully.")
                    except ValueError:
                        print(f"Error: The player '{name}' does not exist.")
                case "4":
                    if not player_list:
                        print("No players available to display.")
                        continue
                    print("Display players by criteria:")
                    print("1. Display by country and points divisibility")
                    print("2. Display by country and points greater than a value")
                    print("3. Display by more tournaments won than a value, but points less than a value")
                    try:
                        type_of_display = int(input("Select display type (1-3): "))
                    except ValueError:
                        print("Error: Please enter a valid integer for display type.")
                        continue
                    match type_of_display:
                        case 1:
                            country = input("Enter country: ")
                            try:
                                number = int(input("Enter number for divisibility check: "))
                            except ValueError:
                                print("Error: Please enter a valid integer for divisibility check.")
                                continue
                            try:
                                result = search_players_by_country_and_points_div_by_number(player_list, country, number)
                                if not player_list or not result:
                                    print("No players found matching the criteria.")
                                else:
                                    for p in result:
                                        print(to_str(p))
                            except ValueError as ve:
                                print(f"Error: {ve}")
                        case 2:
                            country = input("Enter country: ")
                            try:
                                min_points = int(input("Enter minimum points: "))
                            except ValueError:
                                print("Error: Please enter a valid integer for minimum points.")
                                continue
                            try:
                                result = search_players_by_country_and_min_points(player_list, country, min_points)
                                if not result:
                                    print("No players found matching the criteria.")
                                else:
                                    for p in result:
                                        print(to_str(p))
                            except ValueError as ve:
                                print(f"Error: {ve}")
                        case 3:
                            try:
                                min_tournaments = int(input("Enter minimum tournaments played: "))
                                max_points = int(input("Enter maximum points: "))
                            except ValueError:
                                print("Error: Please enter valid integers for tournaments and points.")
                                continue
                            try:
                                result = search_players_by_tournaments(player_list, min_tournaments, max_points)
                                if not result:
                                    print("No players found matching the criteria.")
                                else:
                                    for p in result:
                                        print(to_str(p))
                            except ValueError as ve:
                                print(f"Error: {ve}")
                        case _:
                            print("Invalid display type selected.")
                case _:
                    print("Invalid option. Please select a valid menu option.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            