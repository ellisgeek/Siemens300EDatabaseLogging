######
# 
# The MIT License (MIT)
# 
# Copyright (c) 2014 Eliott Saille
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
######

"""
WARNING
=======
THIS SOFTWARE IS INCOMPLETE!!!
IT IS UNABLE TO WALK DIRECTORIES
IN THE FORMAT I NEED AT THIS TIME.


IMPORTANT: IMPORT ANY EXISTING CALL LOGS BEFORE RUNNING THE NEW LOGGER OR THINGS WILL BE OUT OF ORDER!

This script depends on the following Python
Libraries that do not ship with python!

PySerial - http://pyserial.sourceforge.net/
"""

##        ##
#          #
  SETTINGS 
#          #
##        ##


#Path to the database that you want to import calls to
database   = "pbx.db"

#DO NOT EDIT BELOW THIS LINE
###############################################################################

import sqlite3
from fnmatch import fnmatch
from time import sleep


log = file.open(logfile)
lines = log.readlines()

string = ""

db = sqlite3.connect(database)
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
