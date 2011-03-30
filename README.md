OSU-Registration Library
=======================

Library to work as API to the Oregon State's registration system. I want to this to serve as a tool for other long-suffering students who want to streamline registration/class management. 

Example
------

Working with the library is just instantiating the class and calling it's member functions

First import the module
	import registration

Set up variables with your student id and password for the registration website.
	sid = '930608334'
	pin = '431254'

Instantiate the class
	registration_class = registration.infosu(sid, pin)
