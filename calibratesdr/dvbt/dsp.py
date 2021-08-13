'''
Various DSP functions, calling run_dsp will run the entire DSP chain.
'''

from __future__ import division

import numpy as np
from dvbt_const import *
import logging

def run_dsp(iq_data):
    constellations, num_symbols = get_constellations(iq_data)
    clock_aligned_carriers =  align_clocks(constellations, num_symbols)
    super_frame_start = get_tps_data(clock_aligned_carriers)
    data_carriers = channel_correction(clock_aligned_carriers, 
                                       super_frame_start)

    return data_carriers, super_frame_start

def get_constellations(iq_data):
    '''
    Find the start of a symbol and extract constellation data
    '''
    
    iq_dc = iq_data - np.mean(iq_data)
    
    first_symbol = _find_start_symbol(iq_dc)
    
    num_symbols = (len(iq_dc) - first_symbol) // SYMBOL_LENGTH
    
    iq_dc = iq_dc[first_symbol:num_symbols*SYMBOL_LENGTH+first_symbol]
    
    carriers_data = _extract_data(iq_dc, num_symbols)
    
    return carriers_data, num_symbols
    

def align_clocks(carriers_data, num_symbols):
    ''' 
    Fix frequency and sampling rate offsets
    '''
    
    pilot_delta_phase, num_symbols, first_symbol = _pilot_phase_change(
                                                 carriers_data, num_symbols)
  
    all_delta_phase = _carrier_phase_change(pilot_delta_phase, num_symbols)
    
    carriers_data = carriers_data[first_symbol:first_symbol+num_symbols,:]
    
    all_carriers_clock_aligned = _de_rotate_carriers(carriers_data, 
                                                     all_delta_phase)

  
    return all_carriers_clock_aligned


def _find_start_symbol(iq_data):
    '''
    Correlate to find symbol boundaries
    '''
    
    corr_length = 2*(SYMBOL_LENGTH)
    corr = np.empty(corr_length)
    
    for k in range(corr_length):
        leading = iq_data[k:k+GUARD_LENGTH]
        trailing = iq_data[k+USEFUL_LENGTH:k+SYMBOL_LENGTH]
        corr[k] = np.abs(np.dot(leading, np.conj(trailing)))
    
    first_symbol = np.argmax(corr)%(SYMBOL_LENGTH)
    
    return first_symbol

    
def _extract_data(iq_data, num_symbols):
    '''
    Take FFTs to get the data:
    '''

    carriers = np.empty(NUM_CARRIERS, 'complex')
    carriers_data = np.empty((num_symbols, NUM_CARRIERS), 'complex')

    for k in range(num_symbols):
        start_indx = k*SYMBOL_LENGTH + GUARD_LENGTH//2
        end_indx  = start_indx + USEFUL_LENGTH
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

        start_indx = k*NUM_CARRIERS
        end_indx   = start_indx + NUM_CARRIERS

        carriers_data[k,:] = carriers
    
    return carriers_data

    
def _pilot_phase_change(carriers_data, num_symbols):
    '''
    Calculate 'average' change in phase between pilot carriers from symbol
    to symbol:
    '''
    
    num_pilots = len(CONTINUAL_PILOT_CARRIERS)
    avging_lngth = 100 # empirically found to work well
    num_symbols -= avging_lngth 
    pilot_delta_phase = np.empty((num_symbols,num_pilots))

    for k,pilot_num in enumerate(CONTINUAL_PILOT_CARRIERS):
        pilot_data = carriers_data[:,pilot_num]
        
        # calculate diff_vecs = r1*r2*e^i(theta2 - theta1)
        diff_vecs = pilot_data[0:-1].conj()*pilot_data[1:] 
        cumsum_diff_vecs = np.cumsum(diff_vecs)
        cumsum_diff_vecs = np.insert(cumsum_diff_vecs, 0, 0)

        for kk in range(num_symbols):            
            sum_diff_vecs = cumsum_diff_vecs[kk+avging_lngth] - \
                                                         cumsum_diff_vecs[kk]
            pilot_delta_phase[kk,k] = np.angle(sum_diff_vecs)
            
    first_symbol = 1+avging_lngth//2
       
    return pilot_delta_phase, num_symbols, first_symbol

    
def _carrier_phase_change(pilot_delta_phase, num_symbols):
    '''
    Find change in phase between all carriers from symbol to symbol:
    '''
    
    all_delta_phase = np.empty((num_symbols, NUM_CARRIERS))
    carrier_indcs = np.arange(NUM_CARRIERS)

    for k in range(num_symbols):
        p_fit = np.polyfit(CONTINUAL_PILOT_CARRIERS, pilot_delta_phase[k,:],
                           1)

        all_delta_phase[k,:] = p_fit[0]*carrier_indcs + p_fit[1]
        
    return all_delta_phase

    
def _de_rotate_carriers(carriers_data, all_delta_phase):
    '''
    Stop carriers from spining by de-rotating all carriers:
    '''
    
    all_delta_phase[0,:] = 0
    phase_corrections = np.cumsum(all_delta_phase, axis=0)
    mix_sig = np.exp(-1j*phase_corrections)
    all_carriers_clock_aligned = carriers_data*mix_sig
    
    return all_carriers_clock_aligned


def get_tps_data(carrier_data):
    ''' 
    Extract TPS data
    '''
    
    bit_data = _extract_bit_data(carrier_data)

    frame_start = _find_frame_start(bit_data)
    bit_data = bit_data[frame_start:]
    
    frame_number = _extract_data_fields(bit_data)
    
    return _find_super_frame_start(frame_start, frame_number)


def _find_super_frame_start(frame_start, frame_number):
    '''
    Find symbol number of the start of the first super frame
    '''

    return (frame_start - frame_number*NUM_SYMBOLS_FRAME) \
                             % (NUM_SYMBOLS_FRAME*NUM_FRAMES_SUPER_FRAME)

   
def _extract_bit_data(carrier_data):
    '''
    Extract bit data from one of the TPS carriers
    '''
    
    tps_ind = 34 # index of one of the TPS carriers - arbitrary choice
    
    tps_carrier = carrier_data[:,tps_ind]
    tps_carrier_norm = tps_carrier/np.absolute(tps_carrier)
    diffs = tps_carrier[1:]*np.conj(tps_carrier_norm[0:-1])
    bit_data = diffs < 0
    
    return bit_data.astype('int')

   
def _find_frame_start(bit_data):
    '''
    Look for synchronisation word in bit data to find symbol number of the 
    start of a frame
    '''    
    
    sync_pattern = np.array([0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0])
    
    matched_filter = np.empty(len(bit_data) - len(sync_pattern))
    
    for k in range(len(matched_filter)):
        matched_filter[k] = np.sum(bit_data[k:k+len(sync_pattern)] 
                                                       ^ sync_pattern)
    
    return np.argmax(matched_filter)


def _extract_data_fields(bit_data):
    '''
    Extract and print data fields. Bit positions are given in 
    ETSI EN 300 744 V1.5.1
    '''
    
    tps_lngth = bit_data[16:22]
    logging.info('TPS Length: {}'.format(tps_lngth))
    
    frame_number = bit_data[22:24]
    logging.info('Frame Number: {}'.format(tps_lngth))
    
    constellation = bit_data[24:26]
    logging.info('Constellation: {}'.format(constellation))
    
    hierarchy = bit_data[26:29]
    logging.info('Hierarchy: {}'.format(hierarchy))
    
    code_rate = bit_data[29:32]
    logging.info('HP Stream Code_rate: {}'.format(code_rate))

    code_rate = bit_data[32:35]
    logging.info('LP Stream Code_rate: {}'.format(code_rate))

    guard_interval = bit_data[35:37]
    logging.info('Guard Interval: {}'.format(guard_interval))

    transmission_mode = bit_data[37:39]
    logging.info('Transmission Mode: {}'.format(transmission_mode))

    cell_identifier = bit_data[39:47]
    logging.info('Cell Identifier: {}'.format(cell_identifier))
  
    frame_number_int = 2*frame_number[0] + frame_number[1]
    logging.info('Frame number int: {}'.format(frame_number_int))
    
    return frame_number_int


def channel_correction(clock_aligned_carriers, super_frame_start):
    '''
    Correct for effects of transmission channel 
    '''
    
    channel_corrected_carriers = _correct_each_carrier(
                                   clock_aligned_carriers, super_frame_start)
                                   
    return _correct_each_symbol(channel_corrected_carriers, 
                                                           super_frame_start)


def _correct_each_symbol(channel_corrected_carriers, super_frame_start):
    '''
    Iterate across symbols correcting for rotation anomalies. Return data
    carriers
    '''

    num_symbols = channel_corrected_carriers.shape[0]
    carrier_indcs = _CarrierIndcs(super_frame_start)
 
    all_data_carriers = np.empty((num_symbols,NUM_DATA_CARRIERS), 'complex')   
    for k in range(num_symbols):
        non_data_carriers, data_carriers = carrier_indcs.get_indcs(k)        
        rot = _calc_rotation(channel_corrected_carriers[k,non_data_carriers])
    
        all_data_carriers[k,:] = channel_corrected_carriers[k,data_carriers]\
                                                            *np.exp(1j*rot)
                                                              
    return all_data_carriers

    
def _calc_rotation(carriers):
    
    pos_indcs = carriers.real > 0

    pos = carriers[pos_indcs]
    neg = carriers[~pos_indcs]

    return -np.angle(np.sum(pos) - np.sum(neg))


class _CarrierIndcs(object):
    def __init__(self, super_frame_start):
        self.super_frame_start = super_frame_start
        
        tps_carriers = set(TPS_CARRIERS)
        continual_pilot_carriers = set(CONTINUAL_PILOT_CARRIERS)   
    
        all_non_data_carriers = [0]*4
        all_data_carriers = [0]*4
    
        for k in range(4):
            # location of scattered carriers are defined in 
            # ETSI EN 300 744 V1.5.1 sec. 4.5.3
            scattered_indcs = set(range(k*3, NUM_CARRIERS, 12))
            non_data_carriers = scattered_indcs | continual_pilot_carriers \
                                                             | tps_carriers
                                                             
            data_carriers = set(range(NUM_CARRIERS)) - non_data_carriers
            all_non_data_carriers[k] = np.array(list(non_data_carriers)) 
            all_data_carriers[k] = np.array(list(data_carriers))
            
        self.all_non_data_carriers = all_non_data_carriers
        self.all_data_carriers = all_data_carriers
        
    def get_indcs(self, symbol_num):
        frame_number = (symbol_num - self.super_frame_start)%4
        
        non_data_carriers = self.all_non_data_carriers[frame_number]
        data_carriers = self.all_data_carriers[frame_number]
        
        return non_data_carriers, data_carriers


def _correct_each_carrier(clock_aligned_carriers, super_frame_start):
    '''
    Iterate across carriers correcting for rotation and scale variation due
    to transmission channel. The processing applied varies depending on the
    channel type
    '''
    
    num_symbols = clock_aligned_carriers.shape[0]
    
    channel_estimator = _ChannelEstimator(super_frame_start, num_symbols)
    
    
    channel_estimates = np.empty(NUM_CARRIERS,'complex')
    channel_corrected_carriers = np.empty(clock_aligned_carriers.shape, 
                                          'complex')
    
    for carrier in range(NUM_CARRIERS):
        
        carrier_data = clock_aligned_carriers[:,carrier]
        
        if carrier in CONTINUAL_PILOT_CARRIERS:
            corrected_carriers, channel_est = channel_estimator.cp(
                                                       carrier_data, carrier)
                                                       
        elif carrier in TPS_CARRIERS:
            corrected_carriers, channel_est = channel_estimator.tps(
                                  carrier_data, channel_estimates[carrier-1])
                                  
        elif (carrier%3)==0:
            # carrier with scattered pilots          
            corrected_carriers, channel_est = channel_estimator.sp(
                                                       carrier_data, carrier)
                                                       
        else:
            corrected_carriers, channel_est = channel_estimator.dat(
                                  carrier_data, channel_estimates[carrier-1])
            
        channel_corrected_carriers[:,carrier] = corrected_carriers
        channel_estimates[carrier] = channel_est
            
    return channel_corrected_carriers

  
class _ChannelEstimator(object):
    def __init__(self, super_frame_start, num_symbols):
        self.num_symbols = num_symbols
        
        #Calculate PRBS as defined in ETSI EN 300 744 V1.5.1 sec. 4.5.2
        wk = np.ones(NUM_CARRIERS)        
        for k in range(11, NUM_CARRIERS):
            wk[k] = (wk[k-11] + wk[k-9])%2            
        self.wk = -2*wk + 1
        
        # calculate all pilot indcs, scattered pilot indcs as defined in 
        # ETSI EN 300 744 V1.5.1 sec. 4.5.3
        all_pilots = [0]*4
        for k in range(4):
            all_pilots[k] = range((k + super_frame_start)%4, num_symbols, 4)
        self.all_pilots = all_pilots
        
    def cp(self, pilots, carrier):
        channel_estimate = self._pilot_chan_estimator(pilots, carrier)        
        
        return pilots*channel_estimate, channel_estimate
        
    def tps(self, carrier_data, previous_chan_est): 
        carrier_data = carrier_data*previous_chan_est
        refined_channel_estimate = self._est_tps_channel(carrier_data)
        carrier_data = carrier_data*refined_channel_estimate
        
        return carrier_data, previous_chan_est*refined_channel_estimate
        
    def sp(self, carrier_data, carrier):
        # location of pilot carriers are defined in 
        # ETSI EN 300 744 V1.5.1 sec. 4.5.3
        pilot_indcs = self.all_pilots[(carrier%12)//3]
        
        carrier_data, rotation = self._apply_rotation(carrier_data, 
                                                      pilot_indcs, carrier)
        
        carrier_data, scale = self._apply_scaling(carrier_data, pilot_indcs)
        
        return carrier_data, scale*np.exp(1j*rotation)
        
    def dat(self, carrier_data, previous_chan_est):
        carrier_data *= previous_chan_est
            
        rotation = self._estimate_constellation_angle(carrier_data)
            
        carrier_data *= np.exp(1j*rotation)
            
        carrier_data, scale = self._apply_scaling(carrier_data, [])
            
        return carrier_data, scale*np.exp(1j*rotation)*previous_chan_est

    def _pilot_chan_estimator(self, pilots, carrier):
        sum_carrier = self.wk[carrier]*np.sum(pilots)
        channel_estimate = PILOT_2_DATA_AMP/(sum_carrier)
        
        return channel_estimate
    
    @staticmethod
    def _est_tps_channel(channel_data):
        pos_indcs = channel_data.real > 0
        
        pos = channel_data[pos_indcs]
        neg = channel_data[~pos_indcs]
    
        sum_carrier = np.sum(pos) - np.sum(neg)
    
        return PILOT_2_DATA_AMP/(sum_carrier)
        
    def _apply_rotation(self, carrier_data, pilot_indcs, carrier):
        pilots = carrier_data[pilot_indcs]        
        channel_estimate = self._pilot_chan_estimator(pilots, carrier)

        rotation = np.angle(channel_estimate)
        carrier_data = carrier_data*np.exp(1j*rotation)

        return carrier_data, rotation        
        
    def _apply_scaling(self, carrier_data, pilot_indcs):
        all_indcs = np.arange(self.num_symbols)                
        non_pilot_indcs = np.delete(all_indcs, pilot_indcs)

        avg_x = np.mean ( np.abs(carrier_data[non_pilot_indcs].real))
        scale_x = 4/avg_x
        
        return carrier_data*scale_x, scale_x       

    @staticmethod
    def _estimate_constellation_angle(vectors):
        '''
        Use points on the diagonals to estimate the rotation angle of the 
        constellation
        '''
        
        x_coords = np.floor(vectors.real)
        y_coords = np.floor(vectors.imag)
    
        x_coords = x_coords.astype('int')
        y_coords = y_coords.astype('int')
        
        x_coords //= 2
        y_coords //= 2
        
        x_equal_y = np.array(x_coords == y_coords)
        x_inv_y = np.array(-x_coords -1 == y_coords)
        x_great_zero = np.array(x_coords >= 0)

        quad_indcs = [0]*4
        quad_indcs[0] = x_equal_y & x_great_zero
        quad_indcs[2] = x_equal_y & ~x_great_zero
        quad_indcs[3] = x_inv_y & x_great_zero
        quad_indcs[1] = x_inv_y & ~x_great_zero
        
        quad_sums = [0]*4
        for k, indcs in enumerate(quad_indcs):
            quad_sums[k] = np.sum(vectors[indcs])

        sum_vec = quad_sums[0] + quad_sums[1]*-1j - quad_sums[2] + \
                                                             quad_sums[3]*1j

        return -np.angle(sum_vec) + np.pi/4