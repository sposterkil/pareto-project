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
        self.counts = {}

        def update_counts(self, str_to_count):
            zero_punctuation = str_to_count.translate(None, string.punctuation)
            word_list = zero_punctuation.split()
            for word in word_list:
                word = word.upper()
                if word in self.counts:
                    self.counts[word] += 1
                else:
                    self.counts[word] = 1

        def pareto(self, column_list):
            dialect = csv.Sniffer().sniff(self.input_file.read(1024))
            input_file.seek(0)
            reader = csv.reader(csvfile, dialect)
            if csv.Sniffer().has_header(self.input_file.read(1024)):
                print "Reading from these columns:"
                for number in column_list:
                    print reader.next()[number]
            else:
                reader.next()

            for line in reader:
                for number in column_list:
                    update_counts(line[number])

        def write_counts(self):
            count_tuples = self.counts.iteritems()
            sorted_tuples = sorted(count_tuples, key=lambda word: word[1])
            for word, count in sorted_tuples:
                self.output_file.write("%s: %s" % word, count)
                self.output_file.write("\n")

if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    column_string = input(
        'Which columns would you like to read from? Numbers separated by commas, please.\n')
    column_list = int(x) for x in column_string.split(",")
    paretoer = CSVParetoer(input_path, output_path)
    paretoer.pareto(column_list)
    paretoer.write_counts()
