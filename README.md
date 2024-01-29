# Telangulate

Telangulate is a Python program that utilizes the Telegram API to find users in the vicinity of a given GPS coordinate. The program employs a triangulation approach by querying the "find people near" feature on Telegram at three locations surrounding the input coordinates to determine the exact locations of users within a 500-meter radius.

## Installation

Clone the Telangulate repository from GitHub:

    git clone https://github.com/your-username/Telangulate.git
    cd Telangulate
    pip install -r requirements.txt

## Configuration

Before running the program for the first time, you need to provide your Telegram API ID, API Hash, and the phone number associated with your Telegram account in the config.csv file. Additionally, make sure you have a profile photo on your Telegram account for the program to function correctly.
Usage

Run the program by executing the following command:

    python telangulate.py

The program will prompt you to enter a GPS coordinate. It takes approximately four minutes to complete.

After execution, a CSV file named user_list.csv will appear in the program folder, containing a list of users in the specified area along with their profile details and locations.

Please move the file to another location after running the program, as it will be replaced with new results in subsequent executions.
Note on Telegram API Limitations

The Telegram API allows an account to change its location at a rate of 10 meters per second. If you wish to run the program for a different location, either calculate the time needed to wait or update the config.csv file with another account.
