import multiprocessing as mp
import mmap

class CSVSummarizer:
    def __init__(self, data, header):
        self.data = data
        self.header = header

    def most_frequent_values(self, column_name):
        index = self.header.index(column_name)
        frequency = {}
        for row in self.data:
            value = row[index]
            if value in frequency:
                frequency[value] += 1
            else:
                frequency[value] = 1
        return max(frequency, key=frequency.get), frequency[max(frequency, key=frequency.get)]

    def find_outliers(self, column_name, threshold=1.5):
        index = self.header.index(column_name)
        column = [float(row[index]) for row in self.data]
        q1 = self._percentile(column, 25)
        q3 = self._percentile(column, 75)
        iqr = q3 - q1
        lower_bound = q1 - (threshold * iqr)
        upper_bound = q3 + (threshold * iqr)
        outliers = [row for row in self.data if float(row[index]) < lower_bound or float(row[index]) > upper_bound]
        return outliers

    def _percentile(self, data, percentile):
        size = len(data)
        sorted_data = sorted(data)
        k = (size - 1) * percentile / 100
        f = int(k)
        c = k - f
        if f + 1 < size:
            return sorted_data[f] + (c * (sorted_data[f + 1] - sorted_data[f]))
        else:
            return sorted_data[f]

    def create_histogram(self, column_name, bins=10):
        index = self.header.index(column_name)
        column = [float(row[index]) for row in self.data]
        min_val, max_val = min(column), max(column)
        bin_ranges = [min_val + i * ((max_val - min_val) / bins) for i in range(bins + 1)]
        histogram = [0] * bins
        for value in column:
            for i in range(bins):
                if bin_ranges[i] <= value < bin_ranges[i + 1]:
                    histogram[i] += 1
                    break
            else:
                histogram[-1] += 1
        return histogram

    def calculate_sum(self, column_name):
        index = self.header.index(column_name)
        return sum(float(row[index]) for row in self.data)

    def calculate_max(self, column_name):
        index = self.header.index(column_name)
        return max(float(row[index]) for row in self.data)

    def calculate_min(self, column_name):
        index = self.header.index(column_name)
        return min(float(row[index]) for row in self.data)

    def calculate_mean(self, column_name):
        total = self.calculate_sum(column_name)
        count = len(self.data)
        return total / count if count else None

    def calculate_median(self, column_name):
        index = self.header.index(column_name)
        sorted_column = sorted(float(row[index]) for row in self.data)
        mid = len(sorted_column) // 2
        if len(sorted_column) % 2 == 0:
            return (sorted_column[mid - 1] + sorted_column[mid]) / 2
        else:
            return sorted_column[mid]

    def calculate_mode(self, column_name):
        index = self.header.index(column_name)
        frequency = {}
        for row in self.data:
            value = row[index]
            if value in frequency:
                frequency[value] += 1
            else:
                frequency[value] = 1
        return max(frequency, key=frequency.get), frequency[max(frequency, key=frequency.get)]

    def calculate_variance(self, column_name):
        mean = self.calculate_mean(column_name)
        index = self.header.index(column_name)
        return sum((float(row[index]) - mean) ** 2 for row in self.data) / len(self.data)

    def calculate_std_dev(self, column_name):
        variance = self.calculate_variance(column_name)
        return variance ** 0.5

    def calculate_range(self, column_name):
        return self.calculate_max(column_name) - self.calculate_min(column_name)

    def calculate_percentile(self, column_name, percentile):
        index = self.header.index(column_name)
        sorted_column = sorted(float(row[index]) for row in self.data)
        return self._percentile(sorted_column, percentile)

    def calculate_z_scores(self, column_name):
        mean = self.calculate_mean(column_name)
        std_dev = self.calculate_std_dev(column_name)
        index = self.header.index(column_name)
        return [(float(row[index]) - mean) / std_dev for row in self.data]

    def parallel_calculate_sum(self, column_name):
        index = self.header.index(column_name)
        num_threads = mp.cpu_count()
        chunk_size = len(self.data) // num_threads

        with mp.Pool(num_threads) as pool:
            results = pool.map(self._partial_sum, [(index, self.data[i:i + chunk_size]) for i in range(0, len(self.data), chunk_size)])

        return sum(results)

    def _partial_sum(self, args):
        index, data_chunk = args
        return sum(float(row[index]) for row in data_chunk)

    def mmap_calculate_sum(self, column_name, file_path):
        index = self.header.index(column_name)
        total_sum = 0

        with open(file_path, 'r') as f:
            mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            for line in iter(mmapped_file.readline, b""):
                row = line.decode().strip().split(',')
                try:
                    total_sum += float(row[index])
                except ValueError:
                    continue

        return total_sum

    def mmap_calculate_max(self, column_name, file_path):
        index = self.header.index(column_name)
        max_val = float('-inf')

        with open(file_path, 'r') as f:
            mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            for line in iter(mmapped_file.readline, b""):
                row = line.decode().strip().split(',')
                try:
                    max_val = max(max_val, float(row[index]))
                except ValueError:
                    continue

        return max_val
