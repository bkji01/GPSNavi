# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 08:17:07 2019

@author: win10_NB
"""


import os
import serial
import time
import threading
import copy

HOME_DIR = r'D:\work\GPS'
os.chdir(HOME_DIR)


DISPLAY_LINE_NUM = 20       # 20줄 읽기 
MAX_SERIAL_COMM = 100000

#%%
#
#with serial.Serial('COM6', 4800, timeout=1) as ser:
#    x = ser.read()          # read one byte
#    s = ser.read(10)        # read up to ten bytes (timeout)
#    line = ser.readline()   # read a '\n' terminated line
#    
    
#%%    
#import serial


#데이터 처리할 함수
def parsing_data(data):
    # 리스트 구조로 들어 왔기 때문에
    # 작업하기 편하게 스트링으로 합침
    tmp = ''.join(data)

    #출력!
    #print(tmp)
    return tmp.strip()


#port = 'COM6' # 시리얼 포트
#baud = 4800 # 시리얼 보드레이트(통신속도)
#ser = serial.Serial(port, baud, timeout=0)
def get_serial(): 
    k = 0
    line = [] #라인 단위로 데이터 가져올 리스트 변수
    serial_data = []
    
    cnt_line_num = 0
    with serial.Serial('COM6', 4800, timeout=1) as ser:
        print('Start Serial Comm:')
        for i in range(MAX_SERIAL_COMM):
            k = k + 1
            c = ser.read()
            try:
                c = c.decode('utf-8')
                line.append(c)
            except:
                print('except:', c)
                pass
    
            if ord(c) == 10:            
                 #데이터 처리 함수로 호출
                serial_data.append(parsing_data(line))
            
                #line 변수 초기화
                del line[:]
                
                cnt_line_num = cnt_line_num + 1
                print('read line num:', cnt_line_num)
                if cnt_line_num > DISPLAY_LINE_NUM:
                    break
    return serial_data

#%%
import re
def chksum_nmea(sentence):
    
    # This is a string, will need to convert it to hex for 
    # proper comparsion below
    cksum = sentence[len(sentence) - 2:]
    
    # String slicing: Grabs all the characters 
    # between '$' and '*' and nukes any lingering
    # newline or CRLF
    chksumdata = re.sub("(\n|\r\n)","", 
                        sentence[sentence.find("$")+1:sentence.find("*")])
    
    # Initializing our first XOR value
    csum = 0 
    
    # For each char in chksumdata, XOR against the previous 
    # XOR'd char.  The final XOR of the last char will be our 
    # checksum to verify against the checksum we sliced off 
    # the NMEA sentence
    
    for c in chksumdata:
       # XOR'ing value of csum against the next char in line
       # and storing the new XOR value in csum
       csum ^= ord(c)
    
    # Do we have a validated sentence?
    if hex(csum) == hex(int(cksum, 16)):
       return True

    return False
#%%

#%%
time.sleep(1)
print(time.ctime())
while True:
    serial_data = get_serial()
    for data in serial_data:
        print(data)
        gps_data = data.split(',')
        if gps_data[0] == '$GPGGA' and chksum_nmea(data) == True:
            gpgga_data = data
            gps_time_str = gps_data[1]
            gps_latitude = gps_data[2]
            gps_latitude_flag = gps_data[3]
            gps_longitude = gps_data[4]
            gps_longitude_flag = gps_data[5]
            gps_data_mode = gps_data[6]
            gps_num_sat = gps_data[7]
            gps_precision = gps_data[8]
            gps_altitude = gps_data[9]
            gps_checksum = gps_data[-1].split('*')[-1]
    
    time.sleep(1)
    print(time.ctime())
    





