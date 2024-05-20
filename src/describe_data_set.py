import numpy as np
import pandas as pd
import plotly.express as px


def normalised_term(years):
    months = round(12*years)
    y = months // 12
    m = months % 12
    term = ""
    if y > 0:
        term = term + str(y) + "Y"
    if m > 0:
        term = term + str(m) + "M"
    return term


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


def plot_data_table(data_table):
    table = data_table.copy()
    for col in table.columns:
        if col[1] == 0: # assume FX rate
            table[col] = np.log(table[col])
    table = table - table.iloc[0]
    table.columns = [ c[0]+"_"+str(c[1]) for c in table.columns ]
    fig = px.line(table)
    fig.update_layout(
        xaxis_title = "Date",
        yaxis_title = "Normalised rate",
    )
    return fig


def plot_volatility_distribution(std_table, return_days):
    table = std_table.copy()
    table = table * np.sqrt(365. / return_days)  # annualised volatility
    for c in table.columns:
        if c[1] == 0:
            table[c] = table[c] * 100  # FX vol in percent
        else:
            table[c] = table[c] * 10000  # rates vol in basis points
    table.columns = [ c[0] + "_" + normalised_term(c[1]/12) for c in table.columns ]
    fig = px.box(table)
    fig.update_layout(
        xaxis_title = "Currency",
        yaxis_title = r"Volatility (% for FX, bp for rates)",
    )
    return fig


def plot_correlation_distribution(corr_table):
    table = corr_table.copy()
    table = table * 100  # in percent
    fig = px.box(table)
    fig.update_layout(
        xaxis_title = "Currency",
        yaxis_title = r"Correlation (%)",
    )
    return fig
