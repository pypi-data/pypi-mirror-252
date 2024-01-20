

def save_report_example_usage():
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib_add_ons.save_report_tool import save_report_tool
    # Generating the data
    x = np.linspace(0, 2 * np.pi, 100)  # Create an array of 100 points from 0 to 2*pi
    y = np.sin(x)  # Compute the sine of each value

    # Create the figure and axis objects
    fig, ax = plt.subplots()
    list_of_figures = [fig]

    # Add save report tool
    save_report_tool(list_of_figures)

    # Plot the sine wave
    ax.plot(x, y)

    # Adding labels and title
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('A Sine Wave')

    # Show the plot
    plt.show()


def twinx_hover_example_usage():
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib_add_ons.twinx_hover import make_format

    # Sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x) * 10

    # Create a figure and axis
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # Plot data on the primary y-axis
    ax1.plot(x, y1, 'b-')
    ax1.set_ylabel('Primary Y-axis', color='b')
    ax1.tick_params('y', colors='b')

    # Plot data on the secondary y-axis
    ax2.plot(x, y2, 'r-')
    ax2.set_ylabel('Secondary Y-axis', color='r')
    ax2.tick_params('y', colors='r')

    # Set format for coordinate display
    ax2.format_coord = make_format(ax1, ax2)

    # Add labels and title
    plt.xlabel('X-axis')
    plt.title('Plot with Twin Axis')

    # Show the plot
    plt.show()


def event_stopper(stop_event):
    import time
    time.sleep(5)
    stop_event.set()


def close_plot_when_complete_example():
    import multiprocessing
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib_add_ons.misc_add_ons import close_plot_when_complete

    # Set up the figure and axis
    fig, ax = plt.subplots()
    xdata = np.linspace(0, 2 * np.pi, 1000)
    ydata = np.sin(xdata)
    line, = ax.plot(xdata, ydata)

    def update(frame):
        ydata = np.sin(xdata + frame * 0.1)  # Shift the sine wave
        line.set_ydata(ydata)

    # Create the FuncAnimation object
    ani = FuncAnimation(fig, update, frames=100, interval=50)

    stop_event = multiprocessing.Event()
    multiprocessing.Process(target=event_stopper, args=(stop_event,)).start()

    # Add the listener that closes the plot when it is complete
    close_plot_when_complete(stop_event=stop_event, animation_to_stop=ani, figure_to_close=fig)
    plt.show()


def annotation_and_copy_axis_to_clipboard_and_ask_close_example():
    from matplotlib_add_ons.copy_axis_to_clipboard import copy_axis_to_clipboard
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib_add_ons.annotations import annotator, redraw_annotations, get_annotations, put_annotations
    from matplotlib_add_ons.ask_close import ask_close

    # Set up the figure and axis
    fig, ax = plt.subplots()
    xdata = np.linspace(0, 2 * np.pi, 1000)
    ydata = np.sin(xdata)
    line, = ax.plot(xdata, ydata)

    def update(frame):
        ydata = np.sin(xdata + frame * 0.1)  # Shift the sine wave
        line.set_ydata(ydata)

    # Create the FuncAnimation object
    ani = FuncAnimation(fig, update, frames=100, interval=50)

    # Add the annotator
    list_of_annotators = annotator([fig])

    # Some other functions you might need... (most likely implemented in another section of the code)
    # If you clear the axes or redraw them
    redraw_annotations(list_of_annotators)

    # If you want the annotations in a dictionary form:
    annotations = get_annotations(list_of_annotators)
    # if you want to put the annotations from a dictionary form:
    put_annotations(annotations, list_of_annotators)

    # Copy axis to clipboard setup
    copy_axis_to_clipboard([fig])

    # Ask Close
    ask_close([fig])

    plt.show()


if __name__ == '__main__':
    # save_report_example_usage()
    # twinx_hover_example_usage()
    # close_plot_when_complete_example()
    annotation_and_copy_axis_to_clipboard_and_ask_close_example()
