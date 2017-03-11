import pandas as pd
from tkinter import *
from tkinter import filedialog
import os
import numpy as np


MATCHES_FILENAME = './matches.csv'
NM_FILENAME = './no_matches.csv'
UNI_SEQ = 'ACACTCCAGCTGGG'


def get_csv_files(LIB_PATH, MIR_PATH):
    # Read in library and query files
    lib = pd.read_csv(LIB_PATH, delimiter=',', header=None, names=['pName', 'pSeq'], index_col=0)
    mir = pd.read_csv(MIR_PATH, delimiter=',', header=None, names=['mirName', 'mirSeq'], index_col=0)
    return lib, mir


def finishedpopup():
    toplevel = Toplevel()
    toplevel.geometry('300x100')
    Label(toplevel, text='Scan Finished!').pack()
    toplevel.focus_force()


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title('miRNA Primer Library Scanner')
        self.pack(fill=BOTH, expand=1)

        libraryopenButton = Button(
            self, text='Library File', command=self.askopenlibrary)
        libraryopenButton.place(x=300, y=10)

        queryopenButton = Button(
            self, text='Query File', command=self.askopenquery)
        queryopenButton.place(x=300, y=60)

        scanButton = Button(self, text='Scan', command=self.scan)
        scanButton.place(x=300, y=110)

        self.librarytext = Entry(self, width=35)
        self.librarytext.place(x=0, y=10)

        self.querytext = Entry(self, width=35)
        self.querytext.place(x=0, y=60)

        # Options for Import File dialogue box
        self.file_opt = options = {}
        options['filetypes'] = [('Comma Separated Value File', '*.csv'),
                                ('All files', '*.*')]
        options['title'] = 'Import File'
        options['initialdir'] = os.getcwd()

    # Library file, deletes text in text box and replaces with filename selected
    def askopenlibrary(self):
        if len(self.librarytext.get()) != 0:
            self.librarytext.delete('0', END)
        self.librarytext.insert(END, filedialog.askopenfilename(**self.file_opt))

    # Library file, deletes text in text box and replaces with filename selected
    def askopenquery(self):
        if len(self.querytext.get()) != 0:
            self.querytext.delete('0', END)
        self.querytext.insert(END, filedialog.askopenfilename(**self.file_opt))

    # Checks for filenames in textboxes, then proceedes with conversion
    def scan(self):
        lib, mir = get_csv_files(self.librarytext.get(), self.querytext.get())

        # RNA to DNA, removes spaces in sequences, creates primer seq from mirSeq
        mir['mirSeq'] = mir['mirSeq'].apply(lambda y: y.upper())
        mir['mirSeq'] = mir['mirSeq'].str.replace('U', 'T')
        mir['mirSeq'] = mir['mirSeq'].str.replace(' ', '')
        lib['pSeq'] = lib['pSeq'].str.replace(' ', '')
        mir['pSeq'] = UNI_SEQ + mir['mirSeq'].str[:15]
        # Finds primer matches from library and appends column
        matches = []
        for mirSeq in mir['pSeq']:
            matches.append(', '.join(lib[lib['pSeq'] == mirSeq].index.tolist()))
        mir['matches'] = matches
        mir.matches = mir.matches.apply(lambda y: np.nan if len(y) == 0 else y)

        # Reset index as first column, append miRNA with no matches to new dataframe
        mir.reset_index(level=0, inplace=True)
        mirNM = mir[mir['matches'].isnull()]
        mir.dropna(inplace=True)

        # Determine if miRNA in list have unique primers
        unique = []
        for match in mir['matches']:
            if len(mir[mir['matches'] == match]) > 1:
                unique.append('NOT UNIQUE')
            else:
                unique.append('OK')
        mir['unique'] = unique

        mir.sort_values('matches', inplace=True)
        mirNM.sort_values('mirName', inplace=True)

        mir.to_csv(MATCHES_FILENAME, sep=',', index=False)
        mirNM.to_csv(NM_FILENAME, sep=',', index=False)

        finishedpopup()

if __name__ == '__main__':
    gui = Tk()
    gui.geometry('400x150')
    gui.resizable(width=False, height=False)
    app = Window(gui)
    gui.mainloop()
