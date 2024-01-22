import sys
import pandas as pd
import numpy as np
import argparse
import os



def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("Input_File", help="Path of the Input File eg: 102103562.csv")
    parser.add_argument("Weights", help='Weights for topsis analysis  eg: "1,1,1,2"')
    parser.add_argument("Impacts", help='The Impacts for each weight  eg: "+,-,+,-"')
    parser.add_argument(
        "Output_File", help="The name of the Output file  eg: 102103563_result.csv"
    )

    args = parser.parse_args()


    flag_File = False
    flag_Weights = False
    flag_Impacts = False
    UTILITY_IMPACT_FACTOR_CONV = {"+": 1, "-": -1}
    ###############################################################
    if args.Input_File is not None:
        inptFilePath = args.Input_File
        # check file existance
        if os.path.exists(inptFilePath):
            ext = os.path.splitext(inptFilePath)[-1]
            # check file extension
            if ext in {".csv", ".xlsx"}:
                # read file
                try:
                    if ext == ".csv":
                        input_file = pd.read_csv(inptFilePath)
                    elif ext == ".xlsx":
                        input_file = pd.read_excel(inptFilePath)

                    len_cols = len(input_file.columns)
                    if len_cols >= 3:
                        # can improve here
                        if all(
                            input_file.iloc[:, 1:].applymap(
                                lambda x: isinstance(x, (int, float))
                            )
                        ):
                            flag_File = True
                        else:
                            print("Non numerical data")
                    else:
                        print("Please provide a file with atleast 3 columns")
                except:
                    print("Error in Reading file")

            else:
                print("Please provide a .csv or .xlsx file")
        else:
            print(inptFilePath, "File Does not Exsist")


    if args.Weights is not None and args.Impacts is not None and flag_File:
        weights, impacts = list(map(float, args.Weights.split(","))), args.Impacts.split(
            ","
        )
        if len(weights) == len_cols - 1 and len(impacts) == len_cols - 1:
            converted_impacts = []
            for impact in impacts:
                if impact not in UTILITY_IMPACT_FACTOR_CONV:
                    print("Impacts Should be + or -")
                    break
                else:
                    converted_impacts.append(UTILITY_IMPACT_FACTOR_CONV[impact])

            if len(weights) == len(impacts):
                flag_Impacts, flag_Weights = True, True
            else:
                print("Weights and Impacts must be seprated by ',' ")
        else:
            print("Please provide the same length of Weights and Impacts")

    if flag_File and flag_Weights and flag_Impacts:
        newDf = topsis(input_file, np.array(weights), np.array(impacts))
        print(newDf)

        try:
            newDf.to_csv(args.Output_File,index=False)
            print("File exported as ", args.Output_File)
        except:
            print("error in exporting file")



def topsis(df: pd.DataFrame, wts: np.ndarray, impact: np.ndarray) -> pd.DataFrame:
    mat = np.array(df.iloc[:, 1:])
    rows, cols = mat.shape
    # mat / rootOfSumOfSquare * weight
    for i in range(cols):
        temp = 0
        for j in range(rows):
            temp += mat[j][i] ** 2
        temp = temp**0.5
        wts[i] /= temp

    weightedNormalized = mat * wts

    idealBestWorst = []  # (best,worst)

    for i in range(cols):
        maxi = weightedNormalized[:, i].max()
        mini = weightedNormalized[:, i].min()
        idealBestWorst.append((maxi, mini) if impact[i] == 1 else (mini, maxi))
    topsisScore = []
    for i in range(rows):
        temp_p, temp_n = 0, 0
        for j in range(cols):
            temp_p += (weightedNormalized[i][j] - idealBestWorst[j][0]) ** 2
            temp_n += (weightedNormalized[i][j] - idealBestWorst[j][1]) ** 2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        topsisScore.append(temp_n / (temp_p + temp_n))

    df["score"] = np.array(topsisScore).T
    df["rank"] = df["score"].rank(method="max", ascending=False)
    df["rank"] = df.astype({"rank": int})["rank"]
    return df


if __name__ == "__main__":
    main()