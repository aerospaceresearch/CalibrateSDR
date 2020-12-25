import numpy as np
def test():
    print("test")

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'same')
    return sma

def reduce_outliers(dif):

    limit_b4 = 0.0
    limit_set = 1.0
    std_factor = 3.0
    counter = 0

    while limit_b4 - np.std(dif) * std_factor != 0 and \
            limit_set < np.std(dif) * std_factor and \
            counter < 20 and np.std(dif) != 0:

        std = np.std(dif)
        meany = np.mean(dif)

        limit = std * std_factor

        for j in range(len(dif)):

            if np.abs(dif[j] - meany) >= limit:
                #print("pop", counter, j, np.abs(dif[j] - meany), limit)
                dif = np.delete(dif, j)
                break

        limit_b4 = limit
        counter += 1

    return dif