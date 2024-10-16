import csv
from rouge_score import rouge_scorer
import os

def save_to_csv(data, filename="summary_comparison.csv"):
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header row (without the File Name)
        writer.writerow([
            "Model Name", "Original Text", "Summary", 
            "Summary Length", "ROUGE-L Score"
        ])
        
        # Write the data rows (only 5 fields now)
        for row in data:
            if len(row) == 5:  # Ensure that each row contains exactly 5 fields
                writer.writerow([
                    row[0],  # Model Name (e.g., Mistral, Gemma, LLaMA)
                    row[1],  # Original Text
                    row[2],  # Summary
                    row[3],  # Summary Length
                    row[4]   # ROUGE-L Score
                ])
            else:
                print(f"Row has incorrect number of fields: {row}")
    
    print(f"Summary results saved to {file_path}")

# Function to calculate ROUGE-L F1 score
def calculate_rouge_l(reference_summary, generated_summary):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    score = scorer.score(reference_summary, generated_summary)
    return score['rougeL'].fmeasure
