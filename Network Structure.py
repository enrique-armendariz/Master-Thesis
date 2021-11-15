# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics

def walletsbtc():

    # Leer datos y meterlos en un dataframe
    # Reducir anális a 1 hora despues del trigger

    df = pd.read_excel(io='C:/Users/armen/PycharmProjects/degrees/chartsBTC/BREs.xlsx',
                            skiprows=0,
                            names=['epoch', 'day', 'month', 'year', 'hour', 'min', 'usd', 'pol'])


    print(df)
    walletsin = pd.DataFrame({'ranking': range(0, 10)})
    walletsout = pd.DataFrame({'ranking': range(0, 10)})

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

        #df_in['valueusd'] = df_in.value*df.iloc[count]['usd']/10^8
        df_in['value'] = df_in['value'].apply(lambda x: x * df.iloc[count]['usd'])

        df_out = pd.read_excel(io = 'C:/Users/armen/PycharmProjects/degrees/chartsBTC/BRE/' +
                                    str(df.iloc[count]['year']) +
                                    str(df.iloc[count]['month']) +
                                    str(df.iloc[count]['day']) +
                                    '/outTx.xlsx',
                                  skiprows=0,
                                  names=['id', 'value', 'addr', 'block', 'time', 'hash', 'vin', 'vout'])

        df_out.head()

        #df_out['valueusd'] = df_out.value*df.iloc[count]['usd']/10^8
        df_out['value'] = df_out['value'].apply(lambda x: x * df.iloc[count]['usd'])

        df_in.drop(df_in[df_in['time'] < df.iloc[count]['epoch']/1000].index, inplace=True)
        df_out.drop(df_out[df_out['time'] < df.iloc[count]['epoch']/1000].index, inplace=True)

        n = 10

        #walletsin[date] = df_in['addr'].value_counts()[:n].index.tolist()
        walletsin[date] = df_in['addr'].value_counts()[:n].index.tolist()
        #walletsout[date] = df_out['addr'].value_counts()[:n].sort_values(ascending=False)



        count += 1
    #timeframe.to_excel("Charts.xlsx")
    #print(walletsin)
    #print(walletsout)
    print(df_in['addr'].value_counts()[:n])
    print(df_in['addr'].value_counts()[:n].index.tolist())

def blockchainBTC():

    # Leer datos y meterlos en un dataframe
    # Reducir anális a 1 hora despues del trigger

    df = pd.read_excel(io='C:/Users/armen/PycharmProjects/degrees/chartsBTC/BREs.xlsx',
                            skiprows=0,
                            names=['epoch', 'day', 'month', 'year', 'hour', 'min', 'usd', 'pol'])



    kpis = pd.DataFrame({'date': np.zeros(len(df), dtype=str, order='C'),
                         'nsen': np.zeros(len(df), dtype=float, order='C'),
                         'nrec': np.zeros(len(df), dtype=float, order='C'),
                         'txsen': np.zeros(len(df), dtype=float, order='C'),
                         'txrec': np.zeros(len(df), dtype=float, order='C'),
                         'vols': np.zeros(len(df), dtype=float, order='C'),
                         'avgs': np.zeros(len(df), dtype=float, order='C'),
                         'stds': np.zeros(len(df), dtype=float, order='C'),
                         'volr': np.zeros(len(df), dtype=float, order='C'),
                         'avgr': np.zeros(len(df), dtype=float, order='C'),
                         'stdr': np.zeros(len(df), dtype=float, order='C'),
                         'wha': np.zeros(len(df), dtype=float, order='C'),
                         'inv': np.zeros(len(df), dtype=float, order='C'),
                         'ret': np.zeros(len(df), dtype=float, order='C'),
                         'txwha': np.zeros(len(df), dtype=float, order='C'),
                         'txinv': np.zeros(len(df), dtype=float, order='C'),
                         'txret': np.zeros(len(df), dtype=float, order='C'),
                         'vwha': np.zeros(len(df), dtype=float, order='C'),
                         'vinv': np.zeros(len(df), dtype=float, order='C'),
                         'vret': np.zeros(len(df), dtype=float, order='C')
                         })
    tempresult = pd.DataFrame({'ts': range(0, 60)})

    whales = pd.DataFrame({'addr': np.zeros(1, dtype=str, order='C'),
                         'value': np.zeros(1, dtype=float, order='C')})
    investors = pd.DataFrame({'addr': np.zeros(1, dtype=str, order='C'),
                           'value': np.zeros(1, dtype=float, order='C')})

    count = 0
    aaa = 1e-08

    while count < len(df):

        countcol = 0
        date = str(df.iloc[count]['year']) + str(df.iloc[count]['month']) + str(df.iloc[count]['day'])
        kpis.iat[count,countcol] = str(df.iloc[count]['year']) + str(df.iloc[count]['month']) + str(df.iloc[count]['day'])
        countcol += 1

        df_in = pd.read_excel(io = 'C:/Users/armen/PycharmProjects/degrees/chartsBTC/BRE/' +
                                    str(df.iloc[count]['year']) +
                                    str(df.iloc[count]['month']) +
                                    str(df.iloc[count]['day']) +
                                    '/inTx.xlsx',
                                    skiprows=0,
                                    names=['id', 'script', 'value', 'addr', 'hash', 'vin', 'vout', 'fee', 'time', 'block'])

        df_in.head()

        df_in['value'] = df_in['value'].apply(lambda x: x * df.iloc[count]['usd'])
        df_in['value'] = df_in['value']*aaa

        df_out = pd.read_excel(io = 'C:/Users/armen/PycharmProjects/degrees/chartsBTC/BRE/' +
                                    str(df.iloc[count]['year']) +
                                    str(df.iloc[count]['month']) +
                                    str(df.iloc[count]['day']) +
                                    '/outTx.xlsx',
                                  skiprows=0,
                                  names=['id', 'value', 'addr', 'block', 'time', 'hash', 'vin', 'vout'])

        df_out.head()

        df_out['value'] = df_out['value'].apply(lambda x: x * df.iloc[count]['usd'])
        df_out['value'] = df_out['value']*aaa

        if df.iloc[count]['pol'] == "positive":
            dfprov = df_out
        else:
            dfprov = df_in

        # TIME ANALYSIS
        # to initialize the provisional dataframe for each event
        tempprov = pd.DataFrame({'time': dfprov['time'], 'value': dfprov['value']})
        bbb = 60e09
        # Only for ETH
        #tempprov['ts'] = tempprov.time.values.astype(np.int64)

        # to change the time column to minutes from 0 to 60, that are minute count since the trigger
        tempprov['ts'] = tempprov['time'].div(bbb).round(0)
        tempprov.sort_values('ts')
        tempprov['ts'] -= tempprov.iloc[0][2]

        # to clean the dataframe and group all the transaction in minute intervals
        tempprov = tempprov[['ts', 'value']]
        tempprov2 = tempprov.groupby('ts', as_index=False)[['value']].sum()

        # saving the analysis in the results dataframe that stores all the events
        tempresult = pd.merge(tempresult, tempprov2, on='ts', how='left').fillna(0)
        tempresult = tempresult.rename(columns={'value': date})


        #Blockchain analysis

        nsen = df_in['addr'].nunique()
        nrec = df_out['addr'].nunique()

        txsen = len(df_in)
        txrec = len(df_out)

        vols = df_in['value'].sum()
        avgs = df_in['value'].mean()
        stds = df_in['value'].std()

        volr = df_out['value'].sum()
        avgr = df_out['value'].mean()
        stdr = df_out['value'].std()

        kpis.iat[count, countcol] = nsen
        countcol += 1

        kpis.iat[count, countcol] = nrec
        countcol += 1

        kpis.iat[count, countcol] = txsen
        countcol += 1

        kpis.iat[count, countcol] = txrec
        countcol += 1

        kpis.iat[count, countcol] = vols
        countcol += 1

        kpis.iat[count, countcol] = avgs
        countcol += 1

        kpis.iat[count, countcol] = stds
        countcol += 1

        kpis.iat[count, countcol] = volr
        countcol += 1

        kpis.iat[count, countcol] = avgr
        countcol += 1

        kpis.iat[count, countcol] = stdr
        countcol += 1

        #Address classification

        volume = dfprov['value'].sum()
        volume1per = volume/100
        volumedot1per = volume/1000

        txwha = len(dfprov[(dfprov['value'] > volume1per)])
        txinv = len(dfprov[(dfprov['value'] > volumedot1per)]) - txwha
        txret = len(dfprov) - txinv - txwha

        inprov = pd.DataFrame({'addr': dfprov['addr'],
                               'value': dfprov['value']})
        inprov2 = inprov.groupby('addr').sum()
        inprov2.sort_values(by=['value'])

        numwha = len(inprov2[(inprov2['value'] > volume1per)])
        numinv = len(inprov2[(inprov2['value'] > volumedot1per)]) - numwha
        numret = len(inprov2) - numwha - numinv

        whalesprov = inprov2[(inprov2['value'] > volume1per)]
        investorsprov = inprov2[(inprov2['value'] > volumedot1per) & (inprov2['value'] < volume1per)]

        vwha = whalesprov['value'].sum()
        vinv = investorsprov['value'].sum()
        vret = inprov2['value'].sum() - vwha - vinv

        kpis.iat[count,countcol] = numwha
        countcol += 1

        kpis.iat[count,countcol] = numinv
        countcol += 1

        kpis.iat[count,countcol] = numret
        countcol += 1

        kpis.iat[count,countcol] = txwha
        countcol += 1

        kpis.iat[count,countcol] = txinv
        countcol += 1

        kpis.iat[count,countcol] = txret
        countcol += 1

        kpis.iat[count,countcol] = vwha
        countcol += 1

        kpis.iat[count,countcol] = vinv
        countcol += 1

        kpis.iat[count,countcol] = vret
        countcol += 1

        whalesprov.insert(len(whalesprov.columns), date, 'yes')
        investorsprov.insert(len(investorsprov.columns), date, 'yes')

        # Check if whales and investors acted in a specific range of time. EX: 25-30 minst
        tempprov4 = pd.DataFrame({'time': dfprov['time'], 'value': dfprov['value'], 'addr': dfprov['addr']})
        bbb = 60e09
        tempprov4['ts'] = tempprov4['time'].div(bbb).round(0)
        tempprov4.sort_values('ts')
        tempprov4['ts'] -= tempprov4.iloc[0][3]
        print(tempprov4)
        tempprov4.drop(tempprov4[(tempprov4['ts'] < 25)].index, inplace=True)
        #tempprov4.drop(tempprov4[(tempprov4['ts'] > 30)].index, inplace=True)
        print(tempprov4)
        whalesprov[date + ' 25-30 mins'] = whalesprov.index.isin(tempprov4.addr).astype(int)
        investorsprov[date + ' 25-30 mins'] = investorsprov.index.isin(tempprov4.addr).astype(int)

        frames = [whales, whalesprov]
        whales = pd.concat(frames)

        frames2 = [investors, investorsprov]
        investors = pd.concat(frames2)

        count += 1

    # delete a single row by index value 0
    whales = whales.drop(labels=0, axis=0)
    investors = investors.drop(labels=0, axis=0)

    print(kpis)
    print(whales)
    print(investors)
    kpis.to_excel("KPIs.xlsx")
    whales.to_excel("whales.xlsx")
    investors.to_excel("investors.xlsx")
    tempresult.to_excel("timeresultsBTC.xlsx")

def blockchainETH():

    # Read the excel with the list of events
    df = pd.read_excel(io='C:/Users/armen/PycharmProjects/degrees/chartsBTC/EREs.xlsx',
                            skiprows=0,
                            names=['epoch', 'day', 'month', 'year', 'hour', 'min', 'usd', 'pol'])


    # Create KPIs and time  dataframe
    kpis = pd.DataFrame({'date': np.zeros(len(df), dtype=str, order='C'),
                         'nsen': np.zeros(len(df), dtype=float, order='C'),
                         'nrec': np.zeros(len(df), dtype=float, order='C'),
                         'txsen': np.zeros(len(df), dtype=float, order='C'),
                         'txrec': np.zeros(len(df), dtype=float, order='C'),
                         'vols': np.zeros(len(df), dtype=float, order='C'),
                         'avgs': np.zeros(len(df), dtype=float, order='C'),
                         'stds': np.zeros(len(df), dtype=float, order='C'),
                         'volr': np.zeros(len(df), dtype=float, order='C'),
                         'avgr': np.zeros(len(df), dtype=float, order='C'),
                         'stdr': np.zeros(len(df), dtype=float, order='C'),
                         'wha': np.zeros(len(df), dtype=float, order='C'),
                         'inv': np.zeros(len(df), dtype=float, order='C'),
                         'ret': np.zeros(len(df), dtype=float, order='C'),
                         'txwha': np.zeros(len(df), dtype=float, order='C'),
                         'txinv': np.zeros(len(df), dtype=float, order='C'),
                         'txret': np.zeros(len(df), dtype=float, order='C'),
                         'vwha': np.zeros(len(df), dtype=float, order='C'),
                         'vinv': np.zeros(len(df), dtype=float, order='C'),
                         'vret': np.zeros(len(df), dtype=float, order='C')
                         })
    tempresult = pd.DataFrame({'ts': range(0, 60)})

    whales = pd.DataFrame({'addr': np.zeros(1, dtype=str, order='C'),
                         'value': np.zeros(1, dtype=float, order='C')})
    investors = pd.DataFrame({'addr': np.zeros(1, dtype=str, order='C'),
                           'value': np.zeros(1, dtype=float, order='C')})

    count = 0
    aaa = 1e-18

    while count < len(df):

        countcol = 0
        date = str(df.iloc[count]['year']) + str(df.iloc[count]['month']) + str(df.iloc[count]['day'])
        kpis.iat[count,countcol] = date
        countcol += 1
        df_in = pd.read_excel(io = 'C:/Users/armen/PycharmProjects/degrees/chartsBTC/ERE/' +
                                    str(df.iloc[count][3]) +
                                    str(df.iloc[count][2]) +
                                    str(df.iloc[count][1]) +
                                    '.xlsx',
                                    skiprows=0,
                                    names=['hash', 'time', 'sender', 'recipient', 'value', 'internal_value'],
                                    sheet_name= 'Hoja1')

        df_in.head()
        df_in.drop(df_in[(df_in['value'] == 0) & (df_in['internal_value'] == 0)].index, inplace=True)

        df_in['value'] = df_in['value'] * df.iloc[count]['usd']
        df_in['value'] = df_in['value'] * aaa

        df_out = pd.read_excel(io = 'C:/Users/armen/PycharmProjects/degrees/chartsBTC/ERE/' +
                                    str(df.iloc[count][3]) +
                                    str(df.iloc[count][2]) +
                                    str(df.iloc[count][1]) +
                                    '.xlsx',
                                  skiprows=0,
                                  names=['hash', 'time', 'sender', 'recipient', 'value', 'internal_value'],
                                  sheet_name= 'Hoja1')
        df_out.head()
        df_out.drop(df_out[(df_out['value'] == 0) & (df_out['internal_value'] == 0)].index, inplace=True)
        pd.to_numeric(df_out['value'])
        df_out['value'] = df_out['value'] * df.iloc[count]['usd']
        df_out['value'] = df_out['value'] * aaa

        #CHOOSE INPUTS or OUTPUTS: depending on the impact of the event (positive or negative on the market)

        if df.iloc[count]['pol'] == "positive":

            dfprov = df_out
            dfprov = dfprov.rename(columns={'sender': 'addr'})
        else:
            dfprov = df_in
            dfprov = dfprov.rename(columns={'recipient': 'addr'})

        #TIME ANALYSIS
        #to initialize the provisional dataframe for each event
        tempprov = pd.DataFrame({'time': dfprov['time'], 'value': dfprov['value']})
        bbb = 60e09
        tempprov['ts'] = tempprov.time.values.astype(np.int64)

        #to change the time column to minutes from 0 to 60, that are minute count since the trigger
        tempprov['ts'] = tempprov['ts'].div(bbb).round(0)
        tempprov['ts'] -= tempprov.iloc[0][2]

        #to clean the dataframe and group all the transaction in minute intervals
        tempprov = tempprov[['ts', 'value']]
        tempprov2 = tempprov.groupby('ts', as_index=False)[['value']].sum()

        #saving the analysis in the results dataframe that stores all the events
        tempresult = pd.merge(tempresult, tempprov2, on='ts', how='left').fillna(0)
        tempresult = tempresult.rename(columns={'value': date})

        ########
        #BLOCKCHAIN ANALYSIS: number of senders, recipients, transactions and circulating assets metrics

        nsen = df_in['sender'].nunique()
        nrec = df_out['recipient'].nunique()

        txsen = df_in['hash'].nunique()
        txrec = df_out['hash'].nunique()

        vols = df_in['value'].sum()
        avgs = df_in['value'].mean()
        stds = df_in['value'].std()

        volr = df_out['value'].sum()
        avgr = df_out['value'].mean()
        stdr = df_out['value'].std()

        kpis.iat[count, countcol] = nsen
        countcol += 1

        kpis.iat[count, countcol] = nrec
        countcol += 1

        kpis.iat[count, countcol] = txsen
        countcol += 1

        kpis.iat[count, countcol] = txrec
        countcol += 1

        kpis.iat[count, countcol] = vols
        countcol += 1

        kpis.iat[count, countcol] = avgs
        countcol += 1

        kpis.iat[count, countcol] = stds
        countcol += 1

        kpis.iat[count, countcol] = volr
        countcol += 1

        kpis.iat[count, countcol] = avgr
        countcol += 1

        kpis.iat[count, countcol] = stdr
        countcol += 1

        #Address classification

        volume = dfprov['value'].sum()
        volume1per = volume/100
        volumedot1per = volume/1000

        txwha = len(dfprov[(dfprov['value'] > volume1per)])
        txinv = len(dfprov[(dfprov['value'] > volumedot1per)]) - txwha
        txret = len(dfprov) - txinv - txwha

        inprov = pd.DataFrame({'addr': dfprov['addr'],
                               'value': dfprov['value']})
        inprov2 = inprov.groupby('addr').sum()
        inprov2.sort_values(by=['value'])

        numwha = len(inprov2[(inprov2['value'] > volume1per)])
        numinv = len(inprov2[(inprov2['value'] > volumedot1per)]) - numwha
        numret = len(inprov2) - numwha - numinv

        whalesprov = inprov2[(inprov2['value'] > volume1per)]
        investorsprov = inprov2[(inprov2['value'] > volumedot1per) & (inprov2['value'] < volume1per)]

        vwha = whalesprov['value'].sum()
        vinv = investorsprov['value'].sum()
        vret = inprov2['value'].sum() - vwha - vinv

        kpis.iat[count,countcol] = numwha
        countcol += 1

        kpis.iat[count,countcol] = numinv
        countcol += 1

        kpis.iat[count,countcol] = numret
        countcol += 1

        kpis.iat[count,countcol] = txwha
        countcol += 1

        kpis.iat[count,countcol] = txinv
        countcol += 1

        kpis.iat[count,countcol] = txret
        countcol += 1

        kpis.iat[count,countcol] = vwha
        countcol += 1

        kpis.iat[count,countcol] = vinv
        countcol += 1

        kpis.iat[count,countcol] = vret
        countcol += 1

        whalesprov.insert(len(whalesprov.columns), date, 'yes')
        investorsprov.insert(len(investorsprov.columns), date, 'yes')
        #whalesprov[date] = 'yes'
        #investorsprov[date] = 'yes'

        # Check if whales and investors acted in a specific range of time. EX: 25-30 minst
        tempprov4 = pd.DataFrame({'time': dfprov['time'], 'value': dfprov['value'], 'addr': dfprov['addr']})
        bbb = 60e09
        tempprov4['ts'] = tempprov4.time.values.astype(np.int64)

        tempprov4['ts'] = tempprov4['ts'].div(bbb).round(0)
        tempprov4['ts'] -= tempprov4.iloc[0][3]
        tempprov4.drop(tempprov4[(tempprov4['ts'] <25)].index, inplace=True)
        tempprov4.drop(tempprov4[(tempprov4['ts'] >30)].index, inplace=True)
        whalesprov[date + ' 25-30 mins'] = whalesprov.index.isin(tempprov4.addr).astype(int)
        investorsprov[date + ' 25-30 mins'] = investorsprov.index.isin(tempprov4.addr).astype(int)


        frames = [whales, whalesprov]
        whales = pd.concat(frames)

        frames2 = [investors, investorsprov]
        investors = pd.concat(frames2)

        count += 1

    # delete a single row by index value 0
    whales = whales.drop(labels=0, axis=0)
    investors = investors.drop(labels=0, axis=0)
    print(kpis)
    print(whales)
    print(investors)
    kpis.to_excel("KPIsETH.xlsx")
    whales.to_excel("whalesETH.xlsx")
    investors.to_excel("investorsETH.xlsx")
    tempresult.to_excel("timeresultsETH.xlsx")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #walletsbtc()
    blockchainBTC()
    #blockchainETH()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
