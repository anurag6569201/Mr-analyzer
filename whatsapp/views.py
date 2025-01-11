from django.shortcuts import render,redirect
from whatsapp.forms import FileUploadForm
from whatsapp.models import UploadedFile
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

import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt
# def response_to_whatsapp(request):
#     pass
def whatsapp(request):
    if request.method == 'POST':
        # getting the form
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():

            # choosing option it can be whatsapp insta or phone
            choosen_option = request.POST.get('contact_method') 
            file_instance = form.save(commit=False)
            file_instance.choosenoption = choosen_option 
            file_instance.save()

            # after choosing saving it to the data base
            form.save()
            # getting the path of the uploaded file for data analysis
            uploaded_file_path = form.instance.file.path 

            if choosen_option=="whatsapp":
                initializing(uploaded_file_path)
                df = pd.read_csv('whatsapp/static/whatsapp/temp/data.csv')
                timepng(df)
            elif choosen_option=="instagram":
                Instainitializing(uploaded_file_path)
                df = pd.read_csv('whatsapp/static/whatsapp/temp/Idata.csv')
                
            return redirect('whatsapp:path1')
    else:
        form = FileUploadForm()
    return render(request, "whatsapp/app/whatsapp.html", {'form': form})

def path1(request):
    # reading the csv using pandas
    df = pd.read_csv('whatsapp/static/whatsapp/temp/data.csv')
    emojipng(df)
    return redirect('whatsapp:path2')
            
def path2(request):
    # reading the csv using pandas
    df = pd.read_csv('whatsapp/static/whatsapp/temp/data.csv')
    activepng(df)
    return redirect('whatsapp:path3')

def path3(request):
    # reading the csv using pandas
    df = pd.read_csv('whatsapp/static/whatsapp/temp/data.csv')
    useractivepng(df)
    return redirect('whatsapp:path4')

def path4(request):
    # reading the csv using pandas
    df = pd.read_csv('whatsapp/static/whatsapp/temp/data.csv')
    heatmappng(df)
    return redirect('whatsapp:path5')

def path5(request):
    # reading the csv using pandas
    df = pd.read_csv('whatsapp/static/whatsapp/temp/data.csv')
    wordpng(df)
    return redirect('whatsapp:path6')

def path6(request):
    # reading the csv using pandas
    df = pd.read_csv('whatsapp/static/whatsapp/temp/data.csv')
    topmsgpng(df)
    return redirect('whatsapp:analysis')

def analysis(request):
    # Retrieve the first UploadedFile record
    contactMod = UploadedFile.objects.first()
    
    # Ensure the file exists before reading
    if not contactMod or not contactMod.file:
        return render(request, "whatsapp/app/analysis.html", {"error": "No file available for analysis."})

    # Read the CSV file
    try:
        df = pd.read_csv('whatsapp/static/whatsapp/temp/data.csv')
    except Exception as e:
        return render(request, "whatsapp/app/analysis.html", {"error": f"Failed to load CSV: {str(e)}"})

    # Check if DataFrame is empty
    if df.empty:
        return render(request, "whatsapp/app/analysis.html", {"error": "No data in the CSV file."})

    # Group by "Sender" and count messages
    message_counts = df.groupby("Sender")["Message"].count().sort_values(ascending=False)
    message_counts = message_counts.reset_index()

    # Check if there are any users
    if message_counts.empty:
        return render(request, "whatsapp/app/analysis.html", {"error": "No messages found in the data."})

    # Get top user
    top_user = message_counts.head(1)["Sender"].iloc[0]

    # Emoji usage analysis
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

    emoji_data = combined_emoj_ctr.most_common()

    context = {
        'contactMod': contactMod,
        'top_user': top_user,
        'emoji_data': emoji_data
    }

    # Close any open matplotlib plots to avoid issues
    plt.close('all')

    return render(request, "whatsapp/app/analysis.html", context)

# ---------------------------------------#
# Whatsapp functions for genrating images
# ---------------------------------------#

def Instainitializing(uploaded_file_path):
    pass
# function for initializing for csv data from txt data of whatsapp
def initializing(uploaded_file_path):
    with open(uploaded_file_path, 'r', encoding='utf-8') as txt_file, open("whatsapp/static/whatsapp/temp/data.csv", 'w', newline='', encoding='utf-8') as csv_file:
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

# function for getting time analysis
def timepng(df):
    # time spends on chats
    df.dropna(subset=['Sender', 'Message'], inplace=True)
    messages_by_sender = df.groupby('Sender')['Message'].apply(lambda x: ' '.join(x)).reset_index()
    messages_by_sender['Total Characters'] = messages_by_sender['Message'].apply(len)
    messages_by_sender['time'] = messages_by_sender['Total Characters'] / 200
    result = messages_by_sender[['Sender', 'time']]
    result = result.sort_values(by='time', ascending=False)

    # plotting the graph using seaborn and matplot
    custom_palette = sns.color_palette("husl", len(result))
    plt.figure(figsize=(12, 12))
    sns.pointplot(x='time', y='Sender', data=result, palette=custom_palette,errorbar=None)
    plt.xlabel('Time in Minutes')
    plt.ylabel('Senders')
    plt.title('Time insights of all users in chatting')
    labels = [f"{sender}: {time} mins" for sender, time in zip(result['Sender'].values, result['time'].values)]
    plt.legend(title='Time (mins)', labels=labels)
    plt.tight_layout()
    plt.savefig('whatsapp/static/whatsapp/temp/time.png')

# function for getting no. of messages by the user analysis
def topmsgpng(df):
    # getting the message and sender from the dataframe and grouping them
    message_counts = df.groupby("Sender")["Message"].count().sort_values(ascending=False)
    message_counts = message_counts.reset_index()

    # plotting the graph using seaborn and matplot
    custom_palette = sns.color_palette("husl", len(message_counts))
    plt.figure(figsize=(12, 12))
    sns.barplot(x='Message', y='Sender', data=message_counts, palette=custom_palette,errorbar=None)
    plt.xlabel('Message Counts')
    plt.ylabel('Senders')
    plt.title('Messages insights of all users')
    plt.legend(title='Message Counts', labels=message_counts['Message'].values)
    plt.tight_layout()
    plt.savefig('whatsapp/static/whatsapp/temp/graph.png')

# function for getting emoji used in the dataset analysis
def emojipng(df):
    # getting messages from the dataframe
    df["Message"].fillna("", inplace=True)

    # counting the emoji on the messages amd storing it on the dictionary
    emoji_counters = defaultdict(Counter)
    emojis_list = map(lambda x: ''.join(x.split()), emoji.EMOJI_DATA.keys())
    r = re.compile('|'.join(re.escape(p) for p in emojis_list))
    users_to_count = df["Sender"].unique()

    # getting the emojis count for each emoji
    for idx, row in df.iterrows():
        sender = row["Sender"]
        if sender in users_to_count:
            emojis_found = r.findall(str(row["Message"]))
            emoji_counters[sender].update(emojis_found)
    combined_emoji_ctr = Counter()
    for user_ctr in emoji_counters.values():
        combined_emoji_ctr.update(user_ctr)

    # combining the emoji counts of sender specific
    combined_df = pd.DataFrame(combined_emoji_ctr.items(), columns=['Emoji', 'Combined_Count'])
    user_dfs = []
    for user, user_ctr in emoji_counters.items():
        user_df = pd.DataFrame(user_ctr.items(), columns=['Emoji', f'{user}'])
        user_dfs.append(user_df)
    result_df = combined_df

    for user_df in user_dfs:
        result_df = pd.merge(result_df, user_df, on='Emoji', how='outer')
    total_emojis_per_user = result_df.sum(axis=0)
    total_user_used=total_emojis_per_user.count()

    # removed two rows total emojies and total emoji count 
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
    plt.savefig('whatsapp/static/whatsapp/temp/emoji.png')

def activepng(df):
    # Check if DataFrame is empty
    if df.empty:
        print("DataFrame is empty. Please check your input data.")
        return
    
    try:
        # Convert to datetime and filter valid timestamps
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df = df.dropna(subset=['Timestamp'])

        if df.empty:
            print("No valid timestamps found after filtering.")
            return
        
        # Extract hour and compute hourly activity
        df['Hour'] = df['Timestamp'].dt.hour
        hourly_activity = df.groupby('Hour').size()

        if hourly_activity.empty:
            print("No data available for hourly activity plotting.")
            return

        # Plot the graph
        plt.figure(figsize=(12, 12))
        hourly_activity.plot(kind='bar', color='skyblue')
        plt.title('Overall Hourly Activity Pattern')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Total Number of Messages')
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('whatsapp/static/whatsapp/temp/active.png')
    
    except ValueError as e:
        print(f"Error processing data: {e}")

# function for getting user activity analysis
def useractivepng(df):
    # getting time from the dataframe in valid datetime format
    try:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df = df.dropna(subset=['Timestamp']) #removing the row where timestamp is not in valid form or not a number (NaN)
    except ValueError:
        print("Timestamp format does not match expected format.")
    
    # extrating hour from timestamp
    df['Hour'] = df['Timestamp'].dt.hour

    # grouped hour and sender data
    sender_hourly_activity = df.groupby(['Sender', 'Hour']).size()
    most_active_hours = sender_hourly_activity.groupby(level=0).idxmax().apply(lambda x: x[1])
    
    # created custon color palette for the graph
    custom_palette = sns.color_palette("husl", len(most_active_hours))
    
    # plotting the graph using seaborn and matplot
    plt.figure(figsize=(12, 12))
    sns.barplot(data=most_active_hours, palette=custom_palette)
    plt.title('Most Active Hour for Each Sender')
    plt.xlabel('Sender')
    plt.ylabel('Most Active Hour')
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # created label for all the bars with thier respecting hours fir the senders
    for sender, hour in zip(most_active_hours.index, most_active_hours.values):
        plt.text(sender, hour, str(int(hour)), fontsize=8, ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig('whatsapp/static/whatsapp/temp/usertime.png')

# function for getting heatmap of weekely msg insights analysis

def heatmappng(df):
    # Check if DataFrame is empty
    if df.empty:
        print("DataFrame is empty. Please check your input data.")
        return

    try:
        # Convert to datetime and filter valid timestamps
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df = df.dropna(subset=['Timestamp'])

        if df.empty:
            print("No valid timestamps found after filtering.")
            return

        # Extract hour and weekday
        df['Hour'] = df['Timestamp'].dt.hour
        df['Day_of_Week'] = df['Timestamp'].dt.dayofweek

        # Group by weekday and hour
        activity_by_day_hour = df.groupby(['Day_of_Week', 'Hour']).size().unstack(fill_value=0)

        # Ensure all days are included
        activity_by_day_hour = activity_by_day_hour.reindex(index=range(7), fill_value=0)

        # Check if data is available for plotting
        if activity_by_day_hour.empty or (activity_by_day_hour.values.sum() == 0):
            print("No activity data available for plotting.")
            return

        # Plot heatmap
        plt.figure(figsize=(12, 12))
        sns.heatmap(activity_by_day_hour, cmap='rocket', square=False)
        plt.title('Activity by Day of the Week and Hour')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Day of the Week')
        plt.yticks(ticks=range(7), labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], rotation=0)
        plt.tight_layout()
        plt.savefig('whatsapp/static/whatsapp/temp/heatmap.png')
    
    except ValueError as e:
        print(f"Error processing data: {e}")

# function for getting word graph that most used analysis
def wordpng(df):
    # Check if DataFrame is empty
    if df.empty:
        print("DataFrame is empty. Please check your input data.")
        return

    # Initialize empty string for words
    comment_words = ''
    
    # Update stopwords to exclude unwanted words
    stopwords = STOPWORDS.update(['ok'])

    # Extract words from messages
    for val in df['Message'].dropna().values:
        val = str(val).strip()  # Convert to string and strip unnecessary spaces

        # Skip empty messages
        if not val:
            continue

        # Tokenize and normalize words
        tokens = val.split()
        tokens = [word.lower() for word in tokens if word.isalpha()]  # Keep only alphabetic words

        # Append to comment words
        comment_words += ' '.join(tokens) + ' '

    # Ensure there are words to generate the word cloud
    if not comment_words.strip():
        print("No valid words available to generate a word cloud.")
        return

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=800, background_color='black', stopwords=stopwords, min_font_size=10)
    wordcloud.generate(comment_words)
    
    # Save word cloud image
    image = wordcloud.to_image()
    image.save("whatsapp/static/whatsapp/temp/word.png")