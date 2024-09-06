import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import numpy.typing as npt
import time
import warnings
warnings.filterwarnings("error")

from atmosphere import Atmosphere
from rocket import Rocket, StageOne, StageTwo
from forces import g, aerodynamic_force, thirst_force, G, r0, M


def get_mach_val(
    v,
    v_s
):
    return v / v_s


def V1(
    h: float
)-> float:
    return np.sqrt(G * M / (r0 + h))


def get_vals(
    t: float, 
    v: float, 
    h: float,
    rt: Rocket,
    atm: Atmosphere
) -> tuple[float]:
    if h < 0.0: 
        raise KeyboardInterrupt("Negative H, error", h)
    
    if h <= 1200000.:
        mach = get_mach_val(v, atm.get_Vs(h))
        Cx = rt.get_aero_cf(mach, h)
        rho = atm.get_rho(h)

        D = aerodynamic_force(Cx, rho, v, rt.S)
        P_atm = atm.get_P(h)
    else:
        D = 0.
        P_atm = 0.

    if v > (V1(h) + 5) and rt.is_active:
        rt.is_active = False
        rt.inactive_time -= t
    elif not (v > (V1(h) + 5)) and not rt.is_active:
        rt.is_active = True
        rt.inactive_time += t


    m = rt.get_current_total_m(t)
    F = thirst_force(*rt.get_thirst_vals(t), P_atm)
    return (m, F, D)


def solver(
    rt: Rocket,
    atm: Atmosphere,
    t_span: tuple[float, float],
):
    t_ev = np.linspace(t_span[0], t_span[1], 1000000)
    tetha1 = 0.

    def func(t, vals):
        h = vals[0]
        s = vals[1]
        v = vals[2]
        tetha = vals[3]

        nonlocal tetha1
        t1 = 30.2
        t2 = rt.stage_one.engine_time
        t3 = rt.stage_two.engine_time / 5 + t2
        m, F, D = get_vals(t, v, h, rt, atm)

        dot_h = v * np.sin(tetha)
        dot_s = r0 / (r0 + h) * v * np.cos(tetha)
        dot_v = (F - D) / m - g(h) * np.sin(tetha)


        if 0. <= t <= t1:
            dot_tetha = 0.
        elif t1 < t <= t2:
            dot_tetha = -1 / 200 / np.sqrt(1 - (t / 200 - 1.15) ** 2)
        elif t2 < t <= t3 and F > 0.:
            dot_tetha = - 77 / 109 / np.sqrt(2500 * np.exp(2 * t / 109) - 5929)
        elif abs(tetha) >= 1e-3:
            dot_tetha = - ((g(h) / v - V1(270000) / (r0 + 270000)) * np.cos(tetha))
        else:
            tetha1 = tetha
            dot_tetha = - tetha1 / 10

        # print(f"t = {round(t, 2)}, h = {round(h, 1)}, v1 = {round(V1(h), 1)} v = {round(v, 1)}, theta = {round(tetha, 20)}, m = {round(m, 1)}, F = {round(F, 1)}, D = {round(D, 5)}")
        
        return np.array([dot_h, dot_s, dot_v, dot_tetha])
    
    sol = integrate.solve_ivp(func, t_span=t_span, y0=(0, 0, 0, np.pi / 2), t_eval = t_ev, max_step = 0.1)

    return sol


def find_active_idx(
    solution
)-> int:
    return np.where(solution.y[2] >= V1(solution.y[0][np.where(abs(solution.y[0] - max(solution.y[0])) <= 1e-2)[0][0]]))[0][0]
    


def coord_rotate(
    y_prev: float,
    angle: float
)-> tuple[float, float]:
    x_new = y_prev * np.sin(angle) 
    y_new = y_prev * np.cos(angle)
    return (x_new, y_new)


def find_geecentrical_coords(
    h: npt.NDArray,
    s: npt.NDArray,
) -> tuple[npt.NDArray, npt.NDArray]:
    angles = s / (2 * np.pi * r0)
    y_old = h + r0
    x, y = coord_rotate(y_old, angles)
    return x, y


def earth(
)-> tuple[float, float]:
    angle = np.linspace(0, 2 * np.pi, 100000)
    x = r0 * np.cos(angle)
    y = r0 * np.sin(angle)
    return (x, y)


def plot_portrait(
    solution,
) -> None:
    active = find_active_idx(solution)

    fig = plt.figure(figsize=(12,12))

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(solution.t[:active], solution.y[0][:active])
    ax1.set_xlabel('t, s')
    ax1.set_ylabel('h, m')
    ax1.set_title("Зависимость высоты от времени")
    ax1.grid(True)

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(solution.t[:active], solution.y[2][:active])
    ax2.set_xlabel('t, s')
    ax2.set_ylabel('v, m/s')
    ax2.set_title("Зависимость скорости от времени")
    ax2.grid(True)

    ax3 = fig.add_subplot(2, 2, 3)
    ax3.plot(solution.t[:active], solution.y[3][:active] / np. pi * 180)
    ax3.set_xlabel('t, s')
    ax3.set_ylabel('tetha, grad')
    ax3.set_title("Зависимость угла между веткором сокрости и горизонтом от времени")
    ax3.grid(True)

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.plot(solution.y[0][:active] / (10 ** 3), solution.y[2][:active])
    ax4.set_xlabel('h, km')
    ax4.set_ylabel('v, m/s')
    ax4.set_title("Зависимость скорости от высоты")
    ax4.grid(True)

    plt.show()


def plot_trajectory_geocentrical(
    x: npt.NDArray,
    y: npt. NDArray,
    idx: int
)-> None:
    fig = plt.figure(figsize=(12,12))

    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(x[:idx], y[:idx], color='r', label="Активный участок траектории")
    ax1.plot(x[idx:], y[idx:], color='g', label="Пассивный участок траеткори")
    ax1.plot(*earth(), color='b', linestyle="--", label="Планета Земля")
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title("Траектория полета")
    ax1.legend()
    ax1.grid(True)

    plt.show()


if __name__ == "__main__":
    st1 = StageOne()
    st2 = StageTwo()
    rocket = Rocket(stage_one=st1, stage_two=st2)
    atmosphere = Atmosphere()

    t_span = (0, 32900 + int(np.ceil(rocket.engine_time)))


    start = time.time()

    solution = solver(rocket, atmosphere, t_span)

    print(f"time = {time.time() - start}")
    plot_portrait(solution)

    x, y = find_geecentrical_coords(solution.y[0], solution.y[1])
    idx = find_active_idx(solution)
    plot_trajectory_geocentrical(x, y, idx)
    