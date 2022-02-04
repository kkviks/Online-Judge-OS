from email.headerregistry import Group
import os
import time_program
import pandas as pd
import sys
import numpy as np

codes_dir = 'codes'

df = pd.read_excel('leaderboard.xlsx', index_col=0) 
print(df)


# Reading directories
groups = [d for d in os.listdir(codes_dir)]

for group in groups:
    parentPath = 'codes' + '/' + group
    c_files = [c_files for c_files in os.listdir(parentPath) ]
    for c_file in c_files:
        filepath = parentPath + '/' + c_file
        status, t = time_program.run(parentPath,filepath)
        
        if status is time_program.FILE_PASSED:
            print(filepath + ' passed successfuly with runtime: ' + str(t) +' ms\n')
            #update and save the leaderboard excel file here
            #df.drop(df.loc[df['Group']==group].index, inplace=True)
            #print("Leaderboard updated!")
        else:
            print(filepath + ' failed to pass all the test cases')
