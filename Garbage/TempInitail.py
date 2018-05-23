import time
import sys
import Adafruit_ADS1x15
import socket
import logging
import os
from ISStreamer.Streamer import Streamer

host = socket.gethostname()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')

logging.info('initialState inits')

isBucketKeyHHF = 'Your value here'
isBucketNameHHF = 'Your Value here'
isAccessKey = 'Your value here'

hhfInitState= Streamer(bucket_name=isBucketNameHHF, bucket_key=isBucketKeyHHF, access_key=isAccessKey)

# Constants
KPA_PER_CM= 0.0980665
GAL_PER_CM= 3.0840887

# ADS1015 inits
# Channels for each sensor

TANK=0
ATMOS=1
TEMP=2

# Constants
SENS=1.2
INTERVALS=2048

# create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.

GAIN = 16

logging.info('Gain is %i', GAIN)

gainVoltages = {
	0.66:   6.144,
	1:      4.096,
	2:      2.048,
	4:      1.024,
	8:      0.512,
	16:     0.256
}

offsets = {
    1:  12.0,
    2:  24.0,
    4:  48.0,
    8:  96.0,
    16: 192.0
}

# read the thermometer and convert to F

timestamp = int(time.time())

value = adc.read_adc(TEMP, gain=2)
mV = ((value * 2.048)/2048) * 1000
tempInC = (mV - 500) / 10
tempInF = (tempInC * 1.8) + 32
logging.info('temp reading: %f', tempInF)

logging.info('Posting enclosure temp to InitialState')
streamName = host + "EnclosureTemp"

hhfInitState.log(streamName, str(tempInF), str(timestamp))

# Read the difference between channel 0 and 1 (i.e. channel 0 minus channel 1).
# Note you can change the differential value to the following:
#  - 0 = Channel 0 minus channel 1
#  - 1 = Channel 0 minus channel 3
#  - 2 = Channel 1 minus channel 3
#  - 3 = Channel 2 minus channel 3

# read differential between tank and atmosphere.

value = adc.read_adc_difference(0, gain=GAIN)
logging.info('value : %f', value)
logging.info('gainVoltage: %f', gainVoltages[GAIN])
logging.info('offset: %f', offsets[GAIN])

# Note you can also pass an optional data_rate parameter above, see
# simpletest.py and the read_adc function for more information.
# Value will be a signed 12 or 16 bit integer value (depending on the ADC
# precision, ADS1015 = 12-bit or ADS1115 = 16-bit).

# for reference... 

# 1cm water column = 0.0980665 kPa pressure
# therefore, net pressure observed * 0.0980665 = # of cm tall...

# my tank is 48" in diameter, so...
# 1 cm = 11690 cubic cm
# 1 cm of water in the tank = 3.09 gallons 

deltaMV = ((value * gainVoltages[GAIN])/INTERVALS) * 1000
offsetMV= ((offsets[GAIN] * gainVoltages[GAIN])/INTERVALS) * 1000

logging.info('deltaMV - %f',deltaMV)
logging.info('offsetMV - %f', offsetMV)

mV = float(deltaMV - offsetMV)
pressure = float(mV / SENS)
columnHeight = float(pressure / KPA_PER_CM)
tankLevel = round(columnHeight * GAL_PER_CM, 2)

# yes, it can happen when the tank is empty.

if tankLevel <= 0.0:
	tankLevel = 0.0

logging.info('mV = %f', mV)
logging.info('pressure = %f kPa', pressure)
logging.info('columnHeight = %f cm', columnHeight)
logging.info('tankLevel = %f gallons', tankLevel)

timestamp = int(time.time())

logging.info('Posting tank level to InitialState')
streamName = host + "TankLevel"

hhfInitState.log(streamName, str(tankLevel), str(timestamp))

logging.info('Done.')

sys.exit(0)
