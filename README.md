# Hansard-LLM-Report-Summarizer

## Overview

This repository contains scripts for downloading Hansard reports from the Canadian House of Commons, extracting relevant information, and summarizing it using various large language models (LLMs). It also includes functionality to compare summaries and evaluate them using the ROUGE-L metric.

### Key Features:
- Download Hansard reports for specific dates or date ranges.
- Extract relevant content from PDFs using vector embeddings.
- Summarize the extracted content with multiple LLMs, including **Mistral 7B**, **Gemma 2 9B**, and **LLaMA 3.1 8B**.
- Calculate the **ROUGE-L** score to compare generated summaries.
- Save extracted text and summaries in text files, and generate CSV reports.


## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/Hansard-LLM-Report-Summarizer.git
cd Hansard-LLM-Report-Summarizer   
```
### 2. Install the required libraries using the requirements.txt file:
```bash
pip install -r requirements.txt
```
Required Libraries:

- langchain
- ollama
- PyPDF2
- pdfplumber
- sentence-transformers
- nltk
- torch
- tqdm
- rouge_score
    
## Usage
### 1. Download Hansard Reports

To download Hansard reports for specific dates, use the download_hansard_reports function in the hansard_downloader.py script.
```bash
python src/hansard_downloader.py
```
Example:
```bash
from datetime import datetime
download_hansard_reports(datetime(2024, 6, 17), datetime(2024, 6, 19))
```

### 2. Extract and Summarize Reports

Once the Hansard reports are downloaded, use the compare_llm_summaries function from the summarization.py script to extract relevant content based on a specific topic and generate summaries using different LLMs
```bash
python src/main.py
```
Example:
```bash
topic = "Carbon Tax"
length = "medium"
pdf_files = get_hansard_pdfs()
for pdf_path in pdf_files:
    result = compare_llm_summaries(pdf_path, topic, length)
```

### 3. Save Results to CSV

Use the function save_to_csv in the utils.py to save the generated summaries and ROUGE-L scores into a CSV file.
```bash
python src/main.py --save-results
```

### 4. Evaluate Summaries

To compare summaries with a reference summary, the script also provides functionality to calculate the ROUGE-L F1 score for each model.
Example:
```bash
reference_summary = """Your reference summary here"""
compare_llm_summaries_and_save_results(pdf_path, topic, length, reference_summary)
```
### File Structure:

- `hansard_downloader.py`: Handles the downloading of Hansard reports.
- `text_processing.py`: Extracts text, tokenizes sentences, and creates vector embeddings.
- `summarization.py`: Contains functions for summarizing text using multiple LLMs.
- `utils.py`: Utility functions like saving results to CSV and calculating ROUGE-L scores.
- `main.py`: Main script that integrates all functionalities.
