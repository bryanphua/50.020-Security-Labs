import itertools
import hashlib
import timeit
import random


def get_lines(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
    return lines


def dict_attack(word_list, hashes):
    collisions = {hash_value: [] for hash_value in hashes}
    for i in range(len(word_list)):
        word = word_list[i]
        permutations = get_word_permutations(word)
        for perm in permutations:
            hasher_object = hashlib.md5()
            hasher_object.update(perm.encode('utf-8'))
            perm_hash = hasher_object.hexdigest()
            if perm_hash in hashes:
                if perm not in collisions[perm_hash]:
                    print('HIT')
                    collisions[perm_hash].append(perm)
    return collisions


def brute_force_attack(hashes):
    collisions = {hash_value: [] for hash_value in hashes}
    character_combinations = get_char_combination()
    for combination in character_combinations:
        word = ''.join(combination)
        permutations = get_word_permutations(word)
        for perm in permutations:
            hasher_object = hashlib.md5()
            hasher_object.update(perm.encode('utf-8'))
            perm_hash = hasher_object.hexdigest()
            if perm_hash in hashes:
                if perm not in collisions[perm_hash]:
                    print('HIT')
                    collisions[perm_hash].append(perm)
    return collisions


def get_word_permutations(word):
    if len(word) == 0 or len(word) == 1:
        return [word]
    else:
        permutations = []
        for i in range(len(word)):
            char = word[i]
            subword = word[:i]+word[i+1:]
            sub_permutations = get_word_permutations(subword)
            for j in range(len(sub_permutations)):
                sub_permutations[j] = char + sub_permutations[j]
            permutations += sub_permutations
        return permutations


def get_char_combination():
    """returns an iterator of tuples with all possible character
    combinations(no order)"""
    characters = 'abcdefghijklmnopqrstuvwxyz1234567890'
    length = 5
    return itertools.combinations_with_replacement(characters, length)


def salt():
    passwords = get_lines('plaintext5.txt')
    lower_alpha = list('abcdefghijklmnopqrstuvwxyz')

    plaintext_file = open('pass6.txt', 'w')
    hash_file = open('salted6.txt', 'w')

    for password in passwords:
        random_int = random.randint(0, len(lower_alpha)-1)
        random_char = lower_alpha[random_int]
        salted_password = password + random_char
        hasher_object = hashlib.md5()
        hasher_object.update(salted_password.encode('utf-8'))
        salted_hash = hasher_object.hexdigest()

        plaintext_file.write(salted_password + '\n')
        hash_file.write(salted_hash+'\n')

    plaintext_file.close()
    hash_file.close()
    print('finish salting and saving')


if __name__ == '__main__':
    hasher_object = hashlib.md5()
    hashes = get_lines('hash5.txt')
    word_list = get_lines('words5.txt')

#    print("start dictionary attack")
#    start_time = timeit.default_timer()
#    print(dict_attack(word_list, hashes))
#    print("time taken:{}".format(timeit.default_timer()-start_time))
#
#    print("start brute force attack")
#    start_time = timeit.default_timer()
#    print(brute_force_attack(hashes))
#    print("time taken:{}".format(timeit.default_timer()-start_time))

    salt()
