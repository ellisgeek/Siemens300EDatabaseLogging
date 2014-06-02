"""
This script depends on the following Python
Libraries that do not ship with python!

PySerial - http://pyserial.sourceforge.net/
MySQL Connector - http://dev.mysql.com/downloads/connector/python/
"""


import sqlite3
from fnmatch import fnmatch
from time import sleep


log = file.open(logfile)
lines = log.readlines()

string = ""

db = sqlite3.connect('pbx.db')
cursor = db.cursor()

"""
Call Format:
"02 04/28/14 05:31 00:00:18 --1---  1234            1234567890                            9     0    45   000000                "
"""
for root, subFolders, files in os.walk(rootdir):
    if fnmatch.fnmatch(file, '*.txt') in files:
        with open(os.path.join(root, 'data.txt'), 'r') as log:
            for lines in log:             
				if line:
					string += line.rstrip('\r\n')
					if len(string) == 128:
						line = string
						string = ""

						# Split line into useful segments
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
						query = [(
							service,
							source_type,
							date,
							time,
							duration,
							flags,
							source_number,
							dest_number,
							diverting_number,
							access_code,
							source_trunk,
							dest_trunk,
							account,
							pin,
							modem_pool
						)]
						cursor.executemany(
							"INSERT INTO calls VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
							query)
						db.commit()
						print line
				sleep(0.001)

db.close()
ser.close()
