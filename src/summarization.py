from langchain.llms import Ollama
from sentence_transformers import SentenceTransformer, util
import torch
from transformers import T5TokenizerFast
from langchain.prompts import PromptTemplate

# Function to create vector embeddings for each chunk of the PDF text
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
    # Get top_k indices
    top_k_indices = torch.topk(similarities, k=top_k).indices
    relevant_chunks = [text_chunks[idx] for idx in top_k_indices]
    if not relevant_chunks:
        print("No relevant chunks found based on the topic")
        return None
    return ' '.join(relevant_chunks)

# Function to truncate text to a maximum number of tokens
def truncate_text(text, max_tokens=4096):
    tokenizer = T5TokenizerFast.from_pretrained("t5-base")
    tokens = tokenizer.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        text = tokenizer.decode(tokens)
    return text

# Function to call an LLM for summarization
def summarize_with_model(model_name, text, length, topic, prompt_template):
    try:
        llm = Ollama(model=model_name)
        prompt = prompt_template.format(topic=topic, length=length, text=text)
        summary = llm.invoke(prompt)
        return summary
    except Exception as e:
        print(f"Error with model {model_name}: {e}")
        return f"Failed to summarize with {model_name}"
