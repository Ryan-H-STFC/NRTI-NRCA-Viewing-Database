import scipy as sp


class PeakDetection:
    def __init__(self):
        self.peak_limits_x = None
        self.peak_limits_y = None
        self.peak_list = None

    # ! Check functionality of maxima function

    def maxima(self, data):  # Finds the maxima in a sample and the peak widths
        x, y = data.iloc[:, 0], data.iloc[:, 1]
        maxima, _ = sp.signal.find_peaks(y, height=100, prominence=0.1)
        width = sp.signal.peak_widths(y, maxima, rel_height=1, wlen=300)
        # Extracting maxima coordinates
        maxima_list_x = []
        maxima_list_y = []
        maxima = maxima.tolist()
        for i in maxima:
            maxima_list_x.append(x[i])  # Get list of maxima # !
            maxima_list_y.append(y[i])
        # Extracting peak width coordinates
        self.peak_limits_x = dict()  # Re-setting if used before
        self.peak_limits_y = dict()
        first_limits = width[2].tolist()
        second_limits = width[3].tolist()
        # Refining peak limits
        # first_limits, second_limits = self.PeakLimitsCheck(first_limits, second_limits, maxima)
        print("FL", first_limits)
        for i in first_limits:
            index = first_limits.index(i)
            peak = maxima_list_x[index]
            # ! Loss of Accuracy? check how indexing is done
            coordinate = x[round(i)]
            # Finding the y- value for corresponding limits
            coordinate_index = x.loc[x == coordinate].index[0]
            self.peak_limits_y[str(peak) + "_first"] = y[coordinate_index]
            self.peak_limits_x[str(peak) + "_first"] = coordinate
        for i in second_limits:
            index = second_limits.index(i)
            peak = maxima_list_x[index]
            coordinate = x[round(i)]
            # Finding the y- value for corresponding limits
            coordinate_index = x.loc[x == coordinate].index[0]
            self.peak_limits_y[str(peak) + "_second"] = y[coordinate_index]
            self.peak_limits_x[str(peak) + "_second"] = coordinate
        print("Peak limits x: ", self.peak_limits_x)
        print("Peak limits y: ", self.peak_limits_y)
        self.peak_list = maxima_list_x
        return maxima_list_x, maxima_list_y

    def minima(self, data):  # Inverts the data to find the minima in the sample
        x = data[0]
        y = (lambda data: -1 * data[1])(data)
        minima, _ = sp.signal.find_peaks(y, height=-0.90, prominence=0.0035)
        width = sp.signal.peak_widths(y, minima, rel_height=1, wlen=300)
        # Extracting peak center coordinates
        minima_list_x = []
        minima_list_y = []
        minima = minima.tolist()
        for i in minima:
            minima_list_x.append(x[i])
            minima_list_y.append(y[i])
        # Extracting peak width coordinates
        self.peak_limits_x = dict()  # Resetting if used before
        self.peak_limits_y = dict()
        first_limits = width[2].tolist()
        second_limits = width[3].tolist()
        for i in first_limits:
            index = first_limits.index(i)
            peak = minima_list_x[index]
            coordinate = x[round(i)]
            # Finding the y- value for corresponding limits
            coordinate_index = x.loc[x == coordinate].index[0]

            self.peak_limits_y[str(peak) + "_first"] = y[coordinate_index]
            self.peak_limits_x[str(peak) + "_first"] = coordinate
        for i in second_limits:
            index = second_limits.index(i)
            peak = minima_list_x[index]
            coordinate = x[round(i)]
            # Finding the y- value for corresponding limits
            coordinate_index = x.loc[x == coordinate].index[0]
            self.peak_limits_y[str(peak) + "_second"] = y[coordinate_index]
            self.peak_limits_x[str(peak) + "_second"] = coordinate

        print("Peak limits x: ", self.peak_limits_x)
        minima_list_y = list(map(lambda val: -1 * val, minima_list_y))
        return minima_list_x, minima_list_y

    def PeakCalculations(self, xlimits, limits):
        # Calculates the necessary information to put in the table for the detected peaks
        # This involves:
        # Rank by Integral
        # Peak Centre Coordinate in terms of energy (eV) and TOF (microseconds)
        # Integral
        # Rank by Peak Width
        # Peak Height
        # Rank by Peak Height
        # fake = 10
        pass

    def PeakLimitsCheck(first_limits, second_limits, maxima):
        # Ensuring the limits are symmetrical about the peak center
        print("original: ", first_limits, second_limits)
        print("maxima: ", maxima)
        first_limits_changed = []
        second_limits_changed = []
        for i in first_limits:
            changed_first = False
            changed_second = False
            index = first_limits.index(i)
            peak = maxima[index]
            diff_first = peak - i
            diff_second = second_limits[index] - peak
            if diff_first < diff_second:
                second_limit = peak + diff_first
                second_limits_changed.append(second_limit)
                changed_second = True
            elif diff_second < diff_first:
                first_limit = peak - diff_second
                first_limits_changed.append(first_limit)
                changed_first = True
            else:
                continue
            if not changed_first:
                first_limits_changed.append(i)
            if not changed_second:
                second_limits_changed.append(second_limits[index])
        print("Changed: ", first_limits_changed, second_limits_changed)
        return first_limits_changed, second_limits_changed