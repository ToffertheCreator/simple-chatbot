from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def summarize_text(input_text: str, sentence_count: int = 25) -> str:
    """Summarize the given text using LSA summarizer."""
    parser = PlaintextParser.from_string(input_text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=sentence_count)
    return "\n".join([str(sentence) for sentence in summary])
