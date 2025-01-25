from sumy.parsers.plaintext import PlaintextParser  # Import the parser to convert text into a document format
from sumy.nlp.tokenizers import Tokenizer  # Import the tokenizer for processing the text
from sumy.summarizers.lsa import LsaSummarizer  # Import the LSA (Latent Semantic Analysis) summarizer

def summarize_text(input_text: str, sentence_count: int = 25) -> str:
    """Summarize the given text using LSA summarizer."""
    
    # Convert the input text into a document that can be processed by the summarizer
    parser = PlaintextParser.from_string(input_text, Tokenizer("english"))
    
    # Initialize the LSA summarizer
    summarizer = LsaSummarizer()

    # Use the summarizer to generate the summary with the specified number of sentences
    summary = summarizer(parser.document, sentences_count=sentence_count)

    # Join the sentences of the summary into a single string and return it
    return "\n".join([str(sentence) for sentence in summary])  # Convert each sentence to string and join them
