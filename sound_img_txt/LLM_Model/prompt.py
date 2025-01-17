from langchain.prompts import PromptTemplate

prompt_template_name = PromptTemplate(
    input_variables=["sound","no_of_words"],
    template="""
    You will be given a sound, and your task is to generate {no_of_words} words using that sound. 
    Additionally, provide a simple image description for each word.
    
    Format your response as a Python dictionary where:
    - Keys are words.
    - Values are descriptions of an image that visually represents A simple and clean illustration of [WORD]. The image should show a recognizable character or object related to [WORD] with minimal details, using simple lines and shapes. The background should be plain, with no extra distractions, making it easy to guess the word.

    Example output:
    {{
        "Cook": "A simple, clean, and minimal illustration of a cook. A person wearing a chef’s hat and a white uniform, smiling, on a plain background. No extra details, just a clear and recognizable image.",
        "Book": "A simple and clean illustration of a book. An open book with pages visible, with minimal detail and a plain background to make the word easily recognizable.",
    }}

    Now, generate a dictionary for the sound: {sound}
    """
)
