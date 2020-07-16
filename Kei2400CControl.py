import visa
import time
import warnings

class keithley2400c:
    def __init__(self,resource_name):
        instlist=visa.ResourceManager()
        print(instlist.list_resources())
        self.kei2400c=instlist.open_resource(resource_name)
        self.kei2400c.timeout=25000
        self.cmpl='105E-6' # global current protection

    def testIO(self):
        message=self.kei2400c.query('*IDN?')
        print(message)

    def set_current_protection(self,current):
        self.cmpl=str(current)
        self.kei2400c.write(":sense:current:protection "+str(current))

    def set_voltage_protection(self,vol):
        self.kei2400c.write(":source:voltage:range "+str(vol))

    def set_voltage(self,vol,speed=1):
        self.kei2400c.write(":sense:current:protection "+self.cmpl)
        self.kei2400c.write(":source:function voltage")
        self.kei2400c.write(":source:voltage:mode fixed")
        vols=self.show_voltage()
        self.sweep(vols,vol,0.1,speed)
        vols=self.show_voltage()
        return vols

    def show_voltage(self):
        self.kei2400c.write(":source:voltage:mode fixed")
        self.kei2400c.write(":form:elem voltage")
        voltage=self.kei2400c.query(":read?")
        # self.kei2400c.timeout=5000
        print("voltage [V]:  " + str(voltage))
        return float(str(voltage))

    def sweep(self, vols, vole, step, speed):
        if vols < vole: # vol start < vol end
            self.sweep_forward(vols,vole,step,speed)
        else:
            self.sweep_backward(vols,vole,step,speed)

    def sweep_forward(self, vols, vole, step,speed):
        # Conveter from V to mV
        mvols=vols*1000
        mvole=vole*1000+1
        mstep=step*1000
        for mvol in range(int(mvols),int(mvole),int(mstep)):
            vol=mvol/1000 # mV -> V
            self.kei2400c.write(":source:voltage:level "+str(vol))
            time.sleep(0.1/speed)

    def sweep_backward(self, vols, vole, step,speed):
        # Conveter from V to mV
        mvols=vols*1000
        mvole=vole*1000-1
        mstep=step*1000

        for mvol in range(int(mvols),int(mvole), -int(mstep)):
            vol=mvol/1000 # mV -> V
            self.kei2400c.write(":source:voltage:level "+str(vol))
            time.sleep(0.1/speed)

    def display_current(self):
        self.kei2400c.write(":sense:function 'current'")
        # self.kei2400c.write(":sense:current:range "+self.cmpl)
        self.kei2400c.write(":sense:current:range:auto on")
        self.kei2400c.write(":display:enable on")
        self.kei2400c.write(":display:digits 7")
        self.kei2400c.write(":form:elem current")
        current=self.kei2400c.query(":read?")
        #self.kei2400c.timeout=5000
        print("current [A]:  " + str(current))
        return float(str(current))

    def hit_compliance(self):
        tripped=int(str(self.kei2400c.query(":SENSE:CURRENT:PROTECTION:TRIPPED?")))
        if tripped:
            print("Hit the compliance "+self.cmpl+"A.")
        return tripped

    def output_on(self):
        self.kei2400c.write(":output on")
        print("On")

    def output_off(self):
        self.kei2400c.write(":output off")
        print("Off")

    def beep(self, freq=1046.50, duration=0.3):
        self.kei2400c.write(":system:beeper "+str(freq)+", "+str(duration))
        time.sleep(duration)

    def filter_on(self, count=20, mode="repeat"):
        self.kei2400c.write(":sense:average:count "+str(count))
        self.kei2400c.write(":sense:average:tcontrol "+mode) # repeat or moving
        self.kei2400c.write(":sense:average:state on")

    def filter_off(self):
        self.kei2400c.write(":sense:average:state off")

    def __del__(self):
        self.kei2400c.close()

if __name__=="__main__":
    # kei2400c=keithley2400c("ASRL1::INSTR")
    kei2400c=keithley2400c("ASRL15::INSTR")
    kei2400c.testIO()

