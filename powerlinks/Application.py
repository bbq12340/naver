import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread

from ScrapeNaverPowerlinks import Scraper

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.query = tk.StringVar()
        self.v = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        self.label_frame = tk.Frame(self)
        self.search_label = tk.Label(self.label_frame, text="검색어")
        self.search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(self.label_frame, textvariable=self.query)
        self.search_entry.pack(side=tk.LEFT)
        self.label_frame.pack(pady=5, padx=5)

        self.btn_frame = tk.Frame(self)
        self.only_powerlinks = tk.Radiobutton(self.btn_frame, text="파워링크만", variable=self.v, value=1).pack()
        self.phone_numbers = tk.Radiobutton(self.btn_frame, text="전화번호", variable=self.v, value=2).pack()
        self.btn_frame.pack(pady=5, padx=5)

        self.search_btn = tk.Button(self, text="검색", command=self.start_process)
        self.search_btn.pack(pady=5, padx=5)

        self.progress_frame = tk.Frame(self)
        self.progress = ttk.Progressbar(self.progress_frame, length=150)
        self.progress_label = tk.Label(self.progress_frame, text="")
        self.progress.grid(row=0, column=0, padx=5)
        self.progress_label.grid(row=0, column=1, padx=5)
        self.progress_frame.pack(pady=5, padx=5)

    
    def start_process(self):
        self.thread = Thread(target=self.scrape)
        self.thread.start()
        return
    
    def scrape(self):
        app = Scraper(self.query.get(), self.progress, self.master)
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
        df.to_csv(f'{self.query.get()}.csv', index=False, encoding='utf-8-sig')
        self.progress['value'] = 0
        self.master.update_idletasks()
        messagebox.showinfo('info', message="크롤링 완료!")
        return


root = tk.Tk()
root.title("파워링크 크롤러")
root.geometry("400x400")
app = Application(master=root)
app.mainloop()
