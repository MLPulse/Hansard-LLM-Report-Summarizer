import pdfplumber
import nltk
from nltk.tokenize import sent_tokenize
from transformers import T5TokenizerFast
nltk.download('punkt')

# Function to extract text from a PDF
def extract_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()  # Extract text per page
            if page_text:
                full_text += page_text
            else:
                print(f"Warning: Page {page.page_number} is empty or could not be read")
        return full_text

# Function to split text into sentences
def split_text_into_sentences(text):
    return sent_tokenize(text)

# Function to group sentences into chunks based on token length
def group_sentences_into_chunks(sentences, max_tokens=4096):
    tokenizer = T5TokenizerFast.from_pretrained("t5-base")
    
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(tokenizer.encode(sentence))
        if current_length + sentence_length > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks
