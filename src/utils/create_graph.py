from matplotlib import pyplot as plt
import matplotlib.dates as mdates


def create_3axis_graph(x, y1, y2, y3, x_label, y1_label, y2_label, y3_label, title, save_path):
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.2)
    fig.subplots_adjust(right=0.85)
    fig.subplots_adjust(left=0.15)

    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    ax1.set_xlabel(x_label, fontsize=18)
    ax1.set_ylabel(y1_label, fontsize=18, color="red")
    ax2.set_ylabel(y2_label, fontsize=18, color="green")
    ax3.set_ylabel(y3_label, fontsize=18, color="blue")

    rspine = ax3.spines["right"]
    rspine.set_position(("axes", 1.2))

    ax1.plot(x, y1, color="red", label=y1_label)
    ax2.plot(x, y2, color="green", label=y2_label)
    ax3.plot(x, y3, color="blue", label=y3_label)

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    h3, l3 = ax3.get_legend_handles_labels()
    ax1.legend(h1 + h2 + h3, l1 + l2 + l3, loc="upper right")

    plt.title(title)

    # X軸の時間ラベルを一時間ごとに表示
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H-%M"))

    fig.autofmt_xdate()  # X軸のラベルを自動的にフォーマット

    plt.savefig(save_path, dpi=300)
