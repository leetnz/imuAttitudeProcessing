from matplotlib import axes
import numpy as np
import cv2

def plotAngle(ax : axes, theta : float, label : str):
    ax.cla()
    ax.plot([-theta + np.pi, -theta],[1, 1])
    ax.set_rmax(1)
    ax.set_rticks([])
    ax.set_thetamax(180)
    ax.set_thetamin(-180)
    ax.set_thetagrids(np.arange(180, -180, -30))
    ax.set_theta_direction(1)
    ax.set_theta_offset(theta)
    ax.set_ylabel(label, labelpad=40.0)

def plotFrame(ax: axes, r: float, p: float, image):
    ax.cla()
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    ax.set_xticks([])
    ax.set_yticks([])

    # Get video bounding boxed
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Offset based on having a field of view of 41 degrees vertical
    yFull = np.max(ax.get_ylim())
    radFov = np.pi * 41 / 180
    pixPerRad = yFull/radFov

    xcenter = np.mean(ax.get_xlim())
    ycenter = np.mean(ax.get_ylim()) + -p * pixPerRad
    
    xroll = np.array([xcenter, xcenter]) + np.cos(-r) * np.array([-2000, 2000])
    yroll = np.array([ycenter, ycenter]) + np.sin(-r) * np.array([-2000, 2000])

    l, = ax.plot(xroll, yroll)
    l.set_color("white")

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

def PlotUpdate(axR : axes, axP : axes, axI : axes, r : float, p: float, image):
    plotAngle(axR, r, "Roll")
    plotAngle(axP, p, "Pitch")
    plotFrame(axI, r, p, image)
    