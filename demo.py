
import markov_names
import os


if __name__ == '__main__':
    names = markov_names.create_name_generator_from_file(filename=os.path.join('data' , 'tolkien_forenames.txt'),
                                                         order=2, min_length=5, max_length=8)

    for name in names.generate_names(12):
        print(name)

        names.save_to_json('tolkien-name-generator.json')
