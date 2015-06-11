__author__ = 'Matthew'
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from decimal import *
import time



def remove_single_quotes(string):
    utfstring = string.encode('utf-8', 'ignore')
    # some things have returns(\r)m (\n), and(\\) in them, get rid of those b/c weka hates them in the dataset

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
            corrected_string += slash_split[len(slash_split) - 1]
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
            fixed_string += return_split[len(return_split) - 1]
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
            returner += split_on_quotes[len(split_on_quotes) - 1]
        return returner


def write_att_val(val):
    val = val + ","
    string = val.encode('utf-8', 'ignore')
    output_file.write(string)


def count_words(this_tweet):
    all_words = this_tweet.split()
    lenth = len(all_words)
    return lenth


def count_keywords(this_tweet):
    tweet_words = this_tweet.split()
    count = 0
    for word in tweet_words:
        for keyword in keywords_array:
            lower_word = word.lower()
            lower_keyword = keyword.lower()
            if lower_keyword == lower_word:
                count += 1
    return count


def find_if_replied(reply_user_id):
    if reply_user_id is None:
        return False
    else:
        return True


def get_string_time(time):
    if time > 21.165 or time < 4.9834:
        return 'late'
    elif 4.9832 < time < 11.01:
        return 'morning'
    elif 11.0 < time < 16.9834:
        return 'afternoon'
    elif 16.9832 < time < 21.01:
        return 'evening'


def calc_num_time(date_string):
    split_vals = date_string.split(" ")
    time_string = split_vals[3]
    time_vals = time_string.split(":")
    hour = Decimal(time_vals[0])
    minute_num = Decimal(time_vals[1])
    minute = minute_num / 60
    time = hour + minute
    return time


def find_common_time(late_ct, morning_ct, afternoon_ct, evening_ct):
    top_ct = max(late_ct, morning_ct, afternoon_ct, evening_ct)
    if late_ct == top_ct:
        return 'late'
    elif morning_ct == top_ct:
        return 'morning'
    elif afternoon_ct == top_ct:
        return 'afternoon'
    elif evening_ct == top_ct:
        return 'evening'


def calc_age(date_string):
    time_vals = date_string.split(" ")
    year = Decimal(time_vals[5])
    month_string = time_vals[1]
    month = get_month_from_string(month_string)
    month_diff = month - 6
    year_diff = 2015 - year
    if month_diff <= 0:
        year_diff += Decimal(abs(month_diff)) / 12
    else:
        actual_diff = 12 - month_diff
        year_diff += Decimal(actual_diff) / 12
    return year_diff


def get_month_from_string(string):
    if string == 'Jan':
        return 1
    elif string == 'Feb':
        return 2
    elif string == 'Mar':
        return 3
    elif string == 'Apr':
        return 4
    elif string == 'May':
        return 5
    elif string == 'Jun':
        return 6
    elif string == 'Jul':
        return 7
    elif string == 'Aug':
        return 8
    elif string == 'Sep':
        return 9
    elif string == 'Oct':
        return 10
    elif string == 'Nov':
        return 11
    elif string == 'Dec':
        return 12


input_data_path = 'userdata\\'
output_fil = 'twitter_users.arff'

filenames = os.listdir("userdata")

# load the keywords to use in computation later
keyword_file = open("keywords.txt", "r")
my_words = keyword_file.read()
keywords_array = my_words.split()

# first thing to write is the headers from the other file
headerFile = open('twitterHeaders2.txt', "r")
contents = headerFile.read()
contents = contents.encode('utf-8', 'ignore')
output_file = open(output_fil, "a")
output_file.write(contents)

getcontext().prec = 4
getcontext().rounding = ROUND_UP

fileindex = 0
# start_time = time.clock()
for filename in filenames:
    fileindex += 1
    print "Working on file {index} of {total}".format(index=fileindex, total= len(filenames))
    # time_now = time.clock()
    # time_so_far = time_now - start_time
    # print "Time so far: {}".format(time_so_far)
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

    # set up user values
    num_tweets = Decimal(len(tweets_data))
    retweeted_count = 0
    favorited_count = 0
    avg_wordcount = 0
    avg_hashcount = 0
    avg_keywords = 0
    avg_links = 0
    avg_mentions = 0
    avg_symbols = 0
    num_replies = 0
    media_count = 0
    # these next four variables reference the different times of day that someone's tweets can show up
    # late --> 11:01pm-4:59am
    # morning --> 5:00am-11:00am
    # afternoon --> 11:01am-4:59pm
    # evening --> 5:00pm-11:00pm
    late_count = 0
    morning_count = 0
    afternoon_count = 0
    evening_count = 0

    for x in range(len(tweets_data)):
        tweet = tweets_data[x]
        tweet_text = tweet['text']
        wordcount = count_words(tweet_text)
        avg_wordcount += wordcount

        keyword_count = count_keywords(tweet_text)
        avg_keywords += keyword_count

        hashtag_count = len(tweet['entities']['hashtags'])
        avg_hashcount += hashtag_count

        in_reply_to = find_if_replied(tweet['in_reply_to_user_id'])
        if in_reply_to:
            num_replies += 1

        urls = tweet['entities']['urls']
        num_links = len(urls)
        avg_links += num_links

        mentions = len(tweet['entities']['user_mentions'])
        avg_mentions += mentions

        num_symbols = len(tweet['entities']['symbols'])
        avg_symbols += num_symbols

        time_string = tweet['created_at']
        time_num = calc_num_time(time_string)
        time_of_day = get_string_time(time_num)
        if time_of_day == 'late':
            late_count += 1
        elif time_of_day == 'morning':
            morning_count += 1
        elif time_of_day == 'afternoon':
            afternoon_count += 1
        elif time_of_day == 'evening':
            evening_count += 1

        retweet_count = tweet['retweet_count']
        retweeted_count += retweet_count

        tweet_favorite_count = tweet['favorite_count']
        favorited_count += tweet_favorite_count

        try:
            media = tweet['entities']['media']
            if media is not None:
                has_media = len(tweet['entities']['media'])
                if has_media > 0:
                    media_count += 1
        except:
            pass

        if x == len(tweets_data) - 1:
            # TODO here is where we write the attributes
            wordcount = avg_wordcount / num_tweets
            write_att_val(str(wordcount))

            keyword_count = avg_keywords / num_tweets
            write_att_val(str(keyword_count))

            hashtag_count = avg_hashcount / num_tweets
            write_att_val(str(hashtag_count))

            in_reply_to = num_replies / num_tweets
            write_att_val(str(in_reply_to))

            username = tweet['user']['name']
            write_att_val('\'' + remove_single_quotes(username) + '\'')

            screen_name = tweet['user']['screen_name']
            write_att_val('\'' + remove_single_quotes(screen_name) + '\'')

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

            num_links = avg_links / num_tweets
            write_att_val(str(num_links))

            mentions = avg_mentions / num_tweets
            write_att_val(str(mentions))

            num_symbols = avg_symbols / num_tweets
            write_att_val(str(num_symbols))

            time = find_common_time(late_count, morning_count, afternoon_count, evening_count)
            write_att_val(time)

            user_age = calc_age(tweet['user']['created_at'])
            write_att_val(str(user_age))

            retweet_count = retweeted_count
            write_att_val(str(retweet_count))

            been_favorite_count = favorited_count
            write_att_val(str(been_favorite_count))

            media_freq = media_count / num_tweets
            last_att = str(media_freq) + "\n"
            last_att = last_att.encode('utf-8', 'ignore')
            output_file.write(last_att)

print "Done"


