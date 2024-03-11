import os
import eel
from tkinter import filedialog, Tk
from pathlib import Path

from utils.create_df import process_txt_files
from utils.helpers import remove_after_period
from utils.stats import (
    generate_sample_list_excel,
    generate_combined_stats_excel,
    generate_box_plot,
)

# from utils.stats import stats

# Define the directory where text files will be processed
TEXT_FILES_DIRECTORY = ""
export_area = False
stats_c = False
plot = False

# Define the Eel frontend directory
eel.init("web")


# Eel expose file path to the app
@eel.expose
def choose_directory():
    global TEXT_FILES_DIRECTORY
    root = Tk()
    root.withdraw()  # Hide the Tkinter window
    root.attributes("-topmost", True)
    directory = filedialog.askdirectory(parent=root)
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


@eel.expose
def toggle_plot():
    global plot
    if plot == False:
        plot = True
    else:
        plot = False


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
                excel_filename = os.path.splitext(filename)[0] + "_data" + ".xlsx"
                stats_filename = os.path.splitext(filename)[0] + "_stats" + ".xlsx"

                folder_name = remove_after_period(filename)
                # Create the folder if it doesn't exist
                folder_path = os.path.join("conversion_folder", folder_name)
                os.makedirs(folder_path, exist_ok=True)

                # Export the DataFrame to an Excel file
                df.to_excel(
                    os.path.join(folder_path, excel_filename),
                    index=False,
                )

                if stats_c:
                    try:
                        sample_list = generate_sample_list_excel(df)
                        stats_df = generate_combined_stats_excel(sample_list, df)
                        # Export the DataFrame to an Excel file
                        stats_df.to_excel(
                            os.path.join(folder_path, stats_filename),
                            index=False,
                        )
                    except Exception as e:
                        print("An error occurred:", str(e))
                if plot:
                    try:
                        fig = generate_box_plot(df)
                        fig_filename = f"{filename}_boxplot.pdf"
                        filepath = os.path.join(folder_path, fig_filename)
                        fig.savefig(filepath, bbox_inches="tight")
                    except Exception as e:
                        print("An error occurred:", str(e))

            TEXT_FILES_DIRECTORY = ""
            return "Files processed successfully"

        else:
            return "There was an error processing files"
    except Exception as e:
        print("An error occurred:", str(e))


# Start Eel app
eel.start(
    "index.html",
    size=(1920, 1080),
    mode="chrome",
    port=0,
    host="localhost",
    fullscreen=True,
)
