import numpy as np
import pandas as pd
from datetime import datetime, timedelta
matrix = pd.read_csv('Camps Matrix.csv')

def pick_camp():
    dates = matrix['Start Date'].unique()
    print('Please Select a Start Date:')
    i = 1
    for date in dates:
        print(f'{i}. {date}')
        i += 1
    input_date = dates[int(input('Date: ')) - 1]

    vendors = matrix[matrix['Start Date'] == input_date]['Contractor'].unique()
    print('\nPlease Select a Vendor:')
    i = 1
    for vendor in vendors:
        print(f'{i}. {vendor}')
        i += 1
    input_vendor = vendors[int(input('Vendor: ')) - 1]

    names = matrix[(matrix['Start Date'] == input_date) & (matrix['Contractor'] == input_vendor)]['Camp Name'].unique()
    print('\nPlease Select a Camp:')
    i = 1
    for name in names:
        print(f'{i}. {name}')
        i += 1
    input_name = names[int(input('Camp: ')) - 1]

    return matrix.loc[(matrix['Start Date'] == input_date) & (matrix['Contractor'] == input_vendor) & (matrix['Camp Name'] == input_name)]

def print_camp(camp):
    print('Date:\t', camp['Start Date'].values[0])
    print('Vendor:\t', camp['Contractor'].values[0])
    print('Camp:\t', camp['Camp Name'].values[0])

def print_pool(camp):
    pool = 'No Pool'
    POOL_DURATION = 45
    if camp['Swim'].values[0] == True:
        pool_start = pd.to_datetime(camp['Pool Time']).values[0]
        d = np.timedelta64(POOL_DURATION, 'm')
        pool_end = pool_start + d
        formatted_start = pd.to_datetime(pool_start).strftime('%I:%M%p').lstrip('0')
        formatted_end = pd.to_datetime(pool_end).strftime('%I:%M%p').lstrip('0')
        pool = formatted_start + ' - ' + formatted_end
    print('Pool:\t', pool)

def print_pg(camp):
    pg = 'No Playground'
    PLAYGROUND_DURATION = 30
    if camp['PG'].values[0] == True:
        pg_start = pd.to_datetime(camp['PG Time']).values[0]
        d = np.timedelta64(PLAYGROUND_DURATION, 'm')
        pg_end = pg_start + d
        formatted_start = pd.to_datetime(pg_start).strftime('%I:%M%p').lstrip('0')
        formatted_end = pd.to_datetime(pg_end).strftime('%I:%M%p').lstrip('0')
        pg = formatted_start + ' - ' + formatted_end
    print('PG:\t', pg)

def print_xpg(camp):
    xpg = 'No Extra Playground'
    EXTRA_PLAYGROUND_DURATION = 30
    if camp['PG+'].values[0] == True:
        xpg_start = pd.to_datetime(camp['PG+ Time']).values[0]
        d = np.timedelta64(EXTRA_PLAYGROUND_DURATION, 'm')
        xpg_end = xpg_start + d
        formatted_start = pd.to_datetime(xpg_start).strftime('%I:%M%p').lstrip('0')
        formatted_end = pd.to_datetime(xpg_end).strftime('%I:%M%p').lstrip('0')
        xpg = formatted_start + ' - ' + formatted_end
    print('PG+:\t', xpg)

if __name__ == '__main__':
    camp = pick_camp()
    print('')
    print_camp(camp)
    print('')
    print_pool(camp)
    print_pg(camp)
    print_xpg(camp)