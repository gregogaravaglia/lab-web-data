'''Count catalog phrases in the Trump tweet archive and chart the results.'''
import json

import matplotlib
matplotlib.use('Agg')  # save the chart without needing a display window
import matplotlib.pyplot as plt

YEARS = range(2009, 2019)
REQUIRED_PHRASES = ['obama', 'trump', 'mexico', 'russia', 'fake news']
CHOSEN_PHRASES = ['wall', 'maga', 'mainstream media']
PHRASES = REQUIRED_PHRASES + CHOSEN_PHRASES


def load_tweets():
    '''Load master_2009.json through master_2018.json into one list.'''
    tweets = []
    for year in YEARS:
        with open(f'master_{year}.json', encoding='utf-8') as f:
            tweets.extend(json.load(f))
    return tweets


def message(tweet):
    '''Return a tweet's message: full_text when present, otherwise text.'''
    if tweet.get('full_text'):
        return tweet['full_text']
    return tweet.get('text', '')


def count_phrases(tweets, phrases):
    '''Count the tweets containing each phrase, ignoring capitalization.'''
    messages = [message(tweet).lower() for tweet in tweets]
    counts = {}
    for phrase in phrases:
        target = phrase.lower()
        counts[phrase] = sum(1 for text in messages if target in text)
    return counts


def markdown_table(percents):
    '''Return a Markdown table of phrases and their percent of all tweets.'''
    lines = [
        '| phrase            | percent of tweets |',
        '| ----------------- | ----------------- |',
    ]
    for phrase in sorted(percents):
        lines.append(f'| {phrase:>17} | {percents[phrase]:05.2f}             |')
    return '\n'.join(lines)


def plot(percents, filename='tweets.png'):
    '''Save a horizontal bar chart of each phrase's percent of tweets.'''
    phrases = sorted(percents, key=percents.get)
    values = [percents[phrase] for phrase in phrases]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(phrases, values, color='#4C72B0')
    for y, value in enumerate(values):
        ax.text(value, y, f' {value:.2f}%', va='center', fontsize=9)
    ax.set_xlabel('Percent of tweets containing the phrase')
    ax.set_ylabel('Phrase')
    ax.set_title('Phrases in the Trump tweet archive, 2009-2018')
    ax.set_xlim(0, max(values) * 1.15)
    fig.tight_layout()
    plt.savefig(filename)
    plt.close(fig)


def main():
    tweets = load_tweets()
    total = len(tweets)
    print('total tweets:', total)

    counts = count_phrases(tweets, PHRASES)
    for phrase in PHRASES:
        print(f'{phrase}: {counts[phrase]}')

    percents = {phrase: 100 * counts[phrase] / total for phrase in PHRASES}
    table = markdown_table(percents)
    print()
    print(table)
    with open('tweets_table.md', 'w', encoding='utf-8') as f:
        f.write(table + '\n')

    plot(percents)


if __name__ == '__main__':
    main()
