from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from scipy.io import wavfile
from scipy.fftpack import fft,fftfreq
from numpy.lib.function_base import angle
from calibratesdr.dvbt import dvbt_const as dc
import os
from rtlsdr import RtlSdr


# def file_input():
#     '''
#     Input the data file.
#     '''
#     os.chdir('calibratesdr/dvbt/test')
#     filename = input("Input Recorded File Name:")
#     # filename = 'DVB-T 5MHz 5333333sps_IQ.wav'
#     frequency_center = int(input("Central Frequency:"))
#     # frequency_center = 5333333
#     samplerate, data = wavfile.read(filename)
#     return data,samplerate,frequency_center


def wavtoiq(data):
    '''
    Convert the Interleaved IQ wav file to complex format
    '''
    data = np.ravel(data)
    iq_data = data[0::2] + 1j*data[1::2]
    return iq_data


def run_dsp(iq_data):

    constellations, num_symbols = get_constellations(iq_data)
    return constellations, num_symbols


def get_constellations(iq_data):
    '''
    Find the start of a symbol and extract constellation data
    '''
    
    iq_dc = iq_data - np.mean(iq_data)
    
    first_symbol = _find_start_symbol(iq_dc)
    
    num_symbols = (len(iq_dc) - first_symbol) // dc.SYMBOL_LENGTH
    
    iq_dc = iq_dc[first_symbol:num_symbols*dc.SYMBOL_LENGTH+first_symbol]
    
    carriers_data = _extract_data(iq_dc, num_symbols)
    
    return carriers_data, num_symbols
    
def _find_start_symbol(iq_data):
    '''
    Correlate to find symbol boundaries
    '''
    
    corr_length = 2*(dc.SYMBOL_LENGTH)
    corr = np.empty(corr_length)
    
    for k in range(corr_length):
        leading = iq_data[k:k+dc.GUARD_LENGTH]
        trailing = iq_data[k+dc.USEFUL_LENGTH:k+dc.SYMBOL_LENGTH]
        corr[k] = np.abs(np.dot(leading, np.conj(trailing)))
    
    first_symbol = np.argmax(corr)%(dc.SYMBOL_LENGTH)
    
    return first_symbol

    
def _extract_data(iq_data, num_symbols):
    '''
    Take FFTs to get the data:
    '''

    carriers = np.empty(dc.NUM_CARRIERS, 'complex')
    carriers_data = np.empty((num_symbols, dc.NUM_CARRIERS), 'complex')

    for k in range(num_symbols):
        start_indx = k*dc.SYMBOL_LENGTH + dc.GUARD_LENGTH//2
        end_indx  = start_indx + dc.USEFUL_LENGTH
        symbol_data = iq_data[start_indx:end_indx]
        spec = np.fft.fft(symbol_data)

        #-------------------------
        # expect carrier 3407 to be at DC, so:
        #carriers[0:3408] = spec[-3408:]
        #carriers[3408:6817] = spec[0:3409]

        # however carrier 3408 is at DC, so:
        carriers[0:3407] = spec[-3407:]   
        carriers[3407:6817] = spec[0:3410]
        #-------------------------   

        start_indx = k*dc.NUM_CARRIERS
        end_indx   = start_indx + dc.NUM_CARRIERS

        carriers_data[k,:] = carriers
    
    return carriers_data


def get_offset(carriers_data, num_symbols, samplerate, show_graph):

    offset=  _pilot_phase_change(carriers_data, num_symbols, samplerate, show_graph)
    
    return offset 


def _pilot_phase_change(carriers_data, num_symbols ,samplerate, show_graph):
    '''
    Calculate 'average' change in phase between pilot carriers from symbol
    to symbol. Fix frequency and sampling rate offsets
    '''
    
    num_pilots = len(dc.CONTINUAL_PILOT_CARRIERS)
    avging_lngth = 50 # empirically found to work well
    num_symbols -= avging_lngth 

    pilot_delta_phase = np.empty((num_symbols,num_pilots))
    freq_offset = np.empty((num_symbols,num_pilots))

    for k,pilot_num in enumerate(dc.CONTINUAL_PILOT_CARRIERS):
        pilot_data = carriers_data[:,pilot_num]
        T = 1/samplerate

        # calculate diff_vecs = r1*r2*e^i(theta2 - theta1)
        diff_vecs = pilot_data[0:-1].conj()*pilot_data[1:] 
        cumsum_diff_vecs = np.cumsum(diff_vecs)
        cumsum_diff_vecs = np.insert(cumsum_diff_vecs, 0, 0)

        for kk in range(num_symbols):            
            sum_diff_vecs = cumsum_diff_vecs[kk+avging_lngth] - \
                                                         cumsum_diff_vecs[kk]
            pilot_delta_phase[kk,k] = np.angle(sum_diff_vecs)

            # calculate freq_offset = (1 / (2*np.pi*N*Ts))* np.angle(delta_phase_diff)
            freq_offset[kk,k] = (1 / (2*np.pi*1*T)) * (pilot_delta_phase[kk,k])

    offset = np.mean(freq_offset) / (num_symbols * num_pilots)
    # print("Offset:" ,offset)
    # if show_graph == True:
    show_offset(freq_offset,num_symbols)

    return offset


def get_ppm(data,samplerate,frequency_center,show_graph):   #data, samplerate, show_graph = False, verbose = False):
	
    # frequency offset calculation

    iq_data = wavtoiq(data)
    data_carriers, num_symbols = run_dsp(iq_data)
    offset = get_offset(data_carriers, num_symbols, samplerate, show_graph)
    

    if show_graph == True:
        signal_graph(data,samplerate)

    ppm = (offset / frequency_center) * 1e6 * 1e3
    return ppm


def signal_graph(data,samplerate):

    #Plot data
    plt.title("DVB-T Signal Spectrum")
    plt.plot(data)
    plt.grid()
    plt.show()
    #Power spectral density
    plt.specgram(data, NFFT=1024, Fs=samplerate)
    plt.title("PSD of the DVB-T signal")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.show()

def show_offset(freq_offset,num_symbols):
    '''
    Shows the graph to changing frequency offset.
    '''
    plt.plot(freq_offset[num_symbols-1,::])
    plt.title("Change in Frequency offset over time")
    plt.grid()
    plt.xlabel("Time")
    plt.ylabel("Frequency Offset")    
    plt.show()


def main(frequency_center,samplerate,show_graph):

    # SDR presets
    device = input["rd"]  
    gain = input("Gain")
    t = input["nsec"]
    print("Finding DVB-T signals Offset:")
    sdr = RtlSdr(device_index=device)
    sdr.sample_rate = samplerate
    sdr.gain = gain
    sdr.center_freq = frequency_center
    data = sdr.read_samples(samplerate*t)
    sdr.close()

    # else:
    #     file_input():
    #     data,samplerate,frequency_center = data,samplerate,frequency_center
    
    ppm = get_ppm(data,samplerate,frequency_center,show_graph)

    print("your sdr's precision is", ppm, " ppm")

    print("This is the DVB-T support so far available.")

if __name__ == '__main__':
    main()

