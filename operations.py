from methods import vigenere, ALPHABET, Decipherer

with open("vig_group3.plain", "r") as plaintext_file:
    plaintext = plaintext_file.read()

with open("vig_group3.key", "r") as key_file:
    key = key_file.read()

with open("vig_group3.crypto", "r") as ciphertext_file:
    ciphertext = ciphertext_file.read()

# unit test
recovered_text = vigenere(ALPHABET, key, ciphertext, mode='decrypt')

print('Unit test: assert plaintext == recovered_text: ', recovered_text == plaintext)

decipherer = Decipherer(ciphertext=ciphertext)

print('Decipherer predicts the keylength of ciphertext to be: ', decipherer.keylength_estimate)

pass