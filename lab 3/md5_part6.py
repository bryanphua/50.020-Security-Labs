import hashlib
import string
import itertools
from md5fun import get_lines, get_word_permutations

def get_substitute_dict():
    common_substitutions = {
        'a': ['@'],
        'b': ['8'],
        'c': ['('],
        'd': ['6'],
        'e': ['3'],
        'f': ['#'],
        'g': ['9'],
        'h': ['#'],
        'i': ['1', '!'],
        'k': ['<'],
        'l': ['1', 'i'],
#        'm': [''],
#        'n': [''],
        'o': ['0'],
#        'p': [''],
        'q': ['9'],
#        'r': [''],
        's': ['5', '$'],
        't': ['+'],
#        'u': [''],
        'v': ['>', '<'],
        'w': ['uu', '2u'],
        'x': ['%'],
        'y': ['?'],
#        'z': [''],
    }
    
    for key in list(common_substitutions.keys()):
        # add uppercase letter as replacement
        # add uppercase letters with lower case as replacement
        common_substitutions[key.upper()] = \
            common_substitutions[key].copy() + [key.lower()]
    return common_substitutions


def get_substitutions(word, subdict, binary_perm_dict):
    """return a list of string all possible common substitutions based on
    subdict"""
    'e.g wora - w0ra w0r@ wor@'
    sub_pos = []
    for i in range(len(word)):
        if word[i] in subdict.keys():
            sub_pos.append(i)
#    print('original-word'+word)
#    print(sub_pos)

    if len(sub_pos) not in binary_perm_dict.keys():
        # possible combinations of 1,0s for a fixed length without order
        binary_combinations =\
            itertools.combinations_with_replacement([1, 0], len(sub_pos))

        binary_permutations = []

        # possible permutations of 1,0s for a fixed length where order matters
        for comb in binary_combinations:
            for perm in itertools.permutations(comb, len(comb)):
                if perm not in binary_permutations:
                    count = 0
                    # take only those with at most 3 replacements
                    for e in perm:
                        if e == 1:
                            count += 1
                    if count < 4:
                        binary_permutations.append(perm)

        binary_perm_dict[len(sub_pos)] = binary_permutations

    binary_permutations = binary_perm_dict[len(sub_pos)]

    new_words = []
    for binary_perm in binary_permutations:
        new_word_list = [list(word)]
#        print(new_word_list)
        for i in range(len(sub_pos)):
            if binary_perm[i] != 0:
                pos = sub_pos[i]
                char = word[pos]
                number_of_possible_sub = len(subdict[char])
                # save this as we may extend the list
                list_length = len(new_word_list)

                for j in range(number_of_possible_sub):
                    substitute = subdict[char][j]

                    for k in range(list_length):
                        current_word = new_word_list[k].copy()
                        current_word[pos] = substitute
                        if j == 0:
                            new_word_list[k] = current_word
                        else:
                            new_word_list.append(current_word)

#        print(binary_perm)
#        print(new_word_list)
        for word_list in new_word_list:
            new_words.append(''.join(word_list))
#            print(''.join(word_list))
    return new_words


def dictionary_attack(hashes, word_file, csv_out, start_from=0):
    f = open(word_file, 'r')
    subdict = get_substitute_dict()
    binary_perm_dict = {}  # for memoisation
    preimages = {hashh: [] for hashh in hashes}

    for i in range(start_from):
        f.readline()

    line = f.readline()
    count = start_from

    print("starting dictionary attack----")
    while line:
        word = line.replace('\n', '')
        count += 1
        line = f.readline()
        if count % 100 == 0:
            print("{} % (line {})".format(count*100/99000, count))

        if len(word)>7 or '\'' in word:
#           print('skipping {}'.format(word))
            continue

#        words = get_substitutions(word, subdict, binary_perm_dict)
#        print('original-'+word)
        words = [word] 
        for word in words:
            hasher = hashlib.md5()
            hasher.update(word.encode('utf-8'))
            word_hash = hasher.hexdigest()
#            print(count, word, word_hash)
            if word_hash in hashes:
                if word not in preimages[word_hash]:
                    preimages[word_hash].append(word)
                    print('HIT')
                    print("word:{}|hash:{}".format(word, word_hash))
    print("finished dictionary attack writing results..")
    f_out = open(csv_out, 'w')
    for hashh in hashes:
        results = preimages[hashh]
        line = hashh+','
        for result in results:
            line += ',' + result
        line += '\n'
        f_out.write(line)
    f_out.close()
    print("finish")


def get_char_combination(length):
    """returns an iterator of tuples with all possible character
    combinations(no order)"""
    characters = string.printable[:94]
    return itertools.combinations_with_replacement(characters, length)


def brute_force_attack(hashes, csv_out):
    collisions = {hash_value: [] for hash_value in hashes}

    for length in range(1, 9):
        print('length:{}'.format(length))
              
        character_combinations = get_char_combination(length)

        for combination in character_combinations:
            word = ''.join(combination)
            permutations = get_word_permutations(word)
            for perm in permutations:
                hasher_object = hashlib.md5()
                hasher_object.update(perm.encode('utf-8'))
                perm_hash = hasher_object.hexdigest()

                if perm_hash in hashes:
                    if perm not in collisions[perm_hash]:
                        print('HIT|{}|'.format(perm))
                        collisions[perm_hash].append(perm)

    f_out = open(csv_out, 'w')
    for hashh in hashes:
        results = collisions[hashh]
        line = hashh+','
        for result in results:
            line += ',' + result
        line += '\n'
        f_out.write(line)
    f_out.close()
    print("finish")


if __name__ == '__main__':
    word_file = '/usr/share/dict/words'
    csv_out = 'md5_part6_results_3.csv'

    # get hashes from textfile
    lines = get_lines('./hashes.txt')
    hashes = []

    for i in range(len(lines)):
        hashh = lines[i]
        hashh = hashh.split(' ')
        if len(hashh) == 2:
            hashes.append(hashh[1])

    # attack!
#    dictionary_attack(hashes, word_file, csv_out, 1100)
    brute_force_attack(hashes, csv_out)
