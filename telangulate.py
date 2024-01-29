from colorama import Fore
from triangulate import get_coordinates
from telegram import get_userdistances
from triangulate import triangulate_pos
import pyfiglet
import re
import csv

"""
Main file for program execution
"""

def cords_fromlist():
    """
    Get coordinates from file
    :return: list of coordinates
    """
    coordinates = []
    pattern = re.compile(r'^-?\d{2,3}\.\d+$')

    # print instructions
    instruction = """Enter the cordinates in column A of file coordinates.csv in the following format:\nlat, lon"""
    print(Fore.YELLOW + instruction)
    input(Fore.YELLOW + "Press enter to continue...")

    # get coordinates from file
    with open('coordinates.csv', 'r') as file:
        reader = csv.reader(file)

        # verify correct format
        row_num = 1
        for row in reader:
            cod = row
            if len(cod) != 2:
                raise ValueError(f"Invalid format in row {row_num}")
            lat, lon = map(str.strip, cod)
            if not pattern.match(lat) or not pattern.match(lon):
                raise ValueError(f"Invalid format in row {row_num}")
            
            # add to list
            coordinates.append((float(lat), float(lon)))
            row_num += 1

    return coordinates

def cord_fromuser():
    """
    Get coordinates from user input
    :return cordinate: tuple of coordinates (lat, lon)
    """
    pattern = re.compile(r'^-?\d{2,3}\.\d+$')

    # print instructions
    instruction = """Enter the cordinates in the following format:\nlat, lon"""
    print(Fore.YELLOW + instruction)
    cod = input(Fore.YELLOW + "Enter cordinate: ")

    # verify correct format
    cod = cod.replace(' ', '').split(',')
    if len(cod) != 2:
        raise ValueError("Invalid format")
    if not pattern.match(cod[0]) or not pattern.match(cod[1]):
        raise ValueError("Invalid format")
    
    print(Fore.WHITE + "")
    return (float(cod[0]), float(cod[1]))


def ui():
    """
    User interface for the program
    :return: None
    """

    # print title
    title = pyfiglet.figlet_format("Telangulate")
    print(Fore.GREEN + title)

    # get user input
    print(Fore.WHITE + "Please chose an option: ")
    print(Fore.WHITE + "1. Enter single location to search")
    print(Fore.WHITE + "2. Exit")

    choice = input(Fore.WHITE + "Enter your choice: ")


    # get coordinates from user input
    if choice == "1":
        try:
            coordinates = [cord_fromuser()]
        except ValueError as e:
            print(Fore.RED + str(e))
            return ui()
        except Exception as e:
            print(Fore.RED + str(e))
            exit(0)

    # exit program
    elif choice == "2":
        print(Fore.GREEN + "Exiting program...")
        print(Fore.WHITE + "")
        exit(0)

    # invalid input
    else:
        print(Fore.RED + "Invalid input")
        return ui()
    
    return coordinates


def main():
    """
    Main function for program execution
    :return: None
    """
    while True:
        cordinates = ui()

        # get users from each coordinate
        for cord in cordinates:
            # get cordinates to the north, east and south
            print(f"[+] Getting cordinates sorrounding {cord[0]}, {cord[1]}")
            try:
                cords = get_coordinates(cord)
                print(f"[+] Cordinates: {cords}")
            except Exception as e:
                print(f"[-] Error getting sorrounding cordinates for {cord[0]}, {cord[1]}")
                print(f"[-] {e}")
                continue

            # get users from each coordinate
            users_list = get_userdistances(cords)

            # triangulate location
            for user in users_list:
                try:
                    user['LOCATION'] = triangulate_pos(user['LOCATION'])
                    print(f"[+] Triangulated location for: {user['FIRST NAME']}")
                except Exception as e:
                    print(f"[-] Error triangulating location for {user['FIRST NAME']}")
                    print(f"[-] {e}")
                    continue

            # export to csv
            with open('user_list.csv', 'w') as file:
                fieldnames =(users_list[0].keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for user in users_list:
                    writer.writerow(user)

            print(Fore.GREEN + "[+] Exported resutlts to user_list.csv")
            print(Fore.GREEN + "Please move file to desired location before running new point to avoid loss of data")


        # give continuation istructions
        continuation_instructions1 = "Telegram API allows moving declared location 10 meters for every second from previous query"
        continuation_instructions2 = "To run another location, please wait the required time or change your account details in config.csv"

        print(Fore.WHITE + continuation_instructions1)
        print()
        print(Fore.WHITE + continuation_instructions2)

if __name__ == "__main__":
    main()