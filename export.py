import os
from utils.create_df import process_txt_files

# Get the path to the user's home directory
home_dir = os.path.expanduser("~")

# Navigate to the Desktop folder and the export folder
dir_path = os.path.join(home_dir, "Desktop", "t_export", "stand_samp_dex_pool")

print(dir_path)

# Call the function to process text files and get the dictionary of DataFrames
dfs_dict = process_txt_files(dir_path, export_area=True)

# # Loop through the dictionary of DataFrames
# for file_path, df in dfs_dict.items():
#     # Extract the filename from the file path
#     filename = os.path.basename(file_path)

#     # Define the Excel filename
#     excel_filename = os.path.splitext(filename)[0] + ".xlsx"

#     # Export the DataFrame to an Excel file
#     df.to_excel(os.path.join(dir_path, excel_filename), index=False)
