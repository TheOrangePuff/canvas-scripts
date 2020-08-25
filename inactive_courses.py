"""
    Using a CSV file of courses, filter out courses with zero students.
    (This will take a while to run!)
"""


import os
import sys
import csv

# Import the Canvas class
from canvasapi import Canvas


# Canvas API URL
API_URL = os.environ['API_URL']
# Canvas API key
API_KEY = os.environ['API_KEY']

try:
    csv_file = sys.argv[1]
except IndexError:
    csv_file = None
    print('No csv file')

if csv_file is not None:
    courses = []
    with open(csv_file) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            courses.append(row[0])

    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)

    inactive_courses = []

    for course in courses:
        course = canvas.get_course(course)

        # If there are no enrollments ignore the course
        count = 0
        for user in course.get_users(enrollment_type=['student']):
            count += 1
            break

        active = count == 0

        # Filter out a bunch of courses that are used for testing or as templates
        if 'Sandbox'.lower() in course.name.lower():
            active = True

        if 'Blueprint'.lower() in course.name.lower():
            active = True

        if 'Template'.lower() in course.name.lower():
            active = True

        if 'Test'.lower() in course.name.lower():
            active = True

        if not active:
            inactive_courses.append(course)

    # Print out the results
    for course in inactive_courses:
        print(str(course.id) + ',' + course.name)
