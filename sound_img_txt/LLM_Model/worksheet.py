from langchain.prompts import PromptTemplate

prompt_template_worksheet = PromptTemplate(
    input_variables=["topic", "no_of_sentences"],
    template="""
    Generate an English vocabulary worksheet on the topic: "{topic}". 

    **Instructions:**  
    - Provide {no_of_sentences} sentences.  
    - Each sentence should include a key vocabulary word in **bold**.  
    - Ensure the words belong to different parts of speech (noun, verb, adjective).  
    - Use simple yet meaningful contexts to illustrate the words.  

    **Definitions:**  
    - Below the sentences, provide definitions corresponding to each bolded word.  
    - Each definition should specify the word’s part of speech (noun, verb, adjective).  

    **Output Format:**  
    The output should be structured as follows:  

    ---
    
    **1**  
    **Read the sentences. Then choose a word from each sentence to match the definition. Write in the dictionary form of the word.**  

    - The scientist conducted **research** to find a cure for the disease.  
    - She enjoys **reading** novels in her free time.  
    - The manager will **approve** the project after reviewing it.  
    - His **performance** in the play was outstanding.  
    - The author wrote a **fictional** story about a magical world.  
    - The judge made a **fair** decision based on the evidence.  

    **Fill in the blanks:**  

    1) **___________** (noun) ➤ a detailed study to discover new information  
    2) **___________** (verb) ➤ the action of looking at written words and understanding them  
    3) **___________** (verb) ➤ to officially accept or allow something  
    4) **___________** (noun) ➤ the way someone acts, especially in a show or competition  
    5) **___________** (adjective) ➤ something made up, not real  
    6) **___________** (adjective) ➤ treating people equally and justly  

    ---

    Now, generate a worksheet for the topic: "{topic}" with {no_of_sentences} sentences and definitions.  
    """
)

