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

def pretty_print(data, title):
    '''
    Pretty prints output to terminal.
    '''
    print('')
    print(title)
    print('')
    for datum in data:
        print(datum)
    return

if __name__=='__main__':
    ratings = import_data()
    dct = create_dict()

    # Part 1
    freqs = []
    for i in range(len(ratings)):
        for j in range(len(ratings[i][1])):
            freqs.append(ratings[i][1][j])

    plot(freqs, 'All Ratings')

    # Part 2
    ratings2 = sorted(ratings, key=lambda x: len(x[1]), reverse=True)
    freqs2 = []
    names2 = []
    for d in range(10):
        names2.append(dct[ratings2[d][0]])
        for j in range(len(ratings2[d][1])):
            freqs2.append(ratings2[d][1][j])

    plot(freqs2, 'Ratings of 10 Most Popular Movies')
    pretty_print(names2, '10 Most Popular Movies')

    # Part 3a - 'Best' Movies
    ratings3 = sorted(ratings, key=lambda x: (sum(x[1]) / len(x[1])), reverse=True)
    freqs3 = []
    names3 = []
    for d in range(10):
        names3.append(dct[ratings3[d][0]])
        for j in range(len(ratings3[d][1])):
            freqs3.append(ratings3[d][1][j])

    plot(freqs3, 'Ratings of 10 Highest-Rated Movies')
    pretty_print(names3, '10 Best Movies')

    # Part 3b - Best movies with over 10 Ratings
    ratings4 = [lst for lst in ratings if len(lst[1]) >= 50] # No change from 10, 50
    ratings4 = sorted(ratings4, key=lambda x: (sum(x[1]) / len(x[1])), reverse=True)
    freqs4 = []
    names4 = []
    for d in range(10):
        names4.append(dct[ratings4[d][0]])
        for j in range(len(ratings4[d][1])):
            freqs4.append(ratings4[d][1][j])

    plot(freqs4, 'Ratings of 10 Highest-Rated Movies (>= 50 Ratings)')
    pretty_print(names4, '10 Best Movies (>= 50 Ratings)')

    # Part 4a - Ratings for Three Genres 1
    genres1 = ['Fantasy']
    genre_ratings1 = import_genres(genres1)
    freqs5 = []
    names5 = []
    for i in range(len(genre_ratings1)):
        names5.append(dct[genre_ratings1[i][0]])
        for j in range(len(genre_ratings1[i][1])):
            freqs5.append(genre_ratings1[i][1][j])

    plot(freqs5, 'Ratings for Genres: {0}'.format(genres1[0]))
    # pretty_print(names5, '{0} Movies'.format(genres1[0]))

    # Part 4b - Ratings for Three Genres 2
    genres2 = ['Sci-Fi']
    genre_ratings2 = import_genres(genres2)
    freqs6 = []
    names6 = []
    for i in range(len(genre_ratings2)):
        names6.append(dct[genre_ratings2[i][0]])
        for j in range(len(genre_ratings2[i][1])):
            freqs6.append(genre_ratings2[i][1][j])

    plot(freqs6, 'Ratings for Genres: {0}'.format(genres2[0]))
    # pretty_print(names6, '{0} Movies'.format(genres2[0]))

    # Part 4c - Ratings for Three Genres 3
    genres3 = ['War']
    genre_ratings3 = import_genres(genres3)
    freqs7 = []
    names7 = []
    for i in range(len(genre_ratings3)):
        names7.append(dct[genre_ratings3[i][0]])
        for j in range(len(genre_ratings3[i][1])):
            freqs7.append(genre_ratings3[i][1][j])

    plot(freqs7, 'Ratings for Genres: {0}'.format(genres3[0]))
    # pretty_print(names7, '{0} Movies'.format(genres3[0]))