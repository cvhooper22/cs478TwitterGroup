__author__ = 'Matthew'
import os
import json
import pandas as pd
import matplotlib.pyplot as plt


def remove_single_quotes(string):
    utfstring = string.encode('utf-8', 'ignore')
    #some things have returns(\r)m (\n), and(\\) in them, get rid of those b/c weka hates them in the dataset

    string = string.strip("\\")

    slash_split = string.split("\\")
    if len(slash_split) == 1:
        pass
    else:
        corrected_string = ""
        for x in range(0, len(slash_split) - 1):
            corrected_string += slash_split[x]
        if slash_split[len(slash_split) - 1] == '':
            pass
        else:
            corrected_string += slash_split[len(slash_split) -1]
        string = corrected_string


    string = string.strip("\r")

    return_split = string.split("\r")
    if len(return_split) == 1:
        pass
    else:
        fixed_string = ""
        for x in range(0, len(return_split) - 1):
            fixed_string += return_split[x]
        if return_split[len(return_split) - 1] == '':
            pass
        else:
            fixed_string += return_split[len(return_split) -1]
        string = fixed_string


    string = string.strip("\n")
    newline_split = string.split("\n")
    if len(newline_split) == 1:
        pass
    else:
        better_string = ""
        for x in range(0, len(newline_split) - 1):
            better_string += newline_split[x]
        if newline_split[len(newline_split) - 1] == '':
            pass
        else:
            better_string += newline_split[len(newline_split) - 1]
        string = better_string


    string = string.strip("\'")
    split_on_quotes = string.split("\'")
    if len(split_on_quotes) == 1:
        return string
    else:
        returner = ""
        for x in range(0, len(split_on_quotes) - 1):
            returner += split_on_quotes[x]
        if split_on_quotes[len(split_on_quotes) - 1] == '':
            return returner
        else:
            returner += split_on_quotes[len(split_on_quotes) -1]
        return returner

def write_att_val(val):
    val = val + ","
    string = val.encode('utf-8', 'ignore')
    output_file.write(string)


def count_words(this_tweet):
    all_words = this_tweet.split()
    string_lenth = str(len(all_words))
    return string_lenth


def count_keywords(this_tweet):
    tweet_words = this_tweet.split()
    count = 0
    for word in tweet_words:
        for keyword in keywords_array:
            lower_word = word.lower()
            lower_keyword = keyword.lower()
            if lower_keyword == lower_word:
                count += 1
    return str(count)


def find_if_replied(reply_user_id):
    if reply_user_id is None:
        return 'no'
    else:
        return 'yes'


input_data_path = 'endata\\'
output_fil = 'twitter_full.arff'

filenames = os.listdir("endata")

# load the keywords to use in computation later
keyword_file = open("keywords.txt", "r")
my_words = keyword_file.read()
keywords_array = my_words.split()

#first thing to write is the headers from the other file
headerFile = open('twitterHeaders.txt', "r")
contents = headerFile.read()
contents = contents.encode('utf-8', 'ignore')
output_file = open(output_fil, "a")
output_file.write(contents)

for filename in filenames:
    tweets_data = []
    input_path = input_data_path + filename
    print input_path
    tweets_file = open(input_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue

    for tweet in tweets_data:
        #TODO here is where I do the processing nonsense
        tweet_text = tweet['text']
        wordcount = count_words(tweet_text)
        write_att_val(wordcount)

        keyword_count = count_keywords(tweet_text)
        write_att_val(keyword_count)

        hashtag_count = len(tweet['entities']['hashtags'])
        write_att_val(str(hashtag_count))

        in_reply_to = find_if_replied(tweet['in_reply_to_user_id'])
        write_att_val(in_reply_to)

        username = tweet['user']['name']
        write_att_val('\'' + remove_single_quotes(username) + '\'')

        screen_name = tweet['user']['screen_name']
        write_att_val('\'' + remove_single_quotes(screen_name) + '\'')

        location = tweet['user']['location']
        if location == '':
            write_att_val("\'unknown\'")
        else:
            write_att_val('\'' + remove_single_quotes(location) + '\'')

        user_url = tweet['user']['url']
        if user_url is None:
            write_att_val('\'null\'')
        else:
            write_att_val('\'' + remove_single_quotes(user_url) + '\'')

        verification = tweet['user']['verified']
        write_att_val(str(verification))

        follower_count = tweet['user']['followers_count']
        write_att_val(str(follower_count))

        user_favorited_count = tweet['user']['favourites_count']
        write_att_val(str(user_favorited_count))

        tweet_count = tweet['user']['statuses_count']
        write_att_val(str(tweet_count))

        place = tweet['place']
        if place is None:
            write_att_val("\'unknown\'")
        else:
            tweet_location = tweet['place']['full_name']
            write_att_val('\'' + remove_single_quotes(tweet_location) + '\'')

        urls = tweet['entities']['urls']
        num_links = str(len(urls))
        write_att_val(num_links)

        #this will do the first_url attribute
        if len(urls) != 0:
            write_att_val('\'' + remove_single_quotes(urls[0]['url']) + '\'')
        else:
            write_att_val('\'null\'')

        mentions = len(tweet['entities']['user_mentions'])
        write_att_val(str(mentions))

        num_symbols = len(tweet['entities']['symbols'])
        write_att_val(str(num_symbols))

        time_string = tweet['created_at']
        write_att_val('\'' + time_string + '\'')

        user_birth_date = tweet['user']['created_at']
        write_att_val('\'' + user_birth_date + '\'')

        retweet_count = tweet['retweet_count']
        write_att_val(str(retweet_count))

        tweet_favorite_count = tweet['favorite_count']
        last_att = str(tweet_favorite_count) + "\n"
        last_att = last_att.encode('utf-8', 'ignore')
        output_file.write(last_att)



print "Done"


