# -*- coding: utf-8 -*-
"""
Created on Thu May 17 11:35:28 2018

@author: pretkelisn
"""
from ISStreamer.Streamer import Streamer
import csv



streamer = Streamer(bucket_name= "Testing", bucket_key= "3XJRURS36EB7", access_key= "7wKPG4Cv0iGHgZMLlmtflW2EgwbRjTfH")
streamer.log("test", "hi")
streamer.log("temperature", 33)

# flush and close the stream
streamer.close()