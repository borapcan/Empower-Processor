import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math


def generate_sample_list_excel(df):

    stats = []

    for index, row in df.iterrows():
        sample_name = row["Sample Name"]

        # Skip empty rows
        if pd.isna(sample_name) or not sample_name.strip():
            continue

        # Split the sample name
        parts = sample_name.split("_")

        # Process 'STAND' identifiers
        if parts[0].lower().startswith("stand"):
            stats.append(parts[0] + "_" + parts[1])
        else:
            stats.append(f"{parts[0]}")

    # Sort the list and remove duplicates
    stats = sorted(set(stats))

    return stats


def generate_combined_stats_excel(all_identifiers, df):

    df = df[df["Area type"] == "% Area"]

    # Initialize an empty DataFrame for the combined statistics
    combined_stats_df = pd.DataFrame()

    # Loop through each identifier in the list
    for identifier in all_identifiers:

        # Select rows that match the current identifier
        subset_df = df[df["Sample Name"].str.startswith(identifier)]

        # Convert columns to numeric
        subset_df = subset_df.apply(pd.to_numeric, errors="coerce")

        # Calculate AVG, SD, and CV for each column starting with 'GP'
        gp_columns = subset_df.filter(regex="^GP", axis=1)
        avg_values = gp_columns.mean(axis=0, skipna=True)
        sd_values = gp_columns.std(axis=0, skipna=True)
        cv_values = (
            sd_values / avg_values
        ) * 100  # Calculate coefficient of variation (%)

        # Create a DataFrame for the statistics
        stats_data = {"Sample": identifier, "Statistic": ["AVG", "SD", "CV (%)"]}

        for col in gp_columns.columns:
            stats_data[col] = [avg_values[col], sd_values[col], cv_values[col]]

        stats_df = pd.DataFrame(stats_data)

        # Append the statistics for the current identifier to the combined DataFrame
        combined_stats_df = pd.concat([combined_stats_df, stats_df], ignore_index=True)

    return combined_stats_df


def generate_box_plot(df):
    # Filter DataFrame to include only rows where 'Area type' is '% Area'
    filtered_df = df[df["Area type"] == "% Area"]

    # Set Seaborn style with no grid lines
    sns.set_style("white")

    print(filtered_df)

    # Get columns starting with 'GP'
    gp_columns = [col for col in filtered_df.columns if col.startswith("GP")]

    # Calculate grid dimensions
    num_cols = len(gp_columns)
    num_rows = (num_cols + 5) // 6  # Ceiling division

    # Create subplots
    fig, axes = plt.subplots(num_rows, 6, figsize=(20, num_rows * 4))

    # Flatten axes if needed
    if num_rows == 1:
        axes = axes.reshape(1, -1)

    # Plot rotated boxplots
    for i, col in enumerate(gp_columns):
        row_idx = i // 6
        col_idx = i % 6
        sns.boxplot(y=filtered_df[col], ax=axes[row_idx, col_idx], orient="v")
        axes[row_idx, col_idx].set_title(col)

    # Remove empty subplots
    for i in range(num_cols, num_rows * 6):
        row_idx = i // 6
        col_idx = i % 6
        fig.delaxes(axes[row_idx, col_idx])

    plt.tight_layout()
    return fig
