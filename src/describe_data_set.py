import numpy as np
import pandas as pd


def describe_values(data_set):
    table = pd.pivot_table(data_set, values="VALUE", index="DATE", columns=["CURRENCY", "MONTHS", "TERM"])
    return table.describe().T

def describe_dates(data_set):
    res_list = []
    for curr in data_set["CURRENCY"].drop_duplicates():
        tmp1 = data_set[data_set["CURRENCY"]==curr]
        for term in tmp1["TERM"].drop_duplicates():
            tmp2 = tmp1[tmp1["TERM"]==term]
            dt = np.array([ d / np.timedelta64(1, 'D')  for d in (tmp2["DATE"].values[1:] - tmp2["DATE"].values[:-1]) ]) - 1.0
            time_span = (tmp2["DATE"].values[-1] - tmp2["DATE"].values[0]) / np.timedelta64(1, 'D')
            gap = np.max(dt)
            fill = (1.0 - np.sum(dt) / time_span)
            res_list.append({
                "CURRENCY" : curr,
                "TERM" : term,
                "MONTHS" : tmp2.iloc[0]["MONTHS"],
                "MIN" : np.min(tmp2["DATE"]),
                "MAX" : np.max(tmp2["DATE"]),
                "GAP" : gap,
                "FILL" : fill,
            })
    return pd.DataFrame(res_list)
