import os
import sys
import json
sys.path.append('/home/pi/Desktop/ROBOT/py532lib')
#print(sys.path,'\n',len(sys.path))
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *

def readnfc():
    pn532 = Pn532_i2c()
    pn532.SAMconfigure()
    card_data = pn532.read_mifare().get_data()
    card_len_checksum = pn532.read_mifare().get_length_checksum()
    card_data_checksum = pn532.read_mifare().get_data_checksum()
    card_frame_type = pn532.read_mifare().get_frame_type()
    card_tuple = pn532.read_mifare().to_tuple()
    data={
            "card_data":str(card_data),
            "card_len_checksum":card_data_checksum,
            "card_frame_type":card_frame_type
            }
    return data


print(readnfc())
