import numpy as np
import csv

from alfashape import getAlfaShapes
# from cython_alpha_shapes import getAlfaShapes
import matplotlib.pyplot as plt
from draw_hull import draw

exampleFile = open('data/figure.csv', 'r')
exampleReader = csv.reader(exampleFile, delimiter=',')
exampleData = list(exampleReader)
pts = [(float(x[0]), float(x[1])) for x in exampleData[1:]]

print(len(pts), 'points')

params = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
lines = getAlfaShapes(pts, alfas=params)

for i, line in enumerate(lines):
    plt.figure()
    draw(line, pts, plt, splined=False)
for i, line in enumerate(lines):
    plt.figure()
    draw(line, pts, plt, splined=True)

plt.show()