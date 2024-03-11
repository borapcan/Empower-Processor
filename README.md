# File Processing App

## Description
The File Processing App is a Python application designed to streamline the processing of text files. It provides a user-friendly interface for selecting a directory containing text files, processing them based on user-defined options, and generating statistical analyses and visualizations.

## Features
- **Select Directory**: Allows users to choose a directory containing text files to be processed.
- **Export Area**: Option to export specified areas of the text files.
- **Generate Statistics**: Option to generate statistical analyses of the text files.
- **Create Box Plots**: Option to create box plots for visual analysis.
- **Success and Error Alerts**: Displays success or error messages based on file processing outcomes.

## Usage
1. **Select Directory**: Click the "Choose Directory" button to select a directory containing text files.
2. **Options**:
   - Toggle the "Export Area" checkbox to export specified areas of the text files.
   - Toggle the "Stats" checkbox to generate statistical analyses.
   - Toggle the "Box plot" checkbox to create box plots for visual analysis.
3. **Start Processing**: Click the "Start Processing" button to initiate the file processing.
4. **Feedback**: Success or error alerts will be displayed based on the processing outcome.

## Installation
1. Clone the repository: `git clone https://github.com/your/repository.git`
2. Navigate to the project directory: `cd Empower-Processor`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `app.py`

## Running via Console
To run the program via the console, you can use the `export.py` file. Here's how you can do it (Currently does not support box plots or statistics only file conversion):

```bash
python export.py
```

## Technologies Used
- **Python**: Backend logic and file processing.
- **Eel**: Python library for creating simple Electron-like desktop apps with HTML, CSS, and JavaScript.
- **Bootstrap**: Frontend framework for styling the user interface.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests with any improvements, bug fixes, or additional features.

## License
This project is licensed under the [MIT License](LICENSE).
