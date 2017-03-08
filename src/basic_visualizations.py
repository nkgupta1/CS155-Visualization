#!/usr/bin/env python3

from common import *

import matplotlib.pyplot as plt

def plot(freqs, title):
    '''
    Plots a histogram of given data.
    '''

    fig, ax = plt.subplots()
    ax.hist(freqs, 5, range=(0.5,5.5), color='green', align='mid', normed=1)
    ax.set_xlabel('Rating')
    ax.set_ylabel('Frequency')
    ax.set_title(title)
    plt.savefig('../graphics/{0}.png'.format(title))
    plt.show()

    return

if __name__=='__main__':
    ratings = import_data()

    # Part 1
    freqs = []
    for i in range(len(ratings)):
        for j in range(len(ratings[i])):
            val = ratings[i][j]
            freqs.append(val)

    plot(freqs, 'All Ratings')

    # Part 2
    ratings2 = sorted(ratings, key=lambda x: len(x), reverse=True)
    freqs2 = []
    for d in range(10):
        for j in range(len(ratings2[d])):
            val = ratings2[d][j]
            freqs2.append(val)

    plot(freqs2, 'Ratings of 10 Most Popular Movies')

    # Part 3a - 'Best' Movies
    ratings3 = sorted(ratings, key=lambda x: (sum(x) / len(x)), reverse=True)
    freqs3 = []
    for d in range(10):
        for j in range(len(ratings3[d])):
            val = ratings3[d][j]
            freqs3.append(val)

    plot(freqs3, 'Ratings of 10 Highest-Rated Movies')

    # Part 3b - Best movies with over 10 Ratings
    ratings4 = [lst for lst in ratings if len(lst) >= 10]
    ratings4 = sorted(ratings4, key=lambda x: (sum(x) / len(x)), reverse=True)
    freqs4 = []
    for d in range(10):
        for j in range(len(ratings4[d])):
            val = ratings4[d][j]
            freqs4.append(val)

    plot(freqs4, 'Ratings of 10 Highest-Rated Movies (>= 10 Ratings)')

    # Part 4 - Ratings for Three Genres 
    genres = ['Fantasy', 'Sci-Fi', 'War']
    genre_ratings = import_genres(genres)
    freqs5 = []
    for i in range(len(genre_ratings)):
        for j in range(len(genre_ratings[i])):
            val = genre_ratings[i][j]
            freqs5.append(val)

    plot(freqs5, 'Ratings for Genres: {0}'.format(genres))