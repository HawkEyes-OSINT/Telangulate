import os

"""
This module receives, stores and retreives Telegram API bot configurations
"""

def checkconfig():
    """
    Check if config file exists
    """
    set = True
    # verify file exists
    if os.path.isfile("config.csv"):
        # verify sufficient data
        with open("config.csv", "r") as f:
            lines = f.readlines()
            if not lines[0].split(',')[1]:
                set = False
                print('[-] Missing api_id in config.csv')
            if not lines[1].split(',')[1]:
                set = False
                print('[-] Missing api_hash in config.csv')
            if not lines[2].split(',')[1]:
                set = False
                print('[-] Missing phone in config.csv')
    else:
        set = False
        print('[-] Missing config.csv')

    return set

def getconfig():
    """
    Get bot configurations from config file
    """
    # check configurations
    if not checkconfig():
        exit(0)

    # retreive configuration from file
    with open("config.csv", "r") as f:
        lines = f.readlines()
        config = {
                'api_id': lines[0].split(',')[1].strip(),
                'api_hash': lines[1].split(',')[1].strip(),
                'phone': lines[2].split(',')[1].strip()
                }

    return config
