Of course\! Here is the `README.md` file translated into English based on the previously provided files.

-----

# Grading Automation Tools

This project provides a set of Python scripts to automate and standardize the process of creating grading reports for student assignments. The solution is divided into two main tools:

1.  **Report Generator (`report_tool.py`)**: Creates a folder and file structure for grading in Markdown (`.md`) for each student from a customizable template.
2.  **PDF Converter (`convert_to_pdf.py`)**: Converts the finalized Markdown grading reports to PDF, preserving formatting, tables, and mathematical formulas in LaTeX.

## ✨ Features

  - **Batch Generation**: Create the grading structure for all students in a class at once.
  - **Standardized Template**: Ensure consistency across all grades by using a template file (`template.md`).
  - **Customizable**: Easily modify the `template.md` to adapt to different evaluation criteria.
  - **High-Quality PDF Conversion**: Generate professional-looking PDFs by rendering Markdown with a style similar to GitHub.
  - **LaTeX Support**: Write complex mathematical formulas in your reports using LaTeX syntax, which will be correctly rendered in the final PDF.

## 📂 Expected Directory Structure

For the scripts to work correctly, organize your folders as follows:

```
your_project/
├── submissions/             <-- Folder with each student's directory
│   ├── Example_1/
│   ├── Example_2/
│   └── Example_3/
├── report_tool.py           <-- Generator script
├── convert_to_pdf.py        <-- Converter script
└── template.md              <-- Report template
```

  - The main directory (e.g., `submissions/`) should contain a subfolder for each student. The name of the subfolder will be used as the student's name in the report.

## 🚀 Installation and Setup

### Prerequisites

  - Python 3.7 or higher.

### Installation Steps

1.  **Clone or download the files** to a directory on your computer.

2.  **Create a virtual environment (recommended)**:

    ```bash
    python -m venv venv
    ```

      - On Windows, activate with: `.\venv\Scripts\activate`
      - On macOS/Linux, activate with: `source venv/bin/activate`

3.  **Install the necessary dependencies**:
    The scripts use a few Python libraries to render Markdown and generate the PDF. Install them with the following command:

    ```bash
    pip install "markdown-it-py<3.0.0" "mdit-py-plugins" pyppeteer
    ```

    > **Note**: The first time the `convert_to_pdf.py` script is run, the `pyppeteer` library will automatically download a version of Chromium (a headless browser) to render the page. This may take a few minutes.

## 📝 Workflow and Usage

### Step 1: Generate the Grading Files

Run the `report_tool.py` script to create the `.md` files for each student.

**Basic Usage:**
Provide the activity name as the main argument. The script will look for student folders in the current directory (`.`).

```bash
# Example for an activity named "Lab01"
python report_tool.py Lab01
```

**Advanced Usage with Options:**
You can specify the student directory, the grader's name, and the report title.

```bash
python report_tool.py "Lab02_Circuits" -o "./submissions" -g "Prof. Ada Lovelace" --activity-title "Laboratory 02 Report"
```

After running, the following structure will be created inside each student's folder:

```
submissions/
└── John_Smith/
    └── John_Smith_Lab01_correction/
        ├── John_Smith_Lab01_correction.md  <-- The report to be filled out
        └── src/                            <-- Optional folder for corrected code
```

### Step 2: Fill in the Reports

Open each generated `.md` file and fill in the grades, comments, and feedback for each student.

### Step 3: Convert the Reports to PDF

Once the grades are finalized, run the `convert_to_pdf.py` script to generate the PDFs.

**Usage:**
Provide the directory where the `.md` reports are located. The script will recursively search for all `.md` files and convert them.

```bash
# Converts all reports inside the 'submissions' folder
python convert_to_pdf.py ./submissions
```

The script will create a `.pdf` file with the same name and in the same location as the original `.md` file.

## 🔧 Component Details

### `report_tool.py`

  - **Purpose**: To automate the creation of the grading structure.
  - **Command-Line Arguments**:
      - `activity_name` (required): A short name for the activity, used for naming files.
      - `-o, --output-dir`: The directory where the student folders are located (default: `.`).
      - `-g, --grader`: The name of the grader to be inserted into the report.
      - `-t, --activity-title`: The full title of the activity for the header. If omitted, it uses `activity_name`.
      - `--template`: The path to the template file (default: `template.md`).

### `convert_to_pdf.py`

  - **Purpose**: To convert Markdown files to PDF.
  - **Technology**: Uses `pyppeteer` to control a headless browser that "prints" the HTML version of the Markdown to a PDF file.
  - **Command-Line Arguments**:
      - `base_dir` (optional): The base directory to recursively search for `.md` files (default: `.`).

### `template.md`

  - **Purpose**: To serve as a model for all grading reports.
  - **Syntax**: Uses the `${variable}` syntax from Python's `string.Template` for fields that will be replaced by `report_tool.py`, such as `${student_name}`, `${activity_title}`, etc..
  - **Customization**: Feel free to edit this file, changing the evaluation criteria, weights, text, and the calculation formula to meet your needs. Just keep the placeholders that the script uses.
