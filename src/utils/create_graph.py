from matplotlib import pyplot as plt
import matplotlib.font_manager as fm


def create_3axis_graph(x, y1, y2, y3, x_label, y1_label, y2_label, y3_label, title, save_path):
    # 日本語対応フォントを設定
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # 例としてDejaVu Sansを使用
    font_prop = fm.FontProperties(fname=font_path)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    # Adjust right-side position of ax3
    ax3.spines["right"].set_position(("outward", 60))

    ax1.plot(x, y1, color="r", label=y1_label)
    ax2.plot(x, y2, color="g", label=y2_label)
    ax3.plot(x, y3, color="b", label=y3_label)

    ax1.set_xlabel(x_label, fontproperties=font_prop)
    ax1.set_ylabel(y1_label, color="r", fontproperties=font_prop)
    ax2.set_ylabel(y2_label, color="g", fontproperties=font_prop)
    ax3.set_ylabel(y3_label, color="b", fontproperties=font_prop)
    plt.title(title, fontproperties=font_prop)

    plt.savefig(save_path)
