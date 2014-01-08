#!/usr/bin/env python

import csv
import os
import Tkconstants
import tkFileDialog
import Tkinter as Tk
from paretoer import CSVParetoer, CSVTagger


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

        # pack items
        self.open_button.pack(**button_opt)
        self.header_chooser.pack()

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

    def get_parent_directory(self, findfile):
        return os.path.dirname(os.path.realpath(findfile.name))

    def update_header_chooser(self, items_to_add):
        for item in items_to_add:
            self.header_chooser.insert(Tk.END, item)

    def choose_file(self):
        """Returns an opened file in read mode."""
        file_to_tag = tkFileDialog.askopenfile(mode='r', **self.file_opt)
        tag_file = open(self.get_parent_directory(file_to_tag)
                        + "tagtile.txt", "w")
        headers = next(csv.reader(file_to_tag))
        file_to_tag.seek(0)
        self.counter = CSVParetoer(1, file_to_tag, tag_file)
        self.update_header_chooser(headers)
        self.open_button.config(state=Tk.DISABLED)

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
