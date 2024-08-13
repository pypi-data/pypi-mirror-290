import csv
from decimal import Decimal
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LinearRegression
import os
from threading import Thread
import multiprocessing as mp
import mmap
from .exporter import CSVExporter  # CSVExporter importiert

class CSVAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.header, self.data = self._load_csv()
        self.precision = 2  # Standardmäßige Dezimalpräzision für Berechnungen

    def _load_csv(self):
        delimiters = [',', ';', '\t', '|']  # Liste möglicher Trennzeichen
        with open(self.file_path, 'r', encoding='utf-8') as file:
            sample = file.read(1024)
            file.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters)
            except csv.Error:
                return self._manual_delimiter_detection(file, delimiters)

            reader = csv.reader(file, dialect)
            header = next(reader)
            data = [row for row in reader]
        return header, data

    def _manual_delimiter_detection(self, file, delimiters):
        """Versucht manuell, das Trennzeichen zu bestimmen."""
        for delimiter in delimiters:
            file.seek(0)
            reader = csv.reader(file, delimiter=delimiter)
            header = next(reader)
            if len(header) > 1:  # Wenn die Header-Zeile mehr als ein Feld hat, ist das Trennzeichen korrekt
                data = [row for row in reader]
                return header, data
        raise ValueError("Could not determine delimiter and no valid fallback found.")

    def analyze_and_export(self, column_name, output_file):
        index = self.header.index(column_name)
        column_data = [row[index] for row in self.data]

        try:
            numeric_data = [float(value) for value in column_data]
            mean_value = sum(numeric_data) / len(numeric_data)
            results = [["Mittelwert", mean_value]]
        except ValueError:
            from collections import Counter
            value_counts = Counter(column_data)
            results = [["Wert", "Häufigkeit"]] + [[key, count] for key, count in value_counts.items()]

        # Exportiere die Analyseergebnisse als CSV
        exporter = CSVExporter(results, ["Ergebnis", column_name])
        exporter.export_to_csv(output_file)

    def incremental_median(self, column_name):
        index = self.header.index(column_name)
        values = [Decimal(row[index]) for row in self.data]
        values.sort()
        n = len(values)
        if n % 2 == 0:
            median = (values[n//2 - 1] + values[n//2]) / 2
        else:
            median = values[n//2]
        return round(median, self.precision)

    def calculate_std_dev(self, column_name):
        mean = sum(float(row[self.header.index(column_name)]) for row in self.data) / len(self.data)
        variance = sum((float(row[self.header.index(column_name)]) - mean) ** 2 for row in self.data) / len(self.data)
        return round(variance ** 0.5, self.precision)

    def calculate_variance(self, column_name):
        mean = sum(float(row[self.header.index(column_name)]) for row in self.data) / len(self.data)
        variance = sum((float(row[self.header.index(column_name)]) - mean) ** 2 for row in self.data) / len(self.data)
        return round(variance, self.precision)

    def detect_anomalies_simple(self, column_name, threshold=1.5):
        index = self.header.index(column_name)
        column = [Decimal(row[index]) for row in self.data]
        mean = sum(column) / len(column)
        threshold = Decimal(threshold)
        anomalies = [row for row in self.data if abs(Decimal(row[index]) - mean) > threshold * mean]
        return anomalies

    def calculate_correlation(self, col1, col2, method='pearson'):
        index1 = self.header.index(col1)
        index2 = self.header.index(col2)
        data1 = [float(row[index1]) for row in self.data]
        data2 = [float(row[index2]) for row in self.data]
        if method == 'pearson':
            return pearsonr(data1, data2)[0]
        elif method == 'spearman':
            return spearmanr(data1, data2)[0]
        else:
            raise ValueError("Method must be either 'pearson' or 'spearman'")

    def linear_regression(self, target_col, *feature_cols):
        y_index = self.header.index(target_col)
        X_indices = [self.header.index(col) for col in feature_cols]
        X = [[float(row[i]) for i in X_indices] for row in self.data]
        y = [float(row[y_index]) for row in self.data]
        model = LinearRegression()
        model.fit(X, y)
        return model.coef_, model.intercept_

    # Datenbereinigungsfunktionen
    def remove_duplicates(self):
        seen = set()
        unique_data = []
        for row in self.data:
            row_tuple = tuple(row)
            if row_tuple not in seen:
                seen.add(row_tuple)
                unique_data.append(row)
        self.data = unique_data

    def fill_missing_values(self, column_name, strategy="mean"):
        index = self.header.index(column_name)
        values = [float(row[index]) for row in self.data if row[index] != ""]
        if strategy == "mean":
            fill_value = sum(values) / len(values)
        elif strategy == "median":
            values.sort()
            mid = len(values) // 2
            fill_value = (values[mid] if len(values) % 2 != 0 else (values[mid - 1] + values[mid]) / 2)
        elif strategy == "mode":
            from collections import Counter
            fill_value = Counter(values).most_common(1)[0][0]
        else:
            raise ValueError("Strategy must be 'mean', 'median', or 'mode'")
        for row in self.data:
            if row[index] == "":
                row[index] = fill_value

    def normalize_column(self, column_name):
        index = self.header.index(column_name)
        values = [float(row[index]) for row in self.data]
        min_val, max_val = min(values), max(values)
        for row in self.data:
            row[index] = (float(row[index]) - min_val) / (max_val - min_val)

    def standardize_column(self, column_name):
        index = self.header.index(column_name)
        values = [float(row[index]) for row in self.data]
        mean = sum(values) / len(values)
        std_dev = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
        for row in self.data:
            row[index] = (float(row[index]) - mean) / std_dev

    # Parallelisierung und Optimierung
    def parallel_analyze_column(self, column_name, num_threads=4):
        index = self.header.index(column_name)
        chunk_size = len(self.data) // num_threads
        chunks = [self.data[i:i + chunk_size] for i in range(0, len(self.data), chunk_size)]

        results = [None] * num_threads
        threads = []

        def analyze_chunk(chunk_idx):
            chunk_data = [row[index] for row in chunks[chunk_idx]]
            try:
                numeric_data = [float(value) for value in chunk_data]
                mean_value = sum(numeric_data) / len(numeric_data)
                results[chunk_idx] = mean_value
            except ValueError:
                from collections import Counter
                value_counts = Counter(chunk_data)
                results[chunk_idx] = value_counts

        for i in range(num_threads):
            thread = Thread(target=analyze_chunk, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    def memory_mapped_analyze(self, column_name):
        index = self.header.index(column_name)
        with open(self.file_path, 'r', encoding='utf-8') as f:
            mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            data = mmapped_file.read().decode('utf-8').splitlines()
            column_data = [line.split(',')[index] for line in data[1:]]  # Überspringen des Headers

            try:
                numeric_data = [float(value) for value in column_data]
                mean_value = sum(numeric_data) / len(numeric_data)
                return mean_value
            except ValueError:
                from collections import Counter
                value_counts = Counter(column_data)
                return value_counts

    def index_column(self, column_name):
        """Erstellt einen Index für eine Spalte, um Abfragen zu beschleunigen."""
        index = self.header.index(column_name)
        index_map = {}
        for i, row in enumerate(self.data):
            key = row[index]
            if key in index_map:
                index_map[key].append(i)
            else:
                index_map[key] = [i]
        return index_map
