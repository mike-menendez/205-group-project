import numpy as np, seaborn as sns, sklearn as sk, pandas as pd, matplotlib.pyplot as plt

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
        if not d.data: return ""
        sns.distplot(d.df['Deaths'])
        plt.savefig(f'static/img/{c_code}.svg', dpi=300, format="svg")
        return f'/static/img/{c_code}.svg'

    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_viz2.jpg"
    @staticmethod
    async def viz_2(d, c_code):
        if not d.data: return ""
        pass

    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_viz3.jpg"
    @staticmethod
    async def viz_3(d, c_code):
        if not d.data: return ""
        pass

    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_viz4.jpg"
    @staticmethod
    async def viz_4(d, c_code):
        if not d.data: return ""
        pass

    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_reg.jpg"
    @staticmethod
    async def regression(d, c_code):
        if not d.data: return ""
        pass

    # Most likely won't be doing this one as it is extremely compute intensive, I've only gpu trained these
    # and they took forever even then although the datasets were much larger
    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_arma.jpg"
    @staticmethod
    async def arima(d, c_code):
        if not d.data: return ""
        pass