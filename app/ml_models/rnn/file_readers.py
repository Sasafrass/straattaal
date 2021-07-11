import glob
import re


class SlangReader:
    def __init__(self):
        """Initialize the SlangReader object."""
        pass

    def __repr__(self):
        return "I am a SlangReader object."

    def find_files(self, path):
        """TODO: Say what this does."""
        return glob.glob(path)

    def read_lines(self, filename):
        lines = open(filename, encoding="utf-8").read().strip().split("\n")
        lines = [s.lower() for s in lines]
        lines = [re.sub("[\t\s]", "", s) for s in lines]

        return lines
