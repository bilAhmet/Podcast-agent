from google.adk.tools import FunctionTool


def count_words(text: str) -> int:
    """
    Counts the number of words in a given text.
    The input is the text to be counted.
    """
    return len(text.split())


word_counter_tool = FunctionTool(count_words)
