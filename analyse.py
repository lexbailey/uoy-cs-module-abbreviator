#!/usr/bin/env python

class Analyser(object):
    def __init__(self):
        self.freq = {}

    @staticmethod
    def generate_transitions(states):
        """Generate the transitions between letters and groups of letters"""

        #"$" represents the start of the string here
        previous_state = "$"
        for current_state in states:
            yield previous_state + "-1>" + current_state
            previous_state = current_state
        #"$" represents the end of the string here
        yield previous_state + "-1>" + "$"
        #Include both halves as a special transition
        state_len = len(states)
        if state_len == 3:
            yield states[0] + "-2>" + states[2]

    @staticmethod
    def generate_states(string):
        """Generate the states which are transitioned between"""

        string = string[:4]

        #List containing lists of substrings of size
        states = []
        states += [list(string)] #1
        states += [[string[x:x+2] for x in range(3)]] #2
        states += [[string[x:x+3] for x in range(2)]] #3

        return states

    def generate_freq_table_from_file(self, file_name):
        """Helper function to run generate_freq_table on the contents of the specified file.
           Treats each line as containing one ETLA at the start of the line."""

        with open(file_name, "r") as fp:
            self.generate_freq_table(fp.readlines())

    def generate_freq_table(self, lines):
        """Generates the table of frequencies of transitions from the specified ETLAs"""

        #For each ETLA
        for line in lines:
            acc = line.strip()[:4]
            #Get the states (substrings) which are transitioned between
            states = Analyser.generate_states(acc)
            #Build frequency table
            for state_set in states:
                #Get the transitions for each length of states
                for transition in Analyser.generate_transitions(state_set):
                    if transition in self.freq:
                        self.freq[transition] += 1
                    else:
                        self.freq[transition] = 1

    def analyse_candidate(self, abv, normalised=True):
        """Runs a simple frequency analysis on the input ETLA.
           Normalised by the average frequency by default."""

        abv = abv[:4]
        #Generate the states like usual
        states = Analyser.generate_states(abv)
        score = 0
        normal = 0
        average = sum(self.freq.values())/len(self.freq)
        #Go through the states counting their frequency in our table
        for state_set in states:
            for transition in Analyser.generate_transitions(state_set):
                if transition in self.freq:
                    score += self.freq[transition]
                normal += average
        #Normalise if enabled
        return score/(normal if normalised else 1)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("acronym")
    args = parser.parse_args()

    an = Analyser()
    an.generate_freq_table_from_file(args.file_name)

    print(an.analyse_candidate(args.acronym))
