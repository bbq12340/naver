import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from threading import Thread

from ScrapeNaverPowerlinks import Scraper

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.v = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        self.label_frame = tk.Frame(self)
        self.filename_label = tk.Label(self.label_frame, text="")
        self.filename_label.grid(row=0, column=1)
        self.request_label = tk.Label(self.label_frame, text='요청 파일명:')
        self.request_label.grid(row=0, column=0)
        self.label_frame.pack(pady=5, padx=5)

        self.btn_frame = tk.Frame(self)
        self.only_powerlinks = tk.Radiobutton(self.btn_frame, text="파워링크만", variable=self.v, value=1).pack()
        self.phone_numbers = tk.Radiobutton(self.btn_frame, text="전화번호", variable=self.v, value=2).pack()
        self.btn_frame.pack(pady=5, padx=5)

        self.file_btn = tk.Button(self, text='파일 탐색', command=self.add_file)
        self.file_btn.pack(pady=5, padx=5)
        self.search_btn = tk.Button(self, text="검색", command=self.start_process)
        self.search_btn.pack(pady=5, padx=5)

        self.progress_frame = tk.Frame(self)
        self.query_progress = tk.Label(self.progress_frame, text="요청 검색어:")
        self.query_progress.grid(row=0, column=0)
        self.progress = ttk.Progressbar(self.progress_frame, length=150)
        self.progress_label = tk.Label(self.progress_frame, text="")
        self.progress.grid(row=1, column=0, padx=5)
        self.progress_label.grid(row=1, column=1, padx=5)
        self.progress_frame.pack(pady=5, padx=5)

    
    def add_file(self):
        filename = filedialog.askopenfilename(initialdir='./list', title='파일 탐색', filetypes=[("text files", "*.txt")])
        self.filename_label.config(text=f"{filename.split('/')[-1]}")
        self.FILENAME = filename

    
    def start_process(self):
        self.thread = Thread(target=self.scrape)
        self.thread.start()
        return
    
    def scrape(self):
        with open(self.FILENAME, 'r', encoding='utf-8-sig') as f:
            query_list = f.read().splitlines()
        for query in query_list:
            self.query_progress.config(text=f"요청 검색어:{query} ({query_list.index(query)+1}/{len(query_list)})")
            self.master.update_idletasks()
            app = Scraper(query, self.progress, self.master)
            if self.v.get() == 1:
                self.progress_label.config(text="1/1")
                df = app.extract_powerlinks()
            else:
                self.progress_label.config(text="1/2")
                df = app.extract_powerlinks()
                self.progress['value'] = 0
                self.master.update_idletasks()
                self.progress_label.config(text="2/2")
                df = app.extract_phone(df)
            df.to_csv(f'{query}.csv', index=False, encoding='utf-8-sig')
            self.progress['value'] = 0
            self.master.update_idletasks()

        messagebox.showinfo('info', message="크롤링 완료!")
        return


root = tk.Tk()
root.title("파워링크 크롤러")
root.geometry("400x400")
app = Application(master=root)
app.mainloop()
