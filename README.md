OSU-Registration Library
=======================

Library to work as API to the Oregon State's registration system. I want to this to serve as a tool for other long-suffering students who want to streamline registration/class management. 

Usage
------

Working with the library is just instantiating the class and calling it's member functions

### Instantiation

First import the module
	import registration

Set up variables with your student id and password for the registration website.
	sid = '930608334'
	pin = '431254'

Instantiate the class
	registration_class = registration.infosu(sid, pin)

### Transcript
The `get_transcript` function fetches a list of classes you have taken and the total credits you have and puts them in a class.
	transcript = registration_class.get_transcript()
	transcript.grades  #Print out a list of classes you have taken with grades
	transcript.credits #Print out how many credits you have

You can use the transcript to check if you have already taken a class or not.
	transcript.has_class('cs', '162')
	transcript.has_passed_class('cs', '162')

Or you can use it to see your grade distribution
	transcript.grade_distribution()

### Schedule
The `get_schedule` function fetches what classes you are current taking 
	schedule = registration_class.get_schedule()
	schedule.current_classes #Array of classes and details of classes you are taking
	schedule.schedule	 #Array of your weekly schedule

### Searching
The `class_search` function searches for a class using the Department name and the Course number.
	registration_class.class_search('cs', '261')

### Adding a class
The `add_class` function takes a up to CRNs and tries to add the class, returns `True` or `False`
	registration_class.add_class('54034')

### Major Requirements(not working yet)
The `get_major_requirements` function gets a list of classes that you need to take in order to graduate
	registration_class.get_major_requirements()
