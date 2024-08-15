import os
import subprocess
import ipywidgets
from IPython.display import display, SVG, Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

def do_nothing(one_argument): 
    return(one_argument)

dropbox_path = os.environ.get('DROPBOX_PATH')
def change_directory(path_string_windows_or_unix):
    os.chdir(fix_dropbox_location(path_string_windows_or_unix))

def translate_path(path_string_windows_or_unix):
    # For Mac, the OS is 'posix'.  For PC, the OS is "nt"
    directory_string = path_string_windows_or_unix.encode('unicode-escape').decode()
    if os.name == 'posix':
        directory_string = os.path.normpath(directory_string.replace(r'\\', '/'))
    return os.path.normpath(directory_string)

def fix_dropbox_location(path_string):
    # Adjust this function to use the 'dropbox_path' variable directly
    if dropbox_path and path_string.startswith("Dropbox"):
        p = path_string.replace("\\", "/")
        p = p.lower().replace("dropbox", "dropbox")  # This seems redundant as 'p' is already made lower case.
        p = p[p.find("dropbox"):]
        p = p[p.find("/"):]
        return translate_path(dropbox_path + p)
    else:
        return translate_path(path_string)

def double_click(path_or_file_string):
    # Resolve the full path before attempting to open
    full_path = fix_dropbox_location(path_or_file_string)

    try:
        if os.name == 'nt':  # Windows
            os.startfile(full_path)
        elif os.name == 'posix':  # Unix-like
            if 'darwin' in os.sys.platform:  # macOS
                subprocess.run(['open', full_path], check=True)
            else:  # Linux and others
                subprocess.run(['xdg-open', full_path], check=True)
    except Exception as e:
        print(f"Error opening file: {e}")

def double_click_button(file_name):
    # Resolve the full path before creating the button
    full_path = fix_dropbox_location(file_name)

    button = ipywidgets.Button(description=file_name, tooltip='Launch ' + file_name)
    display(button)

    def button_eventhandler(obj):
        # Use the resolved full path when the button is clicked
        double_click(full_path)
    
    button.on_click(button_eventhandler)

def display_graphic_file(file_name_with_path):
    if file_name_with_path.lower().endswith('.svg'):
        try:
            display(SVG(filename=file_name_with_path))
        except:
            print('SVG file is not displayable')
    else:
       try:
           display(Image(filename=file_name_with_path))
       except:
           print('graphic file is not displayable')

def list_plot(
    xydata_or_list_of_xydata,
    theoretical_curves_lambda_functions=[],
    points_for_theoretical_curves=100,
    title="",
    x_label="Anant will complain if you don't label your x-axis",
    y_label="",
    legend_data_labels=None,
    plot_limits=None,
    x_ticks=None,
    y_ticks=None,
    aspect_ratio=0,
    markers=["o", "^", "s", "v", "D", "*"],
    marker_sizes=5,
    colors=None,
    match_curve_colors=False,
    fill="none",
    major_tick_length=7,
    minor_tick_length=2,
    line_connect="none",  # Use this to specify the line style for theoretical curves
    save_svg=False,
    plot_show=True,
    flip_horizontal_axis=False,
    show_legend=True,
    error_bars=None,  # Percent error
    draw_spline_curve=False, # Works as a list
    connect_points=None, # Set to None to ensure default is not connecting points
    error_bars_data=False  # Use third column in dataset as error bars
):
    if isinstance(xydata_or_list_of_xydata, np.ndarray):
        data = [xydata_or_list_of_xydata]
    else:
        data = xydata_or_list_of_xydata

    if legend_data_labels is None:
        legend_data_labels = [f"Data {i+1}" for i in range(len(data))]
    elif not isinstance(legend_data_labels, list):
        legend_data_labels = [legend_data_labels]

    if isinstance(marker_sizes, int):
        marker_sizes = [marker_sizes] * len(data)

    if connect_points is None:
        connect_points = [False] * len(data)
    elif isinstance(connect_points, bool):
        connect_points = [connect_points] * len(data)

    if isinstance(line_connect, str):
        line_connect = [line_connect] * len(data)

    if fill is None:
        fill = ['none'] * len(data)
    elif isinstance(fill, str):
        fill = [fill] * len(data)

    if error_bars is not None and error_bars < 0:
        raise ValueError("Percent error must be a non-negative number.")

    if colors is None:
        colors = ['k', 'r', 'g', 'b']
    elif not isinstance(colors, list):
        colors = [colors]

    if len(theoretical_curves_lambda_functions) == 1 and len(data) > 1:
        print("Warning: Only one theoretical curve provided. It will be applied to all datasets.")
        theoretical_curves_lambda_functions *= len(data)
    elif len(theoretical_curves_lambda_functions) not in [0, len(data)]:
        raise ValueError("The number of theoretical curves must be either 0, 1, or equal to the number of datasets.")

    if len(theoretical_curves_lambda_functions) == 1:
        theoretical_curves_lambda_functions *= len(data)

    for i, dataset in enumerate(data):
        x = dataset[:, 0]
        y = dataset[:, 1]

        # Determine error values
        if error_bars_data:
            # Use the third column of the dataset as error bars
            error = np.abs(dataset[:, 2])
            print(f"Dataset {i+1} - Error bars (from third column): {error}")
        elif error_bars is not None:
            # Calculate error as a percentage of the absolute value of y
            error = (error_bars / 100.0) * np.abs(y)
            print(f"Dataset {i+1} - Percentage error: {error_bars}%")
        else:
            error = None

        # Plot data points separately
        plt.scatter(
            x, y, marker=markers[i % len(markers)],
            edgecolor=colors[i % len(colors)],
            facecolor='none' if fill[i % len(fill)] == 'none' else colors[i % len(fill)],
            s=marker_sizes[i % len(marker_sizes)]**2,
            label=legend_data_labels[i % len(legend_data_labels)]
        )

        # Plot error bars if error is provided
        if error is not None:
            plt.errorbar(
                x, y, yerr=error, fmt='none', ecolor=colors[i % len(colors)],
                elinewidth=1.5, capsize=5, capthick=1
            )

        # Connect data points if connect_points[i] is True
        if connect_points[i]:
            plt.plot(
                x,
                y,
                linestyle=line_connect[i % len(line_connect)],
                color=colors[i % len(colors)]
            )

    if theoretical_curves_lambda_functions:
        all_x_vals = np.hstack([d[:, 0] for d in data])
        x_min, x_max = all_x_vals.min(), all_x_vals.max()
        x_series = np.linspace(x_min, x_max, num=points_for_theoretical_curves)

        for i, func in enumerate(theoretical_curves_lambda_functions):
            theory_label = f'Theoretical fit {i+1}'
            curve_color = colors[i % len(colors)] if match_curve_colors else 'k'
            curve_style = line_connect[i % len(line_connect)] if line_connect else '--'
            plt.plot(x_series, func(x_series), linestyle=curve_style, color=curve_color, label=theory_label)
            legend_data_labels.append(theory_label)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if aspect_ratio != 0:
        all_x_vals = np.hstack([d[:, 0] for d in data])
        x_min, x_max = all_x_vals.min(), all_x_vals.max()
        x_range = x_max - x_min

        all_y_vals = np.hstack([d[:, 1] for d in data])
        y_min, y_max = all_y_vals.min(), all_y_vals.max()
        y_range = y_max - y_min

        plt.gca().set_aspect(aspect_ratio * (x_range / y_range), adjustable='box')

    if plot_limits:
        plt.axis(plot_limits)

    plt.minorticks_on()

    if x_ticks:
        plt.xticks(np.arange(x_ticks[0], x_ticks[1] + x_ticks[2], step=x_ticks[2]))

    plt.tick_params(axis="x", which="major", length=major_tick_length)
    plt.tick_params(axis="x", which="minor", length=minor_tick_length)

    if y_ticks:
        plt.yticks(np.arange(y_ticks[0], y_ticks[1] + y_ticks[2], step=y_ticks[2]))

    plt.tick_params(axis="y", which="major", length=major_tick_length)
    plt.tick_params(axis="y", which="minor", length=minor_tick_length)

    if flip_horizontal_axis:
        plt.gca().invert_xaxis()

    if draw_spline_curve:
        space = np.linspace(start=plt.xticks()[0][0], stop=plt.xticks()[0][-1], num=100)
        for i in range(len(data)):
            tck = scipy.interpolate.splrep(data[i][:, 0], data[i][:, 1], s=0)
            yfit = scipy.interpolate.splev(space, tck, der=0)
            plt.plot(
                space,
                yfit,
                label=("fit " + legend_data_labels[i % len(legend_data_labels)]),
                color=colors[i % len(colors)],
            )

    if show_legend:
        plt.legend(loc="best")

    if save_svg:
        plt.savefig(title + ".svg", format='svg')

    if plot_show:
        plt.show()   