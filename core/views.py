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
import csv
from collections import Counter, defaultdict

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

            # emoji analysis
            df["Message"].fillna("", inplace=True)
            emoji_counters = defaultdict(Counter)
            emojis_list = map(lambda x: ''.join(x.split()), emoji.EMOJI_DATA.keys())
            r = re.compile('|'.join(re.escape(p) for p in emojis_list))
            users_to_count = df["Sender"].unique()
            for idx, row in df.iterrows():
                sender = row["Sender"]
                if sender in users_to_count:
                    emojis_found = r.findall(str(row["Message"]))
                    emoji_counters[sender].update(emojis_found)
            combined_emoji_ctr = Counter()
            for user_ctr in emoji_counters.values():
                combined_emoji_ctr.update(user_ctr)
            combined_df = pd.DataFrame(combined_emoji_ctr.items(), columns=['Emoji', 'Combined_Count'])

            # combining all emojie for each user
            user_dfs = []
            for user, user_ctr in emoji_counters.items():
                user_df = pd.DataFrame(user_ctr.items(), columns=['Emoji', f'{user}'])
                user_dfs.append(user_df)
            result_df = combined_df
            for user_df in user_dfs:
                result_df = pd.merge(result_df, user_df, on='Emoji', how='outer')
            total_emojis_per_user = result_df.sum(axis=0)
            total_user_used=total_emojis_per_user.count()
            # extracted just user and emoji removed all emoji and total emojies
            new_ndf=total_emojis_per_user.tail(total_user_used-2)

            # drawing graph
            users = new_ndf.index.tolist()
            emoji_counts = new_ndf.values.tolist()
            sorted_data = sorted(zip(users, emoji_counts), key=lambda x: x[1],reverse=True)
            sorted_users = [x[0] for x in sorted_data]
            sorted_counts = [x[1] for x in sorted_data]
            plt.figure(figsize=(12, 12))
            sns.barplot(x=sorted_users, y=sorted_counts,palette="rocket")
            plt.xlabel('Users')
            plt.ylabel('Emoji Counts')
            plt.title('Emoji Usage by Users')
            for user, count in zip(sorted_users, sorted_counts):
                plt.text(user, count, str(int(count)), fontsize=8, ha='center', va='bottom')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.savefig('static/assets/temp/emoji.png')

                # active hours
            try:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
                df = df.dropna(subset=['Timestamp'])
            except ValueError:
                print("Timestamp format does not match expected format.")
            df['Hour'] = df['Timestamp'].dt.hour
            hourly_activity = df.groupby('Hour').size()
            plt.figure(figsize=(12, 12))
            hourly_activity.plot(kind='bar', color='skyblue')
            plt.title('Overall Hourly Activity Pattern')
            plt.xlabel('Hour of the Day')
            plt.ylabel('Total Number of Messages')
            plt.xticks(rotation=0)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/assets/temp/active.png')

            try:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
                df = df.dropna(subset=['Timestamp'])
            except ValueError:
                print("Timestamp format does not match expected format.")
            df['Hour'] = df['Timestamp'].dt.hour
            sender_hourly_activity = df.groupby(['Sender', 'Hour']).size()
            most_active_hours = sender_hourly_activity.groupby(level=0).idxmax().apply(lambda x: x[1])
            custom_palette = sns.color_palette("husl", len(most_active_hours))
            plt.figure(figsize=(12, 12))
            sns.barplot(data=most_active_hours, palette=custom_palette)
            plt.title('Most Active Hour for Each Sender')
            plt.xlabel('Sender')
            plt.ylabel('Most Active Hour')
            plt.xticks(rotation=90)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            for sender, hour in zip(most_active_hours.index, most_active_hours.values):
                plt.text(sender, hour, str(int(hour)), fontsize=8, ha='center', va='bottom')
            plt.tight_layout()
            plt.savefig('static/assets/temp/usertime.png')
            

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

    # emoji used
    emoji_counters = defaultdict(Counter)
    emojis_list = map(lambda x: ''.join(x.split()), emoji.EMOJI_DATA.keys())
    r = re.compile('|'.join(re.escape(p) for p in emojis_list))
    users_to_count = df["Sender"].unique()
    for idx, row in df.iterrows():
        sender = row["Sender"]
        if sender in users_to_count:
            emojis_found = r.findall(str(row["Message"]))
            emoji_counters[sender].update(emojis_found)
    combined_emoj_ctr = Counter()
    for user_ctr in emoji_counters.values():
        combined_emoj_ctr.update(user_ctr)
        
    for user_ctr in emoji_counters.values():
        combined_emoj_ctr.update(user_ctr)
    emoji_data = combined_emoj_ctr.most_common() 


    context={
        'contactMod':contactMod,
        'top_user':top_user,
        'emoji_data':emoji_data
    }
    return render(request, "core/analysis.html",context)