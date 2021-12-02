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
        responce = self.instr.write("FREQ:CENT " + Freq + "MHZ")
        return responce
    #set SA startFreq
    def startFreq(self, Freq, unit="MHz"):
        responce = self.instr.write("FREQ:START " + Freq + "MHZ")
        return responce
    #set SA stopFreq
    def stopFreq(self, Freq, unit="MHz"):
        responce = self.instr.write("FREQ:STOP " + Freq + "MHZ")
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


class AgilentSA(Freq):
    def __init__(self, instr):
        self.instr=instr
    


new_instr = AgilentSA(inst)
new_instr.centFreq("5200")
print(type(new_instr.getStartFreq()))
print("getCentFreq:", format(new_instr.getCentFreq(),"5f.4"))
print("getStartFreq:", new_instr.getStartFreq())
print("getStopFreq:", new_instr.getStopFreq())


