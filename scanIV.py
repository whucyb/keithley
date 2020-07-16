import Kei2400CControl as kei2400
import visa
import time
import pylab
import csv
import numpy as np
import platform
import sys

def csv_writer(data,path):
    with open(path,"w") as csv_file:
        writer=csv.writer(csv_file,lineterminator='\n')
        writer.writerow(['Bias Voltage[V]','Measured Voltage[V]','Measured Current[A]'])
        for val in data:
            writer.writerows([val])

# prevent from running with python2
if platform.python_version().startswith('2'):
   print('You are running with',platform.python_version(),'.')
   print('Please run with python3.')
   print('Exit.')
   sys.exit()
biasSupply=kei2400.keithley2400c("ASRL/dev/ttyUSB1::INSTR")
biasSupply.set_current_protection(100E-6) # current protection in A
biasSupply.set_voltage_protection(800) # voltage protection in V
positiveHV=False # sign of the voltage
#HVrange=200*1e3  # voltage scan range in mV in absolute value
HVrange=100*1e3  # voltage scan range in mV in absolute value
biasSupply.filter_off()

time_start=time.time()
vols=[]
mvols=[]
current=[]

if positiveHV:
    sign=1
else:
    sign=-1
iStart=int(0*1e3)
iEnd=int(sign*HVrange+sign*1)
iStep=int(sign*1*1e3)
for iBias in range(iStart,iEnd,iStep):
    biasSupply.output_on()
    biasvol=iBias/1000 # mV to V
    vols.append(biasvol)
    mvols.append(biasSupply.set_voltage(biasvol))
    time.sleep(0.5)
    current.append(biasSupply.display_current())
    if biasSupply.hit_compliance():
        break

print("Bias Vols: "+str(vols))
print("Measured vols: "+str(mvols))
print("Current: "+str(current))

data=[vols,mvols,current]
dataarray=np.array(data)

filename="test.csv"
csv_writer(dataarray.T,filename)
time_top=time.time()
print("Ramping up takes %3.0f s." % (time_top-time_start))

print("Now ramping down...")
biasSupply.set_voltage(0*1e3,5)
biasSupply.output_off()
biasSupply.beep()
time_end=time.time()

print("Ramping up time:\t%3.0f s" % (time_top-time_start))
print("Ramping down time:\t%3.0f s" % (time_end-time_top))
print("Total time:\t\t%3.0f m %2.0f s" % ((time_end-time_start)//60, (time_end-time_start)%60))
