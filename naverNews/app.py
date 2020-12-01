import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from threading import Thread
import pandas as pd
import numpy as np
from datetime import datetime

from Scraper import Scraper

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.page = tk.IntVar(value="")
        self.delay_time = tk.DoubleVar()
        self.create_widgets()
        

    def create_widgets(self):
        #Label
        self.filename_label = tk.Label(self, text="")
        self.filename_label.grid(row=0, column=1)

        self.request_label = tk.Label(self, text='요청 파일명:')
        self.request_label.grid(row=0, column=0)

        self.page_label = tk.Label(self, text="최대 페이지:")
        self.page_label.grid(row=1, column=0)

        self.page_entry = tk.Entry(self, width=3, textvariable=self.page)
        self.page_entry.grid(row=1, column=1)

        #ProgressBar
        self.progress = Progressbar(self,orient=tk.HORIZONTAL,length=150)
        self.progress.grid(row=2,column=0,columnspan=2,pady=5)

        self.progress_label = tk.Label(self, text="")
        self.progress_label.grid(row=2, column=2, pady=5)

        #Button
        self.search_btn = tk.Button(self, text='파일 탐색', command=self.add_file)
        self.search_btn.grid(row=3, column=0, pady=5)


        self.start_btn = tk.Button(self, text="시작", command=self.start)
        self.start_btn.grid(row=3, column=1, pady=5)
    
    def add_file(self):
        filename = filedialog.askopenfilename(initialdir='./list', title='파일 탐색', filetypes=[("text files", "*.txt")])
        self.filename_label.config(text=f"{filename.split('/')[-1]}")
        self.FILENAME = filename
    
    def start(self):
        thread = Thread(target=self.scrape)
        thread.start()

    def scrape(self):
        with open (self.FILENAME, 'r', encoding='utf-8-sig') as f:
            url_list = f.read().splitlines()
        app = Scraper()
        for url in url_list:
            now = datetime.now().strftime("%Y%m%d_%H%M")
            self.progress_label.config(text=f"{url_list.index(url)+1}/{len(url_list)}")
            EXTRACTED=[]
            p=1
            while p<=self.page.get():
                self.progress['value'] = (p/self.page.get())*100
                root.update_idletasks()
                data = app.extract_main_url(url, p)
                EXTRACTED.extend(data)
                p+=1
                if p>self.page.get():
                    break
            df = pd.DataFrame(EXTRACTED)
            df = df.dropna(0, 'all')
            df.to_csv(f'{now}.csv', encoding='utf-8-sig', index=False)
            self.progress['value'] = 0
            root.update_idletasks()
        messagebox.showinfo('info',message="크롤링 완료!")
        return
        

root = tk.Tk()
root.title('네이버 기자 크롤러')
root.geometry('250x150')
app = Application(master=root)
app.mainloop()
