import PyPDF2
from sentence_transformers import SentenceTransformer, util
from transformers import T5TokenizerFast
import torch

# Function to create embeddings for each chunk of the PDF text
def create_embeddings(text_chunks, model):
    non_empty_chunks = [chunk for chunk in text_chunks if chunk.strip()]
    
    if not non_empty_chunks:
        print("No valid text chunks for embedding.")
        return None
    
    embeddings = model.encode(non_empty_chunks, convert_to_tensor=True)
    return embeddings

# Function to search for the topic using vector embeddings
def find_relevant_text_by_embedding(topic, text_chunks, chunk_embeddings, model, top_k=5):
    if chunk_embeddings is None:
        return None
    topic_embedding = model.encode(topic, convert_to_tensor=True)
    similarities = util.cos_sim(topic_embedding, chunk_embeddings)[0]
    
    # Get top_k most relevant indices
    top_k_indices = torch.topk(similarities, k=top_k).indices
    relevant_chunks = [text_chunks[idx] for idx in top_k_indices]
    
    if not relevant_chunks:
        print("No relevant chunks found based on the topic.")
        return None
    return ' '.join(relevant_chunks)

# Function to truncate text to a maximum number of tokens (e.g., 4096 for large LLMs)
def truncate_text(text, max_tokens=4096):
    tokenizer = T5TokenizerFast.from_pretrained("t5-base")
    tokens = tokenizer.encode(text)
    
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        text = tokenizer.decode(tokens)
    return text

def extract_relevant_text(pdf_path, topic, use_embeddings=False, top_k=5, max_tokens=4096):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text_chunks = []
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text.strip():
                text_chunks.append(text)
        
        if not text_chunks:
            print(f"No text found in {pdf_path}.")
            return None
        
        # Use embedding-based search if specified
        if use_embeddings:
            model = SentenceTransformer('all-MiniLM-L6-v2')  # Example model
            chunk_embeddings = create_embeddings(text_chunks, model)
            if chunk_embeddings is None:
                print(f"Failed to create embeddings for {pdf_path}.")
                return None
            
            relevant_text = find_relevant_text_by_embedding(topic, text_chunks, chunk_embeddings, model, top_k)
            if relevant_text is None:
                print(f"No relevant chunks found for topic '{topic}' in {pdf_path}.")
                return None
        else:
            # Fallback to simple keyword-based extraction
            relevant_text = ' '.join([chunk for chunk in text_chunks if topic.lower() in chunk.lower()])
        
        if relevant_text:
            print(f"Relevant text found for topic '{topic}' in {pdf_path}.")
            # Truncate the text if necessary
            truncated_text = truncate_text(relevant_text, max_tokens)
            return truncated_text
        else:
            print(f"No relevant text found for the topic '{topic}' in {pdf_path}.")
            return None

