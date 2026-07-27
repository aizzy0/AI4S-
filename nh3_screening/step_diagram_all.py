#!/usr/bin/env python3
"""反应能量台阶图 — Co₁₃ vs RuCo₁₂ vs Ru₁₃ NH₃ → N₂"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# ========== 数据 ==========
# 每个 step: {'barrier': Ea, 'rxn': ΔE}
data = {
    'Co₁₃': [
        {'barrier': 6.667, 'rxn': 4.4424},
        {'barrier': 3.661, 'rxn': 3.6611},
        {'barrier': 0.000, 'rxn': -5.6675},
        {'barrier': 8.063, 'rxn': 1.5852},
    ],
    'RuCo₁₂': [
        {'barrier': 4.030, 'rxn': 1.7955},
        {'barrier': 3.020, 'rxn': 2.1646},
        {'barrier': 0.000, 'rxn': -4.3898},
        {'barrier': 7.175, 'rxn': -1.2853},
    ],
    'Ru₁₃': [
        {'barrier': 2.493, 'rxn': 2.3004},
        {'barrier': 4.856, 'rxn': 3.1338},
        {'barrier': 0.000, 'rxn': -4.0734},
        {'barrier': 10.914, 'rxn': 4.0956},
    ],
}

# 状态名称（9个状态 = 4步 × 2 + 1）
all_states = ['NH\u2083*', 'TS\u2081', 'NH\u2082*+H*', 'TS\u2082',
              'NH*+2H*', 'TS\u2083', 'N*+3H*', 'TS\u2084', 'N\u2082']

# 莫兰迪色系
colors = {'Co₁₃': '#C06C6C', 'RuCo₁₂': '#7BA07B', 'Ru₁₃': '#7B8FC0'}
sys_labels = list(data.keys())

def get_all_energies(steps):
    """barrier+rxn → 2N+1 个状态能量"""
    E = [0.0]
    cumul = 0.0
    for s in steps:
        E.append(cumul + s['barrier'])
        cumul += s['rxn']
        E.append(cumul)
    return E

n_states = len(all_states)
pw = 0.30           # 平台半宽
state_x = np.arange(n_states) * 1.0

fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
ax.set_facecolor('white')

for i, name in enumerate(sys_labels):
    Es = get_all_energies(data[name])
    color = colors[name]

    # 水平平台
    for j in range(n_states):
        xc, e = state_x[j], Es[j]
        ax.plot([xc-pw, xc+pw], [e, e], '-', color=color, linewidth=2.8,
                zorder=4, solid_capstyle='butt')

    # 虚线连接
    for j in range(n_states - 1):
        ax.plot([state_x[j]+pw, state_x[j+1]-pw], [Es[j], Es[j+1]], '--',
                color=color, linewidth=1.5, dashes=(6, 3), zorder=3)

    # TS 上标能垒 (奇数索引)
    for j in range(1, n_states, 2):
        barrier = Es[j] - Es[j-1]
        if barrier < 0.01:
            continue  # 无垒不标
        offset = 0.30 if Es[j] < 14 else -0.45
        va = 'bottom' if offset > 0 else 'top'
        ax.text(state_x[j], Es[j]+offset, f'{barrier:.2f}', fontsize=6.5,
                color=color, ha='center', va=va, fontweight='bold')

ax.set_xticks(state_x)
ax.set_xticklabels(all_states, fontsize=9, color='#333333')

# y 轴范围
all_e = [e for n in sys_labels for e in get_all_energies(data[n])]
e_min = min(all_e) - 0.8
e_max = max(all_e) + 1.0
ax.set_ylim(e_min, e_max)
ax.set_xlim(state_x[0]-pw-0.8, state_x[-1]+pw+1.2)

ax.set_ylabel('Relative Energy (eV)', fontsize=11, color='#333333', labelpad=8)

ax.tick_params(axis='both', direction='in', colors='#444444', top=True, right=True, labelsize=10)
for spine in ax.spines.values():
    spine.set_color('#666666')
    spine.set_linewidth(1.0)
ax.grid(axis='y', alpha=0.12, color='#bbbbbb', linestyle='-', zorder=0)
ax.set_axisbelow(True)

# 图例 — 左上角无边框, 带能量范围标注
legend_elements = []
for i, name in enumerate(sys_labels):
    Es = get_all_energies(data[name])
    rds = max(data[name], key=lambda s: s['barrier'])
    l = (f'{name}  |  RDS={rds["barrier"]:.2f} eV'
         if abs(rds['barrier'] - max(s['barrier'] for s in data[name])) < 0.001
         else f'{name}')
    legend_elements.append(Line2D([0], [0], color=colors[name], linewidth=2.5, label=f'{name}'))

# 在 RDS 标注中加 RDS 信息
handles = []
for name in sys_labels:
    handles.append(Line2D([0], [0], color=colors[name], linewidth=2.5, label=name))

# 添加 RDS 标注在下方
ax.legend(handles=handles, loc='upper left', fontsize=8.5, frameon=False,
          handlelength=1.5, labelspacing=1.2)

# 添加 RDS 说明文字
rds_text = ('RDS (N\u2082 coupling):\n'
            + '\n'.join(f'  {n}: {max(s["barrier"] for s in data[n]):.2f} eV'
                       for n in sys_labels))
ax.text(0.98, 0.22, rds_text, transform=ax.transAxes, fontsize=7,
        color='#555555', ha='left', va='top',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8f8f8', edgecolor='#cccccc', alpha=0.9))

outpath = '/home/ubuntu/catalyst-toolkit/results/nh3_step_diagram_all.png'
plt.tight_layout()
plt.savefig(outpath, dpi=200, bbox_inches='tight', facecolor='white')
print(f'Saved: {outpath}')
plt.close()
