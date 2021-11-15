# This is a sample Python script.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
import xlrd
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def prueba():

    # Leer datos y meterlos en un dataframe
    # Reducir anális a 1 hora, +-30 mins desde trigger

    #df = pd.read_excel('txResults.xlsx', sheet_name='Sheet1')

    df = pd.read_excel('inTx.xlsx',
                       skiprows=1,
                       names=['value', 'addr', 'block', 'time', 'hash', 'vin_sz', 'vout_sz'])
    df.head()
    #print(df)

    timetrigger = 1507794000

    df_idx = df[df["time"] <= timetrigger].index
    df_prov = df.drop(df_idx)
    #print(df_prov)

    df_idx = df_prov[df_prov["time"] >= timetrigger + 1800].index
    df_def = df_prov.drop(df_idx)
    #print(df_def)
    #print(df_def.iloc[0][0])

    timeframe = pd.DataFrame({'minute': range(0, 60), 'value': np.zeros(60, dtype=float, order='C')})
    count = 0
    minutecount = 0

    while count < len(df_def)-1:

        minutecheck = int((df_def.iloc[count][3] - timetrigger)/60)
        valuecheck = timeframe.iloc[minutecount][1]

        if minutecheck > minutecount:
            minutecount += 1

        #timeframe.iloc[minutecount]['value'] += df_def.iloc[count][0]
        timeframe.iat[minutecount, 1] += df_def.iloc[count][0]
        #timeframe.iloc[minutecount].replace(to_replace=valuecheck, value=valuecheck+df_def.iloc[count][0])

        count += 1

    #print(timeframe)
    #timeframe.to_excel("Charts.xlsx")

    print(df)
    print(df['addr'].unique())
    print(df['addr'].nunique())

    uniqueaddr_df = df.drop_duplicates(keep='last')
    print(uniqueaddr_df)

    kpis_df = pd.DataFrame({'addr': uniqueaddr_df['addr'], 'value': np.zeros(60, dtype=float, order='C')})
    #list of kpis: amount of big transactions,

def chartsBTC():

    # Leer datos y meterlos en un dataframe
    # Reducir anális a 1 hora despues del trigger

    df = pd.read_excel(io='C:/Users/armen/PycharmProjects/degrees/chartsBTC/BREs.xlsx',
                            skiprows=0,
                            names=['epoch', 'day', 'month', 'year', 'hour', 'min', 'usd', 'pol'])

    #df['epoch'] = df['epoch'] / 1000
    print(df)
    timeframe = pd.DataFrame({'minute': range(0, 60), 'value': np.zeros(60, dtype=float, order='C')})
    count = 0

    while count < len(df):

        date = str(df.iloc[count]['year']) + str(df.iloc[count]['month']) + str(df.iloc[count]['day'])
        timeframe_prov = np.zeros(60, dtype=float, order='C')

        df_in = pd.read_excel(io = 'C:/Users/armen/PycharmProjects/degrees/chartsBTC/BRE/' +
                                    str(df.iloc[count]['year']) +
                                    str(df.iloc[count]['month']) +
                                    str(df.iloc[count]['day']) +
                                    '/inTx.xlsx',
                                    skiprows=0,
                                    names=['id', 'script', 'value', 'addr', 'hash', 'vin', 'vout', 'fee', 'time', 'block'])

        df_in.head()

        df_out = pd.read_excel(io = 'C:/Users/armen/PycharmProjects/degrees/chartsBTC/BRE/' +
                                    str(df.iloc[count]['year']) +
                                    str(df.iloc[count]['month']) +
                                    str(df.iloc[count]['day']) +
                                    '/outTx.xlsx',
                                  skiprows=0,
                                  names=['id', 'value', 'addr', 'block', 'time', 'hash', 'vin', 'vout'])

        df_out.head()
        df_in.drop(df_in[df_in['time'] < df.iloc[count]['epoch']/1000].index, inplace=True)
        df_out.drop(df_out[df_out['time'] < df.iloc[count]['epoch']/1000].index, inplace=True)

        timecount = 0
        minutecount = 0

        while timecount < len(df_in) - 1:

            minutecheck = int((df_in.iloc[timecount][8] - df.iloc[count]['epoch']/1000) / 60)
            if minutecheck > minutecount:
                minutecount += 1
            timeframe_prov[minutecount] += df_in.iloc[timecount][2]
            timecount += 1

        timeframe[date] = timeframe_prov
        count += 1
    timeframe.to_excel("Charts.xlsx")

def chartsETH():

    # Leer datos y meterlos en un dataframe
    # Reducir anális a 1 hora, +-30 mins desde trigger

    df = pd.read_excel(io='C:/Users/armen/PycharmProjects/degrees/chartsBTC/EREsprov.xlsx',
                            skiprows=0,
                            names=['epoch', 'day', 'month', 'year', 'hour', 'min'])

    print(df)
    timeframe = pd.DataFrame({'hour': range(0, 60), 'minute': np.zeros(60, dtype=float, order='C')})
    count = 0

    while count < len(df):

        date = str(df.iloc[count]['year']) + str(df.iloc[count]['month']) + str(df.iloc[count]['day'])
        timeframe_prov = np.zeros(60, dtype=float, order='C')

        dfTX = pd.read_excel(io='C:/Users/armen/PycharmProjects/degrees/chartsBTC/ERE/' +
                                str(df.iloc[count]['year']) +
                                str(df.iloc[count]['month']) +
                                str(df.iloc[count]['day']) +
                                '.xlsx')

        dfTX.head()

        del dfTX["block_id"]
        del dfTX["failed"]
        del dfTX["call_count"]
        del dfTX["input_hex"]
        del dfTX["nonce"]
        del dfTX["v"]
        del dfTX["r"]
        del dfTX["s"]

        timecount = 0
        mininicio = dfTX.iloc[timecount][1].minute
        hourinicio = dfTX.iloc[timecount][1].hour
        minutecount = 0
        minutecount2 = 0

        hourcount = hourinicio

        while timecount < len(dfTX) - 1:
            if dfTX.iloc[timecount][1].hour > hourcount:
                hourcount += 1
                minutecount2 = 0
            minutecheck = int(dfTX.iloc[timecount][1].minute - minutecount2)
            if minutecheck > minutecount:
                minutecount += 1
                minutecount2 += 1
            timeframe_prov[minutecount] += dfTX.iloc[timecount][5]
            timecount += 1

        timeframe[date] = timeframe_prov
        count += 1
    timeframe.to_excel("ChartsETH.xlsx")

def kpisbtc():

    # Leer datos y meterlos en un dataframe
    # Reducir anális a 1 hora, +-30 mins desde trigger



    df = pd.read_excel(io='C:/Users/armen/PycharmProjects/degrees/chartsBTC/BREs.xlsx',
                            skiprows=0,
                            names=['epoch', 'day', 'month', 'year', 'hour', 'min', 'usd', 'pol'])

    aaa = len(df)
    #df['epoch'] = df['epoch'] / 1000
    print(df)
    kpis = pd.DataFrame({'date': np.zeros(aaa, dtype=float, order='C'),
                            'avgsen': np.zeros(aaa, dtype=float, order='C'),
                            'avgrec': np.zeros(aaa, dtype=float, order='C'),
                            'devsen': np.zeros(aaa, dtype=float, order='C'),
                            'devrec': np.zeros(aaa, dtype=float, order='C'),
                            'totsen': np.zeros(aaa, dtype=float, order='C'),
                            'totrec': np.zeros(aaa, dtype=float, order='C'),
                            'avgtime': np.zeros(aaa, dtype=float, order='C'),
                            'devtime': np.zeros(aaa, dtype=float, order='C'),
                            'maxtime': np.zeros(aaa, dtype=float, order='C'),
                            'nsen': np.zeros(aaa, dtype=float, order='C'),
                            'nrec': np.zeros(aaa, dtype=float, order='C'),
                            'txsen': np.zeros(aaa, dtype=float, order='C'),
                            'txrec': np.zeros(aaa, dtype=float, order='C')
                            })

    count = 0
    while count < len(df):

        df_in = pd.read_excel(io = 'C:/Users/armen/PycharmProjects/degrees/chartsBTC/BRE/' +
                                    str(df.iloc[count]['year']) +
                                    str(df.iloc[count]['month']) +
                                    str(df.iloc[count]['day']) +
                                    '/inTx.xlsx',
                                    skiprows=0,
                                    names=['id','script', 'value', 'addr', 'hash', 'vin', 'vout', 'fee', 'time', 'block'])

        df_in.head()

        df_out = pd.read_excel(io = 'C:/Users/armen/PycharmProjects/degrees/chartsBTC/BRE/' +
                                    str(df.iloc[count]['year']) +
                                    str(df.iloc[count]['month']) +
                                    str(df.iloc[count]['day']) +
                                    '/outTx.xlsx',
                                  skiprows=0,
                                  names=['id', 'value', 'addr', 'block', 'time', 'hash', 'vin', 'vout'])

        df_out.head()
        df_in.drop(df_in[df_in['time'] < df.iloc[count]['epoch']/1000].index, inplace=True)
        df_out.drop(df_out[df_out['time'] < df.iloc[count]['epoch']/1000].index, inplace=True)

        df_in['value'] = df_in['value']/100000000
        df_out['value'] = df_out['value']/100000000

        tempprov = pd.DataFrame({'hash': df_out['hash'], 'time': df_out['time']})
        tempprov.drop_duplicates(inplace = True)
        tempprov.sort_values(by=['time'], inplace = True, ascending = False)

        #ANOTHER WAY OF INITIALIZING KPIs DF
        #uniqueaddr_df = df_in.drop_duplicates(keep='last')
        #print(uniqueaddr_df)
        #kpis_df = pd.DataFrame({'addr': uniqueaddr_df['addr'], 'value': np.zeros(len(uniqueaddr_df), dtype=float, order='C')})

        tempprov['timeinterval'] = tempprov['time'] - tempprov['time'].shift(-1)
        #tempprov.drop(tempprov[tempprov['timeinterval'] == 0].index, inplace=True)
        tempprov.dropna(subset = ['timeinterval'], inplace=True)

        kpis.iat[count,0] = str(df.iloc[count]['year']) + str(df.iloc[count]['month']) + str(df.iloc[count]['day'])
        kpis.iat[count,1] = (df_in['value'].sum() / len(df_in))*df.iloc[count]['usd']
        kpis.iat[count,2] = (df_out['value'].sum() / len(df_out))*df.iloc[count]['usd']
        kpis.iat[count,3] = statistics.stdev(df_in['value']*df.iloc[count]['usd'])
        kpis.iat[count,4] = statistics.stdev(df_out['value']*df.iloc[count]['usd'])
        kpis.iat[count,5] = (df_in['value'].sum())*df.iloc[count]['usd']
        kpis.iat[count,6] = (df_out['value'].sum())*df.iloc[count]['usd']

        kpis.iat[count,7] = tempprov['timeinterval'].sum() / (len(tempprov) - 1)
        kpis.iat[count,8] = statistics.stdev(tempprov['timeinterval'])
        kpis.iat[count,9] = tempprov['timeinterval'].max()

        kpis.iat[count,10] = df_in['addr'].nunique()
        kpis.iat[count,11] = df_out['addr'].nunique()
        kpis.iat[count,12] = df_in['hash'].nunique()
        kpis.iat[count,13] = df_out['hash'].nunique()

        count += 1

    print("VOLUME")
    print("Average dollars sent in a transaction: " + str(df_in['value'].sum()/len(df_in)))
    print("Average dollars received in a transaction: " + str(df_out['value'].sum()/len(df_out)))
    print("Standard deviation of dollars sent: " + str(statistics.stdev(df_in['value'])))
    print("Standard deviation of dollars received: " + str(statistics.stdev(df_out['value'])))
    print("Total dollars sent: " + str(df_in['value'].sum()))
    print("Total dollars received: " + str(df_out['value'].sum()))

    print("TEMPORAL")
    print("Average time interval between transactions: " + str(tempprov['timeinterval'].sum()/(len(tempprov)-1)))
    print("Standard deviation time interval between transactions: " + str(statistics.stdev(tempprov['timeinterval'])))
    print("Maximum time interval between transactions: : " + str(tempprov['timeinterval'].max()))

    print("NETWORK")
    print("Number of transactions senders: " + str(df_in['addr'].nunique()))
    print("Number of transactions receivers: " + str(df_out['addr'].nunique()))
    print("Number of sent transactions: " + str(df_in['hash'].nunique()))
    print("Number of received transactions: " + str(df_out['hash'].nunique()))
    kpis.to_excel("KPIs.xlsx")

def kpiseth():

    # Leer datos y meterlos en un dataframe
    # Reducir anális a 1 hora, +-30 mins desde trigger

    df = pd.read_excel(io='C:/Users/armen/PycharmProjects/degrees/chartsBTC/EREsprov.xlsx',
                            skiprows=0,
                            names=['epoch', 'day', 'month', 'year', 'hour', 'min'])

    aaa = len(df)
    print(df)
    kpis = pd.DataFrame({'date': np.zeros(aaa, dtype=float, order='C'),
                            'avgusd': np.zeros(aaa, dtype=float, order='C'),
                            'avgint': np.zeros(aaa, dtype=float, order='C'),
                            'devusd': np.zeros(aaa, dtype=float, order='C'),
                            'devint': np.zeros(aaa, dtype=float, order='C'),
                            'totusd': np.zeros(aaa, dtype=float, order='C'),
                            'totint': np.zeros(aaa, dtype=float, order='C'),
                            'avgtime': np.zeros(aaa, dtype=float, order='C'),
                            'devtime': np.zeros(aaa, dtype=float, order='C'),
                            'maxtime': np.zeros(aaa, dtype=float, order='C'),
                            'nsen': np.zeros(aaa, dtype=float, order='C'),
                            'nrec': np.zeros(aaa, dtype=float, order='C'),
                            'txs': np.zeros(aaa, dtype=float, order='C')
                            })

    count = 0
    while count < len(df):

#        dfTX = pd.read_excel(io = 'C:/Users/armen/PycharmProjects/degrees/chartsBTC/ERE/' +
#                                    str(df.iloc[count]['year']) +
#                                    str(df.iloc[count]['month']) +
#                                    str(df.iloc[count]['day']) +
#                                    '.xlsx',
#                                    skiprows=0,
#                                    names=['bid', 'hash', 'time', 'failed', 'type', 'sender', 'recipient', 'callcount', 'value'
#                                           'valueusd','intvalue', 'intvalueusd', 'fee','feeusd','gasused', 'gaslimit', 'gasprice'                                                              'valueusd',
#                                           'input', 'nonce', 'v', 'r', 's'])

        dfTX = pd.read_excel(io='C:/Users/armen/PycharmProjects/degrees/chartsBTC/ERE/' +
                                str(df.iloc[count]['year']) +
                                str(df.iloc[count]['month']) +
                                str(df.iloc[count]['day']) +
                                '.xlsx')

        dfTX.head()

        del dfTX["block_id"]
        del dfTX["failed"]
        del dfTX["call_count"]
        del dfTX["input_hex"]
        del dfTX["nonce"]
        del dfTX["v"]
        del dfTX["r"]
        del dfTX["s"]
        print(dfTX['time'])
        print(dfTX['time'][0])
        print(dfTX['time'][7])

        td = dfTX['time'][7]-dfTX['time'][0]
        print(td.total_seconds())

        dfTX.drop(dfTX[(dfTX['value_usd'] == 0) & (dfTX['internal_value_usd'] == 0)].index, inplace=True)

        tempprov = pd.DataFrame({'hash': dfTX['hash'], 'time': dfTX['time']})
        tempprov.drop_duplicates(inplace = True)

        #ANOTHER WAY OF INITIALIZING KPIs DF
        #uniqueaddr_df = df_in.drop_duplicates(keep='last')
        #print(uniqueaddr_df)
        #kpis_df = pd.DataFrame({'addr': uniqueaddr_df['addr'], 'value': np.zeros(len(uniqueaddr_df), dtype=float, order='C')})

        tempprov['timeinterval'] = (tempprov['time'].shift(-1) - tempprov['time']).astype('timedelta64[s]')
        #tempprov.drop(tempprov[tempprov['timeinterval'] == 0].index, inplace=True)
        tempprov.dropna(subset = ['timeinterval'], inplace=True)

        print(tempprov)

        kpis.iat[count,0] = str(df.iloc[count]['year']) + str(df.iloc[count]['month']) + str(df.iloc[count]['day'])
        kpis.iat[count,1] = dfTX['value_usd'].sum() / len(dfTX)
        kpis.iat[count,2] = dfTX['internal_value_usd'].sum() / len(dfTX)
        kpis.iat[count,3] = statistics.stdev(dfTX['value_usd'])
        kpis.iat[count,4] = statistics.stdev(dfTX['internal_value_usd'])
        kpis.iat[count,5] = dfTX['value_usd'].sum()
        kpis.iat[count,6] = dfTX['internal_value_usd'].sum()

        kpis.iat[count,7] = tempprov['timeinterval'].sum() / (len(tempprov) - 1)
        kpis.iat[count,8] = statistics.stdev(tempprov['timeinterval'])
        kpis.iat[count,9] = tempprov['timeinterval'].max()

        kpis.iat[count,10] = dfTX['sender'].nunique()
        kpis.iat[count,11] = dfTX['recipient'].nunique()
        kpis.iat[count,12] = dfTX['hash'].nunique()

        count += 1

    kpis.to_excel("KPIsETH.xlsx")

def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    # libraries
    # Make a data frame

    df = pd.DataFrame({'x': range(0, 10), 'y1': np.random.randn(10), 'y2': np.random.randn(10) + range(1, 11),
                       'y3': np.random.randn(10) + range(11, 21), 'y4': np.random.randn(10) + range(6, 16),
                       'y5': np.random.randn(10) + range(4, 14),
                       'y6': np.random.randn(10) + range(2, 12), 'y7': np.random.randn(10) + range(5, 15),
                       'y8': np.random.randn(10) + range(4, 14)})
    df = pd.DataFrame({'x': range(0, 120), 'y1': np.random.randn(120), 'y2': np.random.randn(120),
                       'y3': np.random.randn(120), 'y4': np.random.randn(120),
                       'y5': np.random.randn(120)})

    print(df)


    # Change the style of plot
    plt.style.use('seaborn-darkgrid')

    # set figure size
    my_dpi = 96
    plt.figure(figsize=(720 / my_dpi, 720 / my_dpi), dpi=my_dpi)

    # plot multiple lines
    for column in df.drop('x', axis=1):
        plt.plot(df['x'], df[column], marker='', color='black', linewidth=2, alpha=0.4)

    # Now re do the interesting curve, but biger with distinct color
    plt.plot(df['x'], df['y5'], marker='', color='orange', linewidth=5, alpha=0.7)

    # Change x axis limit
    plt.xlim(0, 121)

    # Let's annotate the plot
    num = 0
    for i in df.values[9][1:]:
        num += 1
        name = list(df)[num]
        if name != 'y5':
            plt.text(120.2, i, name, horizontalalignment='left', size='medium', color='grey')

    # And add a special annotation for the group we are interested in
    plt.text(120.2, df.y5.tail(1), 'Mr Orange', horizontalalignment='left', size='medium', color='orange')

    # Add titles
    plt.title("Evolution of Mr Orange vs other students", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("Time")
    plt.ylabel("Score")

    # Show the graph
    plt.show() # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi()
    #rueba()
    kpisbtc()
    kpiseth()
    #chartsBTC()
    #chartsETH()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
