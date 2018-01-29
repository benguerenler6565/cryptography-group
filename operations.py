from methods import Encrypter, ALPHABET, Decipherer

with open("crypto-files/vig_group3.plain", "r") as plaintext_file:
    plaintext = plaintext_file.read()

with open("crypto-files/vig_group3.key", "r") as key_file:
    key = key_file.read()

with open("crypto-files/vig_group3.crypto", "r") as ciphertext_file:
    ciphertext = ciphertext_file.read()

# unit test of encryption / decryption
recovered_text = Encrypter.vigenere(ALPHABET, key, ciphertext, mode='decrypt')
print('Unit test: assert plaintext == recovered_text: ', recovered_text == plaintext)

decipherer = Decipherer(ciphertext=ciphertext)

# unit test of Decipherer.kasiski
print('Decipherer.kasisiki() gets the following keylength analysis: ', decipherer.keylength_analysis)
print('Decipherer.kasisiki() predicts the keylength of ciphertext to be: ', decipherer.keylength_estimate)

# unit test of Decipherer.decryption_verifier
print('Decipherer.decryption_verifier() tested on the plaintext: ', decipherer.decryption_verifier(plaintext))
print('Decipherer.decryption_verifier() tested on the ciphertext: ', decipherer.decryption_verifier(ciphertext))


