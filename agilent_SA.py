import pyvisa
from matplotlib import pyplot as plt

rm = pyvisa.ResourceManager()

current_instr = "GPIB0::21::INSTR"
# class
inst = rm.open_resource(current_instr,send_end=False)


# def centFreq(inst,Freq,unit="MHz"):
#     response=inst.write("FREQ:CENT " + Freq + "MHZ")
#     print(response)

# centFreq(inst,"5200")

class Freq:
    def __init__(self, instr):
        self.instr = instr
    #set SA centFreq

    def cent_freq(self, Freq, unit="MHz"):
        response = self.instr.write("FREQ:CENT " + Freq + unit)
        return response
    #set SA startFreq

    def start_freq(self, Freq, unit="MHz"):
        response = self.instr.write("FREQ:START " + Freq + unit)
        return response
    #set SA stopFreq

    def stop_freq(self, Freq, unit="MHz"):
        response = self.instr.write("FREQ:STOP " + Freq + unit)
        return response
    #get SA CentFreq

    def get_cent_freq(self):
        response = self.instr.query("FREQ:CENT?")
        return response
    #get SA StartFreq

    def get_start_freq(self):
        response = self.instr.query("FREQ:START?")
        return response
    #get SA StopFreq

    def get_stop_freq(self):
        response = self.instr.query("FREQ:STOP?")
        return response


class Span:
    def __init__(self, instr):
        self.instr = instr

    #set SA SPAN
    def set_span(self, Freq, unit="MHz"):
        response = self.instr.write("FREQ:SPAN " + Freq + unit)
        return response

    #get SA SPAN
    def get_span(self):
        response = self.instr.query("FREQ:SPAN?")
        return response

    #get SA SPAN
    def set_full_span(self):
        response = self.instr.write("FREQ:SPAN:FULL")
        return response


class Amptd:
    def __init__(self, instr):
        self.instr = instr

    def set_ref_leve(self, Amp, unit="dBm"):
        response = self.instr.write("DISP:WIND:TRAC:Y:RLEV " + Amp + unit)
        return response

    def get_ref_leve(self):
        response = self.instr.query("DISP:WIND:TRAC:Y:RLEV?")
        return response

    #set SA Attenuation
    def set_mech_atten(self, att):
        response = self.instr.write("POW:ATT " + att)
        return response

    #get SA Attenuation
    def get_mech_atten(self):
        response = self.instr.query("POW:ATT?")
        return response

    def set_mech_attenAuto(self):
        response = self.instr.write("POW:ATT:AUTO 1")
        return response

    def get_mech_atten_auto(self):
        response = self.instr.query("POW:ATT:AUTO?")
        return response

class Bw:
    def __init__(self, instr):
        self.instr = instr
    
    def set_res_bw(self,rbw='1',unit='K'):
        #nuit = K,M
        response = self.instr.write("BAND {} {}HZ".format(rbw,unit))
        return response
    
    def get_res_bw(self):
        response = self.instr.query('BAND?')
        return response
    
    def set_res_bw_auto(self, states='ON'):
        response = self.instr.write("BWID:AUTO {}".format(states))
        return response

    def get_res_bw_auto(self):
        response = self.instr.query("BWID:AUTO?")
        return response
    
    def set_video_bw(self,vbw='1',unit='k'):
        #nuit = K,M
        response = self.instr.write("BAND:VID {} {}HZ".format(vbw, unit))
        return response
    
    def get_video_bw(self):
        response = self.instr.query('BAND:VID?')
        return response
    
    def set_video_bw_auto(self, states='ON'):
        response = self.instr.write("BWID:VID:AUTO {}".format(states))
        return response

    def get_video_bw_auto(self):
        response = self.instr.query("BWID:VID:AUTO?")
        return response
    


class Fetch:
    def __init__(self):
        pass

    def fetch_data(self): 
    #FETC:SAN1?
        self.instr.timeout = 100000
        self.instr.read_termination = "\n"
        response = self.instr.query("CALC:DATA?")
        # response = self.instr.query("FETC:SAN1?")
        return response

    def fetch_chp(self):
        pass
        # self.instr.timeout = 100000
        # self.instr.read_termination = "\n"
        # response = self.instr.query(":FETC:CHP?")
        # return response


class TraceDetector:
    def __init__(self):
        pass

    def set_trace_type(self, trace='1', traceType='AVER'):
        # trace={1...6} traceType=WRIT or AVER or MAXH ot MINH 
        #print("TRAC{}:TYPE {}".format(trace, traceType))
        response = self.instr.write("TRAC{}:TYPE {}".format(trace, traceType))
        return response

    def set_detector(self, trace='1', detType='AVER'):
        #detType = AVER ，NEG ， NORM ，POS，SAMP，QPE，EAV，RAV
        response = self.instr.write("DET:TRAC{} {}".format(trace, detType))
        return response

    def get_detector(self, trace='1'):
        #detType = AVER ，NEG ， NORM ，POS，SAMP，QPE，EAV，RAV
        response = self.instr.query("DET:TRAC{}?".format(trace))
        return response




class Meas:
    def __init__(self,instr):
        self.instr = instr

    def set_mode(self,mode):
        if mode == 'CHP':
            response = self.instr.write(":CONF:CHP")
            return response
            
    def integ_bw(self,bw='20',unit='M'):
        response = self.instr.write(":CHP:BAND:INT {}".format(bw)+"{}Hz".format(unit))
        return response

    def get_integ_bw(self):
        response = self.instr.query(":CHP:BAND:INT?")
        return response

class AnalyzerSetUp(Freq, Span, Amptd, Fetch, TraceDetector, Bw, Meas):
    def __init__(self, instr):
        self.instr = instr
        
class AgilentSA(AnalyzerSetUp):
    def __init__(self, instr):
        self.instr = instr
    
    def get_sa_mode(self):
        response=self.instr.query(':CONF?')
        return response



def main():
    new_instr = AgilentSA(inst)
    new_instr.cent_freq("5180")
    print(float(new_instr.get_start_freq()))
    print("getCentFreq:", float(new_instr.get_cent_freq()), "Hz")
    print("getStartFreq:", float(new_instr.get_start_freq()), "Hz")
    print("getStopFreq:", float(new_instr.get_stop_freq()), "Hz")
    new_instr.set_span('100')
    print("getSpan:", float(new_instr.get_span()), "Hz")
    new_instr.set_ref_leve('10')
    print("getRefLeve:", float(new_instr.get_ref_leve()), "dBm")
    new_instr.set_mech_atten('10')
    print("getAttenuationStatus(1:ON,0:OFF):", new_instr.get_mech_atten_auto())
    print("getAttenuation:", float(new_instr.get_mech_atten()), "dB")
    new_instr.set_trace_type('1', 'MAXH')
    new_instr.set_detector('1', 'AVER')
    print('get_detector:', new_instr.get_detector())
    print('get_detector:', new_instr.get_sa_mode())

    print("get_res_bw",new_instr.get_res_bw())
    new_instr.set_res_bw('100')
    print("get_res_bw", new_instr.get_res_bw())
    print("get_video_bw", new_instr.get_video_bw())
    new_instr.set_video_bw('300')
    print("get_video_bw", new_instr.get_video_bw())

    new_instr.set_mode('CHP')
    # print("get_video_bw_auto", new_instr.get_video_bw_auto())
    # print("get_res_bw_auto", new_instr.get_res_bw_auto())
    # new_instr.set_res_bw_auto()
    # new_instr.set_video_bw_auto()
    # print("get_video_bw_auto", new_instr.get_video_bw_auto())
    # print("get_res_bw_auto", new_instr.get_res_bw_auto())



    # new_instr.setMechAttenAuto()
    # print("getAttenuationStatus(1:ON,0:OFF):", new_instr.getMechAttenAuto())
    # print("getAttenuation:", float(new_instr.getMechAtten()), "dB")
    # trace = new_instr.fetch_data()
    # trace=trace.split(',')
    # print(trace)
    # amp = trace[1::2]
    # freq = trace[::2]
    # newFreq = []
    # newAmp = []
    # limitLine = []
    #print(freq)
    #print(amp)
    # for f in freq:
    #     newFreq.append(float(f)/1000000)
    # for a in amp:
    #     newAmp.append(float(a)+22)
    # print(len(newFreq))
    # print(len(newAmp))
    # axs[0, 0].set_title("Signal")
    # axs[0, 0].plot(t, s, color='C0')
    # axs[0, 0].set_xlabel("Time")
    #axs[0, 0].set_ylabel("Amplitude")
    
    #fig, ax = plt.subplots()

    #plt.grid(True)
    #####################
    # ax.set(xlabel='freq', ylabel='amp (dBm)',
    #        title='About as simple as it gets, folks')
    # xrange = (min(newFreq), max(newFreq))
    # yrange = (min(newAmp)-10, max(newAmp)+10)
    # for i in range(len(newFreq)):
    #     limitLine.append(10.0)

    # ax.set_xlim(xrange)
    # ax.set_ylim(yrange)
    # ax.grid()
    # ax.plot(newFreq, newAmp)
    # ax.plot(newFreq, limitLine, color='red')
    # plt.show()

if __name__ == '__main__':
    main()
