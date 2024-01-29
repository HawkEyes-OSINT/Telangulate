from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from config import getconfig
from telethon.tl import functions, types
from tqdm import tqdm
import asyncio
import time 


def _wait(seconds):
    """
    Wait for the specified number of seconds.
    :param seconds: The number of seconds to wait.
    :type seconds: int
    :return: None
    :rtype: None
    """

    print()
    print(f"[!] API {seconds} seconds wait to change location")
    for _ in tqdm(range(seconds), desc="Progress", bar_format="{l_bar}{bar}{r_bar}", colour="green", ncols=80):
        time.sleep(1)
    print()

def _get_client(session_name):
    """
    Create a Telegram client session.
    :param session_name: The name of the session.
    :type session_name: str
    :return: The Telegram client session.
    :rtype: TelegramClient
    """

    # create client session
    print('[+] Creating Telegram client session')
    config = getconfig()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(session_name, config['api_id'], config['api_hash'],
                            device_model='A320MH', app_version='2.1.4a',
                            system_version='WIndows 10', lang_code='en', system_lang_code='fr-FR', loop=loop)
    client.connect()
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

    return client


def _get_users(client, coordinate):
    """
    Get users at the specified coordinate.
    :param client: The Telegram client session.
    :type client: TelegramClient
    :param coordinate: The coordinate to get users at.
    :type coordinate: list
    :return: The list of users at the specified coordinate.
    :rtype: list
    """

    output = []
    try:
        result = client(functions.contacts.GetLocatedRequest(
        geo_point=types.InputGeoPoint(
                lat=coordinate[0],
                long=coordinate[1],
            ),
        ))

        # get additional data for users
        for user in result.users:
            for distance_data in result.updates[0].peers:
                try:
                    if user.id == distance_data.peer.user_id:
                        output.append({
                            'ALIAS': user.username,
                            'FIRST NAME': user.first_name,
                            'LAST NAME': user.last_name,
                            'URL': f'https://t.me/{user.username}',
                            'ID': user.id,
                            'PHONE': user.phone,
                            'LOCATION': [{
                                'cord': coordinate,
                                'distance': distance_data.distance
                            }]
                        })
                        break
                except Exception as e:
                    continue

    except Exception as e:
        print(f'[-] Could not get users at {coordinate[0]}, {coordinate[1]}')
        print(e)
        client.disconnect()
        return []
    
    print(f'[+] Users at {coordinate[0]}, {coordinate[1]} found')
    
    return output


def _merge_lists(user_lists):
    """
    Merge the lists of users.
    :param user_lists: The lists of users to merge.
    :type user_lists: list
    :return: The merged list of users.
    :rtype: list
    """

    merged_list = []
    holder_list = user_lists.pop(0)

    for user_list in user_lists:
        for user in user_list:
            for holder_user in holder_list:
                if user['ID'] == holder_user['ID']:
                    holder_user['LOCATION'].extend(user['LOCATION'])
                if len(holder_user['LOCATION']) == 3:
                    merged_list.append(holder_user)
                    holder_list.remove(holder_user)
                    break

    return merged_list


def get_userdistances(coordinates):
    """
    Get the list of users at the specified coordinates.
    :param coordinates: The list of coordinates to get users at.
    :type coordinates: list
    :return: The list of users at the specified coordinates.
    :rtype: list
    """

    user_lists = []
    session_name = 'session'
    client = _get_client(str(session_name))
    for coordinate in coordinates:
        user_lists.append(_get_users(client, coordinate))
        if coordinate != coordinates[-1]:          
            _wait(100)
    client.disconnect()
    print(f'[+] Session {session_name} disconnected')
    
    user_list = _merge_lists(user_lists)

    return user_list
