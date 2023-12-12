import hashlib
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread

class HashChecker:
    def __init__(self):
        self.is_checking = False
        self.is_cancelled = False

    def calculate_hash(self, file_path, algorithm='md5'):
        hash_object = hashlib.new(algorithm)

        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                if self.is_cancelled:
                    return None
                hash_object.update(chunk)

        return hash_object.hexdigest()

    def select_file(self):
        if self.is_checking:
            return

        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.config(text=f'File: {file_path}')
            self.hash_entry.delete(0, tk.END)
            self.calculated_hash_label.config(text='Hash: ')
        else:
            self.file_label.config(text='File: ')
            self.hash_entry.delete(0, tk.END)
            self.calculated_hash_label.config(text='Hash: ')

    def compare_hashes(self):
        if self.is_checking:
            return

        file_path = self.file_label.cget('text')[6:]
        user_hash = self.hash_entry.get()
        if file_path and user_hash:
            self.is_checking = True
            self.is_cancelled = False
            self.result_label.config(text='Comparing Hashes...')
            self.compare_button.config(state='disabled')
            self.select_button.config(state='disabled')
            self.hash_entry.config(state='disabled')
            self.cancel_button.config(state='normal')
            
            def compare():
                calculated_hash = self.calculate_hash(file_path)
                if calculated_hash is None:
                    self.result_label.config(text='Operation canceled')
                else:
                    self.calculated_hash_label.config(text=f'Hash: {calculated_hash}')
                    if user_hash == calculated_hash:
                        self.result_label.config(text='Hashes match')
                    else:
                        self.result_label.config(text='Hashes do not match')
                
                self.is_checking = False
                self.compare_button.config(state='normal')
                self.select_button.config(state='normal')
                self.hash_entry.config(state='normal')
                self.cancel_button.config(state='disabled')

            # background thread
            thread = Thread(target=compare)
            thread.start()
        else:
            self.result_label.config(text='Please select the file and enter the hash')

    def cancel_comparison(self):
        if self.is_checking:
            self.is_cancelled = True

    def show_note(self):
        note = 'If the file you are checking is quite large, please be patient if the program is not responding, it is because the program is reading the file data. The larger the file, the longer the process of reading the file data. It depends on the type of storage you are using.'
        messagebox.showinfo('Note', note)

    def create_window(self):
        window = tk.Tk()
        window.title('Checksum Hash Comparison')
        window.geometry('600x300')
        window.resizable(True, True)

        # select file
        file_frame = tk.Frame(window)
        file_frame.pack(pady=10)

        self.file_label = tk.Label(file_frame, text='File: ', anchor='w', width=50)
        self.file_label.pack(side='left')

        self.select_button = tk.Button(file_frame, text='Select File', command=self.select_file)
        self.select_button.pack(side='left', padx=10)

        # input hash
        hash_frame = tk.Frame(window)
        hash_frame.pack()

        hash_label = tk.Label(hash_frame, text='Hash: ')
        hash_label.pack(side='left')

        self.hash_entry = tk.Entry(hash_frame, width=50)
        self.hash_entry.pack(side='left')

        # calculated hash
        calculated_hash_frame = tk.Frame(window)
        calculated_hash_frame.pack(pady=10)

        self.calculated_hash_label = tk.Label(calculated_hash_frame, text='Hash: ')
        self.calculated_hash_label.pack(side='left')

        # Tombol "Check Hash"
        self.compare_button = tk.Button(window, text='Check Hash', command=self.compare_hashes)
        self.compare_button.pack()

        # Tombol "Batal"
        self.cancel_button = tk.Button(window, text='Cancel', command=self.cancel_comparison, state='disabled')
        self.cancel_button.pack()

        # result comparison
        result_frame = tk.Frame(window)
        result_frame.pack(pady=10)

        self.result_label = tk.Label(result_frame, text='')
        self.result_label.pack()

        # tombol catatan
        note_button = tk.Button(window, text='Note', command=self.show_note)
        note_button.pack()

        return window

hash_checker = HashChecker()
window = hash_checker.create_window()
window.mainloop()