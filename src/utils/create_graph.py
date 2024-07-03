from matplotlib import pyplot as plt
import matplotlib.dates as mdates


def create_3axis_graph(x, y1, y2, y3, x_label, y1_label, y2_label, y3_label, title, save_path):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    # ax3を別の位置に移動
    ax3.spines["right"].set_position(("outward", 60))

    ax1.plot(x, y1, color="r", label=y1_label)
    ax2.plot(x, y2, color="g", label=y2_label)
    ax3.plot(x, y3, color="b", label=y3_label)

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label, color="r")
    ax2.set_ylabel(y2_label, color="g")
    ax3.set_ylabel(y3_label, color="b")
    plt.title(title)

    # X軸の時間表示を調整
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H-%M"))

    # グラフの右側のスペースを確保
    fig.tight_layout(rect=[0, 0, 0.85, 1])

    plt.savefig(save_path, dpi=300)  # 解像度を高めるためにDPIを設定
