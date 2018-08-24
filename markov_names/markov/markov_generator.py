
from markov_names import MarkovModel


class MarkovGenerator:
    def __init__(self, order=0, prior=0, data=None, models=None, json_data=None):
        if json_data is None:
            self.order = order
            self.prior = prior

            if models is None:
                self.alphabet = list()
                for word in data:
                    for i in range(len(word)):
                        if word[i] not in self.alphabet:
                            self.alphabet.append(word[i])

                self.alphabet.sort()
                self.alphabet.insert(0, '#')

                self.models = list()
                for i in range(order):
                    self.models.append(MarkovModel(order - i, prior, self.alphabet, data))
            else:
                self.models = models
        else:
            self.order = json_data['order']
            self.prior = json_data['prior']
            self.alphabet = json_data['alphabet']
            self.models = list()

            for d in json_data['models']:
                self.models.append(MarkovModel(d['model-order'], json_data['prior'], json_data['alphabet'],
                                               observations=d['observations'], chains=d['chains']))

    def get_letter(self, context):
        letter = None
        context = context[-self.order:]

        for model in self.models:
            letter = model.generate(context)
            if letter is None:
                context = context[1:]
            else:
                break

        return letter

    def generate(self):
        word = '#' * self.order
        letter = self.get_letter(word)

        while letter != '#':
            if letter is not None:
                word += letter

            letter = self.get_letter(word)

        return word

    def print(self):
        print('order:    ' + str(self.order))
        print('prior:    ' + str(self.prior))
        for i in range(self.order):
            print('>> model, order: ' + str(self.order - i))
            self.models[i].print()

    def to_json(self):
        return {'order': self.order, 'prior': self.prior, 'alphabet': self.alphabet, 'models': self.models}
