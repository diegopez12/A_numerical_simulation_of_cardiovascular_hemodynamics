from matplotlib.pyplot import show, subplots
from numpy import ceil, exp, linspace, pi, sin
from scipy.integrate import solve_ivp

R = 0.7  # Peripheral resistance [mmHg s/mL]
C = 3.1  # Compliance [mL/mmHg]
SV = 70  # Stroke volume [mL]
T = 0.8333  # Cardiac cycle duration
t_s = 0.4 * T  # Systole duration
Q_max = (pi * SV) / (2 * t_s)  # Maximum flow rate
# for this Q(t)

# I am starting the simulation at 5 time constants to ensure that
# the initialtransient has decayed and the system is in a steady
# state.

t_start = 5 * R * C
t_end = 7 * R * C
t = linspace(t_start, t_end, 3000)


def Q(t):
    # First aproximation of aortic flow (half sine while
    # systole and zero during diastole)
    t_c = t % T
    if t_c < t_s:
        return Q_max * sin(pi * t_c / t_s)  # Systole
    else:
        return 0.0  # Diastole


def f(t, P):
    return Q(t) / C - P / (R * C)


sol = solve_ivp(
    f, t_span=[0, t_end], y0=[0], t_eval=t, max_step=0.01, dense_output=True
)

Q_int = [Q(i) for i in t]

# Figure 1:Flow vs time and Pressure vs time

fig, (ax1, ax2) = subplots(2, 1, sharex=True)

# flow
ax1.plot(t, Q_int)
ax1.set_ylabel("Q [mL/s]")
ax1.set_title("Aortic flow")
ax1.grid(True)

# pressure
ax2.plot(sol.t, sol.y[0])
ax2.set_xlabel("t [s]")
ax2.set_ylabel("P [mmHg]")
ax2.set_title("Aortic pressure")
ax2.grid(True)

fig.tight_layout()
show()

# Figure 2:Pressure vs time (1 beat) compared to exp aproximation
# Westerhoff

k = int(ceil(t_start / T))  # first complete beat inside the
# steady window
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
P_dia = P_es * exp(-(t_dia - t_es) / (R * C))

fig2, ax = subplots()
ax.plot(t_beat - t0, P_beat, label="Simulation")
ax.plot(t_dia - t0, P_dia, "r--", label=r"$P_{es}\,e^{-t/RC}$")
ax.axvline(t_s, color="gray", linestyle=":", label="Aortic valve closes")
ax.set_xlabel("Time [s]")
ax.set_ylabel("P [mmHg]")
ax.set_title("One steady-state beat")
ax.grid(True)
ax.legend()
show()
