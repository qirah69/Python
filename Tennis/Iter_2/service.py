# =============================================================================
# DOMAIN
# Functions to access and manipulate player data
# =============================================================================
from domain import *

def copy_player_list(player_list):
    new_list = [] 
    for player in player_list:
        new_list.append(player.copy())
    return new_list

def find_player_by_name(player_list, name):
    # Defensive: if name is None or empty, there's nothing to search for.
    try:
        name_norm = str(name).strip().lower()
    except Exception:
        return None
    if name_norm == "":
        return None

    for player in player_list:
        try:
            if get_name(player).lower() == name_norm:
                return player
        except Exception:
            # Skip malformed player entries
            continue
    return None

def add_player(player_list, name, nationality, points, tournaments):
    if find_player_by_name(player_list, name):
        raise ValueError(f"Player {name} already exists. Please try again!")
    new_list = copy_player_list(player_list)
    new_player = create_player(name, nationality, points, tournaments)
    new_list.append(new_player)
    return new_list

def modify_player_info(player_list, name, new_points, new_tournaments):
    new_list = copy_player_list(player_list)

    player_to_modify = find_player_by_name(new_list, name)
    if not player_to_modify:
        raise ValueError(f"Player {name} was not found. Please try again!")
    set_points(player_to_modify, new_points)
    set_tournaments(player_to_modify, new_tournaments)
    return new_list

def remove_players_from_country(player_list, country):
    """Return a new list with all players whose nationality != country.

    Raises ValueError if no players were removed (i.e., there were no players
    from the provided country).
    """
    if not player_list:
        return []

    new_list = []
    removed = 0
    for p in player_list:
        if get_nationality(p).lower() == country.lower():
            removed += 1
            continue
        new_list.append(p.copy())

    if removed == 0:
        raise ValueError(f"No players from country '{country}' were found.")

    return new_list

def remove_players_by_points_interval(player_list, min_points, max_points):
    """Return a new list with players whose points are NOT in [min_points, max_points].

    Raises ValueError if no players were removed (i.e., no players fell inside the interval).
    """
    if not player_list:
        return []

    new_list = []
    removed = 0
    for p in player_list:
        try:
            pts = int(get_points(p))
        except Exception:
            # if points can't be parsed, keep the player
            new_list.append(p.copy())
            continue

        if min_points <= pts <= max_points:
            removed += 1
            continue
        new_list.append(p.copy())

    if removed == 0:
        raise ValueError(f"No players with points in interval [{min_points}, {max_points}] were found.")

    return new_list

def search_players_by_country_and_points_div_by_number(player_list, country, number):
    """Return a list of players from the specified country whose points are divisible by number."""
    if not player_list:
        return "No players available."
    
    result_list = []
    for p in player_list:
        if get_nationality(p).lower() == country.lower() and get_points(p) % number == 0:
            result_list.append(p)
    return result_list

def search_players_by_country_and_min_points(player_list, country, min_points):
    """Return a list of players from the specified country whose points are greater than min_points."""
    if not player_list:
        return "No players available."

    result_list = []
    for p in player_list:
        if get_nationality(p).lower() == country.lower() and get_points(p) > min_points:
            result_list.append(p)
    return result_list

def search_players_by_tournaments(player_list, min_tournaments, max_points):
    """Return a list of players who have played more than min_tournaments and have points less than max_points."""
    if not player_list:
        return "No players available."

    result_list = []
    for p in player_list:
        if get_tournaments(p) > min_tournaments and get_points(p) < max_points:
            result_list.append(p)
    return result_list

#==============================================================================
#Tests
#==============================================================================
def test_service():
    players = []
    players = add_player(players, "Player1", "CountryA", 1000, 10)
    players = add_player(players, "Player2", "CountryB", 1500, 15)
    assert len(players) == 2

    players = modify_player_info(players, "Player1", 1100, 12)
    p1 = find_player_by_name(players, "Player1")
    assert get_points(p1) == 1100
    assert get_tournaments(p1) == 12

    players = remove_players_from_country(players, "CountryA")
    assert len(players) == 1
    assert get_name(players[0]) == "Player2"

    players = remove_players_by_points_interval(players, 1400, 1600)
    assert len(players) == 0
