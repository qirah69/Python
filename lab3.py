#Proprietatea P este P4
#Proprietatea R este R4

menu_text = """1. Read a list of integer numbers.
2. Find sublist where the difference between any 2 consecutive elements from the sublist is a prime number.
3. Remove elements that contain the digit 0 (when written in base 10).
4. Print current list.
5. Exit."""

def read_list():
    #Function to read the elements of the list
    global lst
    lst = [int(num) for num in input("Enter your numbers: ").split()]

def is_prime(n):
    #Function to find if the number is prime 
    #Prime numbers are greater than 1
    if n <= 1:
        return False
    # 2 is the only even prime number.
    if n == 2:
        return True
    # All other even numbers are not prime.
    if n % 2 == 0:
        return False
    # Check for odd divisors from 3 up to the square root of n.
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def longest_list():
    #Function to determine the longest sublist
    #Eliminate case where the list has no elem/one elem
    if not lst:
        longest_sublist = []
    elif len(lst) == 1:
        longest_sublist = lst
    #Initiate current and longest sublists
    else:
        longest_sublist = [lst[0]]
        current_sublist = [lst[0]]
        #Generate the current sublist using the given property
        for i in range (1,len(lst)):
            dif = abs(lst[i]-lst[i-1])
            if is_prime(dif):
                current_sublist.append(lst[i])
            else:
                if len(current_sublist) >= len(longest_sublist):
                    longest_sublist = current_sublist
                #Re-Initiate the current sublist
                current_sublist = [lst[i]]
        #Check if last sublist is the longest
        if len(current_sublist) >= len(longest_sublist):
            longest_sublist = current_sublist
    print(f"Longest sublist is: {longest_sublist}")
    print()
 
def remove_elem():
    # Create a new list containing only the numbers we want to keep.
    numbers_to_keep = [num for num in lst if '0' not in str(num)]
    # Replace the contents of the original list with the filtered list.
    lst[:] = numbers_to_keep

#Main menu 
while True:
    print(menu_text)
    option = input("Choose an option: ")
    if option.isdigit():
        option = int(option)
    print()
    match option:
        case 1: 
            read_list() 
        case 2: 
            longest_list()
        case 3:
            remove_elem()
        case 4:
            print(lst)
            print()
        case 5:
            break
        case _:
            print("!NOT AN OPTION!")
            print("Please choose again!")
