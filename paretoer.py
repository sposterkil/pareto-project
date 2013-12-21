#!/usr/bin/env python

import sys
import csv
import string


class CSVParetoer():

    """
    This class represents an instance of paretoization.  In short,
    it operates on a CSV file and produces another file with a list
    of tags to be applied to that file.
    """

    def __init__(self, input_path, output_path):
        self.input_file = open(input_path, "r")
        self.output_file = open(output_path, "w")
        self.stop_words = open("stopwords.txt", "r").read().split()
        self.counts = {}

    def update_counts(self, str_to_count):
        zero_punctuation = str_to_count.translate(None, string.punctuation)
        word_list = zero_punctuation.split()
        for word in word_list:
            word = word.upper()
            if word not in self.stop_words:
                if word in self.counts:
                    self.counts[word] += 1
                else:
                    self.counts[word] = 1

    def pareto(self, column_list):
        dialect = csv.Sniffer().sniff(self.input_file.read(1024))
        self.input_file.seek(0)
        reader = csv.reader(self.input_file, dialect)
        if csv.Sniffer().has_header(self.input_file.read(1024)):
            print "Reading from these columns:"
            for number in column_list:
                print reader.next()[number]
        else:
            reader.next()

        for line in reader:
            for number in column_list:
                self.update_counts(line[number])

    def write_counts(self):
        count_tuples = self.counts.iteritems()
        sorted_tuples = sorted(count_tuples, key=lambda word: -word[1])
        for word, count in sorted_tuples:
            self.output_file.write("%s: %s" % (word, count))
            self.output_file.write("\n")

if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    column_string = raw_input(
        'Which columns would you like to read from? Numbers separated by commas, please.\n')
    column_list = [int(x) - 1 for x in column_string.split(",")]
    print "Opening files..."
    paretoer = CSVParetoer(input_path, output_path)
    print "Counting..."
    paretoer.pareto(column_list)
    print 'Writing output...'
    paretoer.write_counts()
    print "Complete."
