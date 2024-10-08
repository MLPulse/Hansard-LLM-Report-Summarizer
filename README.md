# Hansard-LLM-Report-Summarizer

## Overview

The Hansard LLM Report Summarizer is a toolkit designed to automate the process of downloading, processing, summarizing, and analyzing Hansard reports from the Canadian House of Commons. It uses state-of-the-art large language models (LLMs) for generating concise summaries of parliamentary discussions.

## Features:
- **Automated Report Download**: Fetch Hansard reports based on specified dates or date ranges.
- **Text Extraction with Vector Embeddings**: Extract relevant content from PDFs using vector embeddings.
- **Summarization with LLMs**: Utilize multiple LLMs, including Mistral 7B, Gemma 2 9B, and LLaMA 3.1 8B.
- **ROUGE-L Evaluation**: Compare generated summaries using ROUGE-L metrics.
- **Result Storage**: Store both intermediate and final outputs in text and CSV formats.

## Directory Structure

```bash
Hansard-LLM-Report-Summarizer/
│
├── data/                      # Contains raw data
│   └── .gitkeep
│
├── output/                    # Directory for output data
│   └── .gitkeep
│
├── src/                       # Source code directory
│   ├── hansard_downloader.py  # Script for downloading Hansard reports
│   ├── main.py                # Main execution script to run the complete workflow
│   ├── summarization.py       # LLM-based summarization script
│   ├── text_processing.py     # Script for text extraction and preprocessing
│   ├── utils.py               # Utility functions used across various modules
│
├── .gitignore                 # Specifies files and folders to ignore in Git
├── README.md                  # Project documentation
└── requirements.txt           # List of required Python dependencies
```



## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Hansard-LLM-Report-Summarizer.git
cd Hansard-LLM-Report-Summarizer   
```
### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
    
## Usage
### 1. Download Hansard Reports

To download Hansard reports for specific dates:
```bash
python src/hansard_downloader.py --date YYYY-MM-DD
```
Alternatively, use the following code:
```bash
from datetime import datetime
download_hansard_reports(datetime(2024, 6, 17), datetime(2024, 6, 19))
```

### 2. Extract and Summarize Reports

To extract content and summarize the downloaded reports:
```bash
python src/main.py
```
Example for using specific functions in code:
```bash
topic = "Carbon Tax"
length = "medium"
pdf_files = get_hansard_pdfs()
for pdf_path in pdf_files:
    result = compare_llm_summaries(pdf_path, topic, length)
```

### 3. Save Results to CSV

To save the generated summaries and ROUGE-L scores into a CSV file:
```bash
python src/main.py --save-results
```

### 4. Evaluate Summaries

To compare summaries with a reference summary and calculate ROUGE-L F1 score:
```bash
reference_summary = """Your reference summary here"""
compare_llm_summaries_and_save_results(pdf_path, topic, length, reference_summary)
```
