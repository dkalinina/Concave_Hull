# Concave_Hull
Alpha Shapes algorithm with new cumulative parameter for gradually changes from concave hull to convex hull.

Two implementations are represented. One of them on `python 3` and another one on `cython`.

To execute algorithm run `alfa_example.py`.
You can find example dataset in folder `data` and some analitics pictures in folder `analysis`.

The example dataset is part of Petrogradsky district, Saint Petersburg, Russia by `Open Street Map`. There are 3922 points in the dataset.  ![](https://github.com/dkalinina/Concave_Hull/blob/master/data/figure.jpeg)

Algorithm demonstrates gradually changing from concave hull to convex hull: ![](https://github.com/dkalinina/Concave_Hull/blob/master/analysis/some_parameters.png)

Time estimation for datasets with different counts of points shows good performs. For comparison, the implementation of the `QGIS` for the biggest of these datasets was performed for ~90 minutes. ![](https://github.com/dkalinina/Concave_Hull/blob/master/analysis/time_estimation.png)

And additionally hull smoothing was implemented for better demonstration geospatial results: ![](https://github.com/dkalinina/Concave_Hull/blob/master/analysis/splined_figures.png)
