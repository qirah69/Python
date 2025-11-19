import os

# =============================================================================
# DOMAIN
# Functions to create and access player data
# =============================================================================

def create_player(name, nationality, points, tournaments):
    """
    Creates a new player as a dictionary.
    """
    return {
        'name': name,
        'nationality': nationality,
        'points': points,
        'tournaments': tournaments
    }

def get_name(player):
    return player['name']

def get_nationality(player):
    return player['nationality']

def get_points(player):
    return player['points']

def get_tournaments(player):
    return player['tournaments']

def set_points(player, new_points):
    player['points'] = new_points

def set_tournaments(player, new_tournaments):
    player['tournaments'] = new_tournaments

def to_str(player):
    """
    Returns a string representation of a player.
    """
    return (f"{get_name(player)}, {get_nationality(player)}, "
            f"{get_points(player)} points, {get_tournaments(player)} tournaments")

# =============================================================================
# SERVICE
# Functions that implement the application's logic
# =============================================================================

def _copy_player_list(player_list):
    """
    Creates a new list containing copies of each player dictionary.
    This is a "manual deep copy" of the list for undo.
    """
    new_list = []
    for player in player_list:
        new_list.append(player.copy()) # .copy() creates a shallow copy of the dict
    return new_list

def save_state(history_stack, player_list):
    """
    Saves a copy of the current player list to the history stack.
    Each player dictionary in the saved list is also a copy.
    """
    history_stack.append(_copy_player_list(player_list))

def service_undo(history_stack):
    """
    Reverts to the previous state from the history stack.
    Returns the previous player list.
    Raises ValueError if there is no state to undo.
    """
    if not history_stack:
        raise ValueError("No more operations to undo.")
    return history_stack.pop()

def find_player_by_name(player_list, name):
    """
    Finds and returns a player dictionary by name.
    Returns None if not found.
    """
    for player in player_list:
        if get_name(player).lower() == name.lower():
            return player
    return None

# --- 1. Add and modify players ---

def service_add_player(player_list, name, nationality, points, tournaments):
    """
    Adds a new player to the list.
    Returns a new list containing the added player.
    Raises ValueError if a player with the same name already exists.
    """
    if find_player_by_name(player_list, name):
        raise ValueError(f"Player '{name}' already exists.")
    
    new_list = _copy_player_list(player_list) # Create a new list for modifications
    new_player = create_player(name, nationality, points, tournaments)
    new_list.append(new_player)
    return new_list

def service_modify_player(player_list, name, new_points, new_tournaments):
    """
    Modifies an existing player's points and tournaments.
    Returns a new list with the modified player.
    Raises ValueError if the player is not found.
    """
    new_list = _copy_player_list(player_list) # Work on a copy of the list
    
    # Find the player in the *new_list* to modify
    player_to_modify = find_player_by_name(new_list, name)
    
    if not player_to_modify:
        raise ValueError(f"Player '{name}' not found.")
        
    set_points(player_to_modify, new_points)
    set_tournaments(player_to_modify, new_tournaments)
    return new_list

# --- 2. Remove players ---

def service_remove_by_country(player_list, country):
    """
    Removes all players from a given country.
    Returns a new list without the removed players.
    """
    # Create a new list for the filtered results
    new_list = [p.copy() for p in player_list if get_nationality(p).lower() != country.lower()]
    return new_list

def service_remove_by_points_interval(player_list, min_pts, max_pts):
    """
    Removes all players with points within the inclusive interval [min_pts, max_pts].
    Returns a new list without the removed players.
    """
    if min_pts > max_pts:
        raise ValueError("Minimum points cannot be greater than maximum points.")
    
    # Create a new list for the filtered results
    new_list = [p.copy() for p in player_list if not (min_pts <= get_points(p) <= max_pts)]
    return new_list

# --- 3. Display players (non-modifying, so return existing list or copies if sorting) ---

def service_get_by_country_divisible_points(player_list, country, divisor):
    """
    Finds players from a country with points divisible by a number.
    Returns a new list of found players (copies of originals).
    """
    if divisor == 0:
        raise ValueError("Cannot divide by zero.")
    return [p.copy() for p in player_list
            if get_nationality(p).lower() == country.lower() 
            and get_points(p) % divisor == 0]

def service_get_by_country_min_points(player_list, country, min_pts):
    """
    Finds players from a country with points greater than a number.
    Returns a new list of found players (copies of originals).
    """
    return [p.copy() for p in player_list 
            if get_nationality(p).lower() == country.lower() 
            and get_points(p) > min_pts]

def service_get_by_tournaments_and_points(player_list, min_tourns, max_pts):
    """
    Finds players with > min_tourns and < max_pts.
    Returns a new list of found players (copies of originals).
    """
    return [p.copy() for p in player_list 
            if get_tournaments(p) > min_tourns 
            and get_points(p) < max_pts]

# --- 4. Reports (non-modifying) ---

def service_report_total_tournaments(player_list, country):
    """
    Calculates the total tournaments won by players from a given country.
    """
    total = 0
    for p in player_list:
        if get_nationality(p).lower() == country.lower():
            total += get_tournaments(p)
    return total

def service_report_players_per_country(player_list):
    """
    Counts the number of players from each country.
    Returns a dictionary of {country: count}.
    """
    counts = {}
    for p in player_list:
        nat = get_nationality(p)
        counts[nat] = counts.get(nat, 0) + 1
    return counts

def service_report_by_name_substring(player_list, substring):
    """
    Finds players whose name contains a substring, sorted by points (desc).
    Returns a new list of found players (copies of originals), sorted.
    """
    # Create copies of players to sort, so we don't modify the original list
    found_players = [p.copy() for p in player_list if substring.lower() in get_name(p).lower()]
    return sorted(found_players, key=get_points, reverse=True)

def service_report_top_3_by_tournaments(player_list):
    """
    Returns the top 3 players sorted by tournaments won (desc).
    Returns a new list of found players (copies of originals), sorted and sliced.
    """
    # Create copies of players to sort, so we don't modify the original list
    sorted_players = sorted([p.copy() for p in player_list], key=get_tournaments, reverse=True)
    return sorted_players[:3]

# --- 5. Filtering (Removal) ---

def service_filter_countries_and_points(player_list, countries, max_pts):
    """
    Removes players from a list of countries who have < max_pts.
    Returns a new filtered list.
    """
    countries_lower = [c.strip().lower() for c in countries]
    new_list = [
        p.copy() for p in player_list 
        if not (get_nationality(p).lower() in countries_lower and get_points(p) < max_pts)
    ]
    return new_list

def service_filter_tournaments_and_points(player_list, min_tourns, min_pts):
    """
    Removes players with < min_tourns AND < min_pts.
    Returns a new filtered list.
    """
    new_list = [
        p.copy() for p in player_list 
        if not (get_tournaments(p) < min_tourns and get_points(p) < min_pts)
    ]
    return new_list

# =============================================================================
# TESTS
# Functions to test the Domain and Service layers
# =============================================================================

def test_create_player():
    player = create_player("Test Player", "Testland", 1000, 5)
    assert get_name(player) == "Test Player"
    assert get_nationality(player) == "Testland"
    assert get_points(player) == 1000
    assert get_tournaments(player) == 5
    print("test_create_player passed.")

def test_set_points():
    player = create_player("Test Player", "Testland", 1000, 5)
    set_points(player, 1200)
    assert get_points(player) == 1200
    print("test_set_points passed.")

def test_set_tournaments():
    player = create_player("Test Player", "Testland", 1000, 5)
    set_tournaments(player, 7)
    assert get_tournaments(player) == 7
    print("test_set_tournaments passed.")

def test_service_add_player():
    players = []
    # Test adding a player
    new_players = service_add_player(players, "P1", "C1", 1000, 5)
    assert len(new_players) == 1
    assert get_name(new_players[0]) == "P1"
    # Test adding another player
    new_players2 = service_add_player(new_players, "P2", "C2", 2000, 10)
    assert len(new_players2) == 2
    assert get_name(new_players2[1]) == "P2"
    # Test adding existing player (should raise ValueError)
    try:
        service_add_player(new_players2, "P1", "C1", 1000, 5)
        assert False, "ValueError was not raised for existing player."
    except ValueError as e:
        assert str(e) == "Player 'P1' already exists."
    # Ensure original list is unchanged
    assert len(players) == 0
    print("test_service_add_player passed.")

def test_service_modify_player():
    players = [create_player("P1", "C1", 1000, 5)]
    # Test modifying existing player
    modified_players = service_modify_player(players, "P1", 1500, 7)
    assert get_points(modified_players[0]) == 1500
    assert get_tournaments(modified_players[0]) == 7
    # Ensure original list is unchanged
    assert get_points(players[0]) == 1000
    # Test modifying non-existent player
    try:
        service_modify_player(players, "NonExistent", 2000, 10)
        assert False, "ValueError was not raised for non-existent player."
    except ValueError as e:
        assert str(e) == "Player 'NonExistent' not found."
    print("test_service_modify_player passed.")

def test_service_remove_by_country():
    players = [
        create_player("P1", "C1", 1000, 5),
        create_player("P2", "C2", 2000, 10),
        create_player("P3", "C1", 1500, 7)
    ]
    # Remove by country
    filtered_players = service_remove_by_country(players, "C1")
    assert len(filtered_players) == 1
    assert get_name(filtered_players[0]) == "P2"
    # Ensure original list is unchanged
    assert len(players) == 3
    # Remove non-existent country
    filtered_players2 = service_remove_by_country(players, "C3")
    assert len(filtered_players2) == 3
    print("test_service_remove_by_country passed.")

def test_service_remove_by_points_interval():
    players = [
        create_player("P1", "C1", 1000, 5),
        create_player("P2", "C2", 2000, 10),
        create_player("P3", "C1", 1500, 7),
        create_player("P4", "C3", 500, 2)
    ]
    # Remove players with points in [1000, 1500]
    filtered_players = service_remove_by_points_interval(players, 1000, 1500)
    assert len(filtered_players) == 2
    assert get_name(filtered_players[0]) == "P2"
    assert get_name(filtered_players[1]) == "P4"
    # Ensure original list is unchanged
    assert len(players) == 4
    # Test invalid interval
    try:
        service_remove_by_points_interval(players, 2000, 1000)
        assert False, "ValueError was not raised for invalid interval."
    except ValueError as e:
        assert str(e) == "Minimum points cannot be greater than maximum points."
    print("test_service_remove_by_points_interval passed.")

def test_service_get_by_country_divisible_points():
    players = [
        create_player("P1", "C1", 1000, 5), # Yes (1000 % 100 == 0)
        create_player("P2", "C2", 2000, 10),
        create_player("P3", "C1", 150, 7),  # Yes (150 % 100 != 0, but 150 % 50 == 0)
        create_player("P4", "C1", 200, 2)   # Yes (200 % 100 == 0)
    ]
    result = service_get_by_country_divisible_points(players, "C1", 100)
    assert len(result) == 2
    assert get_name(result[0]) == "P1"
    assert get_name(result[1]) == "P4"

    result2 = service_get_by_country_divisible_points(players, "C1", 50)
    assert len(result2) == 3 # P1, P3, P4
    assert get_name(result2[0]) == "P1"
    assert get_name(result2[1]) == "P3"
    assert get_name(result2[2]) == "P4"

    try:
        service_get_by_country_divisible_points(players, "C1", 0)
        assert False, "ValueError not raised for divisor 0"
    except ValueError as e:
        assert str(e) == "Cannot divide by zero."
    print("test_service_get_by_country_divisible_points passed.")

def test_service_get_by_country_min_points():
    players = [
        create_player("P1", "C1", 1000, 5),
        create_player("P2", "C2", 2000, 10),
        create_player("P3", "C1", 1500, 7)
    ]
    result = service_get_by_country_min_points(players, "C1", 1200)
    assert len(result) == 1
    assert get_name(result[0]) == "P3"
    print("test_service_get_by_country_min_points passed.")

def test_service_get_by_tournaments_and_points():
    players = [
        create_player("P1", "C1", 1000, 5), # No (>5 tournaments needed)
        create_player("P2", "C2", 2000, 10), # No (<1500 points needed)
        create_player("P3", "C1", 1200, 8),  # Yes
        create_player("P4", "C3", 1000, 6)   # Yes
    ]
    result = service_get_by_tournaments_and_points(players, 5, 1500)
    assert len(result) == 2
    assert get_name(result[0]) == "P3"
    assert get_name(result[1]) == "P4"
    print("test_service_get_by_tournaments_and_points passed.")

def test_service_report_total_tournaments():
    players = [
        create_player("P1", "C1", 1000, 5),
        create_player("P2", "C2", 2000, 10),
        create_player("P3", "C1", 1500, 7)
    ]
    total = service_report_total_tournaments(players, "C1")
    assert total == 12 # 5 + 7
    total_none = service_report_total_tournaments(players, "C3")
    assert total_none == 0
    print("test_service_report_total_tournaments passed.")

def test_service_report_players_per_country():
    players = [
        create_player("P1", "C1", 1000, 5),
        create_player("P2", "C2", 2000, 10),
        create_player("P3", "C1", 1500, 7)
    ]
    counts = service_report_players_per_country(players)
    assert counts == {"C1": 2, "C2": 1}
    print("test_service_report_players_per_country passed.")

def test_service_report_by_name_substring():
    players = [
        create_player("Alice", "C1", 1000, 5),
        create_player("Bob", "C2", 2000, 10),
        create_player("Charlie", "C1", 1500, 7),
        create_player("Rob", "C3", 500, 2)
    ]
    result = service_report_by_name_substring(players, "b")
    assert len(result) == 2
    assert get_name(result[0]) == "Bob" # Bob (2000 pts) comes before Rob (500 pts)
    assert get_name(result[1]) == "Rob"
    print("test_service_report_by_name_substring passed.")

def test_service_report_top_3_by_tournaments():
    players = [
        create_player("P1", "C1", 1000, 5),
        create_player("P2", "C2", 2000, 10),
        create_player("P3", "C1", 1500, 7),
        create_player("P4", "C3", 500, 12),
        create_player("P5", "C4", 3000, 8)
    ]
    result = service_report_top_3_by_tournaments(players)
    assert len(result) == 3
    assert get_name(result[0]) == "P4" # 12 tournaments
    assert get_name(result[1]) == "P2" # 10 tournaments
    assert get_name(result[2]) == "P5" # 8 tournaments
    print("test_service_report_top_3_by_tournaments passed.")

def test_service_filter_countries_and_points():
    players = [
        create_player("P1", "Spain", 8000, 10), # Keep (points >= 5000)
        create_player("P2", "Italy", 4000, 5),  # Remove (Italy, points < 5000)
        create_player("P3", "Spain", 3000, 3),  # Remove (Spain, points < 5000)
        create_player("P4", "France", 2000, 2), # Keep (not Spain/Italy)
        create_player("P5", "Italy", 6000, 8)   # Keep (points >= 5000)
    ]
    countries = ["Spain", "Italy"]
    max_pts = 5000
    filtered_players = service_filter_countries_and_points(players, countries, max_pts)
    assert len(filtered_players) == 3
    assert get_name(filtered_players[0]) == "P1"
    assert get_name(filtered_players[1]) == "P4"
    assert get_name(filtered_players[2]) == "P5"
    print("test_service_filter_countries_and_points passed.")

def test_service_filter_tournaments_and_points():
    players = [
        create_player("P1", "C1", 1000, 5),  # Keep (points >= 700)
        create_player("P2", "C2", 500, 3),   # Remove (tournaments < 4 AND points < 700)
        create_player("P3", "C1", 800, 2),   # Keep (points >= 700)
        create_player("P4", "C3", 600, 5)    # Keep (tournaments >= 4)
    ]
    filtered_players = service_filter_tournaments_and_points(players, 4, 700) # Remove if <4 tournaments AND <700 points
    assert len(filtered_players) == 3
    assert get_name(filtered_players[0]) == "P1"
    assert get_name(filtered_players[1]) == "P3"
    assert get_name(filtered_players[2]) == "P4"
    print("test_service_filter_tournaments_and_points passed.")

def test_undo_functionality():
    history_stack = []
    players = []

    # Add P1, P2
    players1 = service_add_player(players, "P1", "C1", 100, 1)
    save_state(history_stack, players) # Save []
    players = players1
    assert len(players) == 1
    assert len(history_stack) == 1

    players2 = service_add_player(players, "P2", "C2", 200, 2)
    save_state(history_stack, players) # Save [P1]
    players = players2
    assert len(players) == 2
    assert len(history_stack) == 2

    # Modify P1
    players3 = service_modify_player(players, "P1", 150, 3)
    save_state(history_stack, players) # Save [P1, P2]
    players = players3
    assert get_points(players[0]) == 150
    assert len(history_stack) == 3

    # Undo 1: Revert to [P1 (original), P2]
    players = service_undo(history_stack)
    assert len(players) == 2
    assert get_points(players[0]) == 100 # P1 should be original points
    assert get_name(players[0]) == "P1"
    assert get_name(players[1]) == "P2"
    assert len(history_stack) == 2

    # Undo 2: Revert to [P1 (original)]
    players = service_undo(history_stack)
    assert len(players) == 1
    assert get_name(players[0]) == "P1"
    assert len(history_stack) == 1

    # Undo 3: Revert to []
    players = service_undo(history_stack)
    assert len(players) == 0
    assert len(history_stack) == 0

    # Try undoing when empty
    try:
        service_undo(history_stack)
        assert False, "ValueError was not raised for undo on empty stack."
    except ValueError as e:
        assert str(e) == "No more operations to undo."
    
    print("test_undo_functionality passed.")

def run_all_tests():
    print("--- Running All Tests ---")
    test_create_player()
    test_set_points()
    test_set_tournaments()
    test_service_add_player()
    test_service_modify_player()
    test_service_remove_by_country()
    test_service_remove_by_points_interval()
    test_service_get_by_country_divisible_points()
    test_service_get_by_country_min_points()
    test_service_get_by_tournaments_and_points()
    test_service_report_total_tournaments()
    test_service_report_players_per_country()
    test_service_report_by_name_substring()
    test_service_report_top_3_by_tournaments()
    test_service_filter_countries_and_points()
    test_service_filter_tournaments_and_points()
    test_undo_functionality()
    print("--- All Tests Passed! ---")

# =============================================================================
# UI (CONSOLE)
# Functions for printing menus and handling user input
# =============================================================================

def print_menu():
    """
    Displays the main menu.
    """
    print("\n--- Tennis Player Manager ---")
    print("1. Add/Modify Players")
    print("   1a. Add new player")
    print("   1b. Modify existing player (points, tournaments)")
    print("2. Remove Players")
    print("   2a. Delete all players from a country")
    print("   2b. Delete all players with points in an interval")
    print("3. Display Players")
    print("   3a. Print players from a country (points divisible by N)")
    print("   3b. Print players from a country (points > N)")
    print("   3c. Print players (tournaments > N, points < M)")
    print("4. Reports")
    print("   4a. Total tournaments won for a country")
    print("   4b. Number of players from each country")
    print("   4c. Players with name containing substring (sorted by points)")
    print("   4d. Top 3 players (sorted by tournaments won)")
    print("5. Filtering (Remove)")
    print("   5a. Eliminate (countries list, points < N)")
    print("   5b. Eliminate (tournaments < N, points < M)")
    print("6. Undo")
    print("   6. Undo last modifying operation")
    print("-----------------------------")
    print("   all. Show all players")
    print("   x. Exit")

def ui_print_players(player_list, header="--- Player List ---"):
    """
    Prints a list of players with a header.
    """
    if not player_list:
        print(f"\n{header}\nNo players found.")
        return
        
    print(f"\n{header}")
    for player in player_list:
        print(to_str(player))

# --- UI for 1. Add/Modify ---

def ui_add_player(player_list):
    name = input("Enter name: ").strip()
    nationality = input("Enter nationality: ").strip()
    points = int(input("Enter ATP ranking points: ")) # Input validation done by int() and ValueError
    tournaments = int(input("Enter tournaments won: "))
    
    if not name or not nationality:
        raise ValueError("Name and nationality cannot be empty.")
    if points < 0 or tournaments < 0:
        raise ValueError("Points and tournaments cannot be negative.")
        
    return service_add_player(player_list, name, nationality, points, tournaments)

def ui_modify_player(player_list):
    name = input("Enter name of player to modify: ").strip()
    new_points = int(input("Enter new ranking points: "))
    new_tournaments = int(input("Enter new tournaments won: "))

    if new_points < 0 or new_tournaments < 0:
        raise ValueError("Points and tournaments cannot be negative.")

    return service_modify_player(player_list, name, new_points, new_tournaments)

# --- UI for 2. Remove ---

def ui_remove_by_country(player_list):
    country = input("Enter country to remove: ").strip()
    return service_remove_by_country(player_list, country)

def ui_remove_by_points(player_list):
    min_pts = int(input("Enter minimum points of interval: "))
    max_pts = int(input("Enter maximum points of interval: "))
    return service_remove_by_points_interval(player_list, min_pts, max_pts)

# --- UI for 3. Display ---

def ui_display_country_divisible(player_list):
    country = input("Enter country: ").strip()
    divisor = int(input("Enter divisor: "))
    result = service_get_by_country_divisible_points(player_list, country, divisor)
    ui_print_players(result, f"Players from {country} with points divisible by {divisor}")

def ui_display_country_min_points(player_list):
    country = input("Enter country: ").strip()
    min_pts = int(input("Enter minimum points (greater than): "))
    result = service_get_by_country_min_points(player_list, country, min_pts)
    ui_print_players(result, f"Players from {country} with more than {min_pts} points")

def ui_display_tourns_points(player_list):
    min_tourns = int(input("Enter minimum tournaments won (greater than): "))
    max_pts = int(input("Enter maximum points (less than): "))
    result = service_get_by_tournaments_and_points(player_list, min_tourns, max_pts)
    ui_print_players(result, f"Players with > {min_tourns} tournaments and < {max_pts} points")

# --- UI for 4. Reports ---

def ui_report_total_tournaments(player_list):
    country = input("Enter country: ").strip()
    total = service_report_total_tournaments(player_list, country)
    print(f"\nTotal tournaments won for {country}: {total}")

def ui_report_players_per_country(player_list):
    counts = service_report_players_per_country(player_list)
    print("\n--- Players per Country ---")
    if not counts:
        print("No players in the list.")
    for country, count in counts.items():
        print(f"{country}: {count} player(s)")

def ui_report_by_name_substring(player_list):
    substring = input("Enter name substring: ").strip()
    result = service_report_by_name_substring(player_list, substring)
    ui_print_players(result, f"Players with '{substring}' in name (sorted by points)")

def ui_report_top_3_by_tournaments(player_list):
    result = service_report_top_3_by_tournaments(player_list)
    ui_print_players(result, "Top 3 Players (by Tournaments Won)")

# --- UI for 5. Filtering ---

def ui_filter_countries_points(player_list):
    countries_str = input("Enter countries to filter (comma-separated): ")
    countries = [c.strip() for c in countries_str.split(',') if c.strip()] # Clean and remove empty strings
    if not countries:
        raise ValueError("No countries entered for filtering.")
    max_pts = int(input("Enter maximum points (less than): "))
    return service_filter_countries_and_points(player_list, countries, max_pts)

def ui_filter_tourns_points(player_list):
    min_tourns = int(input("Enter minimum tournaments (fewer than): "))
    min_pts = int(input("Enter minimum points (fewer than): "))
    return service_filter_tournaments_and_points(player_list, min_tourns, min_pts)
    
# --- Utility ---

def add_initial_data(player_list):
    """
    Populates the list with sample data for testing.
    """
    # NOTE: This function creates new player dictionaries.
    # If it were to modify an existing player_list passed in,
    # it would need to use _copy_player_list and ensure new copies of players
    # are added, or it would break the undo functionality.
    return [
        create_player("Carlos Alcaraz", "Spain", 8535, 12),
        create_player("Novak Djokovic", "Serbia", 8980, 98),
        create_player("Lorenzo Musetti", "Italy", 2650, 5),
        create_player("Casper Ruud", "Norway", 4235, 10),
        create_player("Rafael Nadal", "Spain", 10083, 96)
    ]

# --- UI Helper Functions ---

def clear_screen():
    """
    Clears the terminal screen.
    """
    if os.name == 'nt': # for windows
        _ = os.system('cls')
    else: # for mac and linux(here, os.name is 'posix')
        _ = os.system('clear')

def pause_for_user():
    """
    Pauses execution and waits for the user to press Enter.
    """
    input("\nPress Enter to continue...")

# =============================================================================
# MAIN APPLICATION LOOP
# =============================================================================

def main():
    run_all_tests() # Run all tests once at startup
    print("\nStarting application...")
    pause_for_user() # Pause after tests before main menu

    player_list = add_initial_data([])
    history_stack = []

    display_commands = {
        '3a': ui_display_country_divisible,
        '3b': ui_display_country_min_points,
        '3c': ui_display_tourns_points,
        '4a': ui_report_total_tournaments,
        '4b': ui_report_players_per_country,
        '4c': ui_report_by_name_substring,
        '4d': ui_report_top_3_by_tournaments,
        'all': ui_print_players,
    }
    
    modify_commands = {
        '1a': (ui_add_player, "Player added."),
        '1b': (ui_modify_player, "Player modified."),
        '2a': (ui_remove_by_country, "Players removed."),
        '2b': (ui_remove_by_points, "Players removed."),
        '5a': (ui_filter_countries_points, "Players filtered."),
        '5b': (ui_filter_tourns_points, "Players filtered."),
    }

    while True:
        clear_screen()
        print_menu()
        choice = input("Enter your choice: ").strip().lower()

        try:
            if choice == 'x':
                print("Exiting application. Goodbye!")
                break
            
            elif choice in display_commands:
                if choice == 'all':
                    display_commands[choice](player_list, "== All Players ==")
                else:
                    display_commands[choice](player_list)
                pause_for_user()
            
            elif choice in modify_commands:
                ui_function, success_message = modify_commands[choice]
                
                # Call the UI function, which calls the service function
                # The service function returns a NEW list (with copied players)
                new_list = ui_function(player_list)
                
                if new_list != player_list: # Check if the list reference changed
                    save_state(history_stack, player_list) # Save the *current* state before updating
                    player_list = new_list # Update to the new state
                    print(success_message)
                else:
                    print("No changes were made (e.g., player not found or no players matched criteria).")
                
                pause_for_user()

            elif choice == '6': # Undo operation
                # We don't save state *before* undo, as undo itself is retrieving a past state
                players_before_undo = _copy_player_list(player_list) # Keep a copy in case undo fails
                player_list = service_undo(history_stack)
                # No need to save_state(history_stack, players_before_undo) because undo goes backward,
                # it doesn't add a new state.
                print("Undo successful. Reverted to previous state.")
                pause_for_user()

            else:
                print("Invalid choice. Please try again.")
                pause_for_user()

        except ValueError as e:
            print(f"Error: {e}")
            pause_for_user()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            pause_for_user()

# Run the application
if __name__ == "__main__":
    main()
