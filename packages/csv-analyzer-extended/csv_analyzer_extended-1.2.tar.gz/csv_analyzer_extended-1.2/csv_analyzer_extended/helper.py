# helper.py

class CSVAnalyzerHelp:
    def show_help(self):
        help_text = """
        CSVAnalyzer Extended API - Hilfe und Überblick

        Diese API bietet eine Vielzahl von Funktionen zur Analyse, Bereinigung, Filterung und Visualisierung von CSV-Daten.

        Verfügbare Klassen und ihre Methoden:
        
        1. CSVAnalyzer:
            - __init__(file_path): Initialisiert den Analyzer mit dem Pfad zur CSV-Datei.
            - incremental_mean(column_name): Berechnet den Mittelwert einer Spalte.
            - incremental_median(column_name): Berechnet den Median einer Spalte.
            - calculate_std_dev(column_name): Berechnet die Standardabweichung einer Spalte.
            - calculate_variance(column_name): Berechnet die Varianz einer Spalte.
            - detect_anomalies_simple(column_name, threshold=1.5): Ermittelt einfache Anomalien in einer Spalte.
            - calculate_correlation(col1, col2, method='pearson'): Berechnet die Korrelation zwischen zwei Spalten.
            - linear_regression(target_col, *feature_cols): Führt eine lineare Regression durch.
            - moving_average(column_name, window_size): Berechnet den gleitenden Durchschnitt einer Spalte.
            - remove_duplicates(): Entfernt doppelte Einträge.
            - fill_missing_values(column_name, strategy="mean"): Füllt fehlende Werte in einer Spalte auf.
            - normalize_column(column_name): Normalisiert die Werte einer Spalte.
            - standardize_column(column_name): Standardisiert die Werte einer Spalte.
            - parallel_analyze(column_names, output_files, num_threads=4): Führt eine parallele Analyse durch.

        2. CSVSummarizer:
            - most_frequent_values(column_name): Gibt die häufigsten Werte einer Spalte zurück.
            - find_outliers(column_name, threshold=1.5): Findet Ausreißer in einer Spalte.
            - create_histogram(column_name): Erstellt ein Histogramm für eine Spalte.
            - calculate_sum(column_name): Berechnet die Summe der Werte in einer Spalte.
            - calculate_max(column_name): Findet den maximalen Wert in einer Spalte.
            - calculate_min(column_name): Findet den minimalen Wert in einer Spalte.

        3. CSVSorter:
            - sort_by_column(column_name, reverse=False): Sortiert die Daten nach einer Spalte.
            - multi_column_sort(column_names, reverse=False): Sortiert die Daten nach mehreren Spalten.
            - parallel_sort(column_name, num_threads=4, reverse=False): Führt eine parallele Sortierung der Daten nach einer Spalte durch.

        4. CSVFilter:
            - filter_by_numeric_range(column_name, min_value=None, max_value=None): Filtert die Daten nach einem numerischen Bereich.
            - filter_by_text_pattern(column_name, pattern): Filtert die Daten nach einem Textmuster (Regex).
            - filter_by_date_range(column_name, start_date, end_date, date_format='%Y-%m-%d'): Filtert die Daten nach einem Datumsbereich.
            - filter_by_custom_function(column_name, custom_func): Filtert die Daten basierend auf einer benutzerdefinierten Funktion.
            - normalize_column(column_name): Normalisiert die Werte einer Spalte.
            - rank_column(column_name): Ordnet die Werte einer Spalte nach Rang.
            - filter_by_condition_chain(conditions): Filtert die Daten basierend auf einer Kette von Bedingungen.
            - multidimensional_filter(filters): Führt eine flexible Filterung basierend auf mehreren Kriterien durch.

        5. CSVExporter:
            - export_to_csv(file_path): Exportiert die Daten in eine CSV-Datei.
            - export_to_json(file_path): Exportiert die Daten in eine JSON-Datei.
            - export_to_sql(table_name, cursor): Exportiert die Daten in eine SQL-Datenbank.

        Beispiel für die Nutzung der API:
        from csv_analyzer_extended import CSVAnalyzer, CSVSummarizer, CSVSorter, CSVFilter, CSVExporter

        # Analyse und Bereinigung
        analyzer = CSVAnalyzer('data.csv')
        mean = analyzer.incremental_mean('score')
        std_dev = analyzer.calculate_std_dev('score')
        analyzer.remove_duplicates()

        # Zusammenfassung
        summarizer = CSVSummarizer(analyzer.data, analyzer.header)
        frequent_values = summarizer.most_frequent_values('score')

        # Sortierung
        sorter = CSVSorter(analyzer.data, analyzer.header)
        sorted_data = sorter.sort_by_column('score')

        # Filterung
        filterer = CSVFilter(analyzer.data, analyzer.header)
        filtered_data = filterer.filter_by_numeric_range('score', 80, 90)
        filtered_data_by_date = filterer.filter_by_date_range('date', '2023-01-01', '2023-01-05')

        # Export
        exporter = CSVExporter(filtered_data, analyzer.header)
        exporter.export_to_csv('filtered_data.csv')

        Für weitere Informationen konsultieren Sie bitte die vollständige Dokumentation.
        """
        print(help_text)
