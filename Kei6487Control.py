import visa
import time
import warnings

class keithley6487:
    def __init__(self,resource_name):
        instlist=visa.ResourceManager()
        print(instlist.list_resources())
        self.kei6487=instlist.open_resource(resource_name)
        self.kei6487.timeout=25000
        self.kei6487.write("*RST")
        self.kei6487.write(":sense:function 'current'")
        self.kei6487.write(":form:elem read")
        self.kei6487.write(":display:digits 7")
        #self.zero_correction()

    def testIO(self):
        message=self.kei6487.query('*IDN?')
        print(message)

    def zero_correction(self):
        self.kei6487.write("syst:zch on")
        self.kei6487.write("curr:rang 2e-9")
        self.kei6487.write("init")
        self.kei6487.write("syst:zcor:stat off")
        self.kei6487.write("syst:zcor:acq")
        self.kei6487.write("syst:zcor on")
        self.kei6487.write("curr:rang:auto on")
        self.kei6487.write("syst:zch off")

    def display_current(self):
        self.kei6487.write("syst:zch off")
        current=self.kei6487.query(":read?")
        print("current [A]:  " + str(current))
        return float(str(current))

    def display_on(self):
        self.kei6487.write(":display:enable on")

    def display_off(self):
        self.kei6487.write(":display:enable off")

    def filter_on(self, count=10, mode="repeat"):
        self.kei6487.write(":sense:average:count "+str(count))
        self.kei6487.write(":sense:average:tcontrol "+mode) # repeat or moving
        self.kei6487.write(":sense:average:state on")

    def filter_off(self):
        self.kei6487.write(":sense:average:state off")

    def __del__(self):
        self.kei6487.close()

if __name__=="__main__":
    kei6487=keithley6487("ASRL16::INSTR")
    kei6487.testIO()
    kei6487.zero_correction()

