"""
This script depends on the following Python
Libraries that do not ship with python!

PySerial - http://pyserial.sourceforge.net/
"""

####
# SETTINGS
####


#Path to the database that you want to log to
database   = "pbx.db"

#Serial port you want to log to
serialPort = "COM1"

#Rate at which the serial port should communicate
baudRate   = 9600











#DO NOT EDIT BELOW THIS LINE
###############################################################################

import sqlite3
import serial
from time import sleep

port = "COM1"
ser = serial.Serial(serialPort, baudRate)
string = None

db = sqlite3.connect(database)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS calls ( 
    callid           INTEGER        PRIMARY KEY,
    service          INTEGER( 1 ),
    source_type      INTEGER( 1 ),
    date             DATETIME( 8 ),
    time             DATETIME( 5 ),
    duration         DATETIME( 8 ),
    flags            TEXT( 7 ),
    source_number    INTEGER( 15 ),
    dest_number      INTEGER( 22 ),
    diverting_number INTEGER( 15 ),
    access_code      INTEGER( 5 ),
    source_trunk     INTEGER( 4 ),
    dest_trunk       INTEGER( 4 ),
    account          INTEGER( 6 ),
    pin              INTEGER( 12 ),
    modem_pool       INTEGER( 2 ) 
);")
db.commit()

"""
Call Format:
"02 04/28/14 05:31 00:00:18 --1---  1380            18772989943                            9     0    45   000000                "
"""
while True:
	#Read data from the serial port
    data = ser.readline()
	
	#only process the data if we get stuff over the line
    if len(data) > 0:
        #print "Received data: " , data.rstrip('\r\n')
		
		#Strip Newlines out of the data so we don't screw up the next part
        string += data.rstrip('\r\n')
		
		#The PBX sends EXACTLY 128 Bytes of data for each call
		#We take advantage of this in a pretty bad way and we have our fingers
		#crossed that we NEVER get a partial line as that would break all rows after it
        if len(string) == 128:
			#not 100% sure why i put this here but it seems like a nice check
			#to make sure that string gets cleared before it grabs more data.
            line = string
            string = None

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

            #check strings for Noneness
            if service.isspace():
                service = None
            if source_type.isspace():
                source_type = None
            if date.isspace():
                date = None
            if time.isspace():
                time = None
            if duration.isspace():
                duration = None
            if flags.isspace():
                flags = None
            if source_number.isspace():
                source_number = None
            if dest_number.isspace():
                dest_number = None
            if diverting_number.isspace():
                diverting_number = None
            if access_code.isspace():
                access_code = None
            if source_trunk.isspace():
                source_trunk = None
            if dest_trunk.isspace():
                dest_trunk = None
            if account.isspace():
                account = None
            if pin.isspace():
                pin = None
            if modem_pool.isspace():
                modem_pool = None
			
			#Insert gathered data into database and commit changes
			#(might be better to have a separate loop for committing
			#changes as the disk may get bogged down when under heavy call load)
			#Also the below line is way too long but i can't think of a way to shorten it...
            query = "INSERT INTO calls (service,source_type,date,time,duration,flags,source_number,dest_number,diverting_number,access_code,source_trunk,dest_trunk,account,pin,modem_pool) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (service,source_type,date,time,duration,flags,source_number,dest_number,diverting_number,access_code,source_trunk,dest_trunk,account,pin,modem_pool)
            cursor.execute(query)
            db.commit()
			
			#print call log line to stdout
            print line
			
	#Wait an obscenely small amount of time between loops so we don't eat CPU time.
    sleep(0.001)

db.close()
ser.close()
