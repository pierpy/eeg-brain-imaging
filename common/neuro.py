"""Modelli neuronali semplici per il corso EEG (numpy): Hodgkin-Huxley, integrate-and-fire, PSP, Nernst/GHK."""
import numpy as np

RT_F = 26.7   # mV a 37 °C (RT/F)


def nernst(cout, cin, z=1):
    return RT_F / z * np.log(cout / cin)


def ghk(pK, pNa, pCl, K=(5, 140), Na=(145, 12), Cl=(110, 10)):
    num = pK * K[0] + pNa * Na[0] + pCl * Cl[1]
    den = pK * K[1] + pNa * Na[1] + pCl * Cl[0]
    return RT_F * np.log(num / den)


def hh(I, T=50.0, dt=0.01, V0=-65.0):
    """Hodgkin & Huxley (1952), convenzione moderna (riposo -65 mV).
    I: funzione t->µA/cm² oppure costante. Restituisce t, V, m, h, n, gNa, gK."""
    gNa, gK, gL, ENa, EK, EL, C = 120.0, 36.0, 0.3, 50.0, -77.0, -54.387, 1.0
    am = lambda V: 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
    bm = lambda V: 4 * np.exp(-(V + 65) / 18)
    ah = lambda V: 0.07 * np.exp(-(V + 65) / 20)
    bh = lambda V: 1 / (1 + np.exp(-(V + 35) / 10))
    an = lambda V: 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
    bn = lambda V: 0.125 * np.exp(-(V + 65) / 80)
    n_ = int(T / dt); t = np.arange(n_) * dt
    V = np.empty(n_); m = np.empty(n_); h = np.empty(n_); n = np.empty(n_)
    V[0] = V0; m[0] = am(V0) / (am(V0) + bm(V0)); h[0] = ah(V0) / (ah(V0) + bh(V0)); n[0] = an(V0) / (an(V0) + bn(V0))
    If = I if callable(I) else (lambda tt: I)
    for k in range(n_ - 1):
        v = V[k]
        INa = gNa * m[k] ** 3 * h[k] * (v - ENa); IK = gK * n[k] ** 4 * (v - EK); IL = gL * (v - EL)
        V[k + 1] = v + dt * (If(t[k]) - INa - IK - IL) / C
        m[k + 1] = m[k] + dt * (am(v) * (1 - m[k]) - bm(v) * m[k])
        h[k + 1] = h[k] + dt * (ah(v) * (1 - h[k]) - bh(v) * h[k])
        n[k + 1] = n[k] + dt * (an(v) * (1 - n[k]) - bn(v) * n[k])
    return t, V, m, h, n, gNa * m ** 3 * h, gK * n ** 4


def alpha_psp(t, t0, tau=5.0, amp=1.0):
    """PSP a funzione alfa (ms)."""
    u = np.clip(t - t0, 0, None)
    return amp * (u / tau) * np.exp(1 - u / tau)


def lif(inp, dt=0.1, tau=20.0, Vr=-70.0, Vth=-55.0, Vreset=-75.0):
    """integrate-and-fire con ingresso in mV (già filtrato): restituisce V e tempi di spike."""
    V = np.full(len(inp), Vr); sp = []
    for k in range(1, len(inp)):
        V[k] = V[k - 1] + dt * (-(V[k - 1] - Vr) / tau) + inp[k] - inp[k - 1] * 0
        if V[k] >= Vth:
            sp.append(k); V[k] = 20.0
        elif V[k - 1] >= 20.0 - 1e-9:
            V[k] = Vreset
    return V, sp
