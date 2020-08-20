"""
    Generate a list of all the observers that have never logged in to Canvas.
"""


import os

# Import the Canvas class
from canvasapi import Canvas


# Canvas API URL
API_URL = os.environ['API_URL']
# Canvas API key
API_KEY = os.environ['API_KEY']

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

account = canvas.get_accounts()[0]

users = account.get_users(enrollment_type=['observer'],include=['last_login','email'])

for user in users:
    if user.last_login is None:
        print(user.name + ',' + user.email)

