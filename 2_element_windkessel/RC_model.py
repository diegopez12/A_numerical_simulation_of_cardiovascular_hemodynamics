from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.pyplot import show, subplot_mosaic, subplots
from numpy import cbrt, ceil, exp, linspace, pi, searchsorted, sin
from scipy.integrate import solve_ivp, trapezoid

# To save the animation add FFMpegWriter to matplotlib.animation

R = 1.08  # Peripheral resistance [mmHg s/mL]
C = 1.75  # Compliance [mL/mmHg]
SV = 70  # Stroke volume [mL]
T = 0.8333  # Cardiac cycle duration
t_s = 0.4 * T  # Systole duration
Q_max = (pi * SV) / (2 * t_s)  # Maximum flow rate for this Q(t)

# I am starting the simulation at 5 time constants to ensure that
# the initial transient has decayed and the system is in a steady
# state.

N_beats = 30  # Number of beats to simulate
t_start = 5 * R * C
t_end = t_start + N_beats * T

fps = 30
resolution = 300
step = resolution // fps
t = linspace(t_start, t_end, int((t_end - t_start) * resolution) + 1)


# Unidirectional pulse wave (half sine) for aortic flow
def Q(t):
    # First aproximation of aortic flow (half sine while
    # systole and zero during diastole)
    t_c = t % T
    if t_c < t_s:
        return Q_max * sin(pi * t_c / t_s)  # Systole
    else:
        return 0.0  # Diastole


# Windkessel model 2 elements
def f(t, P):
    return Q(t) / C - P / (R * C)


sol = solve_ivp(
    f, t_span=[0, t_end], y0=[0], t_eval=t, max_step=0.01, dense_output=True
)


Q_int = [Q(i) for i in t]

# Figure 1: Flow vs time and Pressure vs time animation

window = 3 * T  # You can see 3 beats at a time

fig, axs = subplot_mosaic(
    [["Q", "V"], ["P", "V"]], figsize=(10, 5), width_ratios=[2, 1]
)
ax1, ax2, ax3 = axs["Q"], axs["P"], axs["V"]
ax2.sharex(ax1)

# Set up the circle representing the aortic volume
r = lambda P: cbrt(3 * C * P / (4 * pi))  # sphere volume = C·P
ball = Circle((0, 0), r(sol.y[0].max()), color="red")
ax3.add_patch(ball)
ax3.add_patch(
    Circle((0, 0), r(sol.y[0].min()), fill=False, ls="--")
)  # reference: diastolic size

lim = 1.2 * r(sol.y[0].max())
ax3.set_xlim(-lim, lim)
ax3.set_ylim(-lim, lim)

ax3.set_aspect("equal")
ax3.axis("off")

(line_Q,) = ax1.plot([], [])
(line_P,) = ax2.plot([], [])

# Limits are fixed to avoid rescaling during the animation
ax1.set_ylim(-0.05 * Q_max, 1.1 * Q_max)
ax2.set_ylim(sol.y[0].min() - 2, sol.y[0].max() + 2)

# Flow vs time
ax1.set_ylabel("Q [mL/s]")
ax1.set_title("Aortic flow")
ax1.grid(True)

# Pressure vs time
ax2.set_xlabel("t [s]")
ax2.set_ylabel("P [mmHg]")
ax2.set_title("Aortic pressure")
ax2.grid(True)

fig.tight_layout()


def animate(frame):
    i = frame * step  # index of the current time
    t_now = t[i]
    j0 = searchsorted(t, t_now - window)  # first index inside the window
    line_Q.set_data(t[j0 : i + 1], Q_int[j0 : i + 1])
    line_P.set_data(sol.t[j0 : i + 1], sol.y[0][j0 : i + 1])
    ax1.set_xlim(t_now - window, t_now)  # scroll (sharex moves ax2 too)
    ball.set_radius(r(sol.y[0][i]))
    return line_Q, line_P, ball


ani = FuncAnimation(
    fig,
    animate,
    frames=len(t) // step,
    interval=1000 / (fps * 0.8),  # At 80% of actual speed
    blit=False,
    repeat=False,
)

# This block saves the animation as a video file

# writer = FFMpegWriter(fps=fps * 0.8, bitrate=1800)  # 80% speed, same as on screen
# ani.save(
#    "windkessel.mp4",
#    writer=writer,
#    dpi=150,
#    progress_callback=lambda i, n: print(f"\rFrame {i + 1}/{n}", end="", flush=True),
# )
# print("\nSaved!")

show()

# ------------------------------------------------------------------------

# Figure 2:Pressure vs time (1 beat) compared to exp aproximation
# Westerhoff

k = int(ceil(t_start / T))  # first complete beat
t0 = k * T  # start of that beat
t_es = t0 + t_s  # aortic valve closes
t_ed = t0 + T  # end of diastole

# Simulated beat
t_beat = linspace(t0, t_ed, 500)
P_beat = sol.sol(t_beat)[0]  # this generates with dense_output=True
# and it returns the value of P at the requested time

# Westerhof prediction, diastole only
P_es = sol.sol(t_es)[0]
t_dia = linspace(t_es, t_ed, 200)
P_exp = P_es * exp(-(t_dia - t_es) / (R * C))

# Comparasion of the simulated beat with clinic parameters
P_sys = P_beat.max()  # systolic pressure
P_dia = P_beat.min()  # diastolic pressure
PP = P_sys - P_dia  # pulse pressure (amplitude)
MAP = trapezoid(P_beat, t_beat) / T
MAP_ref = 90  # mmHg
PP_ref = 40  # mmHg

print(f"Reference: MAP={MAP_ref:.1f} mmHg (120/80), PP={PP_ref:.1f} mmHg")
print(f"Simulated: MAP={MAP:.1f} mmHg ({P_sys:.0f}/{P_dia:.0f}), PP={PP:.1f} mmHg")


fig2, ax = subplots()
ax.plot(t_beat - t0, P_beat, label="Simulation")
ax.plot(t_dia - t0, P_exp, "r--", label=r"$P_{es}\,e^{-t/RC}$")
ax.axvline(t_s, color="gray", linestyle=":", label="Aortic valve closes")
ax.set_xlabel("Time [s]")
ax.set_ylabel("P [mmHg]")
ax.set_title("One steady-state beat")
ax.grid(True)
ax.legend()
show()
