
import numpy as np


class MarkovModel:
    def __init__(self, order, prior, alphabet, data=None, observations=None, chains=None):
        self.order = order
        self.prior = prior
        self.alphabet = alphabet

        if observations is None:
            self.observations = dict()
            self.train(data)
        else:
            self.observations = observations

        if chains is None:
            self.chains = dict()
            self.build_chains()
        else:
            self.chains = chains

    def train(self, data):
        for d in data:
            d = '#' * self.order + d + '#'

            for i in range(len(d) - self.order):
                key = d[i:i + self.order]
                if key in self.observations.keys():
                    value = self.observations[key]
                else:
                    value = list()
                    self.observations[key] = value

                value.append(d[i + self.order])

    def retrain(self, data):
        if data is None:
            return

        self.train(data)
        self.build_chains()

    def build_chains(self):
        for context in self.observations.keys():
            for prediction in self.alphabet:
                if context in self.chains.keys():
                    value = self.chains[context]
                else:
                    value = list()
                    self.chains[context] = value

                value.append(self.prior + _count_matches(self.observations[context], prediction))

    def generate(self, context):
        if context not in self.chains.keys():
            return None
        else:
            chain = self.chains[context]
            return self.alphabet[_select_index(chain)]

    def print(self):
        print('alphabet: ' + str(self.alphabet))
        for context in self.observations.keys():
            print('context: ' + context + ' -> ', end='')
            for prediction in self.alphabet:
                print(prediction + ': ' + str(self.prior + _count_matches(self.observations[context], prediction)), end=', ')

            print()

    def to_json(self):
        return {'model-order': self.order, 'observations': self.observations, 'chains': self.chains}

    def get_seed(self, char):
        pass


def _select_index(chain):
    totals = list()
    accumulator = 0

    for weight in chain:
        accumulator += weight
        totals.append(accumulator)

    rand = np.random.uniform() * accumulator
    for i in range(len(totals)):
        if rand < totals[i]:
            return i

    return 0


def _count_matches(array, s):
    if array is None or len(array) == 0:
        return 0

    i = 0
    for c in array:
        if c == s:
            i += 1

    return i
