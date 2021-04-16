# Automated MFC FLow Calibration
# Developed for the SJVAPCD Air Monitoring Program
# By Michael Haire and Muhammad Mian


# Import Libraries
import board
import busio
import adafruit_mcp4725
import math
import random
import sys
import serial
import RPi.GPIO as GPIO
import time
import numpy

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP4725.
dac = adafruit_mcp4725.MCP4725(i2c)

#Functions:

#Voltage Readings and Average Function
def Volt(count, avg1, avg2):  #count is the number of time the function has been called, avg1 is setpoint, and avg2 is feedback.
 if (count = 0):
  if(len(avg1)>0):
   #clear old values
   avg1.clear
   avg2.clear
  else:
   avg1 = []
   avg2 = []
   count = count + 1
 else:
  count = count + 1
  avg1.append(adc.read_adc_difference(3, gain=GAIN)*0.0001875*2)) #update to right channel
  avg2.append(adc.read_adc_difference(1, gain=GAIN)*0.0001875*2)) #update to right channel
 return(count, avg1, avg2)

#Writer Function:This function is to output the read in values from the Cal Track and ADC Module
def Writer(flow,parts,kind,feedback,dry_volt):
 x=open("MFC_" + kind + time.strftime("%Y_%m_%d") + ".csv","a+")
 x.write(time.strftime("%Y/%m/%d %H:%M:%S") + " , " + feedback + " , " + dry_volt + " , " +  parts[0] + " , " + parts[1] + " , " + parts[2]+"\n")
 x.close()

#Warm-up: Allows time for the MFC to warm up and works the valve a little to help sticky valves
def Warm_UP():
 start = time.time()
 NOW = start
 print("Warm-up Cycle Take Approx. 30 minutes.")
 while (NOW - start) < 1800:
   setpoint = random.randint(122,4090)
   dac.raw_value = setpoint
   print(str(round(setpoint * (5.00/4096),4)) + " :current setpoint")
   time.sleep(60)
   NOW = time.time()
   print("Time Remaining:" + str((NOW - start)/60,1) +"minutes"
 main()

#Manual Settings
def Manual():
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
       dac.raw_value(int(outCount))
       output = ads.readADCSingleEnded(channel=3)/1000.0 #change to right channel 
      while abs(float(output)-outV)>0.0005: #Voltage output is wrong
        if float(output) > outV: #votlage is high
          outCount = outCount - 1
          dac.raw_value(int(outCount))
          output = adc.read_adc_difference(3, gain=GAIN)*0.0001875*2
        else: #voltage is low
          outCount = outCount +1
          dac.raw_value(int(outCount))
          output =  adc.read_adc_difference(3, gain=GAIN)*0.0001875*2
      while abs(float(output)-outV)<= 0.0005:
        ser = serial.Serial('/dev/ttyUSB0',baudrate = 9600)
        ser.write("$GET DQ DC\r")
        data = ser.readline()
        ser.close
        print(time.strftime("%Y/%m/%d %H:%M:%S"))
        print("Dry Voltage: "+ str((ads.readADCSingleEnded(channel=3)/1000.0)) + " ,  SetPoint: " + str((ads.readADCSingleEnded(channel=3)/1000.0))*(float(flow)/5.0)
        parts = data.split(",")
        print(parts[0] +"," + parts[1] + "," + parts[2])
        time.sleep(10)

 #Auto Point Readings/Calibration collection
def Auto(FLOW):
 ser = serial.Serial(('/dev/ttyS0',baudrate = 9600) # setup com to serial
 ser.write("$GET DQ DC\r") #Send Command to taking reading
 Volt(count, avg1, avg2) #start voltage readings
 while (data=""): #Check if return flow reading is ready, if not loop Voltage reading
  data = ser.readline()
  Volt(count, avg1,avg2)
 Setpoint = np.array(avg1)
 Feedback = np.array(avg2)
 AvgS = np.average(Setpoint)
 AvgF = np.average(Feedback)
 ser.close
 parts = data.split(",")
 
 main()

def main():
 Warm_UP()

if __name__ == "__main__":
    dac.raw_value = 0
    main()
