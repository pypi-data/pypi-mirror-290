from threading import Thread
import multiprocessing as mp
import mmap

class CSVSorter:
    def __init__(self, data, header):
        self.data = data
        self.header = header

    def sort_by_column(self, column_name, reverse=False):
        index = self.header.index(column_name)
        return sorted(self.data, key=lambda row: row[index], reverse=reverse)

    def multi_column_sort(self, column_names, reverse=False):
        indices = [self.header.index(name) for name in column_names]
        sorted_data = sorted(self.data, key=lambda row: tuple(row[i] for i in indices), reverse=reverse)
        return sorted_data

    def parallel_sort(self, column_name, num_threads=4, reverse=False):
        index = self.header.index(column_name)
        chunk_size = len(self.data) // num_threads
        chunks = [self.data[i:i + chunk_size] for i in range(0, len(self.data), chunk_size)]

        sorted_chunks = [None] * num_threads
        threads = []

        def sort_chunk(chunk_idx):
            sorted_chunks[chunk_idx] = sorted(chunks[chunk_idx], key=lambda row: row[index], reverse=reverse)

        for i in range(num_threads):
            thread = Thread(target=sort_chunk, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return [item for sublist in sorted_chunks for item in sublist]

    def memory_mapped_sort(self, column_name, file_path, reverse=False):
        index = self.header.index(column_name)
        with open(file_path, 'r+', encoding='utf-8') as f:
            mmapped_file = mmap.mmap(f.fileno(), 0)
            data = mmapped_file.read().decode('utf-8').splitlines()
            sorted_data = sorted(data, key=lambda line: line.split(',')[index], reverse=reverse)
            mmapped_file.seek(0)
            mmapped_file.write('\n'.join(sorted_data).encode('utf-8'))
            mmapped_file.close()

    def multiprocessing_sort(self, column_name, reverse=False):
        index = self.header.index(column_name)
        with mp.Pool(processes=mp.cpu_count()) as pool:
            sorted_data = pool.map(sorted, self.data, chunksize=len(self.data)//mp.cpu_count())
            sorted_data = [item for sublist in sorted_data for item in sublist]
        return sorted(sorted_data, key=lambda row: row[index], reverse=reverse)

    def optimized_sort(self, column_name, file_path=None, reverse=False, use_parallel=True):
        """Optimierte Sortierung mit mehreren Optionen."""
        if file_path:
            print(f"Using memory-mapped sort for file: {file_path}")
            self.memory_mapped_sort(column_name, file_path, reverse)
        elif use_parallel:
            print("Using parallel sort")
            return self.parallel_sort(column_name, reverse=reverse)
        else:
            print("Using standard sort")
            return self.sort_by_column(column_name, reverse=reverse)
