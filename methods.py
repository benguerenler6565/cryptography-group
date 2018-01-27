# coding=utf-8
from collections import Counter
from utils import factors
import numpy as np

ALPHABET = 'abcdefghijklmnopqrstuvwxyzåäö ,.'


class Encrypter:
    @staticmethod
    def check_unsupported_chars(alphabet, inputtext):
        # convert the uppercase to lowercase for encryption
        inputtext_lower = inputtext.lower()
        # detect and remove unsupported chars:
        unsupp_chars = set(inputtext_lower).difference(alphabet)
        for unsupp_char in unsupp_chars:
            inputtext_lower = inputtext_lower.replace(unsupp_char, '')
        return inputtext_lower

    @classmethod
    def vigenere(cls, alphabet, key, inputtext, mode='encrypt'):
        """
        The function encrypts (or decrypts) a plaintext using the vigenere cipher, from the given alphabet and key.

        Args:
            alphabet (str): a string of characters available in the plaintext, key and ciphertext.
            key (str): a string defining the secret
            inputtext (str): the message to be encoded.
            mode (str, optional): 'encrypt' or 'decrypt', defaults to 'encrypt'.

        Returns:
            String: an encrypted message
        """
        inputtext = cls.check_unsupported_chars(alphabet, inputtext)
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


class Decipherer(Encrypter):
    common_words = ['jag', 'det', 'är', 'du', 'inte', 'att', 'en', 'och', 'har', 'vi', 'på', 'för', 'han', 'vad', 'med',
                    'mig', 'som', 'här', 'om', 'dig', 'var', 'den', 'så', 'till', 'kan', 'de', 'ni', 'ska', 'ett']
    char_frequencies = []

    def __init__(self, ciphertext):
        self.ciphertext = ciphertext
        self.kasiski(2, 12, 20)

    def kasiski(self, min_length, max_length, num_elements):
        """
        Function analyses the ciphertext, scanning for repeated elements and then derives the estimated keylength from
        the separation between them. The estimated keylength is the number greater than 1 with the highest count.

        Args:
            min_length (int): the minimum length of an element to search for repetitions: recommended 2 to 3.
            max_length (int): the maximum length of an element to search for repetitions: recommended 8 to 12.
            num_elements (int): the number of discovered repeated elements to search through: recommended 20.

        Attributes:
            repeated_elements (list): a list of strings of the discovered repeated elements using above params.
            keylength_analysis (Counter): a counter object that returns the count of the possible keylength spectrums.
            keylength_estimate (int): best guess for keylength.
        """

        # systematically cycle through the ciphertext adding elements to a list:
        # e.g. 'abcde' for element lengths 2 and 3 becomes: ['ab', 'bc', 'cd', 'de', 'abc', 'bcd', 'cde']
        for k in range(min_length, max_length+1):  # <- k defines the element length
            cipher_elements = list()
            for i in range(int(len(self.ciphertext)-k)):
                cipher_elements.append(self.ciphertext[i:i+k])
            # attach a counter to see how many times each element is found within the ciphertext
            setattr(self, 'element_counter_' + str(k), Counter(cipher_elements))

        # for the most common repeated elements systematically scan them and ensure they are not subsets of each other
        # e.g. 'ab' and 'bc' will be excluded as a subset of 'abc'.
        repeated_elements = list()
        for k in range(max_length, min_length-1,-1):
            sub_list = getattr(self, 'element_counter_' + str(k)).most_common(num_elements)
            delattr(self, 'element_counter_' + str(k))
            for i in range(num_elements):
                if any(sub_list[i][0] in element for element in repeated_elements) or sub_list[i][1]<2:
                    # if True then the subset condition is met or the count is 1 and thus it is not a repeated element
                    pass
                else:
                    # add the detected element to the list of most common repeated elements
                    repeated_elements.append(sub_list[i][0])
        self.repeated_elements = repeated_elements

        # for repeated elements now we detect their location in the ciphertext and calculate the keylength estimate as
        # factors of the difference in positioning.
        factors_list = list()
        for repeated_element in repeated_elements:
            _start = self.ciphertext.index(repeated_element)
            _factors = factors(self.ciphertext[_start+1:].index(repeated_element)+1)
            factors_list.extend(_factors)

        # return the attributes to the class object, we take the estimate as the most frequently occurring factor > 1.
        self.keylength_analysis = Counter(factors_list)
        self.keylength_estimate = self.keylength_analysis.most_common(2)[1][0]

    def decryption_verifier(self, plaintext_guess, calibration=3):
        """
        Function counts how many times the specified common words are detected in plaintext.
        Returns True or False based on some metrics, for example if more than 3 of the common words are detected per 100
        chars then the text is considered good.

        Notes:
            Other tests could be incorporated, such as the maximum number of the counter suggest one word is used a lot.

        Args:
            plaintext_guess (str): the text to verify whether it is deemed valid or junk
            calibration (int, optional): controls the leniency of the test: defines words per 100 chars allows True.

        Returns:
            Boolean, Dict, Int: Validity, count by common word, and a total of the amount of discovered words.
        """
        counter = dict()
        total = 0
        for word in self.common_words:
            counter.update({word: plaintext_guess.count(word)})
            total += plaintext_guess.count(word)

        boo = total > calibration * len(plaintext_guess) / 100
        return boo, counter, total


