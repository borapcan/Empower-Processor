import os
import eel
from tkinter import filedialog, Tk

from utils.create_df import process_txt_files
from utils.helpers import remove_after_period

# from utils.stats import stats

# Define the directory where text files will be processed
TEXT_FILES_DIRECTORY = ""
export_area = False
stats_c = False

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


@eel.expose
def toggle_stats():
    global stats_c
    if stats_c == False:
        stats_c = True
    else:
        stats_c = False

    print(stats_c)


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

                folder_name = remove_after_period(filename)
                # Create the folder if it doesn't exist
                folder_path = os.path.join("conversion_folder", folder_name)
                os.makedirs(folder_path, exist_ok=True)

                # Export the DataFrame to an Excel file
                df.to_excel(
                    os.path.join(folder_path, excel_filename),
                    index=False,
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
