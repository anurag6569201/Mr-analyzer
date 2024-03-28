from django.shortcuts import render,redirect
from core.forms import FileUploadForm
from core.models import UploadedFile
from django.shortcuts import get_object_or_404

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import emoji
from collections import Counter
import csv


def index(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            choosen_option = request.POST.get('contact_method') 
            file_instance = form.save(commit=False)
            file_instance.choosenoption = choosen_option 
            file_instance.save()
            form.save()
            uploaded_file_path = form.instance.file.path
            with open(uploaded_file_path, 'r', encoding='utf-8') as txt_file, open("static/assets/temp/data.csv", 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Timestamp', 'Sender', 'Message'])

                timestamp = ""
                sender = ""
                message = ""

                for line in txt_file:
                    parts = line.split(' - ', 1)
                    if len(parts) == 2:
                        timestamp, content = parts
                        sender_end_index = content.find(': ')
                        if sender_end_index != -1:
                            sender = content[:sender_end_index]
                            message = content[sender_end_index + 2:].strip()
                        else:
                            sender = content.strip()
                            message = ""
                    else:
                        message += line.strip()

                    if timestamp and sender and message:
                        csv_writer.writerow([timestamp, sender, message])
                        timestamp = sender = message = ""
                
                if timestamp and sender and message:
                    csv_writer.writerow([timestamp, sender, message])

            df = pd.read_csv('static/assets/temp/data.csv')
            # time spends on chats
            df.dropna(subset=['Sender', 'Message'], inplace=True)
            messages_by_sender = df.groupby('Sender')['Message'].apply(lambda x: ' '.join(x)).reset_index()
            messages_by_sender['Total Characters'] = messages_by_sender['Message'].apply(len)
            messages_by_sender['time'] = messages_by_sender['Total Characters'] / 200
            result = messages_by_sender[['Sender', 'time']]
            result = result.sort_values(by='time', ascending=False)
            custom_palette = sns.color_palette("husl", len(result))
            plt.figure(figsize=(12, 12))
            sns.pointplot(x='time', y='Sender', data=result, palette=custom_palette,errorbar=None)
            plt.xlabel('Time in Minutes')
            plt.ylabel('Senders')
            plt.title('Time insights of all users in chatting')
            labels = [f"{sender}: {time} mins" for sender, time in zip(result['Sender'].values, result['time'].values)]
            plt.legend(title='Time (mins)', labels=labels)
            plt.tight_layout()
            plt.savefig('static/assets/temp/time.png')

            # top messages
            message_counts = df.groupby("Sender")["Message"].count().sort_values(ascending=False)
            message_counts = message_counts.reset_index()
            custom_palette = sns.color_palette("husl", len(message_counts))

            plt.figure(figsize=(12, 12))
            sns.barplot(x='Message', y='Sender', data=message_counts, palette=custom_palette,errorbar=None)
            plt.xlabel('Message Counts')
            plt.ylabel('Senders')
            plt.title('Messages insights of all users')
            plt.legend(title='Message Counts', labels=message_counts['Message'].values)
            plt.tight_layout()
            plt.savefig('static/assets/temp/graph.png')
            return redirect('core:analysis')
    else:
        form = FileUploadForm()
    return render(request, "core/index.html", {'form': form})

def analysis(request):
    contactMod=UploadedFile.objects.get()
    df = pd.read_csv('static/assets/temp/data.csv')
    message_counts = df.groupby("Sender")["Message"].count().sort_values(ascending=False)
    message_counts = message_counts.reset_index()

    # top user name
    obj=message_counts.head(1).Sender
    ob=np.array(obj)
    top_user=ob[0]

    # time spends on chat
    
    context={
        'contactMod':contactMod,
        'top_user':top_user,
    }
    return render(request, "core/analysis.html",context)