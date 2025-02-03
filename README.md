# buddycop
Body-word camera metadata analysis 
This is a python script for locating nearby officers using timestamps and GPS coordinates from body worn camera metadata.  It was created using data from Motorola V300 Body Cameras, but may work with others that format metadata the same way, including I suspect, all Motorola Watch Guard products. 

Say you've got a big folder full of hundreds of hours of body cam footage, and you want to know if there an officer was close enough to another one to get a different angle on something. This will help you figure out which officer. 

Requirements: 
Python 3.7+

Usage:
Download the following file from this repository: buddycop3-getting_too_old_for_this_shit.py

`python buddycop3-getting_too_old_for_this_shit.py`

You will then be prompted to 
`Enter directory containing .json/.vtt files:`
`Enter target timestamp (ISO 8601 format, e.g., 2024-05-08T02:04:14.016256Z):` **This is found in the .json file.** 
`Enter officer name to check proximity to:`**John Doe**
`Maximum proximity distance in meters [100]:' **put 100 unless you have a special use case**


I will upload some example files in the near future. I need to keep those to myself for the time being, sorry. 

Much credit to [Haylin Moore](https://github.com/haylinmoore) whose much better work inspired me to prompt deepseek into spitting this code out.  
