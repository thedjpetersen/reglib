OSU-Registration Library
=======================

***Sadly this module is depreciated.***

Library to work as API to the Oregon State's registration system. I want to this to serve as a tool for other long-suffering students who want to streamline registration/class management. 

Installation
------------

First be sure you have the module `lxml` as it is a dependency for parsing the html.

	git clone git@github.com:thedjpetersen/OSU-Registration.git
	cd OSU-Registration
	sudo python setup.py install

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

When the `registration_class` is instantiated it fetches the transcript access it like this:

	registration_class.transcript

The `get_transcript` function updates the transcript

	registration_class.get_transcript()
	registration_class.transcript.grades  #Print out a list of classes you have taken with grades
	registration.transcript.credits #Print out how many credits you have

You can use the transcript to check if you have already taken a class or not.

	transcript.has_class('cs', '162')
	transcript.has_passed_class('cs', '162')

Or you can use it to see your grade distribution

	transcript.grade_distribution()

### Schedule

When the `registration_class` object is instantiated it fetches your current schedule

	registration_class.schedule
	registration_class.schedule.current_classes
	registration_class.schedule.schedule #get dictionary of days of the week

The `get_schedule` function updates the schedule that your `registration_class` objects has 

	registration_class.get_schedule()
	schedule.current_classes #Array of classes and details of classes you are taking
	schedule.schedule	 #Array of your weekly schedule

### Searching
The `class_search` function searches for a class using the Department name and the Course number.

	registration_class.class_search('cs', '261')

Or you can search for a class that does not conflict with your current schedule

	registration_class.class_search_schedule('cs', '261')

### Adding a class
The `add_class` function takes a up to CRNs and tries to add the class, returns `True` or `False`

	registration_class.add_class('54034')

### Possible Schedules(partially functional - works for lectures)
The `make_schedule` will return all possible non-conflicting combinations for a list of classes. This function takes a array of classes, a optional arguement for the term. If no arguement is given it will assume the current term.

 	registration_class.make_schedule(['cs 261', 'fr 213', 'cs 275', 'mth 232']) #current term
 	registration_class.make_schedule(['cs 162', 'mth 111'], 'F12') # This will return the combinations for fall 2012

### Major Requirements
The `get_major_requirements` function gets a list of classes that you need to take in order to graduate

	audit = registration_class.get_major_requirements()
	audit.required_classes.courses

