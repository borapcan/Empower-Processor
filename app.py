import os
import eel
from tkinter import filedialog, Tk

from utils.create_df import process_txt_files

# Define the directory where text files will be processed
TEXT_FILES_DIRECTORY = ""

# Define the Eel frontend directory
eel.init("web")


# Eel expose file path to the app
@eel.expose
def choose_directory():
    global TEXT_FILES_DIRECTORY
    root = Tk()
    root.withdraw()  # Hide the Tkinter window
    directory = filedialog.askdirectory()
    root.destroy()  # Destroy the Tkinter window
    TEXT_FILES_DIRECTORY = str(directory)
    return TEXT_FILES_DIRECTORY


# Eel function to process files based on user input
@eel.expose
def process_files(export_area):
    global TEXT_FILES_DIRECTORY
    if TEXT_FILES_DIRECTORY:
        dfs_dict = process_txt_files(TEXT_FILES_DIRECTORY, export_area)

        # Loop through the dictionary of DataFrames
        for file_path, df in dfs_dict.items():
            # Extract the filename from the file path
            filename = os.path.basename(file_path)

            # Define the Excel filename
            excel_filename = os.path.splitext(filename)[0] + ".xlsx"

            # Export the DataFrame to an Excel file
            df.to_excel(os.path.join("conversion_folder", excel_filename), index=False)
    else:
        print("Please select a directory first.")


# Start Eel app
eel.start(
    "index.html",
    size=(800, 600),
    mode="chrome",
    port=0,
    host="localhost",
    fullscreen=True,
)
