#!/bin/bash
# ============================================
# NH3 分解催化剂 DFT 筛选 — 完整流程手册
# ============================================

echo "=========================================="
echo "  NH₃ 分解催化剂 DFT 计算筛选"
echo "  工作流 v1.0"
echo "=========================================="
echo ""

cat << 'EOF'

┌─────────────────────────────────────────────────────────────────┐
│                       工作流总览                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Phase 1: 结构准备                                               │
│   python3 generate_inputs.py                                    │
│   → 生成所有体系的 POSCAR / INCAR / KPOINTS                    │
│                                                                 │
│ Phase 2: 裸 slab 弛豫                                           │
│   每个体系运行 01_bare 目录下的 VASP                            │
│   → 获得 E(slab)                                                │
│                                                                 │
│ Phase 3: N 原子吸附计算                                         │
│   在弛豫后的 slab 上放置 N 原子，计算 E(N/slab)                │
│   → 获得 ΔE_N = E(N/slab) - E(slab) - 1/2 E(N₂)              │
│                                                                 │
│ Phase 4: 结果分析                                               │
│   python3 analyze_results.py --dir ./nh3_screening              │
│   → 生成筛选结果 CSV + 火山图                                   │
│                                                                 │
│ Phase 5 (可选): d 带中心分析                                    │
│   对候选体系运行 vaspkit 计算 d 带中心                          │
│   vaspkit -task 111                                             │
│                                                                 │
│ Phase 6 (可选): NEB 过渡态搜索 (Top 5)                          │
│   使用 VTST 工具进行 NEB 计算                                   │
│   安装: git clone https://github.com/henniggroup/VTSTscripts.git│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

EOF

echo ""
echo "📁 目录结构 (生成后):"
echo ""
echo "nh3_screening/"
echo "├── pure_Ni/"
echo "│   ├── 01_bare/"
echo "│   │   ├── POSCAR"
echo "│   │   ├── INCAR"
echo "│   │   ├── KPOINTS"
echo "│   │   ├── POTCAR (需手动链接)"
echo "│   │   └── run_vasp.sh"
echo "│   └── 02_N_ads/"
echo "│       ├── POSCAR (需手动放置N原子)"
echo "│       └── ..."
echo "├── Ni_Fe/"
echo "├── Ni_Co/"
echo "├── Ni_Cu/"
echo "├── Ni_Mo/"
echo "├── Ni_Ru/"
echo "├── analyze_results.py"
echo "└── generate_inputs.py"
echo ""
echo ""
echo "========== 使用方法 =========="
echo ""
echo "Step 1: 准备 POTCAR 库"
echo "  # 在集群上找到 POTCAR 路径，例如:"
echo "  export POTCAR_LIB=/path/to/potcars"
echo "  cat \$POTCAR_LIB/POTCAR_Ni \$POTCAR_LIB/POTCAR_Fe > nh3_screening/Ni_Fe/01_bare/POTCAR"
echo ""
echo "Step 2: 生成输入文件"
echo "  python3 generate_inputs.py"
echo ""
echo "Step 3: 修正 N 吸附的 POSCAR"
echo "  # 在 02_N_ads/POSCAR 中手动添加 N 原子到 fcc hollow 位"
echo "  # fcc hollow 位坐标: (0.33333, 0.16667, 0.25) 附近"
echo ""
echo "Step 4: 提交计算"
echo "  cd nh3_screening/Ni_Fe && sbatch run_vasp.sh"
echo ""
echo "Step 5: 分析结果"
echo "  python3 analyze_results.py --dir ./nh3_screening"
echo ""
echo "========== 计算资源建议 =========="
echo ""
echo "  每个体系: 32核, 48小时 (2天)"
echo "  30个体系: 约 2-3 轮提交"
echo "  总耗时: ~1周 (64核集群)"
echo ""
echo "========== 参考文献 =========="
echo ""
echo "  [1] Int. J. H2 Energy 2025 - 29 Ni-based alloys screening"
echo "  [2] J. Phys. Chem. C 2021 - Bimetallic screening workflow"
echo "  [3] J. Catal. 2005 - NH3 decomposition volcano"
echo "  [4] Nature Comm. 2023 - Ru/MgO(111) record activity"
echo ""
echo "=========================================="
