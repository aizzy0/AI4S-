#!/usr/bin/env python3
"""
通用能量台阶图生成器 (Energy Step Diagram Generator)
====================================================
适用于任意催化反应路径的多体系能垒对比图。
特点：白底四轴、莫兰迪色、水平平台+虚线连接、左上无边框图例。

用法：
  from step_diagram_generic import draw_multi_system_diagram, draw_step_diagram
  
  # 多体系对比
  draw_multi_system_diagram(systems_data, states, title, colors, output_path)
  
  # 单体系
  draw_step_diagram(steps, states, title, color, output_path)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# ============================================================
# 核心数据处理
# ============================================================
def get_all_energies(steps):
    """
    从 barrier + rxn 序列计算累积能量。
    
    Parameters
    ----------
    steps : list of dict
        [{'barrier': Ea_eV, 'rxn': ΔE_eV}, ...]
    
    Returns
    -------
    list[float]
        2N+1 个能量值: [IS1, TS1, FS1/IS2, TS2, FS2/IS3, TS3, FS3, ...]
    """
    E = [0.0]
    cumul = 0.0
    for s in steps:
        E.append(cumul + s['barrier'])  # TS
        cumul += s['rxn']
        E.append(cumul)                  # next IS / FS
    return E


# ============================================================
# 单体系台阶图
# ============================================================
def draw_step_diagram(steps, states, title, color, output_path,
                      ylabel='Relative Energy (eV)', label_ts=True,
                      ts_marker='D', dpi=200, figsize=(9, 5.5)):
    """
    画单体系台阶图。
    
    Parameters
    ----------
    steps : list of dict
        [{'barrier': ..., 'rxn': ...}, ...]
    states : list of str
        状态标签，长度 = 2*len(steps) + 1
    title : str
    color : str or list
        颜色（单色字符串，或每个状态一个颜色的列表）
    output_path : str
        输出文件路径
    ylabel : str
    label_ts : bool
        是否标注能垒值
    ts_marker : str
        TS 标记样式 ('D'菱形, 's'方块, 'o'圆点, '^'三角)
    dpi : int
    figsize : tuple
    """
    Es = get_all_energies(steps)
    n = len(states)
    pw = 0.30  # platform half-width
    x = np.arange(n) * 1.0
    
    fig, ax = plt.subplots(figsize=figsize, facecolor='white')
    ax.set_facecolor('white')
    
    # 水平平台
    for j in range(n):
        is_ts = (j % 2 == 1)
        c = color if isinstance(color, str) else color[j]
        ax.plot([x[j]-pw, x[j]+pw], [Es[j], Es[j]], '-', color=c,
                linewidth=3.0 if is_ts else 2.0, zorder=4, solid_capstyle='butt')
        if is_ts:
            ax.plot(x[j], Es[j], ts_marker, color=c, markersize=8, zorder=5,
                    markeredgecolor='white', markeredgewidth=1.0)
    
    # 虚线连接
    for j in range(n - 1):
        c = color if isinstance(color, str) else color[j]
        ax.plot([x[j]+pw, x[j+1]-pw], [Es[j], Es[j+1]], '--', color=c,
                linewidth=1.8, dashes=(6, 3), zorder=3, alpha=0.7)
    
    # TS 能垒标注
    if label_ts:
        for j in range(1, n, 2):
            barrier = Es[j] - Es[j-1]
            if barrier < 0.01:
                continue
            offset = 0.15 if Es[j] < max(Es) * 0.7 else -0.30
            va = 'bottom' if offset > 0 else 'top'
            ax.text(x[j], Es[j] + offset, f'{barrier:.2f} eV', fontsize=9,
                    color='#333333', ha='center', va=va, fontweight='bold')
    
    _apply_style(ax, x, states, title, ylabel, Es)
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f'Saved: {output_path}')
    plt.close()


# ============================================================
# 多体系对比台阶图
# ============================================================
def draw_multi_system_diagram(systems_data, states, title, colors_dict, output_path,
                               ylabel='Relative Energy (eV)', label_ts=True,
                               ts_markers=None, dpi=200, figsize=(9, 5.5)):
    """
    多体系对比台阶图。所有体系使用相同的状态标签。
    
    Parameters
    ----------
    systems_data : dict
        {sys_name: [{'barrier':..., 'rxn':...}, ...]}
        每个体系包含相同的 step 数（对应 states 长度）
    states : list of str
        状态标签，长度 = 2*len(steps_per_system) + 1
    title : str
    colors_dict : dict
        {sys_name: color_str}
    output_path : str
    ylabel : str
    label_ts : bool
    ts_markers : dict or None
        {sys_name: marker} 如 'D', 's', '^', 'o'
    """
    n = len(states)
    pw = 0.30
    x = np.arange(n) * 1.0
    
    if ts_markers is None:
        ts_markers = {name: 'D' for name in systems_data}
    
    fig, ax = plt.subplots(figsize=figsize, facecolor='white')
    ax.set_facecolor('white')
    
    all_Es = []
    for sys_name, steps in systems_data.items():
        Es = get_all_energies(steps)
        all_Es.extend(Es)
        color = colors_dict[sys_name]
        marker = ts_markers.get(sys_name, 'D')
        
        for j in range(n):
            is_ts = (j % 2 == 1)
            lw = 3.0 if is_ts else 2.0
            ax.plot([x[j]-pw, x[j]+pw], [Es[j], Es[j]], '-', color=color,
                    linewidth=lw, zorder=4, solid_capstyle='butt')
            if is_ts:
                ax.plot(x[j], Es[j], marker, color=color, markersize=7, zorder=5,
                        markeredgecolor='white', markeredgewidth=1.0)
                if label_ts:
                    barrier = Es[j] - Es[j-1]
                    if barrier >= 0.01:
                        ax.text(x[j], Es[j] + 0.15, f'{barrier:.2f}', fontsize=7.5,
                                color=color, ha='center', va='bottom', fontweight='bold')
        
        for j in range(n - 1):
            ax.plot([x[j]+pw, x[j+1]-pw], [Es[j], Es[j+1]], '--', color=color,
                    linewidth=1.5, dashes=(6, 3), zorder=3, alpha=0.55)
    
    _apply_style(ax, x, states, title, ylabel, all_Es)
    
    # 图例 — 左上无边框
    handles = [Line2D([0], [0], color=c, linewidth=2.5, label=n) 
               for n, c in colors_dict.items()]
    ax.legend(handles=handles, loc='upper left', fontsize=9.5, frameon=False,
              handlelength=1.5, labelspacing=1.2)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f'Saved: {output_path}')
    plt.close()


# ============================================================
# 内部样式函数
# ============================================================
def _apply_style(ax, x_ticks, labels, title, ylabel, energies):
    """统一设置四轴、白底、极淡网格"""
    ax.tick_params(axis='both', direction='in', colors='#444444',
                   top=True, right=True, labelsize=10)
    for spine in ax.spines.values():
        spine.set_color('#666666')
        spine.set_linewidth(0.8)
    ax.grid(axis='y', alpha=0.06, color='#999999', linestyle='-', zorder=0)
    ax.set_axisbelow(True)
    
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(labels, fontsize=11, color='#333333')
    ax.set_ylabel(ylabel, fontsize=11, color='#333333', labelpad=8)
    ax.set_title(title, fontsize=13, color='#333333', pad=12, fontweight='bold')
    
    # 自动 y 轴范围
    y_min, y_max = min(energies), max(energies)
    y_range = y_max - y_min
    ax.set_ylim(y_min - y_range * 0.12, y_max + y_range * 0.18)
    ax.set_xlim(x_ticks[0] - 0.8, x_ticks[-1] + 0.8)


# ============================================================
# 使用示例
# ============================================================
if __name__ == '__main__':
    # === 示例 1: 单体系 ===
    steps = [
        {'barrier': 0.92, 'rxn': 0.10},
        {'barrier': 0.61, 'rxn': 0.19},
        {'barrier': 0.59, 'rxn': -0.10},
    ]
    states = ['Reactant*', 'TS₁', 'Int₁*', 'TS₂', 'Int₂*', 'TS₃', 'Product*']
    draw_step_diagram(steps, states, 'Reaction Step Diagram', '#7B8FC0',
                      '/tmp/example_single.png')
    
    # === 示例 2: 多体系对比 ===
    sys_data = {
        'Catalyst A': [
            {'barrier': 1.64, 'rxn': 0.50},
            {'barrier': 1.96, 'rxn': 0.30},
        ],
        'Catalyst B': [
            {'barrier': 0.92, 'rxn': 0.10},
            {'barrier': 0.61, 'rxn': 0.19},
        ],
    }
    colors = {'Catalyst A': '#7B8FC0', 'Catalyst B': '#A88B7A'}
    states2 = ['A*', 'TS₁', 'B*', 'TS₂', 'C*']
    draw_multi_system_diagram(sys_data, states2, 'Catalyst Comparison',
                               colors, '/tmp/example_multi.png')
    
    print("Done! Example plots saved to /tmp/")
