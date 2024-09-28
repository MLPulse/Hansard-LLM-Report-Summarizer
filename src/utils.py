import csv
from rouge_score import rouge_scorer

# Function to save the extracted data into a CSV file
def save_to_csv(data, filename="summary_results.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["File Name", "Original Text", "Mistral 7B Summary", "Gemma 2 9B Summary", "LLaMA 3.1 8B Summary", "Avg Summary Length", "ROUGE-L Mistral 7B", "ROUGE-L Gemma 2 9B", "ROUGE-L LLaMA 3.1 8B"])
        # Write the data
        for row in data:
            writer.writerow(row)

# Function to calculate ROUGE-L F1 score
def calculate_rouge_l(reference_summary, generated_summary):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    score = scorer.score(reference_summary, generated_summary)
    return score['rougeL'].fmeasure
