import matplotlib.pyplot as plt
import numpy as np
import calibratesdr as cali

def get_ppm(data, samplerate=2048000, window = 2048000, center_f = 162600000, show_graph = False, verbose = False):
    mean = np.mean(data, axis=0)
    noise = np.mean(mean)

    data = np.array(data)

    # load nwr station data
    stations = channels()

    result = []

    for channel in range(len(stations["nwr"])):

        cf = stations["nwr"][channel]["f_center"]
        station = stations["nwr"][channel]["station"]
        bw = 25000.0 #hz

        # determination of the sample position of the frequency within the fft waterfall data
        station_s = int(samplerate/2 + (cf - center_f) * samplerate / window)
        bw_s = int(bw / 2 * samplerate / window)


        start_s = station_s - bw_s
        end_s = station_s + bw_s
        data_station = data[:, start_s : end_s]

        signal_center = np.argmax(np.mean(data_station, axis=0))

        # only check in this area of 800 Hz. gut feeling. just needed a value
        snr_bw = 800.0 / (samplerate / window)

        signal_left = int(signal_center - snr_bw / 2)
        if signal_left < 0:
            signal_left = 0

        signal_right = int(signal_center + snr_bw / 2)
        if signal_right > len(data_station[0]) - 1:
            signal_right = len(data_station[0]) - 1

        nwr_snr = np.mean(np.mean(data_station, axis=0)[signal_left : signal_right]) - noise


        # discussion needed
        # currently it CANNOT distinguiesh between a lower station's frequency shifted higher,
        # or a higher station's frequency shifted lower!
        ppm_per_step = []
        for i in range(len(data_station)):
            window_roll = 11
            part = cali.utils.movingaverage(data_station[i], window_roll, mode="valid")

            ppm_step = (np.argmax(part) + int(window_roll / 2)) - len(part) / 2
            ppm_step = (cf / 1000.0) / ppm_step
            ppm_per_step.append(ppm_step)


        if show_graph == True:
            plt.imshow(data_station[:,::10])
            plt.show()

            plt.plot(ppm_per_step)
            plt.show()

        nwr_ppm = np.mean(ppm_per_step)
        # maybe the outlier reduction is needed. not yet implemented.

        nwr_station_detected = 0
        if nwr_snr >= 5.0: # needs to be discussed if this needs to be different.
            nwr_station_detected = 2
        else:
            nwr_ppm = None


        result.append([channel, station, cf, nwr_snr, nwr_station_detected, nwr_ppm])

    return result

def channels():
    # https://www.weather.gov/nwr/station_listing

    nwr = {"nwr": [
        {"station": "0", "f_center": 162400000},
        {"station": "1", "f_center": 162425000},
        {"station": "2", "f_center": 162450000},
        {"station": "3", "f_center": 162475000},
        {"station": "4", "f_center": 162500000},
        {"station": "5", "f_center": 162525000},
        {"station": "6", "f_center": 162550000}
    ]}

    return nwr

if __name__ == '__main__':
    get_ppm()