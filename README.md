# Py-xbox

This is a command line python programm that allows you to check xbox messages, friends and recents.

## Setup (for linux)

Go to xbl.io, login with your xbox account and generate a new apikey and write it down somewhere (you can only view it once)

Clone the repository: ``git clone https://github.com/terpii/py-xbox.git && cd py-xbox``

Paste your apikey into a file named api-key : ``echo YOUR-API-KEY-HERE > api-key``

Install the requirements: ``pip3 install -r requirements.txt``

Run it using: ``python3 py-xbox.py``

## Usage

``python3 py-xbox.py {action} {subaction} {arguments}``
Example ``python3 py-xbox.py friends recents --count 5``

Possible actions: friends, messages, help
to view subactions for each action, just type out the command without a subaction
