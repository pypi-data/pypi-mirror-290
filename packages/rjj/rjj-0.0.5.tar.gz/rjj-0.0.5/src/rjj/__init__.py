# !/usr/bin/env python3

__version__="0.0.5"

import argparse, os
import pandas as pd

def detector():
    csv_files = [file for file in os.listdir() if file.endswith('.csv')]

    if csv_files:
        print("CSV file(s) available. Select the 1st csv file:")
        
        for index, file_name in enumerate(csv_files, start=1):
            print(f"{index}. {file_name}")

        choice = input(f"Enter your choice (1 to {len(csv_files)}): ")
        choice_index=int(choice)-1
        input1=csv_files[choice_index]

        print("CSV file(s) available. Select the 2nd csv file:")
        
        for index, file_name in enumerate(csv_files, start=1):
            print(f"{index}. {file_name}")

        choice = input(f"Enter your choice (1 to {len(csv_files)}): ")
        choice_index=int(choice)-1
        input2=csv_files[choice_index]

        output = input("Give a name to the output file: ")
        
        try:              
            file1 = pd.read_csv(input1)
            file2 = pd.read_csv(input2)

            columns_to_merge = list(file1.columns)
            merged = pd.merge(file1, file2, on=columns_to_merge, how='left', indicator=True)

            merged['Coexist'] = merged['_merge'].apply(lambda x: 1 if x == 'both' else '')
            merged = merged.drop(columns=['_merge'])
            merged.to_csv(f'{output}.csv', index=False)

            print(f"Results of coexist-record detection saved to {output}.csv")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")
    else:
        print("No CSV files are available in the current directory.")
        input("--- Press ENTER To Exit ---")

def jointer(output_file):
    output = f'{output_file}.csv'
    csv_files = [f for f in os.listdir() if f.endswith('.csv') and f != output]
    dataframes = []

    for file in csv_files:
        file_name = os.path.splitext(file)[0]
        df = pd.read_csv(file)
        df['File'] = file_name
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df = combined_df[['File'] + [col for col in combined_df.columns if col != 'File']]
    combined_df.to_csv(output, index=False)

    print(f"Combined CSV file saved as {output}")

def spliter():
    csv_files = [file for file in os.listdir() if file.endswith('.csv')]

    if csv_files:
        print("CSV file(s) available. Select which one to split:")
        
        for index, file_name in enumerate(csv_files, start=1):
            print(f"{index}. {file_name}")

        choice = input(f"Enter your choice (1 to {len(csv_files)}): ")
        
        try:
            choice_index=int(choice)-1
            selected_file=csv_files[choice_index]
            print(f"File: {selected_file} is selected!")
            
            df = pd.read_csv(selected_file)
            reference_field = df.columns[0]
            groups = df.groupby(reference_field)

            for file_id, group in groups:
                group = group.drop(columns=[reference_field]) 
                output_file = f'{file_id}.csv'
                group.to_csv(output_file, index=False)

            print("CSV files have been split and saved successfully.")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")
    else:
        print("No CSV files are available in the current directory.")
        input("--- Press ENTER To Exit ---")

def spliterx():
    excel_files = [file for file in os.listdir() if file.endswith('.xls') or file.endswith('.xlsx')]

    if excel_files:
        print("Excel file(s) available. Select which one to split:")
        
        for index, file_name in enumerate(excel_files, start=1):
            print(f"{index}. {file_name}")

        choice = input(f"Enter your choice (1 to {len(excel_files)}): ")
        
        try:
            choice_index=int(choice)-1
            selected_file=excel_files[choice_index]
            print(f"File: {selected_file} is selected!")
            
            df = pd.read_excel(selected_file)
            reference_field = df.columns[0]
            groups = df.groupby(reference_field)

            for file_id, group in groups:
                group = group.drop(columns=[reference_field]) 
                output_file = f'{file_id}.xlsx'
                group.to_excel(output_file, index=False)

            print("Excel files have been split and saved successfully.")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")
    else:
        print("No excel files are available in the current directory.")
        input("--- Press ENTER To Exit ---")

def __init__():
    parser = argparse.ArgumentParser(description="rjj will execute different functions based on command-line arguments")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand", help="choose a subcommand:")
    subparsers.add_parser('d', help='detect coexist-record')
    subparsers.add_parser('j', help='joint csv(s) together')
    subparsers.add_parser('s', help='split csv to piece(s)')
    subparsers.add_parser('x', help='split .xls/.xlsx file')

    args = parser.parse_args()
    if args.subcommand == 'j':
        output_file = input("Give a name to the output file: ")
        jointer(output_file)
    elif args.subcommand == 's':
        spliter()
    elif args.subcommand == 'x':
        spliterx()
    elif args.subcommand == 'd':
        detector()
