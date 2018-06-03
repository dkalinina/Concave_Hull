import numpy as np
import matplotlib.path as path
import scipy.interpolate
import matplotlib

def draw(polygons, points, plt, head='', xlabel='', ylabel='', splined = False):
    base_colors = ['green', 'aquamarine', 'brown', 'blueviolet', 'chocolate', 'crimson', 'cyan', 'darkblue', 'darkred',
                   'dodgerblue', 'forestgreen', 'fuchsia', 'gold', 'gray' , 'greenyellow', 'indigo', 'navy', 'olive',
                   'orange', 'purple', 'salmon', 'teal', 'mediumspringgreen', 'darksalmon', 'pink', 'grey', 'magenta',
                   'aqua', 'goldenrod', 'lawngreen', 'turquoise', 'plum','rosybrown', 'lightcoral', 'midnightblue']

    plt.plot([x[0] for x in points], [x[1] for x in points], '.', color='black', alpha = 0.5, ms=1)
    pathes = [path.Path(p) for p in polygons]
    color_poz = -1
    colors = []

    for i, p in enumerate(polygons):
        color_poz += 1
        if color_poz >= len(base_colors): color_poz = 0
        colors.append(base_colors[color_poz])
        color = colors[-1]
        color_edge = colors[-1]
        alpha = 0.7
        alpha_edge = 1
        parents_count = 0
        last_parent = 0
        spline_coef = 0.00001
        for j in range(0, i):
            p1 = polygons[j]
            p2 = pathes[j]
            point = next(filter(lambda x: x not in p1, p), None)
            if not point or p2.contains_point(point, radius=0.000000001):
                parents_count += 1
                last_parent = j
        if parents_count % 2:
            alpha = 1
            color = 'white'
            color_edge = colors[last_parent]
            color_poz -= 1
            spline_coef /= 10

        if splined:
            if len(p) > 4:
                x = np.array([p[-2][0]]+[p[-1][0]]+[t[0] for t in p]+[p[0][0]]+[p[1][0]])
                y = np.array([p[-2][1]]+[p[-1][1]]+[t[1] for t in p]+[p[0][1]]+[p[1][1]])
                tail = 3
            else:
                x = np.array([p[-1][0]]+[t[0] for t in p]+[p[0][0]])
                y = np.array([p[-1][1]]+[t[1] for t in p]+[p[0][1]])
                tail = 2

            multiple_coef = 10
            dist = np.sqrt((x[:-1] - x[1:]) ** 2 + (y[:-1] - y[1:]) ** 2)
            dist_along = np.concatenate(([0], dist.cumsum()))
            spline, u = scipy.interpolate.splprep([x, y], u=dist_along, s=spline_coef)

            interp_d = np.linspace(dist_along[0], dist_along[-1], len(p)*multiple_coef)
            interp_x, interp_y = scipy.interpolate.splev(interp_d, spline)

            start = 0
            finish = 1
            d = np.sqrt((interp_x[-finish] - interp_x[start]) ** 2 + (interp_y[-finish] - interp_y[start]) ** 2)
            for s in range(0, multiple_coef * tail):
                for f in range(1, multiple_coef * tail):
                    if len(interp_x) - f <= s:
                        continue
                    d1 = np.sqrt((interp_x[-f] - interp_x[s]) ** 2 + (interp_y[-f] - interp_y[s]) ** 2)
                    if d1 < d:
                        d = d1
                        start = s
                        finish = f

            if start == 0 and finish == 1:
                pass
            elif finish == 1:
                interp_x[start-1] = interp_x[-1]
                interp_y[start-1] = interp_y[-1]
                interp_x = interp_x[start-1:]
                interp_y = interp_y[start-1:]
            else:
                interp_x[-finish] = interp_x[start]
                interp_y[-finish] = interp_y[start]
                interp_x = interp_x[start:-finish+1]
                interp_y = interp_y[start:-finish+1]

            plt.fill(interp_x, interp_y, color=color, alpha=alpha)
            plt.plot(interp_x, interp_y, color=color_edge, lw=1, alpha=alpha_edge, solid_capstyle='round')
        else:
            x = np.array([t[0] for t in p]+[p[0][0]])
            y = np.array([t[1] for t in p]+[p[0][1]])

            plt.fill(x, y, color=color, alpha=alpha)
            plt.plot(x, y, color=color_edge, lw=1, alpha=alpha_edge)
    try:
        plt.title(head)
    except:
        plt.set_title(head)
        if ylabel:
            plt.set_ylabel(ylabel)
        if xlabel:
            plt.set_xlabel(xlabel)