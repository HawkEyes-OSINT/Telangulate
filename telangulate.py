from colorama import Fore
from triangulate import get_coordinates
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from config import getconfig
import asyncio
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
        return None
    if not pattern.match(cod[0]) or not pattern.match(cod[1]):
        raise ValueError("Invalid format")
        return None
    
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
    print(Fore.WHITE + "1. Find users from a list of locations")
    print(Fore.WHITE + "2. Enter single location to search")
    print(Fore.WHITE + "3. Exit")

    choice = input(Fore.WHITE + "Enter your choice: ")

    # get coordinates from list in csv
    if choice == "1":
        try:
            coordinates = cords_fromlist()
        except ValueError as e:
            print(Fore.RED + str(e))
            return ui()
        except FileNotFoundError:
            print(Fore.RED + "File not found")
            return ui()
        except Exception as e:
            print(Fore.RED + str(e))
            exit(0)

    # get coordinates from user input
    elif choice == "2":
        try:
            coordinates = [cord_fromuser()]
        except ValueError as e:
            print(Fore.RED + str(e))
            return ui()
        except Exception as e:
            print(Fore.RED + str(e))
            exit(0)

    # exit program
    elif choice == "3":
        print(Fore.GREEN + "Exiting program...")
        exit(0)

    # invalid input
    else:
        print(Fore.RED + "Invalid input")
        return ui()
    
    return coordinates


async def main():
    # create client session
    print('[+] Creating Telegram client session')
    config = getconfig()
    client = TelegramClient('session', config['api_id'], config['api_hash'])
    await client.start(config['phone'])
    if not client.is_user_authorized():
        client.send_code_request(config['phone'])
        try:
            client.sign_in(config['phone'], input('Enter the code: '))
        except SessionPasswordNeededError: # 2FA auth
            client.sign_in(phone=config['phone'], password=input('Enter 2FA password: '))
        except Exception as e:
            print('[-] ' + e)
            exit(0)
    print('[+] Client session created')
    cordinates = ui()

    # get users from each coordinate
    for cord in cordinates:
        # get cordinates to the north, east and south
        cords = get_coordinates(cord)

        # get users from each coordinate


if __name__ == "__main__":
    asyncio.run(main())