from src.data_downloader import download_hansard_report
from src.text_extractor import extract_relevant_text
from src.summarizer import summarize_text

import argparse

def main():
    parser = argparse.ArgumentParser(description="Download and summarize Hansard reports.")
    parser.add_argument('--date', type=str, required=True, help='Date of the Hansard report in YYYY-MM-DD format.')
    parser.add_argument('--topic', type=str, required=True, help='Topic of interest for summary.')
    parser.add_argument('--summary_length', type=str, choices=['short', 'medium', 'long'], default='medium', help='Length of the summary.')
    
    args = parser.parse_args()
    report_date = args.date
    topic = args.topic
    summary_length = args.summary_length

    # Step 1: Download the Hansard report
    pdf_file = download_hansard_report(report_date)

    if pdf_file:
        # Step 2: Extract relevant text based on topic
        relevant_text = extract_relevant_text(pdf_file, topic)

        if relevant_text:
            # Step 3: Summarize the text
            summary = summarize_text(relevant_text, topic, summary_length)
            print(summary)
        else:
            print("No relevant text found for the given topic.")
    else:
        print(f"Could not download the Hansard report for {report_date}.")

if __name__ == "__main__":
    main()
