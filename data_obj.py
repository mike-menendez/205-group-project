import numpy as np, seaborn as sns, sklearn as sk, pandas as pd, matplotlib.pyplot as plt

class Data():
    def __init__(self, data):
        self.data = data
        self.df = pd.DataFrame(data)

    # These are compute intensive tasks, would be good to either do this in the background
    # AOT, or we just run them once every 15 mins and the first access takes a hit with
    # subsequent accesses being fast for the next 15 mins with: time.ctime(os.path.getmtime("image.jpg"))
    
    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_hist.jpg"
    @staticmethod
    async def hist_viz(data, c_code):
        sns.distplot(data['Deaths'])
        plt.savefig(f'static/img/{c_code}.png', dpi=300)
        return f'/static/img/{c_code}.png'

    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_viz2.jpg"
    @staticmethod
    async def viz_2(data, c_code):
        pass

    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_viz3.jpg"
    @staticmethod
    async def viz_3(data, c_code):
        pass

    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_viz4.jpg"
    @staticmethod
    async def viz_4(data, c_code):
        pass

    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_reg.jpg"
    @staticmethod
    async def regression(data, c_code):
        pass

    # Most likely won't be doing this one as it is extremely compute intensive, I've only gpu trained these
    # and they took forever even then although the datasets were much larger
    # takes in a dataframe, returns path to vizualization in the format of "static/{c_code}_arma.jpg"
    @staticmethod
    async def arima(data, c_code):
        pass