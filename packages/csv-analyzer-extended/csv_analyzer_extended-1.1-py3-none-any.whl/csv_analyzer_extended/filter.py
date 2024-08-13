import re
from datetime import datetime
import multiprocessing as mp  # Multiprocessing für parallele Verarbeitung
import mmap  # Memory-Mapping für effizientere Dateioperationen

class CSVFilter:
    def __init__(self, data=None, header=None, file_path=None):
        if file_path:
            self.header, self.data = self._load_csv(file_path)
        else:
            self.data = data
            self.header = header

    def _load_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            header = file.readline().strip().split(';')
            data = [line.strip().split(';') for line in file]
        return header, data

    def filter_by_numeric_range(self, column_name, min_value=None, max_value=None):
        index = self.header.index(column_name)
        filtered_data = [row for row in self.data if (min_value is None or float(row[index]) >= min_value) and (max_value is None or float(row[index]) <= max_value)]
        return filtered_data

    def filter_by_text_pattern(self, column_name, pattern):
        index = self.header.index(column_name)
        regex = re.compile(pattern)
        filtered_data = [row for row in self.data if regex.search(row[index])]
        return filtered_data

    def filter_by_date_range(self, column_name, start_date, end_date, date_format='%Y-%m-%d'):
        index = self.header.index(column_name)
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
        filtered_data = [row for row in self.data if start_date <= datetime.strptime(row[index], date_format) <= end_date]
        return filtered_data

    def filter_by_custom_function(self, column_name, custom_func):
        index = self.header.index(column_name)
        filtered_data = [row for row in self.data if custom_func(row[index])]
        return filtered_data

    def normalize_column(self, column_name):
        index = self.header.index(column_name)
        col_min = min(float(row[index]) for row in self.data)
        col_max = max(float(row[index]) for row in self.data)
        for row in self.data:
            row[index] = (float(row[index]) - col_min) / (col_max - col_min)
        return self.data

    def rank_column(self, column_name):
        index = self.header.index(column_name)
        sorted_data = sorted(self.data, key=lambda row: float(row[index]))
        ranks = {id(row): rank for rank, row in enumerate(sorted_data, 1)}
        for row in self.data:
            row[index] = ranks[id(row)]
        return self.data

    # Erweiterte Filterfunktionen
    def filter_by_condition_chain(self, conditions):
        filtered_data = self.data
        for condition in conditions:
            column_name, operator, value = condition
            index = self.header.index(column_name)
            
            if operator == "==":
                filtered_data = [row for row in filtered_data if row[index] == str(value)]
            elif operator == "!=":
                filtered_data = [row for row in filtered_data if row[index] != str(value)]
            elif operator == ">":
                filtered_data = [row for row in filtered_data if self._convert_to_numeric(row[index]) > self._convert_to_numeric(value)]
            elif operator == "<":
                filtered_data = [row for row in filtered_data if self._convert_to_numeric(row[index]) < self._convert_to_numeric(value)]
            elif operator == ">=":
                filtered_data = [row for row in filtered_data if self._convert_to_numeric(row[index]) >= self._convert_to_numeric(value)]
            elif operator == "<=":
                filtered_data = [row for row in filtered_data if self._convert_to_numeric(row[index]) <= self._convert_to_numeric(value)]
        return filtered_data

    def _convert_to_numeric(self, value):
        try:
            return float(value)
        except ValueError:
            return value  # Rückgabe des Originalwerts, wenn keine Konvertierung möglich ist

    def multidimensional_filter(self, filters):
        filtered_data = self.data
        for filter_func, *args in filters:
            filtered_data = filter_func(*args)
        return filtered_data

    # Erweiterte Funktionen für komplexe Abfragen

    def inner_join(self, other, column_name):
        """Führt einen Inner Join mit einem anderen Datensatz durch."""
        index = self.header.index(column_name)
        other_index = other.header.index(column_name)
        joined_data = [row + other_row for row in self.data for other_row in other.data if row[index] == other_row[other_index]]
        return joined_data

    def left_join(self, other, column_name):
        """Führt einen Left Join mit einem anderen Datensatz durch."""
        index = self.header.index(column_name)
        other_index = other.header.index(column_name)
        joined_data = []
        for row in self.data:
            match_found = False
            for other_row in other.data:
                if row[index] == other_row[other_index]:
                    joined_data.append(row + other_row)
                    match_found = True
            if not match_found:
                joined_data.append(row + [''] * len(other.header))
        return joined_data

    def right_join(self, other, column_name):
        """Führt einen Right Join mit einem anderen Datensatz durch."""
        index = self.header.index(column_name)
        other_index = other.header.index(column_name)
        joined_data = []
        for other_row in other.data:
            match_found = False
            for row in self.data:
                if row[index] == other_row[other_index]:
                    joined_data.append(row + other_row)
                    match_found = True
            if not match_found:
                joined_data.append([''] * len(self.header) + other_row)
        return joined_data

    def full_outer_join(self, other, column_name):
        """Führt einen Full Outer Join mit einem anderen Datensatz durch."""
        index = self.header.index(column_name)
        other_index = other.header.index(column_name)
        all_keys = set(row[index] for row in self.data) | set(row[other_index] for row in other.data)
        joined_data = []
        for key in all_keys:
            left_rows = [row for row in self.data if row[index] == key]
            right_rows = [row for row in other.data if row[other_index] == key]
            if left_rows and right_rows:
                for left_row in left_rows:
                    for right_row in right_rows:
                        joined_data.append(left_row + right_row)
            elif left_rows:
                for left_row in left_rows:
                    joined_data.append(left_row + [''] * len(other.header))
            elif right_rows:
                for right_row in right_rows:
                    joined_data.append([''] * len(self.header) + right_row)
        return joined_data

    def select_columns(self, column_names):
        """Wählt bestimmte Spalten aus den Daten aus."""
        indices = [self.header.index(name) for name in column_names]
        selected_data = [[row[i] for i in indices] for row in self.data]
        return selected_data

    def where(self, column_name, condition):
        """Filtert die Daten basierend auf einer Bedingung."""
        index = self.header.index(column_name)
        filtered_data = [row for row in self.data if condition(row[index])]
        return filtered_data

    def group_by(self, column_name, agg_func):
        """Gruppiert die Daten nach einer Spalte und wendet eine Aggregatfunktion an."""
        index = self.header.index(column_name)
        grouped_data = {}
        for row in self.data:
            key = row[index]
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(row)
        return {key: agg_func(rows) for key, rows in grouped_data.items()}

    def order_by(self, column_name, ascending=True):
        """Sortiert die Daten nach einer bestimmten Spalte."""
        index = self.header.index(column_name)
        return sorted(self.data, key=lambda row: row[index], reverse=not ascending)

    def limit(self, n):
        """Gibt die ersten n Zeilen der Daten zurück."""
        return self.data[:n]

    # Aggregationsabfragen
    def count(self, column_name):
        index = self.header.index(column_name)
        return len([row[index] for row in self.data])

    def sum(self, column_name):
        index = self.header.index(column_name)
        return sum(float(row[index]) for row in self.data)

    def average(self, column_name):
        index = self.header.index(column_name)
        return self.sum(column_name) / self.count(column_name)

    def min(self, column_name):
        index = self.header.index(column_name)
        return min(float(row[index]) for row in self.data)

    def max(self, column_name):
        index = self.header.index(column_name)
        return max(float(row[index]) for row in self.data)

    # Window-Funktionen
    def cumulative_sum(self, column_name):
        index = self.header.index(column_name)
        cumsum = 0
        cumsum_list = []
        for row in self.data:
            cumsum += float(row[index])
            cumsum_list.append(cumsum)
        return cumsum_list

    def cumulative_avg(self, column_name):
        index = self.header.index(column_name)
        cumsum = 0
        cumavg_list = []
        for i, row in enumerate(self.data, 1):
            cumsum += float(row[index])
            cumavg_list.append(cumsum / i)
        return cumavg_list

    def rank(self, column_name):
        index = self.header.index(column_name)
        sorted_data = sorted(self.data, key=lambda row: float(row[index]))
        ranks = {id(row): rank for rank, row in enumerate(sorted_data, 1)}
        return [ranks[id(row)] for row in self.data]

    def dense_rank(self, column_name):
        index = self.header.index(column_name)
        sorted_data = sorted(set(float(row[index]) for row in self.data))
        rank_dict = {value: rank for rank, value in enumerate(sorted_data, 1)}
        return [rank_dict[float(row[index])] for row in self.data]

    # Set-Operationen
    def union(self, other_data):
        return [row for row in self.data + other_data if row not in self.data or row not in other_data]

    def intersection(self, other_data):
        return [row for row in self.data if row in other_data]

    def difference(self, other_data):
        return [row for row in self.data if row not in other_data]

    # Verschachtelte Abfragen
    def subquery(self, subquery_function, *args):
        return subquery_function(*args)

    def exists(self, subquery_function, *args):
        return bool(self.subquery(subquery_function, *args))

    def in_(self, subquery_function, *args):
        subquery_result = self.subquery(subquery_function, *args)
        return [row for row in self.data if row in subquery_result]

    # Verbundene Datensätze
    def self_join(self, column_name):
        return self.inner_join(self, column_name)

    def cross_join(self, other_data):
        return [row1 + row2 for row1 in self.data for row2 in other_data]

    # Bedingte Abfragen
    def case_when(self, conditions):
        results = []
        for row in self.data:
            for condition, value in conditions:
                if condition(row):
                    results.append(value)
                    break
            else:
                results.append(None)
        return results

    # Pivot-Tabellen
    def pivot(self, index_column, columns_column, values_column):
        index_idx = self.header.index(index_column)
        columns_idx = self.header.index(columns_column)
        values_idx = self.header.index(values_column)

        pivot_table = {}
        for row in self.data:
            index = row[index_idx]
            column = row[columns_idx]
            value = float(row[values_idx])

            if index not in pivot_table:
                pivot_table[index] = {}
            pivot_table[index][column] = value

        return pivot_table

    def unpivot(self, columns):
        unpivoted_data = []
        index_columns = [i for i in range(len(self.header)) if i not in columns]

        for row in self.data:
            for col in columns:
                new_row = [row[i] for i in index_columns] + [self.header[col], row[col]]
                unpivoted_data.append(new_row)

        return unpivoted_data

    # Zeitliche Abfragen
    def rolling_window(self, column_name, window_size, agg_func):
        index = self.header.index(column_name)
        values = [float(row[index]) for row in self.data]

        result = []
        for i in range(len(values) - window_size + 1):
            window = values[i:i + window_size]
            result.append(agg_func(window))

        return result

    def time_series_forecast(self, column_name, method='mean'):
        index = self.header.index(column_name)
        values = [float(row[index]) for row in self.data]

        if method == 'mean':
            forecast = sum(values) / len(values)
        elif method == 'linear':
            x = list(range(len(values)))
            slope, intercept = self._linear_regression(x, values)
            forecast = slope * (len(values) + 1) + intercept
        else:
            raise ValueError("Method not supported")

        return forecast

    def _linear_regression(self, x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x_squared = sum(x_i ** 2 for x_i in x)

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept

    # Erweiterte Statistische Funktionen
    def z_score(self, column_name):
        index = self.header.index(column_name)
        values = [float(row[index]) for row in self.data]
        mean = sum(values) / len(values)
        std_dev = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
        return [(value - mean) / std_dev for value in values]

    def percentile(self, column_name, percentile):
        index = self.header.index(column_name)
        values = [float(row[index]) for row in self.data]
        values.sort()
        k = (len(values) - 1) * percentile / 100
        f = int(k)
        c = f + 1 if f + 1 < len(values) else f
        return values[f] + (values[c] - values[f]) * (k - f)

    def correlation_matrix(self, columns):
        indices = [self.header.index(col) for col in columns]
        data = [[float(row[i]) for i in indices] for row in self.data]
        n = len(data)
        means = [sum(col) / n for col in zip(*data)]
        matrix = []
        for i in range(len(indices)):
            row = []
            for j in range(len(indices)):
                covariance = sum((data[k][i] - means[i]) * (data[k][j] - means[j]) for k in range(n)) / (n - 1)
                std_dev_i = (sum((data[k][i] - means[i]) ** 2 for k in range(n)) / (n - 1)) ** 0.5
                std_dev_j = (sum((data[k][j] - means[j]) ** 2 for k in range(n)) / (n - 1)) ** 0.5
                correlation = covariance / (std_dev_i * std_dev_j)
                row.append(correlation)
            matrix.append(row)
        return matrix

    # Textbasierte Abfragen
    def contains_text(self, column_name, text):
        index = self.header.index(column_name)
        return [row for row in self.data if text in row[index]]

    def starts_with(self, column_name, prefix):
        index = self.header.index(column_name)
        return [row for row in self.data if row[index].startswith(prefix)]

    def ends_with(self, column_name, suffix):
        index = self.header.index(column_name)
        return [row for row in self.data if row[index].endswith(suffix)]
