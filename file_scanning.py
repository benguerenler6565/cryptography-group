from methods import Encrypter, ALPHABET, Decipherer
import pandas as pd


def display_dataframe(file_index_max, path):
    index = list(range(file_index_max+1))
    output_df = pd.DataFrame(index=index, columns=['~KeyLen', '~KeyCounters'])
    output_df.index.name = 'Group'

    for i in index:
        try:
            with open(path + str(i) + ".crypto", "r") as ciphertext_file:
                ciphertext = ciphertext_file.read()
        except FileNotFoundError:
            pass
        else:
            decipherer = Decipherer(ciphertext=ciphertext)
            output_df.loc[i, '~KeyLen'] = decipherer.keylength_estimate
            output_df.loc[i, '~KeyCounters'] = str(decipherer.keylength_analysis.most_common(8))

    output_df.dropna(inplace=True)
    print('Showing dataframe for .crypto files in ' + path)
    print(output_df)


display_dataframe(13, 'crypto-files/vig_group')

display_dataframe(3, 'crypto-files/text')