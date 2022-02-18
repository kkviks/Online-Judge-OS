import os
import time_program
import pandas as pd

codes_dir = 'codes'


df = pd.read_csv('leaderboard.csv', index_col=0)
print(df.columns)

# Reading directories
groups = [d for d in os.listdir(codes_dir)]

for group in groups:
    parentPath = 'codes' + '/' + group
    c_files = [c_files for c_files in os.listdir(parentPath)]
    for c_file in c_files:
        filepath = parentPath + '/' + c_file
        status, t = time_program.run(parentPath, filepath)

        if status is time_program.FILE_PASSED:
            print(group + ' passed successfully with runtime: ' + str(t) + ' ms\n')
            print('Updating ', group, 'runtime')

            col_runtime = 'Time'
            print('Group type:', type(group))
            if group in df['GName'].values:
                df.loc[df["GName"] == group, "Time"] = t
                df.loc[df["GName"] == group, "Remarks"] = ['pass']
            else:
                new_row = {'GName': [str(group)], 'Time': [float(t)], 'Remarks': ['pass']}
                df_new = pd.DataFrame(new_row)
                df = pd.concat([df, df_new], ignore_index=True, axis=0)
                # print(df)

        elif status is time_program.FILE_COMPILATION_FAILED: 
            print(filepath + ' failed to compile')
            if group in df['GName'].values:
                df.loc[df["GName"] == group, "Time"] = t
                df.loc[df["GName"] == group, "Remarks"] = "Compile Er"
            else:
                new_row = {'GName': [str(group)], 'Time': [float(t)], 'Remarks': ['Compile Er']}
                df_new = pd.DataFrame(new_row)
                df = pd.concat([df, df_new], ignore_index=True, axis=0)


        elif status is time_program.FILE_FAILED:
            print(filepath + 'Test case didnt match')
            if group in df['GName'].values:
                df.loc[df["GName"] == group, "Time"] = 999999
                df.loc[df["GName"] == group, "Remarks"] = "Wrong Ans"
            else:
                new_row = {'GName': [str(group)], 'Time': [float(t)], 'Remarks': ['Wrong Ans']}
                df_new = pd.DataFrame(new_row)
                df = pd.concat([df, df_new], ignore_index=True, axis=0)
        
        df.sort_values('Time', inplace=True)
        df.to_csv('leaderboard.csv')
