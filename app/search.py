import re
import string
from nltk.tokenize import TweetTokenizer
from nltk.metrics.distance import edit_distance


def fuzzy_match(string1, string2, dist=3):
    return edit_distance(string1, string2, substitution_cost=2) <= dist


def normalize_name(name):
    return TweetTokenizer().tokenize(name.lower())


def normalize_role(role):
    roles = [
        'executive',
        'technical',
        'marketing',
        'financial',
        'technology',
        'operations',
        'human resources',
        'finance',
        'officer',
        'chief',
        'marketing',
        'technology',
        'executive',
        'finance',
        'human resources',
        'operations',
        'lead developer',
        'developer',
        'advisor',
        'co-founder',
        'founder',
        'manager',
        'head',
        'escrow'
    ]
    match_table = {
        'marketing': 'cmo',
        'technology': 'cto',
        'executive': 'ceo',
        'finance': 'cfo',
        'human resources': 'chro',
        'operations': 'coo',
        'technical': 'cto',
        'lead developer': 'lead',
        'developer': 'dev',
        'advisor': 'adv',
        'founder': 'fndr',
        'co-founder': 'fndr',
        'manager': 'mngr',
        'head': 'head',
        'officer': 'ofcr',
        'chief': 'chf',
        'escrow': 'escr'
    }

    role_tokens = re.split("\W+", role)

    role_tokens = [token.lower() for token in role_tokens]

    normal_tokens = []

    for token in role_tokens:
        flag = False
        for other in roles:
            if fuzzy_match(token, other, dist=2):
                normal_tokens.append(other)
                flag = True
        if not flag:
            normal_tokens.append(token)

    matched_tokens = []

    for token in normal_tokens:
        if token in match_table.keys():
            matched_tokens.append(match_table[token])
        else:
            matched_tokens.append(token)

    return matched_tokens


def normalize_ico_name(ico_name):

    regex = re.compile('[%s]' % re.escape(string.punctuation))
    ico_name = regex.sub(' ', ico_name)

    tokens = TweetTokenizer().tokenize(ico_name.lower())

    return tokens
