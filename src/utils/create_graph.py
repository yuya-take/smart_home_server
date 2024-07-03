from matplotlib import pyplot as plt


def create_3axis_graph(x, y1, y2, y3, x_label, y1_label, y2_label, y3_label, title, save_path):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    ax1.plot(x, y1, color="r", label=y1_label)
    ax2.plot(x, y2, color="g", label=y2_label)
    ax3.plot(x, y3, color="b", label=y3_label)

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label, color="r")
    ax2.set_ylabel(y2_label, color="g")
    ax3.set_ylabel(y3_label, color="b")
    plt.title(title)

    plt.savefig(save_path)
