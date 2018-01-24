# coding=utf-8
import numpy as np
ALPHABET = 'abcdefghijklmnopqrstuvwxyzåäö ,.'


def vigenere(alphabet, key, inputtext, mode='encrypt'):
    """
    The function encrypts (or decrypts) a plaintext using the vigenere cipher, from the given alphabet and key.

    Args:
        alphabet (str): a string of characters available in the plaintext, key and ciphertext.
        key (str): a string defining the secret
        plaintext (str): the message to be encoded.

    Returns:
        String: an encrypted message
    """
    inputtext = check_unsupported_chars(alphabet, inputtext)
    m = len(alphabet)   # the length of the alphabet defines the modulo
    get_int = np.vectorize(list(alphabet).index)  # this defines a function to convert 'abc' to '012'
    get_chr = np.vectorize(list(alphabet).__getitem__)  # defines a function to convert '012' to 'abc'

    kl = len(key)       # the length of the key defines the array shapes below
    padding = (kl - len(inputtext) % kl) % kl  # create padding to allow full key repeats
    p = inputtext + alphabet[-1] * padding  # pad the plaintext so it divides the key length.
    blocks = int(len(p) / kl)  # blocks is the number of times the key divides the plaintext.

    # now convert the inputs to numpy arrays for vectorised manipulation
    p_arr = get_int(np.array(list(p)))
    k_arr = get_int(np.tile(np.array(list(key)), blocks))

    # apply the encryption c = p + k % m (or decryption)
    if mode == 'decrypt':
        c_arr = get_chr(np.mod(p_arr - k_arr, m))
    else:
        c_arr = get_chr(np.mod(p_arr + k_arr, m))

    # return a string format, and remove the padding so that the return is consistent with input.
    return ''.join(c_arr[:(len(c_arr)-padding)])


def check_unsupported_chars(alphabet, inputtext):
    # convert the uppercase to lowercase for encryption
    inputtext_lower = inputtext.lower()
    # detect and remove unsupported chars:
    unsupp_chars = set(inputtext_lower).difference(alphabet)
    for unsupp_char in unsupp_chars:
        inputtext_lower = inputtext_lower.replace(unsupp_char, '')
    return inputtext_lower