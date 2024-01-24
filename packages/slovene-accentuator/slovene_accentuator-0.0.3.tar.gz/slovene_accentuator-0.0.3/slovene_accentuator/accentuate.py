# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pickle
from prepare_data import *
import os

current_folder = os.path.dirname(__file__)

class SloveneAccentuator:

    def __init__(self):
        # Get environment variables necessary for calculations
        self.pickle_input = open(os.path.join(current_folder, 'preprocessed_data/environment.pkl'), 'rb')
        self.environment = pickle.load(self.pickle_input)
        self.dictionary = self.environment['dictionary']
        self.max_word = self.environment['max_word']
        self.max_num_vowels = self.environment['max_num_vowels']
        self.vowels = self.environment['vowels']
        self.accented_vowels = self.environment['accented_vowels']
        self.feature_dictionary = self.environment['feature_dictionary']
        self.syllable_dictionary = self.environment['syllable_dictionary']

        # Load models
        self.data = Data('l', shuffle_all_inputs=False)
        self.letter_location_model, self.syllable_location_model, self.syllabled_letters_location_model = self.data.load_location_models(
        'cnn/word_accetuation/cnn_dictionary/v5_3/20_final_epoch.h5',
        'cnn/word_accetuation/syllables/v3_3/20_final_epoch.h5',
        'cnn/word_accetuation/syllabled_letters/v3_3/20_final_epoch.h5')

        self.letter_location_co_model, self.syllable_location_co_model, self.syllabled_letters_location_co_model = self.data.load_location_models(
        'cnn/word_accetuation/cnn_dictionary/v5_2/20_final_epoch.h5',
        'cnn/word_accetuation/syllables/v3_2/20_final_epoch.h5',
        'cnn/word_accetuation/syllabled_letters/v3_2/20_final_epoch.h5')

        self.letter_type_model, self.syllable_type_model, self.syllabled_letter_type_model = self.data.load_type_models(
        'cnn/accent_classification/letters/v3_1/20_final_epoch.h5',
        'cnn/accent_classification/syllables/v2_1/20_final_epoch.h5',
        'cnn/accent_classification/syllabled_letters/v2_1/20_final_epoch.h5')

        self.letter_type_co_model, self.syllable_type_co_model, self.syllabled_letter_type_co_model = self.data.load_type_models(
        'cnn/accent_classification/letters/v3_0/20_final_epoch.h5',
        'cnn/accent_classification/syllables/v2_0/20_final_epoch.h5',
        'cnn/accent_classification/syllabled_letters/v2_0/20_final_epoch.h5')

    def convert_to_correct_accentuation(self, w):
        """The accentuate_word function returns placeholder accentuation symbols.
        They need to be replaced with actual accentuation symbols. """
        w = w.replace('ì', 'ê')
        w = w.replace('à', 'ŕ')
        w = w.replace('ä', 'à')
        w = w.replace('ë', 'è')
        w = w.replace('ě', 'ê')
        w = w.replace('î', 'ì')
        w = w.replace('ö', 'ò')
        w = w.replace('ü', 'ù')

        return w


    def get_accentuated_words(self, list_of_forms):
        # Format data for accentuate_word function; the format is the following: [['besedišči', '', 'Ncnpi', 'besedišči'], ]
        self.content = [[el[0], '', el[1], el[0]] for el in list_of_forms]

        # use environment variables and models to accentuate words
        #data = Data('l', shuffle_all_inputs=False)
        location_accented_words, accented_words = self.data.accentuate_word(self.content, self.letter_location_model,
                                                                       self.syllable_location_model,
                                                                       self.syllabled_letters_location_model,
                                                                       self.letter_location_co_model,
                                                                       self.syllable_location_co_model,
                                                                       self.syllabled_letters_location_co_model,
                                                                       self.letter_type_model, self.syllable_type_model,
                                                                       self.syllabled_letter_type_model,
                                                                       self.letter_type_co_model, self.syllable_type_co_model,
                                                                       self.syllabled_letter_type_co_model,
                                                                       self.dictionary, self.max_word, self.max_num_vowels, self.vowels,
                                                                       self.accented_vowels, self.feature_dictionary,
                                                                       self.syllable_dictionary)

        # Convert placeholder accentuation symbols to actual accentuation symbols
        accented_words_with_correct_accentuation_symbols = []
        for word in accented_words:
            accented_words_with_correct_accentuation_symbols.append(self.convert_to_correct_accentuation(word))

        final_list = []
        for index, form_msd in enumerate(list_of_forms):
            form, msd = form_msd
            accentuated_form = accented_words_with_correct_accentuation_symbols[index]
            final_list.append([form, msd, accentuated_form])

        return final_list