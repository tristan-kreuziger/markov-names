
import json

from markov_names import MarkovGenerator
from markov_names import CustomEncoder


class NameGenerator:
    def __init__(self, data=None, order=0, prior=0, min_length=0, max_length=0, starts_with='', ends_with='',
                 includes='', excludes='', allow_originals=False, filename=''):
        if filename == '':
            self.generator = MarkovGenerator(order, prior, data)
            self.min_length = min_length
            self.max_length = max_length
            self.starts_with = starts_with
            self.ends_with = ends_with
            self.includes = includes
            self.excludes = excludes
            self.allow_originals = allow_originals
            self.data = data
        else:
            with open(filename, 'r') as f:
                d = json.load(f)
                self.min_length = d['min-length']
                self.max_length = d['max-length']
                self.starts_with = d['starts-with']
                self.ends_with = d['ends-with']
                self.includes = d['includes']
                self.excludes = d['excludes']
                self.allow_originals = d['allow-originals']
                self.data = d['data']
                self.generator = MarkovGenerator(json_data=d['generator'])

    def generate_name(self):
        name = self.generator.generate()
        name = name.replace('#', '')

        if self.min_length > 0 and self.min_length > len(name):
            return ''

        if 0 < self.max_length < len(name):
            return ''

        if not (name.startswith(self.starts_with) and name.endswith(self.ends_with)):
            return ''

        if not (self.includes in name and (self.excludes == '' or self.excludes in name)):
            return ''

        if not self.allow_originals and name in self.data:
            return ''

        return name[0].upper() + name[1:]

    def generate_valid_name(self):
        name = self.generate_name()
        while name == '':
            name = self.generate_name()

        return name

    def generate_names(self, num):
        return [self.generate_valid_name() for _ in range(num)]

    def print(self):
        self.generator.print()

    def to_json(self):
        return {'generator': self.generator, 'data': self.data, 'min-length': self.min_length,
                'max-length': self.max_length, 'starts-with': self.starts_with, 'ends-with': self.ends_with,
                'includes': self.includes, 'excludes': self.excludes, 'allow-originals': self.allow_originals}

    def save_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self, file, cls=CustomEncoder, indent=2, sort_keys=False, ensure_ascii=False)


def create_name_generator_from_file(filename, order, **kwargs):
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read().split(' ')

    return NameGenerator(order=order, data=data, **kwargs)
