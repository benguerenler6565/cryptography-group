# coding=utf-8
import numpy as np


def vigenere(alphabet, key, plaintext, mode='encrypt'):
    """
    The function encrypts (or decrypts) a plaintext using the vigenere cipher, from the given alphabet and key.

    Args:
        alphabet (str): a string of characters available in the plaintext, key and ciphertext.
        key (str): a string defining the secret
        plaintext (str): the message to be encoded.

    Returns:
        String: an encrypted message
    """
    m = len(alphabet)   # the length of the alphabet defines the modulo
    get_int = np.vectorize(list(alphabet).index)  # this defines a function to convert 'abc' to '012'
    get_chr = np.vectorize(list(alphabet).__getitem__)  # defines a function to convert '012' to 'abc'

    kl = len(key)       # the length of the key defines the array shapes below
    padding = (kl - len(plaintext) % kl) % kl  # create padding to allow full key repeats
    p = plaintext + alphabet[-1] * padding  # pad the plaintext so it divides the key length.
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

### ARGUMENTS
alphabet = 'abcdefghijklmnopqrstuvwxyzåäö ,.'
key = 'melons'
plaintext = 'big bananas are best for eating, small bananas are best for cakes..'

### RUN ALGORITHM
print('PLAINTEXT: # ', plaintext, ' #')
ciphertext = vigenere(alphabet, key, plaintext)
print('Encrypting...')
print('CIPHERTEXT: # ', ciphertext, ' #')
print('Decrypting...')
decrypted_text = vigenere(alphabet, key, ciphertext, mode='decrypt')
print('DECRYPTED TEXT: # ', decrypted_text, ' #')

# Unit Test:
print('Algorithm works: ', plaintext == decrypted_text)
