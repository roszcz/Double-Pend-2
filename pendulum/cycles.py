import numpy as np
import pandas as pd

from pendulum.solvers.hamiltonian import DoublePendulumHamiltonian


def default_state():
    state = {
        'g': 9.81,
        'm1': 1.0,
        'm2': 2.0,
        't1': np.pi/2,
        't2': 0.0,
        'L1': 2.0,
        'L2': 1.0,
        'w1': 0.0,
        'w2': 0.0
    }

    return state


def find_cycles():
    state = default_state()
    state['t2'] = np.pi/2

    results = []
    for it in range(10):
        state['w2'] = 0.00001 * it
        df = simulate_pendulum(state, steps=100_000, dt=1e-2)
        htf = get_cycles(df)
        ids = (htf.distance < 0.4) & (htf.long > 500)
        if ids.sum() > 0:
            result = {
                'df': df,
                'htf': htf,
                'best_cycle': htf[ids].iloc[0],
                'state': state
            }
            results.append(result)
            print('Found a cycle, ending the search')
            break
        print(it, 'part cycle search done!')
    return results


def simulate_pendulum(state, dt=1e-3, steps=10_000):
    g = state['g']
    m1 = state['m1']
    m2 = state['m2']
    t1 = state['t1']
    t2 = state['t2']
    L1 = state['L1']
    L2 = state['L2']
    w1 = state['w1']
    w2 = state['w2']

    hamiltonian = DoublePendulumHamiltonian(g, m1, m2, t1, t2, w1, w2, L1, L2)

    scores = []
    for it in range(steps):
        score = {
            'V': hamiltonian.potential_energy(),
            'K': hamiltonian.kinetic_energy(),
            'H': hamiltonian.mechanical_energy(),
            't1': hamiltonian.t1,
            't2': hamiltonian.t2,
            'p1': hamiltonian.p1,
            'p2': hamiltonian.p2
        }
        scores.append(score)
        hamiltonian.time_step(dt)

    df = pd.DataFrame(scores)

    def inject_cartesian(row):
        x1 = L1 * np.sin(row.t1)
        y1 = -L1 * np.cos(row.t1)
        x2 = x1 + L2 * np.sin(row.t2)
        y2 = y1 - L2 * np.cos(row.t2)
        result = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2
        }

        return pd.Series(result)

    df[['x1', 'y1', 'x2', 'y2']] = df.apply(inject_cartesian, axis=1)

    return df


def get_cycles(df):
    it = 0
    jt = 1
    results = []
    for _ in range(int(len(df)/2)):
        t = df.iloc[it]
        h = df.iloc[jt]
        # dist = (t.x1 - h.x1) ** 2 + (t.y1 - h.y1) ** 2 + (t.x2 - h.x2) ** 2 + (t.y2 - h.y2) ** 2
        dist = (t.t1 - h.t1) ** 2 + (t.t2 - h.t2) ** 2 + (t.p1 - h.p1) ** 2 + (t.p2 - h.p2) ** 2
        dist = np.sqrt(dist)
        result = {
            'tortoise': it,
            'hare': jt,
            'long': jt - it,
            'distance': dist
        }
        results.append(result)
        it += 1
        jt += 2

    # Haire tortoise frame
    htf = pd.DataFrame(results)
    htf = htf.sort_values('distance')
    return htf
