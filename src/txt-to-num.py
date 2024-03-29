"""
 __      __                    _   _                                          
 \ \    / /                   | | (_)                                         
  \ \  / /__  _ __ _   _ _ __ | |_ _  ___  _ __                               
   \ \/ / _ \| '__| | | | '_ \| __| |/ _ \| '_ \                              
    \  / (_) | |  | |_| | |_) | |_| | (_) | | | |                             
     \/ \___/|_|   \__, | .__/ \__|_|\___/|_| |_|                             
                    __/ | |                                                   
                   |___/|_|                                                   
    ________     ___   ___  __  ___   __      __        _       _   _         
   /  ____  \   |__ \ / _ \/_ |/ _ \  \ \    / /       | |     | | | |        
  /  / ___|  \     ) | | | || | (_) |  \ \  / /__  _ __| |_ ___| |_| |_ _   _ 
 |  | |       |   / /| | | || |\__, |   \ \/ / _ \| '__| __/ _ \ __| __| | | |
 |  | |___    |  / /_| |_| || |  / /     \  / (_) | |  | ||  __/ |_| |_| |_| |
  \  \____|  /  |____|\___/ |_| /_/       \/ \___/|_|   \__\___|\__|\__|\__, |
   \________/                                                            __/ |
                                                                        |___/
  This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
  To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
  
  To obtain rights to use this commercially (if you want to for some reason, contact me on reddit /u/vortetty
  
  if you copy this, please leave me as a credit using the below format:
  
    Original by Vortetty on Github:
    https://github.com/Vortetty/Voryption/
    Vortetty's Github Profile:
    https://github.com/Vortetty/
   
  for consitency with the copyright notice, use 
  http://patorjk.com/software/taag/#p=display&h=2&v=1&f=Big&t=%3C%20your%20text%20here%20%3E
  to generate your banner, all settings provided on that link are the same as used here
  
"""

import os, math
from decimal import *

def tonum( p ):
  pswd = []
  pswd[:0] = p
  result = ""
  #print(pswd)
  for i in range(len(pswd)): 
    num = ord(pswd[i])
    if(num==32):
      num = "25752"
    result += str(num)
  return result

def getpass():
  password = input("Enter password containing only ASCII characters: ")

  if(password.isascii() == True):
    key = tonum(password)
    print("Keep track of this password, you will need it to retrieve files later: " + "'" + password + "'")
    
  elif(password.isascii() == False):
    print("\nPassword contains non-ASCII Characters, Please try again.")
    getpass()

  return key

def getpassdec():
  password = input("Enter password for file containing only ASCII characters: ")

  if(password.isascii() == True):
    key = tonum(password)
    
  elif(password.isascii() == False):
    print("\nPassword contains non-ASCII Characters, Please try again.")
    getpassdec()

  return key

def getfile():
  f = input("what file would you like to encrypt? must be in the same directory this script is run from, or be an absolute path starting from the root directory: ")
  return f

def getfiledec():
  f = input("what file would you like to decrypt? must be in the same directory this script is run from, or be an absolute path starting from the root directory: ")
  return f

def addid(filename,uid):
    name, ext = os.path.splitext(filename)
    return "{name}_{uid}{ext}".format(name=name, uid=uid, ext=ext)
 
def init():
  #get bits
  file = getfile()
  fin = open(file, "r")
  data = fin.read()
  data = str(data)
  data = bin(int.from_bytes(data.encode(), 'big'))
  data = data[2:]

  #get passkey
  key = getpass()

  return (int(key), int("1"+str(data)), file) # add 1 to beginning of data to avoid "SyntaxError: leading zeros in decimal integer literals are not permitted"

def encrypt():
  key, binary, filename = init()
  num1 = key^2+key
  y = ((binary*key)*num1)

  f = open(addid(filename,"encrypted"), "w+")
  f.write(str(y))
  f.close()
  

def decrypt():
  #get bits
  fin = getfiledec()
  f = open(fin, "r")
  file = f.read()
  data = int(file)
  
  #get passkey
  key = int(getpassdec())

  # get num1
  num1 = key^2+key

  # decrypt text and remove the added one
  data = data//num1
  data = data//key
  data = str(data)[1:]
  data = "0b"+data

  # finally we convert it back to hex bytes
  data = int(data, 2)
  data = data.to_bytes((data.bit_length() + 7) // 8, 'big').decode()
  print(data)
  
  # then write to decrypted file
  f = open(addid(fin,"decrypted"), "w+")
  f.write(data)
  f.close()
