#!/usr/bin/env python


import csv
import os
import tkFileDialog
import Tkinter as Tk
import webbrowser
from paretoer import CSVParetoer, CSVTagger
from shutil import copyfile


def get_parent_dir(findfile):
    return os.path.dirname(os.path.realpath(findfile.name))


class AutoScrollbar(Tk.Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Tk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        pass

    def place(self, **kw):
        pass


class TkinterGUI(Tk.Frame):

    def __init__(self, root):
        Tk.Frame.__init__(self, root)
        self.grid(sticky=Tk.N + Tk.W + Tk.E + Tk.S)
        self.create_widgets()

    def create_widgets(self):
        # define items
        headerframe = Tk.LabelFrame(self, text="Select Columns to Count")
        scrollbar = AutoScrollbar(headerframe)
        self.header_list = Tk.Listbox(headerframe, selectmode=Tk.MULTIPLE,
                                      yscrollcommand=scrollbar.set, bd=0)
        scrollbar.config(command=self.header_list.yview)
        headerframe.grid_rowconfigure(1, weight=1)
        headerframe.grid_columnconfigure(0, weight=1)

        self.open_button = Tk.Button(self,
                                     text='Choose a CSV file to tag',
                                     command=self.choose_file)
        self.count_button = Tk.Button(self,
                                      text="Pareto!",
                                      command=self.start_pareto)
        self.tag_button = Tk.Button(self,
                                    text="Tag File",
                                    command=self.tag_file)

        # add items
        self.header_list.grid(row=1, column=0,
                              sticky=Tk.N + Tk.S + Tk.W + Tk.E)
        scrollbar.grid(row=1, column=1,
                       sticky=Tk.N + Tk.S)

        self.open_button.pack()
        headerframe.pack(fill="both", expand=True)
        self.count_button.pack()
        self.tag_button.pack()

        for x in xrange(3):
            self.columnconfigure(x, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Disable buttons until they're needed
        self.count_button.config(state=Tk.DISABLED)
        self.tag_button.config(state=Tk.DISABLED)

        # Default File Dialog options
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('csv files', '.csv')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'Choose File'

    def update_header_list(self, items_to_add):
        self.header_list.delete(0, Tk.END)
        for item in items_to_add:
            self.header_list.insert(Tk.END, item)

    def choose_file(self):
        try:
            self.done_msg.pack_forget()
            self.edit_msg.pack_forget()
        except Exception, e:
            pass
        self.file_to_tag = tkFileDialog.askopenfile(mode='r', **self.file_opt)
        self.tag_path = os.path.join(get_parent_dir(self.file_to_tag),
                                     "tagfile.txt")
        self.file_to_tag.seek(0)
        headers = next(csv.reader(self.file_to_tag))
        self.update_header_list(headers)
        copyfile(self.file_to_tag.name, self.file_to_tag.name + ".BAK")
        self.count_button.config(state=Tk.NORMAL)

    def start_pareto(self):
        with open(self.tag_path, "w") as tag_out:
            self.file_to_tag.seek(0)
            self.counter = CSVParetoer(1, self.file_to_tag, tag_out)
            self.column_list = [int(x)
                                for x in self.header_list.curselection()]
            self.counter.pareto(self.column_list)
            self.counter.write_counts()

        self.count_button.config(state=Tk.DISABLED)
        self.tag_button.config(state=Tk.NORMAL)
        self.edit_msg = Tk.Message(self, text="Please edit tagfile.txt in\
 the same directory as the chosen csv file to select your tags.")
        self.edit_msg.pack()
        webbrowser.open(self.tag_path)

    def tag_file(self):
        self.edit_msg.pack_forget()

        with open(self.tag_path, "r") as tag_in:
            tagger = CSVTagger(self.column_list, tag_in, self.file_to_tag)
            tagger.add_tags()

        self.header_list.delete(0, Tk.END)
        self.tag_button.config(state=Tk.DISABLED)
        self.done_msg = Tk.Label(self, text="Done.")
        self.done_msg.pack()


if __name__ == '__main__':
    root = Tk.Tk()
    root.wm_title("Paretoizer")
    root.minsize(300, 400)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    TkinterGUI(root).grid(padx=10, pady=10, sticky=Tk.N + Tk.S + Tk.W + Tk.E)
    root.mainloop()
