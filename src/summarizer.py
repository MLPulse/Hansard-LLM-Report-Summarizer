from langchain.prompts import PromptTemplate
from langchain.llms import Ollama

# Function to generate a summary using a specific model
def summarize_with_model(model_name, text, length, topic, prompt_template):    
    # Initialize the LLM
    llm = Ollama(model=model_name)
    
    # Prepare input prompt
    input_text = prompt_template.format(topic=topic, length=length, text=text)
    
    # Generate summary
    try:
        summary = llm(input_text)
        return summary
    except Exception as e:
        print(f"Error generating summary with {model_name}: {e}")
        return None

# Main function to summarize text using multiple models and compare results
def summarize_text(relevant_text, topic, length='medium'):
    # Define prompt template for the summarization
    prompt_template = PromptTemplate(
        input_variables=["topic", "length", "text"],
        template="""
Summarize the following text with a focus on discussions, debates, and decisions related to '{topic}', 
highlighting key arguments, impacts, outcomes, and next steps regarding '{topic}' in a {length} paragraph. 
Please maintain a neutral tone throughout the summary.

Exclude any procedural details, personal anecdotes, or content unrelated to '{topic}' to maintain focus on relevant material.

Text:
{text}

Summary:
"""
    )
    
    # Summarize with different models
    models = ["mistral:7b", "gemma2:9b", "llama3.1:8b"]
    comparison = {}
    
    for model in models:
        summary = summarize_with_model(model, relevant_text, length, topic, prompt_template)
        if summary:
            comparison[model] = summary
    
    return comparison
