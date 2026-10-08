import sys, json; sys.path.insert(0, '/tmp/claude-0/-home-user-iconic/118b864e-7445-5af4-819d-cfe4bc0666d5/scratchpad/task15/build')
from engine import *
from fractions import Fraction as F
E = load('/tmp/claude-0/-home-user-iconic/118b864e-7445-5af4-819d-cfe4bc0666d5/scratchpad/task15/raw')
draw = {R: alloc(E, R - 1)[0] for R in range(2020, 2027)}
tp = {R: transition(draw[R - 1], draw[R]) for R in range(2021, 2027)}
est = {y: estabs(E, y) for y in range(2017, 2026)}
proj25 = {c: rnd(F(draw[2024][c]) * F(est[2024][c], est[2023][c])) for c in C}
h1_26, k84 = alloc(E, 2025, qualify=False)
back = {R: alloc(E, R - 1, qualify=False)[0] for R in (2023, 2024, 2025)}
assert all(back[R] == draw[R] for R in back), 'distractor backtest must tie on 2023-2025'
d_tp = transition(draw[2025], h1_26)
out = dict(draw=draw, tp=tp, proj25=proj25, h1_26=h1_26, d_tp=d_tp, est=est)
json.dump(out, open('/tmp/claude-0/-home-user-iconic/118b864e-7445-5af4-819d-cfe4bc0666d5/scratchpad/task15/build/figures.json', 'w'), indent=1, default=str)
print('Medina 2024, proj 2025, actual 2025:', draw[2024]['Medina'], proj25['Medina'], draw[2025]['Medina'])
print('distractor 2026 notices:', {c: v for c, v in d_tp.items() if v}, ' golden:', {c: v for c, v in tp[2026].items() if v})
print('2025 projection misses %:', {c: round((draw[2025][c] - proj25[c]) / proj25[c] * 100, 1) for c in C})
