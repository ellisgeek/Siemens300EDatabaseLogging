"""
This script depends on the following Python
Libraries that do not ship with python!

PySerial - http://pyserial.sourceforge.net/
MySQL Connector - http://dev.mysql.com/downloads/connector/python/
"""


import sqlite3
import serial
from time import sleep

port = "COM1"
ser = serial.Serial("COM1", 9600)
string = ""

db = sqlite3.connect('pbx.db')
cursor = db.cursor()
#cursor.execute('')

"""
Call Format:
"02 04/28/14 05:31 00:00:18 --1---  1380            18772989943                            9     0    45   000000                "
"""
while True:
    #data = "02 04/28/14 05:31 00:00:18 --1---  1380            18772989943                            9     0    45   000000                "
    data = ser.readline()
    if len(data) > 0:
        print "Recieved data: " , data.rstrip('\r\n')
        string += data.rstrip('\r\n')
        if len(string) == 128:
            #print ">128"
            line = string
            string = ""

            # Split data into useful segments
            service = line[0:1]
            source_type = line[1:2]
            date = line[3:11]
            time = line[12:17]
            duration = line[18:26]
            flags = line[27:34]
            source_number = line[35:50]
            dest_number = line[51:73]
            diverting_number = line[75:88]
            access_code = line[90:95]
            source_trunk = line[96:100]
            dest_trunk = line[101:105]
            account = line[106:112]
            pin = line[113:126]
            modem_pool = line[126:128]

            #check strings for nullness
            if service.isspace():
                service = ""
            if source_type.isspace():
                source_type = ""
            if date.isspace():
                date = ""
            if time.isspace():
                time = ""
            if duration.isspace():
                duration = ""
            if flags.isspace():
                flags = ""
            if source_number.isspace():
                source_number = ""
            if dest_number.isspace():
                dest_number = ""
            if diverting_number.isspace():
                diverting_number = ""
            if access_code.isspace():
                access_code = ""
            if source_trunk.isspace():
                source_trunk = ""
            if dest_trunk.isspace():
                dest_trunk = ""
            if account.isspace():
                account = ""
            if pin.isspace():
                pin = ""
            if modem_pool.isspace():
                modem_pool = ""
            query = "INSERT INTO calls (service,source_type,date,time,duration,flags,source_number,dest_number,diverting_number,access_code,source_trunk,dest_trunk,account,pin,modem_pool) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (service,source_type,date,time,duration,flags,source_number,dest_number,diverting_number,access_code,source_trunk,dest_trunk,account,pin,modem_pool)
            cursor.execute(query)
            db.commit()
            print line
    sleep(0.001)
    #print 'Ping!\n'

db.close()
ser.close()
