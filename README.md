
Body-word camera metadata analysis. 

This is a python script for locating nearby officers using timestamps and GPS coordinates from body worn camera metadata. It was created using data from Motorola V300 Body Cameras, but may work with others that format metadata the same way, including I suspect, all Motorola Watch Guard products.

Say you've got a big folder full of hundreds of hours of body cam footage, and you want to know if an officer was close enough to another one to possibly have seen something from a different angle. This will help you figure out which officer.

Requirements: Python 3.7+

Usage: Download the following file from this repository: buddycop3-getting_too_old_for_this_shit.py

`python buddycop3-getting_too_old_for_this_shit.py`

You will then be prompted to 
- Enter directory containing .json/.vtt files:
- Enter target timestamp (ISO 8601 format, e.g., 2024-05-08T02:04:14.016256Z): **This is found in the .json file.**
- Enter officer name to check proximity to:`**John Doe** `Maximum proximity distance in meters [100]: **put 100 unless special case**

I will upload some example files in the near future. I need to keep those to myself for the time being, sorry.

Here is the output with names/times obscured in the meantimes.

`$ python buddycop3-getting_too_old_for_this_shit.py Enter directory containing .json/.vtt files: /path/ Enter target timestamp (ISO 8601 format, e.g., 2024-05-08T02:04:14.016256Z): 2024-05-07T23:53:10.196220Z Enter officer name to check proximity to: Fred Flinstone Maximum proximity distance in meters [100]: 100`

`Processing files...`

`Results for 2024-06-07T13:43:10.196220Z: Target officer: Fred Flinstone Maximum proximity: 100.0 meters`

`Nearby officers:`

- `Steven Colbert: 4.57 meters away`
- `William DeFoe: 5.51 meters away`
- `Jane Kelly: 8.13 meters away`
- `Kevin Shields: 8.16 meters away`
- `Ur Mama: 13.90 meters away`

Much credit to [Haylin Moore](https://github.com/haylinmoore) whose much better work inspired me to prompt deepseek into spitting this code out.  
