import numpy as np
import pandas as pd
import scipy.stats as ss


def cal_topsis_score(df: pd.DataFrame, w: list, i: list, out_file: str):
    df_copy = df.copy(deep=True)
    if not isinstance(df, pd.DataFrame):
        raise Exception("First argument should be a of type pd.DataFrame")
    df = df.select_dtypes(np.number)
    if len(df.columns) != len(w):
        raise Exception(
            "Length of weight list does not match with number of numeric columns in dataframe"
        )
    if len(df.columns) != len(i):
        raise Exception(
            "Length of impact list does not match with number of numeric columns in dataframe"
        )

    for j in range(len(w)):
        if not isinstance(w[j], (int, float)):
            raise Exception("Invalid weight list")

    for j in range(len(i)):
        if not (i[j] == "+" or i[j] == "-"):
            raise Exception("Invalid impact list")

    for column in df:
        sum = 0
        for _, row in df.iterrows():
            val = row[column]
            sum += val**2
        root = np.sqrt(sum)
        for index, row in df.iterrows():
            df.loc[index, column] = row[column] / root

    for j in range(len(w)):
        for index, row in df.iterrows():
            df.iloc[index, j] = df.iloc[index, j] * w[j]

    v_plus = []
    v_minus = []

    for j in range(len(i)):
        if i[j] == "+":
            v_plus.append(df.max().iloc[j])
            v_minus.append(df.min().iloc[j])
        elif i[j] == "-":
            v_plus.append(df.min().iloc[j])
            v_minus.append(df.max().iloc[j])

    s_plus = []
    s_minus = []
    for index in df.index:
        sum_plus = 0
        sum_minus = 0
        for j in range(len(df.columns)):
            sum_plus += (df.iloc[index, j] - v_plus[j]) ** 2
            sum_minus += (df.iloc[index, j] - v_minus[j]) ** 2
        s_plus.append(np.sqrt(sum_plus))
        s_minus.append(np.sqrt(sum_minus))

    performance_score = []
    for j in range(len(s_plus)):
        performance_score.append(s_minus[j] / (s_plus[j] + s_minus[j]))
    df = df_copy.assign(TopsisScore=performance_score)

    for j in range(len(performance_score)):
        performance_score[j] = 1 - performance_score[j]
    rank = ss.rankdata(performance_score).tolist()

    df = df.assign(Rank=rank)

    df.to_csv(out_file, index=False)
