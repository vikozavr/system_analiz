import pandas as pd
import numpy as np

def main(filename: str) -> list:

    data = pd.read_csv(filename, index_col=0)

    total_sum = data.values.sum()
    
    probabilities = data / total_sum
   
    H_AB = -np.nansum(probabilities * np.log2(probabilities))


    row_totals = probabilities.sum(axis=1)
    col_totals = probabilities.sum(axis=0)


    H_A = -np.nansum(row_totals * np.log2(row_totals))
    H_B = -np.nansum(col_totals * np.log2(col_totals))


    H_a_B = -np.nansum(probabilities.apply(lambda row: np.nansum(row * np.log2(row / row_totals[row.name])), axis=1))

    
    I_A_B = H_A - H_a_B

    return [float(round(v, 2)) for v in (H_AB, H_A, H_B, H_a_B, I_A_B)]

if __name__ == '__main__':
    filename = 'aaa.csv'
    print(main(filename))
