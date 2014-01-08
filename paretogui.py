#!/usr/bin/env python

import csv
import os
import Tkconstants
import tkFileDialog
import Tkinter as Tk
from paretoer import CSVParetoer, CSVTagger


def get_parent_dir(findfile):
    return os.path.dirname(os.path.realpath(findfile.name))


class TkinterGUI(Tk.Frame):

    def __init__(self, root):
        Tk.Frame.__init__(self, root)

        # Default Button options
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

        # define items
        self.open_button = Tk.Button(self,
                                     text='Choose a CSV file to tag',
                                          command=self.choose_file)
        self.header_chooser = Tk.Listbox(self, selectmode=Tk.MULTIPLE)
        self.count_button = Tk.Button(self,
                                      text="Pareto!",
                                      command=self.start_pareto)
        self.tag_button = Tk.Button(self,
                                    text="Tag File",
                                    command=self.tag_file)

        # pack items
        self.open_button.pack(**button_opt)
        self.header_chooser.pack()
        self.count_button.pack(**button_opt)
        self.tag_button.pack(**button_opt)

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

        # Default Directory Dialog options
        options['initialdir'] = 'C:\\'
        options['parent'] = root
        options['title'] = 'Choose A Directory'

    def tag_file(self):
        pass

    def update_header_chooser(self, items_to_add):
        for item in items_to_add:
            self.header_chooser.insert(Tk.END, item)

    def choose_file(self):
        """Returns an opened file in read mode."""
        self.file_to_tag = tkFileDialog.askopenfile(mode='r', **self.file_opt)
        headers = next(csv.reader(self.file_to_tag))
        self.file_to_tag.seek(0)
        self.update_header_chooser(headers)
        self.open_button.config(state=Tk.DISABLED)
        self.count_button.config(state=Tk.NORMAL)

    def start_pareto(self):
        self.tag_file = open(os.path.join(get_parent_dir(self.file_to_tag),
                                          "tagfile.txt"), "w")
        self.counter = CSVParetoer(1, self.file_to_tag, self.tag_file)
        column_list = map(int, self.header_chooser.curselection())
        self.counter.pareto(column_list)
        self.counter.write_counts()
        self.count_button.config(state=Tk.DISABLED)
        self.tag_button.config(state=Tk.NORMAL)
        print "Please edit tagfile.txt in the same directory as the chosen csv file to select your tags."

    def asksaveasfile(self):
        """Returns an opened file in write mode."""

        return tkFileDialog.asksaveasfile(mode='w', **self.file_opt)

    def askdirectory(self):
        """Returns a selected directoryname."""

        return tkFileDialog.askdirectory(**self.dir_opt)


if __name__ == '__main__':
    root = Tk.Tk()
    root.wm_title("Paretoizer")
    TkinterGUI(root).pack()
    root.mainloop()
