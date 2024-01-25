import numpy as np
import pandas as pd
from datetime import datetime
import os


def makeCRSPMonthlyData(params):
    # Timekeeping :TODO:Note this function takes around 3 minutes to run.
    print(f"\nNow working on making CRSP monthly data. Run started at {datetime.now()}.")

    "Set path"
    crspFolder = params.crspFolder + os.sep

    """Load and clean msf dataframe"""
    crsp_msf = pd.read_csv(crspFolder + 'crsp_msf.csv', index_col=0)

    "Convert dates to YYYYMM format. These are originally month end dates"
    # first convert dates to datatype - date-time"
    crsp_msf['dates'] = pd.to_datetime(crsp_msf.date)
    # then change to YYYYMM format
    crsp_msf['dates'] = crsp_msf['dates'].dt.strftime('%Y%m')
    crsp_msf['dates'] = crsp_msf['dates'].astype(int)

    "Load CRSP montly stock file with share code information"
    crsp_mseexchdates = pd.read_csv(crspFolder + 'crsp_mseexchdates.csv', index_col=0)
    # only want to keep certain columns
    crsp_mseexchdates = crsp_mseexchdates.loc[:, ['permno', 'namedt', 'nameendt', 'shrcd', 'exchcd', 'siccd']]
    crsp_mseexchdates.duplicated(subset=['permno', 'siccd']).sum()

    # Merge the share code from the header file to crsp_msf
    crsp_msf = crsp_msf.merge(crsp_mseexchdates, how='outer', on='permno')
    duplicates = crsp_msf.duplicated(subset=['dates', 'permno', 'shrcd'])
    duplicates.sum()
    print(f"There are {duplicates.sum()} duplicate shrcd/permno/date values.")

    # creating index to drop
    idxToDrop1 = np.where(crsp_msf.date < crsp_msf.namedt)[0]
    idxToDrop2 = np.where(crsp_msf.date > crsp_msf.nameendt)[0]
    idxToDrop = np.concatenate((idxToDrop1, idxToDrop2))
    idxToDrop = np.sort(idxToDrop)

    # keeping those NOT in idxToDrop
    crsp_msf = crsp_msf.loc[~crsp_msf.index.isin(idxToDrop)]

    # delete dataframe to free up RAM (not sure if this actually does anything)
    del crsp_mseexchdates

    "Check to see if we should only keep share codes 10 or 11 (domestic common equity)"
    if params.domComEqFlag:  # :TODO:N If error then comment out this block and rerun
        crsp_msf = crsp_msf[crsp_msf['shrcd'].isin([10, 11])].copy()

    "Check to keep only the sample specified in params."
    first_date = params.sample_start*100 + 1
    last_date = params.sample_end*100 + 1
    # idx_to_keep = np.where((crsp_msf['dates'] >= first_date) & (crsp_msf['dates'] <= last_date))
    # idx_to_keep = np.sort(idx_to_keep)
    # crsp_msf = crsp_msf.loc[crsp_msf.index.isin(idx_to_keep)]
    crsp_msf = crsp_msf[(crsp_msf['dates'] >= first_date) & (crsp_msf['dates'] <= last_date)].copy()

    "Rename returns to indicate they are without delisting adjustments"
    crsp_msf.rename(columns={'ret': 'ret_x_dl'}, inplace=True)
    "Rename volume to indicate it is without adjustment for NASDAQ"
    crsp_msf.rename(columns={'vol': 'vol_x_adj'}, inplace=True)

    "Save the link file for the COMPUSTAT matrices creation"
    crsp_link = crsp_msf.loc[:, ['permno', 'date']]
    crsp_link.to_csv(crspFolder + 'crsp_link.csv')
    del crsp_link

    # Create reference DataFrame for 'ret_x_dl'
    ref_df = pd.pivot_table(crsp_msf, index='dates', columns='permno', values='ret_x_dl')
    ref_df.to_csv(crspFolder + 'ret_x_dl.csv')

    "Create and store the permno and dates vectors"
    permno = ref_df.columns
    dates = ref_df.index

    "Save permno, dates"
    pd.DataFrame(permno).to_csv(crspFolder + 'permno.csv')
    pd.DataFrame(dates).to_csv(crspFolder + 'dates.csv')

    # Choose variables from crsp_msf to convert into matrices
    varNames_crsp_msf = ['shrcd', 'exchcd', 'siccd', 'prc', 'bid', 'ask', 'bidlo', 'askhi', 'vol_x_adj',
                         'shrout', 'cfacpr', 'cfacshr', 'spread', 'retx']

    # Create DataFrames for other variables and align them with the reference DataFrame
    for i, var in enumerate(varNames_crsp_msf):
        print(f"{var}: {i+1}/{len(varNames_crsp_msf)}")
        # Create DataFrame for current variable
        temp_df = pd.pivot_table(crsp_msf, index='dates', columns='permno', values=var)

        # Align columns
        for col in ref_df.columns:
            if col not in temp_df.columns:
                temp_df[col] = np.nan

        # Align rows
        for row in ref_df.index:
            if row not in temp_df.index:
                temp_df.loc[row] = np.nan

        # Sort index and columns to match reference DataFrame
        temp_df = temp_df.reindex(index=ref_df.index, columns=ref_df.columns)
        print(f"{var} shape is {temp_df.shape}")
        # Save the aligned DataFrame
        temp_df.to_csv(crspFolder + var + '.csv')

    # Timekeeping
    print(f"\nFinished making CRSP monthly data. Run ended at {datetime.now()}.\n")

    return

