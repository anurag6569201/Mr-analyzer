from django.shortcuts import render
from sound_img_txt.LLM_Model.model import produce_words
from sound_img_txt.LLM_Model.prompt import prompt_template_name
from sound_img_txt.LLM_Model.dale import get_images

def index(request):
    data = 0
    if request.method == "POST":
        data = 1
        middle_chars = ['a', 'c', 'e', 'i', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'x', 'z']
        bottom_chars = ['g', 'j', 'p', 'q', 'y']
        upper_chars = ['b', 'd', 'f', 'h', 'k', 'l', 't']

        number_of_words_to_produce = int(request.POST.get('number_of_words', 2))
        sound_to_use = request.POST.get('sound_to_use', "ing")
        print(number_of_words_to_produce)
        
        llm_words_and_prompts = produce_words(prompt_template_name, sound_to_use, number_of_words_to_produce)
        image_urls_data = get_images(llm_words_and_prompts)

        main_data = []
        for word, url in image_urls_data:
            final_data = []
            char_list = []
            for chars in word.strip('"'):
                if chars in middle_chars:
                    char_list.append('01')
                elif chars in bottom_chars:
                    char_list.append('02')
                else:
                    char_list.append('03')
            final_data.append(word.strip('"'))
            final_data.append(url)
            main_data.append(final_data)

        context = {
            'data': data,
            'main_data': main_data,
            'middle_chars': middle_chars,
            'bottom_chars': bottom_chars,
            'upper_chars': upper_chars,
            'word': word,
            'sound': sound_to_use,
        }
    else:
        context = {
            'data': data,
        }
    return render(request, 'sound_img_txt/app/index.html', context)
