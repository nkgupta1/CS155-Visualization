#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from common import *


movie_names = create_dict()  # dict[movie_id: movie_name]
movie_ratings = import_data()  # movies[movie_id, ratings[rating]]
genre_names = list({
        'Unknown' : 0,
        'Action' : 1,
        'Adventure' : 2,
        'Animation' : 3,
        'Childrens' : 4,
        'Comedy' : 5,
        'Crime' : 6,
        'Documentary' : 7,
        'Drama' : 8,
        'Fantasy' : 9,
        'Film-Noir' : 10,
        'Horror' : 11,
        'Musical' : 12,
        'Mystery' : 13,
        'Romance' : 14,
        'Sci-Fi' : 15,
        'Thriller' : 16,
        'War' : 17,
        'Western' : 18
    }.keys())

def twoD_viz(title, movie_ids, xy_coords, rect, dpi=100, buf=0.1, annotate=True):
    '''
    param: title: title for plot as well as save-name
    param: movie_ids: 1d-list or numpy array of [movie_ids]
    param: xy_coords: 2d numpy array of [movie_x, movie_y] corresponding to 
    movie_id in movie_ids
    param: rect: rectangle bounding all possible xy coordinates in V 
    given by [minimum X, maximum X, minimum Y, maximum Y]
    return: none: plots points on a scatter plot and annotates them with 
    movie names before saving them into /graphics with the name param:title
    '''
    # define rect according according to points in xy_coords
    if rect is None:
        rect = np.array([xy_coords[:, 0].min(), xy_coords[:, 0].max(), 
            xy_coords[:, 1].min(), xy_coords[:, 1].max()])
        width = rect[1] - rect[0]
        height = rect[3] - rect[2]
        rect[0] -= width * buf
        rect[1] += width * buf
        rect[2] -= height * buf
        rect[3] += height * buf

    # create plot dimensions, resolution, and axis ranges
    plt.clf()
    fig, ax = plt.subplots(figsize=(10., 10.), dpi=dpi)
    ax.set_title(title, fontdict={'fontsize': 25})
    ax.axis(rect)

    # get relative sizes and ranges of drawing window
    x_mid, y_mid = (rect[0] + rect[1]) / 2., (rect[2] + rect[3]) / 2.
    x_interval, y_interval = (rect[1] - rect[0]), (rect[3] - rect[2])
    
    # draw points
    ax.scatter(xy_coords[:, 0], xy_coords[:, 1])
    
    # remove top and right axis-lines for aesthetic purposes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # draw annotations next to points with coordinate offsets
    if annotate:
        for i, movie in enumerate(movie_ids):
            label_position = xy_coords[i]
            label_position[1] += .01 * y_interval
            ax.annotate(movie_names[movie], xy_coords[i], xytext=label_position)

    # save plot
    print('saving...', title)
    plt.savefig('../graphics/{0}.png'.format(title), bbox_inches='tight', 
               transparent=True, dpi=dpi)


def viz_comparison(title, xy_coords_lst, colors, rect, names=None, dpi=100):
    # create plot dimensions, resolution, and axis ranges
    plt.clf()
    fig, ax = plt.subplots(figsize=(10., 10.), dpi=dpi)
    ax.set_title(title, fontdict={'fontsize': 25})
    ax.axis(rect)

    # get relative sizes and ranges of drawing window
    x_mid, y_mid = (rect[0] + rect[1]) / 2., (rect[2] + rect[3]) / 2.
    x_interval, y_interval = (rect[1] - rect[0]), (rect[3] - rect[2])
    
    # draw points. use decimal colors if one group. else, colors are distinct
    if len(xy_coords_lst) == 1:
        ax.scatter(xy_coords_lst[0][:, 0], xy_coords_lst[0][:, 1], c=colors[0])
    else:
        for i, xy_coords in enumerate(xy_coords_lst):
            if names is not None:
                ax.scatter(xy_coords[:, 0], xy_coords[:, 1], color=colors[i], 
                    label=names[i], s=15)
            else:
                ax.scatter(xy_coords[:, 0], xy_coords[:, 1], color=colors[i])
    
    if names is not None:
        plt.legend(loc='center left')
    # remove top and right axis-lines for aesthetic purposes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # save plot
    print('saving...', title)
    plt.savefig('../graphics/{0}.png'.format(title), bbox_inches='tight', 
               transparent=True, dpi=dpi)


def viz_tasks(V):
    '''
    param: V: 2-d numpy matrix as defined in guide as "V", V.shape = [2, n],
    V = movie_id[x, y]
    return: none: find the movie ids belonging to each group as defined in 
    the guide and their coordinates in param:V. plots, annotates, and saves 
    the points using twoD_viz().
    '''
    movie_ids = movie_names.keys()
    # 10 random movies
    rand_movies = np.random.randint(1, len(movie_ids) + 1, 10)

    # 10 most popular movies
    movie_sizes = []
    movie_avg_ratings = []
    for movie, ratings in movie_ratings:
        movie_sizes.append(len(ratings))
        movie_avg_ratings.append(sum(ratings) / len(ratings))
    all_popular = np.array(list(zip(*sorted(zip(movie_sizes, movie_ids)))))
    most_popular = all_popular[1][-10:]

    # 10 best movies
    best_movies = np.array(list(zip(*sorted(zip(movie_avg_ratings, movie_ids)))))[1][-10:]

    # first 10 movies from three genres. only include over 50 ratings
    fantasy_all = import_genres(['Fantasy'])
    scifi_all = import_genres(['Sci-Fi'])
    war_all = import_genres(['War'])
    fantasy, scifi, war = [np.array([x for x, y in 
        sorted(genre, key=lambda x: sum(x[1]) / len(x[1]), reverse=True) if 
        len(y) >= 50][:10]) for genre in [fantasy_all, scifi_all, war_all]]

    # regroup models. only include over 50 ratings
    genre_coords = [V[np.array([x for x, y in genre if len(y) >= 50]) - 1] 
        for genre in [fantasy_all, scifi_all, war_all]]
    all_genres = [import_genres([name]) for name in genre_names]
    all_genre_coords = [V[np.array([x for x, y in genre if len(y) >= 50]
        ).astype(np.uint16) - 1] for genre in all_genres]

    # turn popularity values into colors
    all_popular = all_popular.astype(np.float32)
    all_popular[0] /= all_popular[0].max()
    all_popular[0] = all_popular[0] ** .25

    # get rating values above 20 frequency and turn into colors
    all_best = [x for x in movie_ratings if len(x[1]) >= 20]
    all_best = [[x[0], sum(x[1]) / len(x[1])] for x in all_best]
    all_best = sorted(all_best, key=lambda x: x[1], reverse=True)
    all_best = np.array(all_best).astype(np.float32).transpose()
    all_best[1] /= all_best[1].max()

    # rectangle bounding all possible xy coordinates in V
    rect = [V[:, 0].min(), V[:, 0].max(), V[:, 1].min(), V[:, 1].max()]

    # create and save plots using movie ids and coordinates from V
    twoD_viz('All Movies', movie_ids, V, rect, annotate=False)
    viz_comparison('3-Genre Comparison', genre_coords, 
        ['blue', 'green', 'red'], rect, names=['Fantasy', 'Sci-Fi', 'War'])
    viz_comparison('All Genre Comparison', all_genre_coords, 
        np.random.random((len(genre_names), 3)), rect, names=genre_names)
    viz_comparison('Popularity Comparison', 
        [V[all_popular[1].astype(np.uint16) - 1]], [all_popular[0]], rect)
    viz_comparison('Rating Comparison', 
        [V[all_best[0].astype(np.uint16) - 1]], [all_best[1]], rect)
    twoD_viz('10 Random Films', rand_movies, V[rand_movies - 1], rect)
    twoD_viz('10 Most Popular Films', most_popular, V[most_popular - 1], rect)
    twoD_viz('10 Top Rated Films', best_movies, V[best_movies - 1], rect)
    twoD_viz('Top 10 Genre: Fantasy Films', fantasy, V[fantasy - 1], rect)
    twoD_viz('Top 10 Genre: Sci-Fi Films', scifi, V[scifi - 1], rect)
    twoD_viz('Top 10 Genre: War Films', war, V[war - 1], rect)
    print('done!')

if __name__ == '__main__':
    A = np.load('models/0.30616-A-0.1000-0.0100.npy')
    V = np.load('models/0.30616-V-0.1000-0.0100.npy')
    viz_tasks(np.matmul(A.transpose(), V).transpose())
