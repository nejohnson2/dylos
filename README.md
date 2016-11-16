# Dylos 1700 Python Module

This is a module to collect readings from the Dylos 1700 over serial communication.   Only basic functionality has been implemented though there is lots of room for improvement.

## Usage

```python
from dylos import Dylos

# initialize
d = Dylos(port='/dev/ttyUSB0')

# start listening
d.read()
```

The read function will listen to the serial port forever and **I believe this is implemented as a BLOCKING function**.  I have not tested this and I would like to look further at the ```serial.thread``` module.

You can also pass a ```True``` value to the read function in order to write the data to a csv file.

```
# write to csv file
d.read(store=True)
```

## About the Dylos

The Dylos returns air quality readings via serial in the form of small particles and large particles.  Small particles are all particles detected down to the detection limit of 0.5 microns.  Large particles are counts above the threshold of 2.5 microns.  In order to get the number of particles between 0.5 and 2.5 microns, subtract the large particle counts from the small particles counts.

Data is output from the Dylos in the form:

```
small_count,large_count<CR><LR>
```

Data is output every minute and the counts represent the average concentration over the past minute.  Units are - ```counts/100 per cubic foot```.  An output of 675 would mean 67,500 particles per cubic foot.  The detection limit is stated at 0.5 microns.

```
Air Quality Chart:
-----------------
3000+		= VERY POOR
1050-3000	= POOR
300-1050	= FAIR
150-300 	= GOOD
75-150		= VERY GOOD
0-75		= EXCELLENT
```

