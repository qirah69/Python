# =============================================================================
# Services
# Functions to manage player data
# =============================================================================
from domain import *

def copy_player_list(player_list):
    new_list = [] 
    for player in player_list:
        new_list.append(player.copy())
    return new_list

def find_player_by_name(player_list, name):
    for player in player_list:
        if get_name(player).lower() == name.lower():
            return player
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

