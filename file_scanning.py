from methods import Encrypter, ALPHABET, Decipherer
import pandas as pd

index = list(range(14))
output_df = pd.DataFrame(index=index, columns=['~KeyLen', '~KeyCounters'])
output_df.index.name = 'Group'

for i in index:
    try:
        with open("crypto-files/vig_group" + str(i) + ".crypto", "r") as ciphertext_file:
            ciphertext = ciphertext_file.read()
    except FileNotFoundError:
        pass
    else:
        decipherer = Decipherer(ciphertext=ciphertext)
        output_df.loc[i, '~KeyLen'] = decipherer.keylength_estimate
        output_df.loc[i, '~KeyCounters'] = str(decipherer.keylength_analysis.most_common(8))

output_df.dropna(inplace=True)
print(output_df)