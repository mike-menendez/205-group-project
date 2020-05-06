import numpy as np
import seaborn as sns
import sklearn as sk
import pandas as pd
import matplotlib.pyplot as plt


class Data():
    def __init__(self, data):
        if len(data) > 0:
            self.data = data
            self.df = pd.DataFrame(data)
        else:
            self.data = None

    # These are compute intensive tasks, would be good to either do this in the background
    # AOT, or we just run them once every 15 mins and the first access takes a hit with
    # subsequent accesses being fast for the next 15 mins with: time.ctime(os.path.getmtime("image.jpg"))

    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_hist.jpg"
    @staticmethod
    async def hist_viz(d, c_code):
        if not d.data:
            return ""
        sns.distplot(d.df['NewDeaths'])
        plt.savefig(f'static/img/{c_code}.svg', dpi=300, format="svg")
        return f'/static/img/{c_code}.svg'
