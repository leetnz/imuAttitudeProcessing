import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from plotters import PlotUpdate
import csv

FILE_PREFIX="bittle202112030054"

vidcap = cv2.VideoCapture(FILE_PREFIX+".h264")
success,image = vidcap.read()
count = 0

with plt.style.context("dark_background"):
    fig = plt.figure(figsize=(13, 5))
    gs = GridSpec(2, 3, figure=fig)

    axR = fig.add_subplot(gs[0, 0], polar=True)
    axP = fig.add_subplot(gs[1, 0], polar=True)
    axI = fig.add_subplot(gs[:, 1:])
    PlotUpdate(axR, axP, axI, 0, 0, image)
    fig.tight_layout()

videoDelayFrames = 13

with open(FILE_PREFIX+".log", "r") as f:
    csvData = list(csv.reader(f, delimiter=','))

    def animate(i):
        with plt.style.context("dark_background"):
            success, image = vidcap.read()
            if not success:
                return None

            try:
                data = csvData[videoDelayFrames + i]
                PlotUpdate(axR, axP, axI, float(data[6]), float(data[7]), image)
            except Exception as e:
                print(e)
                return None

        return axR, axP, axI,

    ani = animation.FuncAnimation(fig, animate, interval=40, save_count=len(csvData))

    # with plt.style.context("dark_background"):
    #     FFwriter = animation.FFMpegWriter(fps=25)
    #     ani.save('animation.mp4', writer = FFwriter)

    plt.show()

