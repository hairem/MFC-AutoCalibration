import ADS1115
import time
import math

from random import randint
import sys
import serial
import RPi.GPIO as GPIO

ads = ADS1115.ADS1115(0x48)
dac = Adafruit_MCP4725.MCP4725(0x60)



def Writer(flow,parts,kind):
  x=open("MFC_"+ kind + time.strftime("%Y_%m_%d")+".csv","a+")
  x.write(time.strftime("%Y/%m/%d %H:%M:%S")+" , "+ str((ads.readADCSingleEnded(channel=3)/1000.0))+" , "+ str((ads.readADCSingleEnded(channel=2))*(float(flow)/5.00))+" , "+str((ads.readADCSingleEnded(channel=0))*(float(flow)/5.00)) + " , " +  parts[0] + " , " + parts[1] + " , " + parts[2]+"\n")
  x.close()
  return()

def Auto(flow):
  kind = "Auto_"
  StepU=0
  Set=408+(204*StepU)
  while StepU <=19:
    dac.set_voltage(Set)
    time.sleep(30)
    Stime = int(time.time())
    Ctime = int(time.time())
    dtime = Ctime - Stime
    while dtime < 900:
      ser = serial.Serial('/dev/ttyUSB0',baudrate = 9600)
      ser.write("$GET DQ DC\r")
      data = ser.readline()
      ser.close
      parts = data.split(",")
      Writer(flow,parts,kind)
      print (dtime)
      print( "Dry Voltage: " + str((ads.readADCSingleEnded(channel=3)/1000.0)) + ",  Set Point: " + str((ads.readADCSingleEnded(channel=2))*(float(flow)/5.00)) + ", Feedback: " +  str((ads.readADCSingleEnded(channel=0))*(float(flow)/5.00)) + " , STD Flow:  " +  parts[0] + " , Temp:  " + parts[1] + " , Pressure: " + parts[2])
      time.sleep(5)
      Ctime = int(time.time())
      dtime = Ctime - Stime
    StepU=StepU+1
    Set=409+(204*StepU)
  #GPIO.output(26, GPIO.LOW)
  dac.set_voltage(0)
  raw_input('Press enter to complete run: ')
  Start()
def Fast(flow):
  kind = "Fast_"
  StepU=0
  Set=408+(204*StepU)
  while StepU <=19:
    dac.set_voltage(Set)
    time.sleep(30)
    Stime = int(time.time())
    Ctime = int(time.time())
    dtime = Ctime - Stime
    while dtime < 300:
      ser = serial.Serial('/dev/ttyUSB0',baudrate = 9600)
      ser.write("$GET DQ DC\r")
      data = ser.readline()
      ser.close
      parts = data.split(",")
      Writer(flow,parts,kind)
      print (dtime)
      print( "Dry Voltage: " + str((ads.readADCSingleEnded(channel=3)/1000.0)) + ",  Set Point: " + str((ads.readADCSingleEnded(channel=2))*(float(flow)/5.00)) + ", Feedback: " +  str((ads.readADCSingleEnded(channel=0))*(float(flow)/5.00)) + " , STD Flow:  " +  parts[0] + " , Temp:  " + parts[1] + " , Pressure: " + parts[2])
      time.sleep(5)
      Ctime = int(time.time())
      dtime = Ctime - Stime
    StepU=StepU+1
    Set=409+(204*StepU)
  GPIO.output(26, GPIO.LOW)
  dac.set_voltage(0)
  raw_input('Press enter to complete run: ')
  Start()
def Manual(flow):
  try:
    setPoint = raw_input("Flow output desired?(LPM) ")
    type(setPoint)
    time.sleep(20)
    outV = (5.00/float(flow))*float(setPoint)
    outCount = outV*819
    if float(setPoint)>float(flow):
      print("Desired Flow is not within operational range.")
      Manual()
    else:
      dac.set_voltage(int(outCount))
      output = ads.readADCSingleEnded(channel=3)/1000.0
      while abs(float(output)-outV)>0.0005: #Voltage output is wrong
        if float(output) > outV: #votlage is high
          outCount = outCount - 1
          dac.set_voltage(int(outCount))
          output = ads.readADCSingleEnded(channel=3)/1000.0
        else: #voltage is low
          outCount = outCount +1
          dac.set_voltage(int(outCount))
          output = ads.readADCSingleEnded(channel=3)/1000.0
      while abs(float(output)-outV)<= 0.0005:
        ser = serial.Serial('/dev/ttyUSB0',baudrate = 9600)
        ser.write("$GET DQ DC\r")
        data = ser.readline()
        ser.close
        print(time.strftime("%Y/%m/%d %H:%M:%S"))
        print("Dry Voltage: "+ str((ads.readADCSingleEnded(channel=3)/1000.0)) + " ,  SetPoint: " + str((ads.readADCSingleEnded(channel=2))*(float(flow)/5.00)) + "  , FeedBack: " + str((ads.readADCSingleEnded(channel=0))*(float(flow)/5.00)))
        parts = data.split(",")
        print(parts[0] +"," + parts[1] + "," + parts[2])
        time.sleep(10)
  except KeyboardInterrupt:
    exit = raw_input("Do you wish to set a new (V)alue or (E)xit?")
    if exit.upper() == "E":
      dac.set_voltage(0)
      Start()
    else:
      Manual(flow)
def Quit():
  dac.set_voltage(0)
  GPIO.cleanup()
  sys.exit(0)
def Start():
  option= raw_input("Would you like to run (M)anual Mode, (A)uto Mode, or (Q)uit?")
  type(option)
  if option.upper() == "M":
    flow = raw_input("What is the Max flow Rate?(LPM) ")
    type(flow)
    Manual(flow)
  if option.upper() == "A":
    flow = raw_input("What is the Max flow Rate?(LPM) ")
    type(flow)
    FA = raw_input(" Would you like to run a (S)imple Cal or a(F)ull Cal?")
    type(FA)
    if FA.upper() == "F":
      Auto(flow)
    if FA.upper() == "S":
      Fast(flow)
    else:
      print("Not a valid entry. PLease try again?")
      time.sleep(1)
      Start()
  if option.upper() == "Q":
    dac.set_voltage(0)
    Quit()
  else:
    print("Not a valid entry")
    Start()
dac.set_voltage(0)
Start()
