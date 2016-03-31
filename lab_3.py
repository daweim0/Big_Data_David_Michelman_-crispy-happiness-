__author__ = 'david'


import numpy as np
import csv
import copy
import math
import scipy.stats as stats
import matplotlib.pyplot as plt


def main():
    raw_file = open('movies.csv')

    reader = csv.reader(raw_file)

    intermediate_data_list_because_csv_wont_tell_us_how_long_a_file_is = list()

    first_line = True

    for line in reader:
        if first_line:
            headers = line
            first_line = False
        else:
            intermediate_data_list_because_csv_wont_tell_us_how_long_a_file_is.append(line)

    data = np.zeros((len(headers), len(intermediate_data_list_because_csv_wont_tell_us_how_long_a_file_is)), dtype=object)

    # data array is structured as follows: data[data feild being accessed, n_movie]

    for line_n in range(len(intermediate_data_list_because_csv_wont_tell_us_how_long_a_file_is)):
        line_components = intermediate_data_list_because_csv_wont_tell_us_how_long_a_file_is[line_n]
        for i in range(len(line_components)):
            line_data = str(line_components[i])
            data[i][line_n] = line_data

    print('Level 1:')
    # calculate if movies that pass the bechdel test do worse than movies which don't
    print('movies that passed grossed ', filtered_average(data, 8, [[5, "PASS"]]))
    print('movies that failed grossed ', filtered_average(data, 8, [[5, "FAIL"]]))

    print('\n\n')
    print('Level 2:')
    print_correlation_array(data, headers)

    bar_graph(data, [4], 7, 'domestic gross by test result', 'average gross', headers)

    plt.show()


def bar_graph(data_array, index_x, index_y, title, y_title, headers):
    """
    Shows a plot of the passed data, plt.show() must be called after all calls of scatter_plot()
    :param data_array: data array (must be 2 dimensional)
    :param index_x: Coordinates for x axises (in form [x axis 1, x axis 2, x axis 3, ... x axis n]
    :param index_y: Coordinates for Y axis
    :param title: Title of graph
    :param y_title: Y axis title
    :param headers: the labels for the data
    :return: None
    """
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)


    # create list of all unique values in x_index

    x_values = find_unique_values(data_array, index_x[0])


    # The following code is from the matplotlib api reference.
    # It can be found here: http://matplotlib.org/examples/api/barchart_demo.html

    averages = list()
    for axis in index_x:
        averages.append(filtered_average(data_array, index_y, [axis, ]))

    ind = np.arange(len(index_x))  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects = list()
    for i in range(len(averages)):
        rects.append(ax.bar(ind, i, averages[i], color='r', yerr=1))

    # add some text for labels, title and axes ticks

    ax.set_xticks(ind + width)
    ax.set_xticklabels(headers)

    ax.legend(rects, ('Men', 'Women'))

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects)


    ax1.set_title(title + ')\n')
    ax1.set_ylabel(y_title)


def find_unique_values(data, axis):
    values = set()
    for i in data[axis]:
        values.update(i)
    return list(values)


def scatter_plot(data_array, index_x, index_y, title, x_title, y_title, compute_best_fit=False):
    """
    Shows a plot of the passed data, plt.show() must be called after all calls of scatter_plot()
    :param data_array: data array (must be 2 dimensional)
    :param index_x: Coordinates for x axis
    :param index_y: Coordinates for Y axis
    :param title: Title of graph
    :param x_title: X axis title
    :param y_title: Y axis title
    :param compute_best_fit: Should a best fit line be computed? (boolean)
    :return: None
    """
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.scatter(data_array[index_x], data_array[index_y])

    if compute_best_fit:
        sorted = list()
        for i in range(data_array.shape[1]):
            if not (math.isnan(data_array[index_x][i]) or math.isnan(data_array[index_y][i])):
                sorted.append([data_array[index_x][i], data_array[index_y][i]])

        #this line comes from Stephen on stack exchange
        # (http://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples)
        sorted.sort(key=lambda tup: tup[1])

        x = list()
        y = list()
        for i in sorted:
            x.append(i[0])
            y.append(i[1])

        # the next 3 lines come from DSM on stack exchange
        # (http://stackoverflow.com/questions/6148207/linear-regression-with-matplotlib-numpy)
        fit = np.polyfit(x, y, 1)
        fit_fn = np.poly1d(fit)
        plt.plot(x, y, 'yo', x, fit_fn(x), '--k')

        ax1.set_title(title + '\n ( correlation coefecient = ' + str(pearsonr_filtered(data_array[index_x], data_array[index_y])[0])
                      + ', regression slope = ' + str(fit_fn[1]) + ')\n')

    else:
        ax1.set_title(title + ')\n')
    ax1.set_xlabel(x_title)
    ax1.set_ylabel(y_title)


def filtered_average(data, target, constraints):
    """
    Calculates the average of columns in the passed numpy array data which meet some constraint
    :param constraints: columns which must equal some value (in form [[0, 2013], [3, FAIL]], which means
                        column 0 must equal 2013 and column 3 must equal FAIL).
    :param target: column to be averaged
    :param data: data array (must be 2 dimensional)
    :return: average value
    """

    sum = 0.0
    n = 0
    for line in range(data.shape[1]):
        failed = False
        for rule in constraints:
            if data[rule[0], line] != rule[1]:
                failed = True
        if failed is False:
            try:
                sum += float(data[target, line])
                n += 1
            except ValueError as e:
                pass  # data[target, line] probably can't be turned into a float
    try:
        return sum / n
    except ZeroDivisionError:
        raise ZeroDivisionError('no float data fit constraints in filtered_average([data], '
                                + str(target) + ' ' + str(constraints))


def print_correlation_array(data, headers):
    """
    Prints a matrix of the correlations between all different variables
    :param data: data array
    :param headers: array of header values
    :return: None
    """

    # TODO: make header_length changeable without messing up formatting

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Make copy of headers then make them all the same length
    headers_full = headers
    headers = copy.deepcopy(headers)
    header_length = 9
    for i in range(len(headers)):
        if len(headers[i]) > header_length:
            headers[i] = headers[i][0:header_length]
        while len(headers[i]) < header_length:
            headers[i] += ' '
    max_length = 0
    for i in headers_full:
        if len(i) > max_length:
            max_length = len(i)
    for i in range(len(headers_full)):
        while len(headers_full[i]) < max_length:
            headers_full[i] += ' '

    # first z dimension is z values, second z dimension is p values
    corelation_array = np.zeros([data.shape[0], data.shape[0]], dtype = np.float64)

    for i in range(corelation_array.shape[0]):
        for j in range(corelation_array.shape[1]):
            if j < i:
                corelation_array[i][j] = pearsonr_filtered(data[i], data[j])[0]
            else:
                corelation_array[i][j] = -2.0


    coloring_bound_upper = 0.5
    coloring_bound_lower = 0.3
    for i in range(len(headers_full[0])):
        print(' ', end='')
    print(HEADER + "      " + str(headers[0:-1]).replace("', '", ' ').replace("('", '').replace("['", '').replace("']", '') + ENDC)
    for i_num in range(1, len(corelation_array)):
        if i_num < 10:
            print(' ', end='')
        print(HEADER + str(i_num) + ' ' + headers_full[i_num] + ENDC, end='')
        i = corelation_array[i_num]
        for j_num in range(len(i)-1):
            j = i[j_num]
            if j_num > i_num - 1:
                if j_num > i_num:
                    print('    |     ', end='')
                else:
                    print('    \u25BC     ', end='')  # the escape code is for a triangle pointing down
            elif math.isnan(j):
                print('   nan   ', end=' ')
            elif j >= 0:
                if 1.0 > abs(j) > coloring_bound_upper:
                    print(OKGREEN + '   ' + '%.4f' % j + ENDC, end=' ')
                elif 1.0 > abs(j) > coloring_bound_lower:
                    print(OKBLUE + '   ' + '%.4f' % j + ENDC, end=' ')
                else:
                    print('   ' + '%.4f' % j, end=' ')
            else:
                if 1.0 > abs(j) > coloring_bound_upper:
                    print(OKGREEN + '  ' + '%.4f' % j + ENDC, end=' ')
                elif 1.0 > abs(j) > coloring_bound_lower:
                    print(OKBLUE + '   ' + '%.4f' % j + ENDC, end=' ')
                else:
                    print('  ' + '%.4f' % j, end=' ')
        print('   ' + HEADER + str(i_num) + ' ' + headers_full[i_num] + ENDC)
    print('\n')


def pearsonr_filtered(x, y):
    # remove any nan values from x and y
    x = list(copy.deepcopy(x))
    y = list(copy.deepcopy(y))

    initial_len = len(x)

    # a while loop is used instead of a for loop because the list of x changes during loop execution
    i = 0
    while i < len(x):
        try:
            if math.isnan(float(x[i])) or math.isnan(float(y[i])):
                x.pop(i)
                y.pop(i)
                i -= 1
        except ValueError as e:
            x.pop(i)
            y.pop(i)
            i -= 1
        except TypeError as e:
            x.pop(i)
            y.pop(i)
            i -= 1

        i += 1

    if len(x) < initial_len / 4.0:
        # There was not enough numerical data to do proper analysis on
        return math.nan, math.nan
    return stats.pearsonr(np.array(x).astype(np.float),  np.array(y).astype(np.float))



if __name__ == "__main__":
    main()