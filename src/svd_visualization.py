#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from common import *


movie_names = create_dict()  # dict[movie_id: movie_name]
movie_ratings = import_data()  # movies[movie_id, ratings[rating]]


def twoD_viz(title, movie_ids, xy_coords, rect=None, dpi=100, off_set=0.04):
    '''
    param: movie_ids: 1d-list or numpy array of [movie_ids]
    param: xy_coords: 2d numpy array of [movie_x, movie_y] corresponding to 
    movie_id in movie_ids
    return: none: 
    '''
    # define rect according according to points in xy_coords
    if rect is None:
        rect = np.array([xy_coords[:, 0].min(), xy_coords[:, 0].max(), 
            xy_coords[:, 1].min(), xy_coords[:, 1].max()])
        print(rect)

    # create plot dimensions, resolution, and axis ranges
    plt.clf()
    plt.title(title)
    fig, ax = plt.subplots(figsize=(10., 10.), dpi=dpi)
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
    for i, movie in enumerate(movie_ids):
        label_position = xy_coords[i]
        # dynamic offsets
        #label_position[0] += np.sign(xy_coords[i, 0] - x_mid) * off_set * x_interval
        #label_position[1] += np.sign(xy_coords[i, 1] - y_mid) * off_set * y_interval
        # static offsets
        #label_position[0] -= .05 * x_interval
        label_position[1] -= .03 * y_interval
        ax.annotate(movie_names[movie], xy_coords[i], xytext=label_position)

    # save plot
    print('saving...', title)
    plt.savefig('../graphics/{0}.png'.format(title), bbox_inches='tight', 
               transparent=True, dpi=dpi)


def viz_tasks(V):
    '''
    param: V: 2-d numpy matrix as defined in guide as "V", V.shape = [2, n],
    V = movie_id[x, y]
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
    most_popular = np.array(list(zip(*sorted(zip(movie_sizes, movie_ids))))[1][-10:])

    # 10 best movies
    best_movies = np.array(list(zip(*sorted(zip(movie_avg_ratings, movie_ids))))[1][-10:])

    # first 10 movies from three genres
    animation, scifi, war = [np.array([x for x, y in genre][:10])
        for genre in [import_genres(['Animation']), import_genres(['Sci-Fi']), 
        import_genres(['War'])]]

    #rect = [V[:, 0].min(), V[:, 0].max(), V[:, 1].min(), V[:, 1].max()]
    twoD_viz('10 Random Films', rand_movies, V[rand_movies - 1])
    twoD_viz('10 Most Popular Films', most_popular, V[most_popular - 1])
    twoD_viz('10 Most Rated Films', best_movies, V[best_movies - 1])
    twoD_viz('Top 10 Animation Films', animation, V[animation - 1])
    print('done!')

if __name__ == '__main__':
    A = np.load('models/0.30616-A-0.1000-0.0100.npy')
    V = np.load('models/0.30616-V-0.1000-0.0100.npy')
    viz_tasks(np.matmul(A.transpose(), V).transpose())


