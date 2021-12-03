import pyvisa


rm = pyvisa.ResourceManager()
current_instr="GPIB0::21::INSTR"
# class
inst = rm.open_resource(current_instr)


# def centFreq(inst,Freq,unit="MHz"):
#     responce=inst.write("FREQ:CENT " + Freq + "MHZ")
#     print(responce)

# centFreq(inst,"5200")



class Freq:
    def __init__(self, instr):
        self.instr = instr
    #set SA centFreq
    def centFreq(self, Freq, unit="MHz"):
        responce = self.instr.write("FREQ:CENT " + Freq + unit)
        return responce
    #set SA startFreq
    def startFreq(self, Freq, unit="MHz"):
        responce = self.instr.write("FREQ:START " + Freq + unit)
        return responce
    #set SA stopFreq
    def stopFreq(self, Freq, unit="MHz"):
        responce = self.instr.write("FREQ:STOP " + Freq + unit)
        return responce
    #get SA CentFreq
    def getCentFreq(self):
        responce = self.instr.query("FREQ:CENT?")
        return responce
    #get SA StartFreq
    def getStartFreq(self):
        responce = self.instr.query("FREQ:START?")
        return responce
    #get SA StopFreq
    def getStopFreq(self):
        responce = self.instr.query("FREQ:STOP?")
        return responce


class Span:
    def __init__(self, instr):
        self.instr = instr

    #set SA SPAN
    def setSpan(self, Freq, unit="MHz"):
        responce = self.instr.write("FREQ:SPAN " + Freq + unit)
        return responce
    
    #get SA SPAN
    def getSpan(self):
        responce = self.instr.query("FREQ:SPAN?")
        return responce
    
    #get SA SPAN
    def setFullSpan(self):
        responce = self.instr.write("FREQ:SPAN:FULL")
        return responce


class Amptd:
    def __init__(self, instr):
        self.instr = instr
    
    def SetRefLeve(self, Amp, unit="dBm"):
        responce = self.instr.write("DISP:WIND:TRAC:Y:RLEV " + Amp + unit)
        return responce
    def GetRefLeve(self):
        responce = self.instr.query("DISP:WIND:TRAC:Y:RLEV?")
        return responce

    
class AgilentSA(Freq, Span,Amptd):
    def __init__(self, instr):
        self.instr = instr
    

def main():
    new_instr = AgilentSA(inst)
    new_instr.centFreq("5200")
    print(float(new_instr.getStartFreq()))
    print("getCentFreq:", float(new_instr.getCentFreq()),"Hz")
    print("getStartFreq:", float(new_instr.getStartFreq()),"Hz")
    print("getStopFreq:", float(new_instr.getStopFreq()),"Hz")
    new_instr.setSpan('40')
    print("getSpan:", float(new_instr.getSpan()), "Hz")
    new_instr.SetRefLeve('10')
    print("getRefLeve:", float(new_instr.GetRefLeve()), "dBm")


if __name__ == '__main__':
    main()



