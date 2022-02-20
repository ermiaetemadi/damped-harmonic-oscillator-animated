import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, TextBox, Button
from  matplotlib.animation import FuncAnimation

EPSILON = 0.001
ANIM_SPEED = 200

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
ax2.set_aspect('equal')
plt.subplots_adjust(bottom=0.2)
w0 = 3
b = 0.1
xi = 1
vi = 0
t_min, t_max = 0 ,10
FRAMES = int((t_max-t_min) / (ANIM_SPEED*EPSILON))



def submitw(omega0_t):
    global w0
    w0 = eval(omega0_t)
    t, x, v = damp(w0, b, xi, vi, t_max)
    p1.set_xdata(t)
    p1.set_ydata(x)
    p2.set_xdata(x)
    p2.set_ydata(v)
    ax1.relim()
    ax2.relim()
    ax1.autoscale_view()
    ax2.autoscale_view()
    plt.draw()


def submitb(beta_t):
    global b
    b = eval(beta_t)
    t, x, v = damp(w0, b, xi, vi, t_max)
    p1.set_xdata(t)
    p1.set_ydata(x)
    p2.set_xdata(x)
    p2.set_ydata(v)
    ax1.relim()
    ax2.relim()
    ax1.autoscale_view()
    ax2.autoscale_view()
    plt.draw()


def submitx(x0_t):
    global xi
    xi = eval(x0_t)
    t, x, v = damp(w0, b, xi, vi, t_max)
    p1.set_xdata(t)
    p1.set_ydata(x)
    p2.set_xdata(x)
    p2.set_ydata(v)
    ax1.relim()
    ax2.relim()
    ax1.autoscale_view()
    ax2.autoscale_view()
    plt.draw()


def submitv(v0_t):
    global vi
    vi = eval(v0_t)
    t, x, v = damp(w0, b, xi, vi, t_max)
    p1.set_xdata(t)
    p1.set_ydata(x)
    p2.set_xdata(x)
    p2.set_ydata(v)
    ax1.relim()
    ax2.relim()
    ax1.autoscale_view()
    ax2.autoscale_view()
    plt.draw()


def updatet(val):
    global t_max
    t_max = val
    global FRAMES
    FRAMES = int((t_max-t_min) / (ANIM_SPEED*EPSILON))
    t, x, v = damp(w0, b, xi, vi, t_max)
    p1.set_xdata(t)
    p1.set_ydata(x)
    p2.set_xdata(x)
    p2.set_ydata(v)
    ax1.relim()
    ax2.relim()
    ax1.autoscale_view()
    ax2.autoscale_view()
    plt.draw()


def anim_init():
    # ax1.set_xlim([t_min, t_max])
    ax1.autoscale_view()
    ax2.autoscale_view()
    ax2.set_aspect("equal")
    del x1data[:]
    del y1data[:]
    del x2data[:]
    del y2data[:]
    p1.set_data(x1data, y1data)
    p2.set_data(x2data, y2data)
    return p1, p2


def data_gen():
    n = FRAMES
    h = EPSILON
    t, x, v = damp(w0, b, xi, vi, t_max)
    for i in range(n):
        r = i * ANIM_SPEED
        yield t[r:r+ANIM_SPEED:2], x[r:r+ANIM_SPEED:2], v[r:r+ANIM_SPEED:2]

def update_frame(data):
    t, y1, y2 = data
    x1data.append(t)
    y1data.append(y1)
    x2data.append(y1)
    y2data.append(y2)
    p1.set_data(x1data, y1data)
    p2.set_data(x2data, y2data)
    return p1, p2


def run_animation(event):
    global anim
    anim = FuncAnimation (
    fig, update_frame, frames=data_gen, init_func=anim_init
    , interval = 1, blit=False, save_count=FRAMES, repeat=False)


    plt.show()


def damp(omega0=np.pi, beta=0.1, x0=1, v0=0, time=10, step=EPSILON):
    t = np.arange(0, time, step)
    if omega0 == beta:
        return t, np.exp(-beta*t), -beta*np.exp(-beta*t)

    omega = np.sqrt(omega0**2 - beta**2 + 0j)
    x = np.exp(-beta*t) * (x0 * np.cosh(1j*omega*t)
        - 1j*(v0/omega) * np.sinh(1j*omega*t))
    v = -beta * x + np.exp(-beta*t) * (1j*omega) * (
        x0 * np.sinh(1j*omega*t) - 1j*(v0/omega) * np.cosh(1j*omega*t))
    return t, x, v

x1data, y1data = [], []
x2data, y2data = [], []
t, x, v = damp(w0)
p1, = ax1.plot(t, x, 'blue')
p2, = ax2.plot(x, v, 'red')


axw = fig.add_axes([0.15, 0.09, 0.1, 0.04])
axb = fig.add_axes([0.3, 0.09, 0.1, 0.04])
axx = fig.add_axes([0.6, 0.09, 0.1, 0.04])
axv = fig.add_axes([0.75, 0.09, 0.1, 0.04])
axt = fig.add_axes([0.1, 0.025, 0.8, 0.04])
ax_play = fig.add_axes([0.45, 0.09, 0.1, 0.04])

boxw = TextBox(axw, r'$\omega_0$', initial='3')
boxb = TextBox(axb, r'$\beta$', initial='0.1')
boxx = TextBox(axx, r'$x_0$', initial='1')
boxv = TextBox(axv, r'$v_0$', initial='0')
slidert = Slider(axt, r'time', 1.0, 100, valinit=10, color='limegreen')
bplay = Button(ax_play, "Play")

boxw.on_submit(submitw)
boxb.on_submit(submitb)
boxx.on_submit(submitx)
boxv.on_submit(submitv)
slidert.on_changed(updatet)
bplay.on_clicked(run_animation)

plt.show()
