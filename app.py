import os
import eel
from tkinter import filedialog, Tk

from utils.create_df import process_txt_files

# Define the directory where text files will be processed
TEXT_FILES_DIRECTORY = ""
export_area = False


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


@eel.expose
def toggle_export_area():
    global export_area
    if export_area == False:
        export_area = True
    else:
        export_area = False


# Eel function to process files based on user input
@eel.expose
def process_files(export_area):
    global TEXT_FILES_DIRECTORY
    try:
        if TEXT_FILES_DIRECTORY:
            dfs_dict = process_txt_files(TEXT_FILES_DIRECTORY, export_area)

            # Loop through the dictionary of DataFrames
            for file_path, df in dfs_dict.items():
                # Extract the filename from the file path
                filename = os.path.basename(file_path)

                # Define the Excel filename
                excel_filename = os.path.splitext(filename)[0] + ".xlsx"

                # Export the DataFrame to an Excel file
                df.to_excel(
                    os.path.join("conversion_folder", excel_filename), index=False
                )

            TEXT_FILES_DIRECTORY = ""
            return "Files processed successfully"
        else:
            return "There was an error processing files"
    except ValueError:
        return ValueError


# Start Eel app
eel.start(
    "index.html",
    size=(1920, 1080),
    mode="chrome",
    port=0,
    host="localhost",
    fullscreen=True,
)
