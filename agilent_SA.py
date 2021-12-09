import pyvisa
from matplotlib import pyplot as plt


rm = pyvisa.ResourceManager()
current_instr = "GPIB0::21::INSTR"
# class
inst = rm.open_resource(current_instr,send_end=False)


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

    def setRefLeve(self, Amp, unit="dBm"):
        responce = self.instr.write("DISP:WIND:TRAC:Y:RLEV " + Amp + unit)
        return responce

    def getRefLeve(self):
        responce = self.instr.query("DISP:WIND:TRAC:Y:RLEV?")
        return responce

    #set SA Attenuation
    def setMechAtten(self, att):
        responce = self.instr.write("POW:ATT " + att)
        return responce

    #get SA Attenuation
    def getMechAtten(self):
        responce = self.instr.query("POW:ATT?")
        return responce

    def setMechAttenAuto(self):
        responce = self.instr.write("POW:ATT:AUTO 1")
        return responce

    def getMechAttenAuto(self):
        responce = self.instr.query("POW:ATT:AUTO?")
        return responce


class Fetch:
    def __init__(self):
        pass

    def fetchData(self): 
    #
    #FETC:SAN1?
        self.instr.timeout = 550000
        responce = self.instr.write("CALC: DATA?")
        responce = self.instr.read()
        return responce

class TraceDetector:
    def __init__(self):
        pass

    def setTraceType(self, trace='1', traceType='AVER'):
        #trace={1...6} traceType=WRIT or AVER or MAXH ot MINH 
        responce = self.instr.query("TRAC{}:TYPE {}".format(trace,traceType))
        return responce


class AnalyzerSetUp(Freq, Span, Amptd, Fetch, TraceDetector):
    def __init__(self, instr):
        self.instr = instr


class AgilentSA(AnalyzerSetUp):
    def __init__(self, instr):
        self.instr = instr


def main():
    new_instr = AgilentSA(inst)
    new_instr.centFreq("5180")
    print(float(new_instr.getStartFreq()))
    print("getCentFreq:", float(new_instr.getCentFreq()), "Hz")
    print("getStartFreq:", float(new_instr.getStartFreq()), "Hz")
    print("getStopFreq:", float(new_instr.getStopFreq()), "Hz")
    new_instr.setSpan('100')
    print("getSpan:", float(new_instr.getSpan()), "Hz")
    new_instr.setRefLeve('10')
    print("getRefLeve:", float(new_instr.getRefLeve()), "dBm")
    new_instr.setMechAtten('10')
    print("getAttenuationStatus(1:ON,0:OFF):", new_instr.getMechAttenAuto())
    print("getAttenuation:", float(new_instr.getMechAtten()), "dB")
    new_instr.setTraceType()
    # new_instr.setMechAttenAuto()
    # print("getAttenuationStatus(1:ON,0:OFF):", new_instr.getMechAttenAuto())
    # print("getAttenuation:", float(new_instr.getMechAtten()), "dB")
    trace = new_instr.fetchData()
    print(trace)
    amp = trace[1::2]
    freq = trace[::2]
    newFreq = []
    newAmp = []
    limitLine = []
    #print(freq)
    #print(amp)

    for f in freq:
        newFreq.append(float(f)/1000000)
    for a in amp:
        newAmp.append(float(a)+22)
    print(len(newFreq))
    print(len(newAmp))

    #axs[0, 0].set_title("Signal")
    #axs[0, 0].plot(t, s, color='C0')
    #axs[0, 0].set_xlabel("Time")
    #axs[0, 0].set_ylabel("Amplitude")
    fig, ax = plt.subplots()

    #plt.grid(True)
    ax.set(xlabel='freq', ylabel='amp (dBm)',
           title='About as simple as it gets, folks')
    xrange = (min(newFreq), max(newFreq))
    yrange = (min(newAmp)-10, max(newAmp)+10)
    for i in range(len(newFreq)):
        limitLine.append(10.0)

    ax.set_xlim(xrange)
    ax.set_ylim(yrange)
    ax.grid()
    ax.plot(newFreq, newAmp)
    ax.plot(newFreq, limitLine, color='red')
    plt.show()

if __name__ == '__main__':
    main()
