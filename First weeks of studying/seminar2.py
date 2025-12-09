# Defines a function to display the application's main menu.
def afiseaza_meniu():
    print("1. Adauga melodie la lista/  Add song to list")
    print("2. Cauta melodie dupa titlu si artist / Search song by title and artist")
    print("3. Stergea unui cantec dupa titlu si artist/ Delete song bby title and artist")
    print("P. Afiseaza lista de melodii/ Display song list")
    print("E. Iesire din aplicatie/ Exit application")


# F1: This comment seems to mark a section related to the 'add' functionality, possibly F1 for Functionality 1.
# It's an internal note for organization.

# Defines a function to read the song's information (title, artist, genre, duration) from the user.
# It specifies that it returns a tuple of values.

def citeste_info_melodie() -> tuple:
    # Prompts the user to enter the song's title and stores the input in the 'titlu' variable.
    titlu = input("Introduceti titlul melodiei/ Enter the song title:")
    # Prompts the user to enter the song's artist and stores the input in the 'artist' variable.
    artist = input("Introduceti artist melodiei/ Enter the song artist:")
    # Prompts the user to enter the song's genre and stores the input in the 'gen' variable.
    gen = input("Introduceti genul melodiei/ Enter the song genre:")
    # Prompts the user to enter the song's duration and stores the input in the 'durata' variable.
    durata = input("Introduceti durata melodiei/ Enter the song duration:")
    # Converts the duration input (which is a string) into a floating-point number.
    durata = float(durata)
    # Returns the collected information as a tuple (title, artist, genre, duration).
    return titlu, artist, gen, durata

# Defines a function to create a song object (a dictionary) from the provided details.
def creare_melodie(titlu: str, artist: str, gen: str, durata: float) -> dict:
    # Defines the function's documentation (docstring).
    """
    Creates a song based on the information provided
    :param title: song title
    :param artist: song artist
    :param genre: the genre of the song
    :param duration: the duration of the song
    :return: a dictionary representing the song

    """
    # Returns a new dictionary where keys are the song attributes (title, artist, gen, duratin)
    # and values are the corresponding input parameters.
    return {'titlu': titlu, 'artist': artist, 'gen': gen, 'durata': durata}
    # return [titlu, artist, gen, durata]

# Defines a function to retrieve the title of a song from its dictionary representation.
def get_titlu(melodie: dict):
    # Returns the value associated with the 'titlu' key.
    return melodie['titlu']

# Defines a function to retrieve the artist of a song from its dictionary representation.
def get_artist(melodie: dict):
    # Returns the value associated with the 'artist' key.
    return melodie['artist']

# Defines a function to retrieve the genre of a song from its dictionary representation.
def get_gen(melodie: dict):
    # Returns the value associated with the 'gen' key.
    return melodie['gen']

# Defines a function to retrieve the duration of a song from its dictionary representation.
def get_durata(melodie: dict):
    # Returns the value associated with the 'durata' key.
    return melodie['durata']

# Defines a function to add a song dictionary to the list of songs.
def add_to_list(lst_melodii: list, melodie: dict) -> None:
    """
    Adds the given song to the song list.
    :param song_list: list of songs
    :param song: song to be added
    :return: -; the given list is modified by adding the song to the end of the list
    """
    # Uses the list's built-in 'append' method to add the new song dictionary to the end of the list.
    lst_melodii.append(melodie)


def cauta_melodie(lista_melodii: list, titlu_cautat: str, artist_cautat: str) -> dict:
    """
     Searches for a song in the list by title and artist
    :param song_list: list in which the song is searched
    :param search_title: title searched for
    :param search_artist: artist searched for
    :return: song with the given title and artist, if it exists in the list
             None, otherwise
    """
    # Iterates through each song (dictionary) in the provided list.
    for melodie in lista_melodii:
        # Checks if the current song's title AND artist match the search criteria.
        if get_titlu(melodie) == titlu_cautat and get_artist(melodie) == artist_cautat:
            # If a match is found, returns the song dictionary immediately.
            return melodie
    # If the loop completes without finding a match, no song is returned, implicitly returning None (or we can explicitly return None).


# Defines a function to delete a song from the list based on its title and artist.
def sterge_melodie(lista_melodii: list, titlu: str, artist: str):
    """
   Delete the song with the given title and artist, if it exists in the list
    :param song_list: list of songs from which to delete
    :param title: title of the song to be deleted
    :param artist: artist of the song to be deleted
    :return: -; song_list is modified by deleting the song with the given title and artist,
                if this song exists; otherwise, the list remains unchanged
    """
    # Calls the search function to find the song object that matches the title and artist.
    melodie_cautata = cauta_melodie(lista_melodii, titlu, artist)
    # Checks if the search function returned a song (i.e., not None).
    if melodie_cautata is not None:
        # If the song was found, uses the list's built-in 'remove' method to delete the song object from the list.
        lista_melodii.remove(melodie_cautata)


# Defines a function to display all songs in the list.
def afiseaza_melodii(lista_melodii):
    # Iterates through the list, getting both the index (i) and the song object (song).
    for i, song in enumerate(lista_melodii):
        # end = "": don't jump to new line, end fiind caracterul
        # displayed after the last value to be displayed (by default, end=new line
        # that's why print() usually displays what we give it and then moves to a new line)

        # Prints the song number (index + 1 implicitly, but using i here) followed by ": ", without a newline character at the end.
        print("Melodie #" + str(i) + ": ", end="")
        # we build a string with the information of a song
        # (just for practicing working with str, it can be printed directly)

        # Initializes an empty string to hold the formatted song information.
        song_info = ""

        # Iterates through the key-value pairs (attribute name and value) in the song dictionary.
        for key, value in song.items():
            # Appends the capitalized key, a colon, the value (converted to string), and a separator " | " to the song_info string.
            song_info += key.capitalize() + ": " + str(value) + " | "

        # Prints the final formatted song information string. Since 'end' was used on the previous print, this line starts printing on the same line and then adds a newline.
        print(song_info)

# Defines the main function that runs the application's user interface.
def run():
    # Executes the function containing all the unit tests.
    ruleaza_teste()
    # Initializes an empty list to store the song dictionaries. This is the application's main data structure.
    lista_melodii = []
    # Sets a flag to control the main loop.
    is_running = True

    # Starts the main application loop, which continues as long as 'is_running' is True.
    while is_running:
        # Displays the menu options to the user.
        afiseaza_meniu()
        # Prompts the user for input (>>>), converts it to uppercase, and removes any leading/trailing whitespace.
        optiune = input(">>>").upper().strip()
        # Uses a 'match' statement (Python 3.10+) for elegant handling of menu options.
        match optiune:
            # Case for option '1' (Add song).
            case '1':
                # add la lista
                # F1: Adaugare in lista
                #   T1: citire informatii --done
                #   T2: crearea melodiei pe baza informatii
                #   T3: adaugare in lista
                #   T4: interactiune cu utilizatorul

                # Calls a function to read song details from the user and unpacks the returned tuple into four variables.
                titlu, artist, gen, durata = citeste_info_melodie()
                # Calls a function to create a song dictionary from the gathered details.
                melodie = creare_melodie(titlu, artist, gen, durata)
                # Calls a function to add the newly created song dictionary to the main song list.
                add_to_list(lista_melodii, melodie)

            # Case for option '2' (Search song).
            case '2':
                # cautare in lista / search in list
                # Prompts the user for the title of the song to search for.
                titlu_cautat = input("Titlul melodiei cautate: ")
                # Prompts the user for the artist of the song to search for.
                artist_cautat = input("Artistul melodiei cautate: ")
                # Calls the search function with the list and search criteria.
                melodie_cautata = cauta_melodie(lista_melodii, titlu_cautat, artist_cautat)
                # Checks if the search function returned a song (not None).
                if melodie_cautata is not None:
                    # Prints a success message and the details of the found song.
                    print("Melodia a fost gasita, acestea sunt toate informatiile despre ea:", melodie_cautata)
                else:
                    # Prints a message indicating the song was not found.
                    print("Melodia nu a fost gasita in lista.")

            # Case for option '3' (Delete song).
            case '3':
                # stergere din lista / delete from list
                # Prompts the user for the title of the song to delete.
                titlu_de_sters = input("Titlul melodiei de sters:")
                # Prompts the user for the artist of the song to delete.
                artist_de_sters = input("Artistul melodiei de sters: ")
                # Calls the function to attempt to delete the song from the list.
                sterge_melodie(lista_melodii, titlu_de_sters, artist_de_sters)
                # how to check if something was deleted to display a success message
                # or a message that the song was not found in the list?

            # Case for option 'P' (Print/Display list).
            case 'P':
                # Calls the function to display all songs in the current list.
                afiseaza_melodii(lista_melodii)

            # Case for option 'E' (Exit).
            case 'E':
                # Sets the running flag to False, which will terminate the 'while' loop.
                is_running = False


# Defines a unit test function for the 'creare_melodie' function.
def test_creare_melodie():
    # melodie_de_test1 = {'titlu': 'T1', 'artist': 'A1', 'gen': 'folk', 'durata': 3.40}
    # Calls the function under test and stores the resulting song dictionary.
    melodie1 = creare_melodie('T1', 'A1', 'folk', 3.40)
    # Assertion: Checks if the title retrieved from the created song matches the expected value.
    assert (get_titlu(melodie1) == "T1")
    # Assertion: Checks if the artist retrieved from the created song matches the expected value.
    assert (get_artist(melodie1) == "A1")
    # Assertion: Checks if the genre retrieved from the created song matches the expected value.
    assert (get_gen(melodie1) == "folk")
    # Assertion: Checks if the duration retrieved from the created song matches the expected value.
    assert (get_durata(melodie1) == 3.40)


# Defines a unit test function for the 'add_to_list' function.
def test_add_to_list():
    # Initializes an empty list for testing.
    test_list = []
    # Assertion: Checks that the list is initially empty.
    assert (len(test_list) == 0)
    # Adds the first song to the list.
    add_to_list(test_list, creare_melodie('T1', 'A1', 'folk', 3.40))
    # Assertion: Checks that the list now contains one item.
    assert (len(test_list) == 1)

    # Adds a second song to the list.
    add_to_list(test_list, creare_melodie('T2', 'A2', 'rock', 4.02))
    # Assertion: Checks that the list now contains two items.
    assert (len(test_list) == 2)


# Defines a unit test function for the 'cauta_melodie' (search song) function.
def test_cauta_in_lista():
    # Initializes an empty list.
    test_list = []
    # Creates three song dictionaries to populate the list.
    melodie1 = creare_melodie("T1", "A1", "pop", 2.37)
    melodie2 = creare_melodie("T2", "A2", "rock", 2.21)
    melodie3 = creare_melodie("Thunderstruck", "AC/DC", "rock", 3.45)
    # Adds the songs to the test list.
    add_to_list(test_list, melodie1)
    add_to_list(test_list, melodie2)
    add_to_list(test_list, melodie3)

    # Assertion: Checks if searching for 'T1' and 'A1' correctly returns 'melodie1'.
    assert (cauta_melodie(test_list, "T1", "A1") == melodie1)
    # Assertion: Checks if searching for a non-existent song returns None.
    assert (cauta_melodie(test_list, "Highway to Hell", "AC/DC") is None)
    # Assertion: Checks that the search is case-sensitive (lowercase input fails to find uppercase match).
    assert (cauta_melodie(test_list, "t1", "a1") is None)
    # the test for swapped title/artist. inversat artist cu titlu
    # Assertion: Checks that swapping title and artist fails to find the song.
    assert (cauta_melodie(test_list, "A1", "T1") is None)


# Defines a unit test function for the 'sterge_melodie' (delete song) function.
def test_stergere_din_lista():
    # Creates three song dictionaries.
    melodie1 = creare_melodie("T1", "A1", "pop", 2.37)
    melodie2 = creare_melodie("T2", "A2", "rock", 2.21)
    melodie3 = creare_melodie("Thunderstruck", "AC/DC", "rock", 3.45)
    # Initializes an empty list.
    test_list = []
    # Adds all three songs to the list.
    add_to_list(test_list, melodie1)
    add_to_list(test_list, melodie2)
    add_to_list(test_list, melodie3)

    # Assertion: Checks that the list has 3 songs.
    assert (len(test_list) == 3)
    # Deletes the first song ('T1', 'A1').
    sterge_melodie(test_list, "T1", "A1")
    # Assertion: Checks that the list now has 2 songs.
    assert (len(test_list) == 2)
    # Attempts to delete a song that is not in the list.
    sterge_melodie(test_list, "Titlu", "Artist")
    # Assertion: Checks that the list size remains 2 (deletion failed).
    assert (len(test_list) == 2)
    # Deletes the second song ('T2', 'A2').
    sterge_melodie(test_list, "T2", "A2")
    # Assertion: Checks that the list now has 1 song.
    assert (len(test_list) == 1)
    # Deletes the last song ('Thunderstruck', 'AC/DC').
    sterge_melodie(test_list, "Thunderstruck", "AC/DC")
    # Assertion: Checks that the list is now empty.
    assert (len(test_list) == 0)

    # Initializes a second empty list to test deletion on an empty list.
    test_list2 = []
    # Assertion: Checks that the list is initially empty.
    assert (len(test_list2) == 0)
    # Attempts to delete a song from the empty list.
    sterge_melodie(test_list2, "T1", "A1")
    # Assertion: Checks that the list remains empty.
    assert (len(test_list2) == 0)

# Defines a function to run all the defined unit tests.
def ruleaza_teste():
    # Executes the test for creating a song.
    test_creare_melodie()
    # Executes the test for adding to the list.
    test_add_to_list()
    # Executes the test for searching in the list.
    test_cauta_in_lista()
    # Executes the test for deleting from the list.
    test_stergere_din_lista()
    # Prints a confirmation message if all tests passed (i.e., no assertion failed).
    print("[INFO]: Au trecut toate testele")

# The main execution point of the script: calls the 'run' function to start the application.
run()

