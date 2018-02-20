#!/usr/bin/env python
import sys
import argparse

class Analyser(object):
    def __init__(self):
        self.freq = {}

    @staticmethod
    def generate_transitions(states):
        previous_state = "$"
        for current_state in states:
            yield previous_state + "-1>" + current_state
            previous_state = current_state
        state_len = len(states)
        if state_len == 3:
            yield states[0] + "-2>" + states[2]

    @staticmethod
    def generate_states(string):
        states = []
        string = string[:4]
        states += [list(string)]
        states += [[string[x:x+2] for x in range(3)]]
        states += [[string[x:x+3] for x in range(2)]]
        return states

    def generate_freq_table_from_file(self, file):
        with open(file, "r") as fp:
            self.generate_freq_table(fp.readlines())

    def generate_freq_table(self, lines):
        for line in lines:
            acc = line.strip()[:4]
            states = Analyser.generate_states(acc)
            for state_set in states:
                for transition in Analyser.generate_transitions(state_set):
                    if transition in self.freq.keys():
                        self.freq[transition] += 1
                    else:
                        self.freq[transition] = 1

    def analyse_candidate(self, abv):
        abv = abv[:4]
        states = Analyser.generate_states(abv)
        for state_set in states:
            for transition in Analyser.generate_transitions(state_set):
                print(transition)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    an = Analyser()
    an.generate_freq_table_from_file(args.file)
    an.analyse_candidate("EMBS")
