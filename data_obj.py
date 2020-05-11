# Authors: Mike Menendez, Frank Piva, Felix Romero-Flores, Edgaras Slezas
# Date: May 11, 2020
# Course: CST 205
# Description: This is a supporting class, Data. It holds the country stat data and generates
#              a barplot of country specific stats that are log scaled for clarity.
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


class Data():
    def __init__(self, data):
        if len(data) > 0:
            self.data = data
            self.df = pd.DataFrame(data)
        else:
            self.data = None

    # takes in a data obj, creates dataframe, returns path to vizualization
    @staticmethod
    async def hist_viz(d, c_code):
        if not d.data:
            return ""
        for x in d.data:
            # print("data: ", x, file=sys.stderr)
            if x['CountryCode'].lower() == c_code:
                df = pd.DataFrame([[
                    int(x['TotalDeaths']),
                    int(x['TotalConfirmed']),
                    int(x['TotalRecovered'])
                ]], columns=['Total Deaths', 'Total Confirmed', 'Total Recovered'])
                df = np.log(df)
                sns.set_style('darkgrid')
                sns.barplot(data=df, order=[
                            'Total Confirmed', 'Total Recovered', 'Total Deaths'])
                plt.ylabel("Log 10 Scaled Values")
                plt.savefig(f'static/img/{c_code}.svg', format="svg")
                return f'/static/img/{c_code}.svg'
        return ""
