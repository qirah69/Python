#Nr problema P2
from domain import to_str
from service import (
    add_player,
    modify_player_info,
    remove_players_from_country,
    remove_players_by_points_interval,
    find_player_by_name,
)


def print_menu():
    print('\n--- Tennis player_listayers menu ---')
    print('1. Add player_listayer')
    print('2. List player_listayers')
    print('3. Modify player_listayer')
    print('4. Remove player_listayers from a country')
    print('5. Remove player_listayers by points interval')
    print('0. Exit')


def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print('Please enter a valid integer.')


def main():
    player_list = []

    while True:
        print_menu()
        choice = input('Choose option: ').strip()

        if choice == '1':
            name = input('Name: ')
            # immediate duplicate check
            if find_player_by_name(player_list, name):
                print(f"Error: Player {name} already exists.")
                continue
            nationality = input('Nationality: ')
            points = read_int('Points: ')
            tournaments = read_int('Tournaments: ')
            try:
                player_list = add_player(player_list, name, nationality, points, tournaments)
                print('Player added.')
            except ValueError as e:
                print('Error:', e)

        elif choice == '2':
            if not player_list:
                print('No player_listayers.')
            else:
                for p in player_list:
                    print(to_str(p))

        elif choice == '3':
            if not player_list:
                print('No player_listayers to modify.')
                continue
            name = input('Name of player_listayer to modify: ')
            new_points = read_int('New points: ')
            new_tournaments = read_int('New tournaments: ')
            try:
                player_list = modify_player_info(player_list, name, new_points, new_tournaments)
                print('Player modified.')
            except ValueError as e:
                print('Error:', e)

        elif choice == '4':
            if not player_list:
                print('No player_listayers.')
                continue
            country = input('Country to remove: ')
            try:
                player_list = remove_players_from_country(player_list, country)
                print(f'Players from {country} removed.')
            except ValueError as e:
                print('Error:', e)

        elif choice == '5':
            if not player_list:
                print('No player_listayers.')
                continue
            min_p = read_int('Min points: ')
            max_p = read_int('Max points: ')
            try:
                player_list = remove_players_by_points_interval(player_list, min_p, max_p)
                print(f'Players with points in [{min_p},{max_p}] removed.')
            except ValueError as e:
                print('Error:', e)

        elif choice == '0':
            print('Goodbye.')
            break

        else:
            print('Unknown option, try again.')


if __name__ == '__main__':
    main()
