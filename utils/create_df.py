import os
import pandas as pd


def process_txt_files(dir_path, export_area=False):
    # Initialize an empty dictionary to store the dataframes
    dfs = {}

    # Loop through all files in the directory
    for filename in os.listdir(dir_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(dir_path, filename)
            # Open the txt file and read its content
            with open(file_path, "r") as f:
                lines = f.readlines()

                # Get the column names from the header line
                header = lines[0].strip().split("\t")

                # Check if the required columns are present
                if "SampleName" not in header or "% Area" not in header:
                    raise ValueError(
                        f"Error: Required columns not found in {filename}. Skipping..."
                    )
                    continue
                else:
                    # Get the index of each required column
                    sample_name_idx = header.index("SampleName")
                    percent_area_idx = header.index("% Area")

                    # Check if the "Area" column is present and export_area is True
                    area_idx = (
                        header.index("Area")
                        if "Area" in header and export_area
                        else None
                    )

                    # Create a dictionary to store the data for each sample name
                    sample_data = {}

                    # Extract data from each line and group it by sample name
                    for line in lines[1:]:
                        cols = line.strip().split("\t")

                        sample_name = cols[sample_name_idx]
                        percent_area = cols[percent_area_idx]

                        if percent_area == "%Area":
                            continue

                        if sample_name not in sample_data:
                            sample_data[sample_name] = {
                                "percent_areas": [],
                                "areas": [] if area_idx is not None else None,
                            }

                        # Convert percent_area to float and append it to the list
                        if "," in percent_area:
                            percent_area = percent_area.replace(",", ".")
                        try:
                            percent_area_float = float(percent_area)
                        except ValueError:
                            continue
                        sample_data[sample_name]["percent_areas"].append(
                            percent_area_float
                        )

                        # Process the "Area" information if available
                        if area_idx is not None:
                            area = cols[area_idx]
                            try:
                                area_int = float(area)
                            except ValueError:
                                area_int = ""
                            sample_data[sample_name]["areas"].append(area_int)

                    # Create a list to store the rows for the Excel file
                    rows = []

                    # Add a row for each sample name
                    for sample_name, data in sample_data.items():
                        percent_areas = [
                            round(float(val), 5) for val in data["percent_areas"]
                        ]
                        areas = (
                            [val for val in data["areas"]]
                            if area_idx is not None
                            else []
                        )

                        # Check if the percent_areas list is not empty before adding the row
                        if percent_areas:
                            row = [sample_name] + ["% Area"] + percent_areas
                            rows.append(row)
                            if area_idx is not None:
                                row = [sample_name] + ["Area"] + areas
                                rows.append(row)

                    # Sort the rows by the first column (sample name)
                    rows = sorted(rows, key=lambda row: row[0])

                    # Create a dataframe from the rows
                    df = pd.DataFrame(rows)

                    # Create a list of header labels for the dataframe
                    header = ["Sample Name", "Area type"] + [
                        f"GP{i+1}" for i in range(df.shape[1] - 2)
                    ]
                    df.columns = header

                    # Add the DataFrame to the dictionary with the file path as the key
                    dfs[file_path] = df
    return dfs
