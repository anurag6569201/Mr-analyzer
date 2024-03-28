from django.shortcuts import render,redirect
from .forms import FileUploadForm

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
            form.save()
            contact_method = request.POST.get('contact_method')
            uploaded_file_path = form.instance.file.path
            with open(uploaded_file_path, 'r', encoding='utf-8') as txt_file, open("temp/data.csv", 'w', newline='', encoding='utf-8') as csv_file:
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

            df = pd.read_csv('temp/data.csv')
            sender_counts = df.groupby("Sender")["Message"].count().sort_values(ascending=False)
            custom_palette = sns.color_palette("husl", len(sender_counts))

            plt.figure(figsize=(12, 12))
            sns.barplot(x=df.index, y='Sender', data=df, palette=custom_palette,errorbar=None)
            plt.xlabel('Sender')
            plt.ylabel('Message Count')
            plt.title('Message Count by Sender')
            plt.tight_layout()
            plt.savefig('temp/graph.png')
            return redirect('core:analysis')
    else:
        form = FileUploadForm()
    return render(request, "core/index.html", {'form': form})

def analysis(request):
    return render(request, "core/analysis.html")