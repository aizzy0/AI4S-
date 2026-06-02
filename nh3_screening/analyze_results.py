#!/usr/bin/env python3
"""
NH3 分解催化剂筛选 — 数据分析脚本
使用方法：
  python3 analyze_results.py --dir ./nh3_screening
"""

import os
import re
import argparse
import numpy as np

# Atomic reference energies for adsorption energy calculation
# 这些值需要根据你的 PBE 计算校准
REF_N2 = -16.65  # N2 molecule energy (eV), PBE reference
REF_H2 = -6.77   # H2 molecule energy (eV), PBE reference
REF_NH3 = -19.50 # NH3 molecule energy (eV), PBE reference

# Metal bulk energy per atom (PBE, eV/atom)
REF_NI = -5.57   # Ni bulk
REF_RU = -9.34   # Ru bulk (参考值，需要校准)


def read_oszicar(path):
    """读取 OSZICAR 获取最后的能量"""
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        lines = f.readlines()
    energy = None
    for line in reversed(lines):
        if 'E0=' in line:
            parts = line.split()
            for i, p in enumerate(parts):
                if p == 'E0=' and i + 1 < len(parts):
                    energy = float(parts[i+1])
                    break
            if energy is not None:
                break
    return energy


def read_dos_center(path, element, orbital='d'):
    """
    从 DOSCAR 中读取 d 带中心
    简化版本：需要配合 vaspkit 使用
    """
    # 实际使用需要 vaspkit 或手动积分
    # 这里提供占位逻辑
    return None


def read_contcar_for_analysis(path):
    """读取 CONTCAR 进行结构分析"""
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        content = f.read()
    # 提取原子位置
    lines = content.strip().split('\n')
    return {
        'content': content,
        'n_lines': len(lines),
    }


def analyze_system(base_dir, system_name):
    """分析一个体系的计算结果"""
    bare_e = read_oszicar(f"{base_dir}/01_bare/OSZICAR")
    n_ads_e = read_oszicar(f"{base_dir}/02_N_ads/OSZICAR")
    
    result = {
        'system': system_name,
        'E_bare': bare_e,
        'E_N_ads': n_ads_e,
        'dE_N': None,
        'status': 'incomplete',
    }
    
    if bare_e is not None and n_ads_e is not None:
        # ΔE_N = E(N/slab) - E(slab) - 1/2 E(N2)
        dE_N = n_ads_e - bare_e - 0.5 * REF_N2
        result['dE_N'] = dE_N
        result['status'] = 'completed'
    
    return result


def print_volcano_plot(results):
    """打印简单的火山图 ASCII 表示"""
    print("\n" + "="*70)
    print("NH3 分解催化活性火山图 (N* 吸附能筛选)")
    print("="*70)
    
    print(f"\n{'催化剂':<15} {'ΔE_N (eV)':<15} {'火山位置':<20} {'建议'}")
    print("-"*70)
    
    for r in sorted(results, key=lambda x: x.get('dE_N', 0) or 0):
        dE = r.get('dE_N')
        name = r['system']
        if dE is None:
            print(f"{name:<15} {'--':<15} {'计算未完成':<20} {'⏳'}")
            continue
        
        if dE < -1.0:
            volcano = "左支（结合过强）"
            suggestion = "❌ 表面毒化"
        elif dE < -0.5:
            volcano = "中左（较强结合）"
            suggestion = "⚠️ 可能合适"
        elif dE < -0.1:
            volcano = "🔥 火山顶附近"
            suggestion = "✅ 很有潜力"
        elif dE < 0.3:
            volcano = "中右（弱结合）"
            suggestion = "⚠️ 需要验证RDS"
        else:
            volcano = "右支（结合过弱）"
            suggestion = "❌ 难以活化NH3"
        
        print(f"{name:<15} {dE:<15.3f} {volcano:<20} {suggestion}")


def main():
    parser = argparse.ArgumentParser(description='NH3 分解催化剂 DFT 筛选结果分析')
    parser.add_argument('--dir', type=str, default='./nh3_screening',
                        help='筛选计算目录')
    parser.add_argument('--ref-n2', type=float, default=-16.65,
                        help='N2 分子能量 (eV)')
    args = parser.parse_args()
    
    # 更新参考能量
    global REF_N2
    REF_N2 = args.ref_n2
    
    # 扫描目录
    systems = []
    for d in sorted(os.listdir(args.dir)):
        dpath = os.path.join(args.dir, d)
        if os.path.isdir(dpath) and os.path.exists(f"{dpath}/01_bare"):
            systems.append((dpath, d))
    
    if not systems:
        print("❌ 未找到计算结果。请确认计算目录结构正确。")
        print("   预期结构: base_dir/sys_name/01_bare/OSZICAR")
        print(f"   执行目录: {args.dir}")
        return
    
    # 分析每个体系
    results = []
    for dpath, name in systems:
        result = analyze_system(dpath, name)
        results.append(result)
        en_str = f"{result['dE_N']:.3f} eV" if result['dE_N'] is not None else "N/A"
        status = "✅" if result['status'] == 'completed' else "⏳"
        print(f"  {status} {name:<15} ΔE_N = {en_str}")
    
    # 打印火山图
    print_volcano_plot(results)
    
    # 输出 CSV
    csv_path = os.path.join(args.dir, "screening_results.csv")
    with open(csv_path, 'w') as f:
        f.write("system,E_bare,E_N_ads,delta_E_N,status\n")
        for r in results:
            f.write(f"{r['system']},{r['E_bare']},{r['E_N_ads']},{r['dE_N']},{r['status']}\n")
    print(f"\n📊 结果已保存: {csv_path}")
    print("\n💡 下一步: 在 Excel 中打开 CSV 文件，绘制 ΔE_N 排序图")


if __name__ == "__main__":
    main()
