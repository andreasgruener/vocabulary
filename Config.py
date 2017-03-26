# -*- coding: utf-8 -*-
"""Configuration File for Vocabulary

"""
# need to i18n
NAME_OF_PROBLEM_VOCABULARY_FILE = "problem-vocabulary.csv"
SUPPORTED_LANGUAGES = ['translation', 'source']
ANSWER_LANGUAGE_4_QUESTION = {'translation' : 'source', 'source' : 'translation'}
QUESTION_TEXT = {'translation' : 'Fremdsprache --> Deutsch',
         'source' : 'Deutsch --> Fremdsprache ',
         'mixed' : 'Deutsch/Fremdsprache gemischt'}
LIST_OF_PROBLEM_VOCABULARY = []


class Color:
    """Color codes for terminal
    """
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BLACK = '\033[0;30m'
    WHITE = '\033[0;37m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    LIGHTBLUE = '\033[34m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    BG_BLUE = '\033[44m'
    BG_WHITE = '\033[47m'
