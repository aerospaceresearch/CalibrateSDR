import numpy as np
import matplotlib.pyplot as plt
import calibratesdr as cali

def get_ppm(data, samplerate = 2048000, show_graph = False, verbose=False):
    adc_offset = -127

    data_slice = (adc_offset + data[0:: 2]) + 1j * (adc_offset + data[1:: 2])

    signal = np.abs(data_slice)


    signal_meaned = cali.utils.movingaverage(signal, 80)


    #signal_mean = np.mean(signal_meaned)

    #low = signal_mean / 2.0
    #signal_gaps = np.copy(signal_meaned)
    #signal_gaps[signal_gaps > signal_mean / 2.0] = signal_mean
    #signal_gaps[signal_gaps <= signal_mean / 2.0] = low

    signal_mean = np.mean(signal_meaned)
    low = (signal_mean + np.min(signal_meaned)) / 2.0

    signal_gaps = np.copy(signal_meaned)
    signal_gaps[signal_gaps > low] = signal_mean
    signal_gaps[signal_gaps <= low] = low

    counter_gap = 0

    gap_length = []
    gap_position = []

    transmission_frame_duration = 0.096  # sec
    transmission_frame_samples = samplerate * transmission_frame_duration

    for i in range(len(signal_gaps)):
        if signal_gaps[i] == low:
            counter_gap += 1

        if counter_gap > 0 and signal_gaps[i] != low:
            #print(i, counter_gap)
            gap_length.append(counter_gap)
            gap_position.append(i - counter_gap)
            counter_gap = 0


    null_symbol_duration = int(2656 * samplerate / 2048000.0)

    # finding the null gap that is closest to the null symbol duration
    needle_index = 0
    needle_gap = 0
    for i in range(len(gap_length)):
        if i == 0 or np.abs(gap_length[i] - null_symbol_duration) < needle_gap:
            needle_index = i
            needle_gap = np.abs(gap_length[i] - null_symbol_duration)


    # needle can reach out of data. no check yet
    needle_length = 2400
    needle_start = gap_position[needle_index] + gap_length[needle_index] + 200
    needle_end = gap_position[needle_index] + gap_length[needle_index] + needle_length
    needle = signal_meaned[needle_start: needle_end]


    if show_graph == True:
        # just showing the needle on the signal

        graph_start = gap_position[needle_index] + gap_length[needle_index] - null_symbol_duration * 2
        graph_end = gap_position[needle_index] + gap_length[needle_index] + null_symbol_duration * 2
        if graph_start <0:
            graph_start = 0

        needle_x_position = []
        start = (gap_position[needle_index] + gap_length[needle_index] + 200) - graph_start
        for i in range(len(needle)):
            needle_x_position.append(start + i)

        plt.plot(signal_meaned[graph_start: graph_end], label="signal")
        plt.plot(needle_x_position, needle, label="needle")
        plt.grid()
        plt.xlabel("sample [s]")
        plt.ylabel("amplitude [int]")
        plt.title("synch. channel symbols w/ phase reference as selected needle")
        plt.legend()
        plt.show()



    needle2 = np.sum(np.multiply(needle, needle))
    window = len(needle)

    cor_result = np.zeros(len(signal_meaned))

    for i in range(len(gap_position)):

        end = gap_position[i] + gap_length[i] + 4000
        if gap_length[i] > 500:# and end < len(signal_meaned)-1: # needle could range into end of signal

            start = gap_position[i] + gap_length[i] - 100
            haystack = signal_meaned[start: end]

            for j in range(0, len(haystack) - len(needle)):
                haystack_part = np.array(haystack[j: j + window])
                normed_cross_correlation = np.sum(np.multiply(haystack_part, needle))
                normed_cross_correlation = normed_cross_correlation / \
                                           (np.sum(np.multiply(haystack_part, haystack_part)) * needle2) ** 0.5

                cor_result[start + j] = normed_cross_correlation * signal_mean

    gap_location = []
    gap_location_pin = []

    for i in range(0, len(cor_result), int(transmission_frame_samples)):
        haystack = cor_result[i: i + int(transmission_frame_samples)]

        if np.max(haystack) > 0.0 and i > 0:

            index_max = i + np.argmax(haystack)

            gap_location.append(index_max)
            gap_location_pin.append(signal_mean * 1.4)


    if show_graph == True:
        for i in range(len(gap_location)):
            plt.plot(signal_meaned[gap_location[i]: gap_location[i] + needle_length], label="signal")

        plt.grid()
        plt.xlabel("sample [s]")
        plt.ylabel("amplitude [int]")
        plt.title("all found phase reference symbols in the recording")
        plt.show()


    # delete the outliers
    dif = np.diff(gap_location)

    ppm = None

    if len(dif) > 8:

        dif = cali.utils.reduce_outliers(dif)

        # calculate the ppm
        total_samples_measured = np.sum(dif)
        total_samples = len(dif) * samplerate * transmission_frame_duration
        ppm_measured = total_samples - total_samples_measured
        factor = total_samples_measured / 1000000
        ppm = ppm_measured / factor

        if total_samples_measured == 0 or np.abs(ppm) >= 10000.0:
            ppm = None

    else:
        ppm = None


    if show_graph == True:

        steps = np.linspace(0, len(signal_meaned)-1, num=len(signal_meaned))

        plt.plot(steps[::20], signal_meaned[::20], label="signal")
        plt.plot(steps[::20], cor_result[::20], label="correlations of needle")
        plt.plot(gap_location, gap_location_pin, "*", label="locations of needle")

        plt.grid()
        plt.xlabel("sample [s]")
        plt.ylabel("amplitude [int]")
        plt.title("show detected phase syncronizations")
        plt.legend()
        plt.show()

    return ppm


def channels():
    dab = {"dab": [
        {"block": "5A", "f_center": 174928000},
        {"block": "5B", "f_center": 176640000},
        {"block": "5C", "f_center": 178352000},
        {"block": "5D", "f_center": 180064000},
        {"block": "6A", "f_center": 181936000},
        {"block": "6B", "f_center": 183648000},
        {"block": "6C", "f_center": 185360000},
        {"block": "6D", "f_center": 187072000},
        {"block": "7A", "f_center": 188928000},
        {"block": "7B", "f_center": 190640000},
        {"block": "7C", "f_center": 192352000},
        {"block": "7D", "f_center": 194064000},
        {"block": "8A", "f_center": 195936000},
        {"block": "8B", "f_center": 197648000},
        {"block": "8C", "f_center": 199360000},
        {"block": "8D", "f_center": 201072000},
        {"block": "9A", "f_center": 202928000},
        {"block": "9B", "f_center": 204640000},
        {"block": "9C", "f_center": 206352000},
        {"block": "9D", "f_center": 208064000},
        {"block": "10A", "f_center": 209936000},
        {"block": "10N", "f_center": 210096000},
        {"block": "10B", "f_center": 211648000},
        {"block": "10C", "f_center": 213360000},
        {"block": "10D", "f_center": 215072000},
        {"block": "11A", "f_center": 216928000},
        {"block": "11N", "f_center": 217088000},
        {"block": "11B", "f_center": 218640000},
        {"block": "11C", "f_center": 220352000},
        {"block": "11D", "f_center": 222064000},
        {"block": "12A", "f_center": 223936000},
        {"block": "12N", "f_center": 224096000},
        {"block": "12B", "f_center": 225648000},
        {"block": "12C", "f_center": 227360000},
        {"block": "12D", "f_center": 229072000},
        {"block": "13A", "f_center": 230784000},
        {"block": "13B", "f_center": 232496000},
        {"block": "13C", "f_center": 234208000},
        {"block": "13D", "f_center": 235776000},
        {"block": "13E", "f_center": 237488000},
        {"block": "13F", "f_center": 239200000}
    ]}

    return dab

def signal_level(data, segment):

    step = int(len(data) / segment)
    #print(step)

    level = []
    for i in range(0, len(data), step*2):
        level.append(np.mean(data[i : i + step]))

    return level


def signal_dynamics(data, side):

    dyn_sides = (np.mean(data[0:side]) + np.mean(data[-side:])) / 2.0
    dyn_center = np.mean(data[side: -side])

    return dyn_center - dyn_sides


def signal_dynamics_edges(left, right):

    dyn_left = np.mean(left)
    dyn_right = np.mean(right)

    return np.abs(dyn_left - dyn_right)


def block_check(signal_bins, snr, limit_db=2.0):
    left = signal_dynamics_edges(signal_bins[0 : 20], signal_bins[20 : 20 * 2])
    right = signal_dynamics_edges(signal_bins[-20 * 2 : -20], signal_bins[-20 : ])

    block_detected = 0

    if snr > limit_db:
        block_detected = 2

        if np.abs(left - right) > limit_db:
            block_detected = 1

    return block_detected


if __name__ == '__main__':
    print("this is dab support so far")
