from summarization import summarize_with_model, find_relevant_text_by_embedding, create_embeddings, truncate_text
from text_processing import extract_pdf_text, split_text_into_sentences, group_sentences_into_chunks
from utils import save_to_csv, calculate_rouge_l
from sentence_transformers import SentenceTransformer
import os

# Function to get all PDF files with the prefix "Hansard" in the current directory
def get_hansard_pdfs():
    return [file for file in os.listdir() if file.startswith("Hansard") and file.endswith(".pdf")]

# Function to compare summaries and save relevant text
def compare_llm_summaries_and_save_results(pdf_path, topic, length, reference_summary, top_k=5):
    full_text = extract_pdf_text(pdf_path)
    sentences = split_text_into_sentences(full_text)
    text_chunks = group_sentences_into_chunks(sentences, max_tokens=4096)

    # Initialize embedding model once
    embedding_model = SentenceTransformer('all-mpnet-base-v2')
    chunk_embeddings = create_embeddings(text_chunks, embedding_model)
    relevant_text = find_relevant_text_by_embedding(topic, text_chunks, chunk_embeddings, embedding_model, top_k=top_k)

    relevant_text = truncate_text(relevant_text, max_tokens=3596)

    # Prepare prompt template
    prompt_template = """
        Summarize the following text with a focus on discussions, debates, and decisions related to '{topic}', 
        highlighting key arguments, impacts, outcomes, and next steps regarding '{topic}' in a {length} paragraph. 
        Please maintain a neutral tone throughout the summary.

        Text:
        {text}

        Summary:
    """

    # Summarize with different models
    mistral_summary = summarize_with_model("mistral:7b", relevant_text, length, topic, prompt_template)
    gemma_summary = summarize_with_model("gemma2:9b", relevant_text, length, topic, prompt_template)
    llama_summary = summarize_with_model("llama3.1:8b", relevant_text, length, topic, prompt_template)

    # Calculate ROUGE-L scores for each model's summary
    rouge_l_mistral = calculate_rouge_l(reference_summary, mistral_summary)
    rouge_l_gemma = calculate_rouge_l(reference_summary, gemma_summary)
    rouge_l_llama = calculate_rouge_l(reference_summary, llama_summary)

    # Calculate average summary length
    avg_length = (len(mistral_summary.split()) + len(gemma_summary.split()) + len(llama_summary.split())) / 3

    # Collect data for CSV
    data = {
        "File Name": pdf_path,
        "Original Text": relevant_text,
        "Mistral 7B Summary": mistral_summary,
        "Gemma 2 9B Summary": gemma_summary,
        "LLaMA 3.1 8B Summary": llama_summary,
        "Avg Summary Length": avg_length,
        "ROUGE-L Mistral 7B": rouge_l_mistral,
        "ROUGE-L Gemma 2 9B": rouge_l_gemma,
        "ROUGE-L LLaMA 3.1 8B": rouge_l_llama
    }
    return data

if __name__ == "__main__":
    topic = "Carbon Tax"
    length = "medium"
    reference_summary = """The debates surrounding the Carbon Tax in the Canadian House of Commons..."""  # Add full reference summary here
    pdf_files = get_hansard_pdfs()

    results = []
    for pdf_path in pdf_files:
        result = compare_llm_summaries_and_save_results(pdf_path, topic, length, reference_summary)
        results.append(list(result.values()))

    # Save all results into a CSV file
    save_to_csv(results)
