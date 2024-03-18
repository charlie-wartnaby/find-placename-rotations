import pandas    # To load CSV as dataframe
import re
import unidecode # Thought I would need to remove accents but pandas import maybe does already


# Download from:
# https://geoportal.statistics.gov.uk/datasets/6cb9092a37da4b5ea1b5f8b054c343aa/about
dataset_filename = 'IPN_GB_2023.csv'
placename_col_heading = 'place22nm'


non_letter_regex = re.compile('\W')

def find_rotate_matches(name_list):
    known_rings = {}
    all_multiname_lists = []
    for original_name in name_list:
        # Remove spaces/hyphens/capitals etc so we match regardless of those
        letters_only = non_letter_regex.sub('', original_name.lower())
        if letters_only in known_rings:
            # We've seen this name before in some rotation so add this name
            name_list = known_rings[letters_only]
            name_list.append(original_name)
            # As we've seen this one at least twice, save in set of multi-matches
            if name_list not in all_multiname_lists:
                all_multiname_lists.append(name_list)
        else:
            # The first time we've seen this name in any rotation
            name_list = [original_name]
            # Point to same list for all possible rotations of this name:
            for i in range(len(letters_only)):
                known_rings[letters_only] = name_list
                letters_only = letters_only[1:] + letters_only[0]

    return all_multiname_lists


def load_gb_data():
    # Have to specify encoding because of non-ASCII characters (does it convert them?)
    names_df = pandas.read_csv(dataset_filename, encoding='latin-1')
    name_list = names_df[placename_col_heading].tolist()
    return name_list


def pre_process_placename_list(name_list):
    seen_names = set()
    de_duplicated = []
    for name in name_list:
        if ',' in name:
            # E.g. not interested in finding "Hampstead, West" and "West Hampstead"
            pass
        elif '(' in name:
            # Avoid finding both versions of e.g.
            # 'Priestholm (Puffin Island)', 'Puffin Island (Priestholm)'
            pass
        else:
            # Avoid names differing only in space or hyphen etc
            letters_only = non_letter_regex.sub('', name.lower())
            if letters_only in seen_names:
                pass
            else:
                seen_names.add(letters_only)
                de_duplicated.append(name)

    return de_duplicated


# test_data = ['Tokyo', 'Osaka', 'Kyoto']

name_list = load_gb_data()
name_list = pre_process_placename_list(name_list)
all_multiname_lists = find_rotate_matches(name_list)

for i, multiname_list in enumerate(all_multiname_lists):
    print(i + 1, multiname_list)
