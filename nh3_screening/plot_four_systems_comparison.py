#!/usr/bin/env python3
"""对比台阶图 — 4 systems, 按已有模板风格"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# ===== 数据（barrier + rxn 格式，匹配 get_all_energies） =====
systems = {}

# Co₁₃: S1=1.020(-4.702), S2=0.566(+0.566), S3=2.918(-1.007), 
#        S5_n2couple=1.525(-2.067), S6_desorp=0.090(-0.609)
systems['Co₁₃'] = {
    'nh3': [{'barrier':1.020,'rxn':-4.702}, {'barrier':0.566,'rxn':0.566}, {'barrier':2.918,'rxn':-1.007}],
    'n2':  [{'barrier':1.525,'rxn':-2.067}, {'barrier':0.090,'rxn':-0.609}],
}

# Ru₁₃: S1=1.322(+1.322), S2=2.438(-0.281), S3=1.106(-0.746),
#        S4(merged 2N→N₂(g))=0.182(-0.113)
systems['Ru₁₃'] = {
    'nh3': [{'barrier':1.322,'rxn':1.322}, {'barrier':2.438,'rxn':-0.281}, {'barrier':1.106,'rxn':-0.746}],
    'n2':  [{'barrier':0.182,'rxn':-0.113}],  # 一步完成
}

# Ru₁Co₁₂: S1=1.643(-5.674), S2=1.958(+0.645), S3=3.174(-2.123),
#           S5=1.233(-0.623), S6=0.013(-0.684)
systems['Ru₁Co₁₂'] = {
    'nh3': [{'barrier':1.643,'rxn':-5.674}, {'barrier':1.958,'rxn':0.645}, {'barrier':3.174,'rxn':-2.123}],
    'n2':  [{'barrier':1.233,'rxn':-0.623}, {'barrier':0.013,'rxn':-0.684}],
}

# Ru₁Co₁₂+Mg: S1=0.922(+0.101), S2=0.611(+0.186), S3=0.591(-0.102),
#              S5=1.725(+0.100), S6=0.679(+0.573)
systems['Ru₁Co₁₂+Mg'] = {
    'nh3': [{'barrier':0.922,'rxn':0.101}, {'barrier':0.611,'rxn':0.186}, {'barrier':0.591,'rxn':-0.102}],
    'n2':  [{'barrier':1.725,'rxn':0.100}, {'barrier':0.679,'rxn':0.573}],
}

# 莫兰迪色
colors = {'Co₁₃': '#7B8FC0', 'Ru₁₃': '#A88B7A', 'Ru₁Co₁₂': '#6B8E7B', 'Ru₁Co₁₂+Mg': '#B85450'}
# 标签、线型
styles = {'Co₁₃': ('-', 'o'), 'Ru₁₃': ('--', 's'), 'Ru₁Co₁₂': ('-.', '^'), 'Ru₁Co₁₂+Mg': (':', 'D')}

def get_all_energies(steps):
    """barrier+rxn → 2N+1 个状态能量"""
    E = [0.0]
    cumul = 0.0
    for s in steps:
        E.append(cumul + s['barrier'])
        cumul += s['rxn']
        E.append(cumul)
    return E

def draw_platform(ax, x, e, pw, color, ls, lw=3.0, ts_marker='D'):
    """水平平台"""
    ax.plot([x-pw, x+pw], [e, e], '-', color=color, linewidth=lw,
            zorder=4, solid_capstyle='butt')

def draw_dashed(ax, x1, x2, e1, e2, pw, color, ls='--', alpha=0.7):
    """虚线连接"""
    ax.plot([x1+pw, x2-pw], [e1, e2], '--', color=color, linewidth=1.8,
            dashes=(6, 3), zorder=3, alpha=alpha)

# ===========================
# Figure 1: NH₃ 脱氢
# ===========================
nh3_states = ['NH₃*', 'TS₁', 'NH₂*+H*', 'TS₂', 'NH*+2H*', 'TS₃', 'N*+3H*']
n_nh3 = len(nh3_states)
pw = 0.30

fig1, ax1 = plt.subplots(figsize=(9, 5.5), facecolor='white')
ax1.set_facecolor('white')
ax1.set_xlim(-0.8, n_nh3 - 1 + 0.8)

x_pos = np.arange(n_nh3) * 1.0

for sys_name in ['Co₁₃', 'Ru₁₃', 'Ru₁Co₁₂', 'Ru₁Co₁₂+Mg']:
    Es = get_all_energies(systems[sys_name]['nh3'])
    color = colors[sys_name]
    ls, marker = styles[sys_name]
    
    # 水平平台
    for j in range(n_nh3):
        draw_platform(ax1, x_pos[j], Es[j], pw, color, ls,
                      lw=3.0 if j%2==1 else 2.0)
        if j % 2 == 1:  # TS标记
            ax1.plot(x_pos[j], Es[j], marker, color=color, markersize=8, zorder=5,
                     markeredgecolor='white', markeredgewidth=1.0)
            # 能垒标注
            barrier = Es[j] - Es[j-1]
            e_val = Es[j]
            if sys_name == 'Co₁₃' and j == 3:
                offset, va = -0.30, 'top'
            elif sys_name == 'Co₁₃' and j == 5:
                offset, va = 0.20, 'bottom'
            elif sys_name == 'Ru₁₃' and j == 1:
                offset, va = 0.20, 'bottom'
            elif sys_name == 'Ru₁₃' and j == 3:
                offset, va = 0.20, 'bottom'
            elif sys_name == 'Ru₁Co₁₂' and j == 1:
                offset, va = 0.25, 'bottom'
            elif sys_name == 'Ru₁Co₁₂' and j == 5:
                offset, va = -0.35, 'top'
            elif sys_name == 'Ru₁Co₁₂+Mg':
                offset, va = 0.20, 'bottom'
            else:
                offset, va = 0.20, 'bottom'
            ax1.text(x_pos[j], e_val + offset, f'{barrier:.2f}', fontsize=7.5,
                    color=color, ha='center', va=va, fontweight='bold', zorder=6)
    
    # 虚线连接
    for j in range(n_nh3 - 1):
        draw_dashed(ax1, x_pos[j], x_pos[j+1], Es[j], Es[j+1], pw, color)

# 四轴
ax1.tick_params(axis='both', direction='in', colors='#444444', top=True, right=True, labelsize=10)
for spine in ax1.spines.values():
    spine.set_color('#666666')
    spine.set_linewidth(0.8)
ax1.grid(axis='y', alpha=0.06, color='#999999', linestyle='-', zorder=0)
ax1.set_axisbelow(True)

# 状态标签
ax1.set_xticks(x_pos)
ax1.set_xticklabels(nh3_states, fontsize=11, color='#333333')
ax1.set_ylabel('Relative Energy (eV) vs NH₃*', fontsize=11, color='#333333', labelpad=8)
ax1.set_title('NH₃ Dehydrogenation on CeO₂(111)', fontsize=13,
             color='#333333', pad=12, fontweight='bold')

# y轴自动
all_e = []
for sys_name in systems:
    all_e.extend(get_all_energies(systems[sys_name]['nh3']))
y1_min, y1_max = min(all_e), max(all_e)
y1_range = y1_max - y1_min
ax1.set_ylim(y1_min - y1_range*0.12, y1_max + y1_range*0.18)

# 图例左上无边框
handles1 = [Line2D([0],[0], color=colors[n], linewidth=2.5, label=n) for n in systems]
ax1.legend(handles=handles1, loc='upper left', fontsize=9.5, frameon=False,
           handlelength=1.5, labelspacing=1.2)

out1 = '/home/ubuntu/catalyst-toolkit/results/ceo2_four_systems_step_diagram_nh3.png'
plt.tight_layout()
plt.savefig(out1, dpi=200, bbox_inches='tight', facecolor='white')
print(f'Saved: {out1}')
plt.close()

# ===========================
# Figure 2: N₂ 偶联 + 脱附
# ===========================
n2_states_all = ['2N*', 'TS₅', 'N₂*', 'TS₆', 'N₂(g)']
n_n2 = len(n2_states_all)
x_n2 = np.arange(n_n2) * 1.0

fig2, ax2 = plt.subplots(figsize=(8, 4.5), facecolor='white')
ax2.set_facecolor('white')
ax2.set_xlim(-0.7, n_n2 - 1 + 0.7)

# 莫兰迪色 — N₂图用不同色调
n2_colors = {'Co₁₃': '#7B8FC0', 'Ru₁₃': '#A88B7A', 'Ru₁Co₁₂': '#6B8E7B', 'Ru₁Co₁₂+Mg': '#B85450'}

for sys_name in ['Co₁₃', 'Ru₁₃', 'Ru₁Co₁₂', 'Ru₁Co₁₂+Mg']:
    n2_steps = systems[sys_name]['n2']
    Es = get_all_energies(n2_steps)
    color = n2_colors[sys_name]
    ls, marker = styles[sys_name]
    
    n_states_actual = len(Es)
    # 对齐到 5 个状态
    if n_states_actual == 3:  # Ru₁₃: 只有2N*→TS→N₂(g)
        x_aligned = [x_n2[0], x_n2[1], x_n2[4]]
        Es_aligned = Es  # [0, barrier, rxn]
    elif n_states_actual == 5:  # 完整 5 状态
        x_aligned = x_n2
        Es_aligned = Es
    else:
        continue
    
    # 水平平台
    for i in range(len(x_aligned)):
        j = int(np.where(x_n2 == x_aligned[i])[0][0]) if x_aligned[i] in x_n2 else i
        is_ts = i % 2 == 1
        lw = 3.0 if is_ts else 2.0
        ax2.plot([x_aligned[i]-pw, x_aligned[i]+pw], [Es_aligned[i], Es_aligned[i]], '-',
                color=color, linewidth=lw, zorder=4, solid_capstyle='butt')
        if is_ts:
            ax2.plot(x_aligned[i], Es_aligned[i], marker, color=color, markersize=8, zorder=5,
                     markeredgecolor='white', markeredgewidth=1.0)
            # 能垒标注
            barrier = Es_aligned[i] - Es_aligned[i-1]
            ax2.text(x_aligned[i], Es_aligned[i] + 0.15, f'{barrier:.2f}', fontsize=8,
                    color=color, ha='center', va='bottom', fontweight='bold', zorder=6)
    
    # 虚线连接
    for i in range(len(x_aligned) - 1):
        ax2.plot([x_aligned[i]+pw, x_aligned[i+1]-pw], 
                [Es_aligned[i], Es_aligned[i+1]], '--',
                color=color, linewidth=1.8, dashes=(6,3), zorder=3, alpha=0.7)
    
    # Ru₁₃ 的特有虚线延长
    if sys_name == 'Ru₁₃' and n_states_actual == 3:
        # 从 N₂(g) 标记向左延伸到未知中间态
        ax2.plot([x_n2[1]+pw, x_n2[4]-pw], [Es[2], Es[2]], '--',
                color=color, linewidth=1.2, dashes=(2,3), zorder=2, alpha=0.3)

ax2.tick_params(axis='both', direction='in', colors='#444444', top=True, right=True, labelsize=10)
for spine in ax2.spines.values():
    spine.set_color('#666666')
    spine.set_linewidth(0.8)
ax2.grid(axis='y', alpha=0.06, color='#999999', linestyle='-', zorder=0)
ax2.set_axisbelow(True)

ax2.set_xticks(x_n2)
ax2.set_xticklabels(n2_states_all, fontsize=11, color='#333333')
ax2.set_ylabel('Relative Energy (eV) vs 2N*', fontsize=11, color='#333333', labelpad=8)
ax2.set_title('N₂ Coupling & Desorption on CeO₂(111)', fontsize=13,
             color='#333333', pad=12, fontweight='bold')

# y轴
all_n2_e = []
for sys_name in systems:
    all_n2_e.extend(get_all_energies(systems[sys_name]['n2']))
y2_min, y2_max = min(all_n2_e), max(all_n2_e)
y2_range = y2_max - y2_min
ax2.set_ylim(y2_min - y2_range*0.15, y2_max + y2_range*0.2)

handles2 = [Line2D([0],[0], color=n2_colors[n], linewidth=2.5, label=n) for n in systems]
ax2.legend(handles=handles2, loc='upper left', fontsize=9.5, frameon=False,
           handlelength=1.5, labelspacing=1.2)

out2 = '/home/ubuntu/catalyst-toolkit/results/ceo2_four_systems_step_diagram_n2.png'
plt.tight_layout()
plt.savefig(out2, dpi=200, bbox_inches='tight', facecolor='white')
print(f'Saved: {out2}')
plt.close()

print('Done!')
