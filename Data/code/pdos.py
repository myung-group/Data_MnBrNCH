import numpy as np
import matplotlib.pyplot as plt

# POSCAR 파일 경로 지정
poscar_file = './pristine/DOS_calc_magmom/POSCAR'

# DOSCAR 파일 경로 지정
doscar_file = './pristine/DOS_calc_magmom/DOSCAR'

# 데이터 읽기
with open(poscar_file, 'r') as file:
    lines = file.readlines()

# 원자 유형 및 개수 추출
atom_types = lines[5].split()
atom_counts = list(map(int, lines[6].split()))

# 원자별 PDOS 계산을 위한 초기 라인 설정
initial_start_line = 1008  # 시작 라인
initial_end_line = 2007    # 끝 라인
lines_per_atom = 1001      # 원자당 증가할 라인 수

# Fermi 에너지 설정
Fermi_E = 2.50203548

# 원자별 색상 지정
colors = ['blue', 'green', 'orange', 'orange', 'orange', 'magenta', 'yellow', 'red']
atom_colors = {atom: colors[i % len(colors)] for i, atom in enumerate(atom_types)}

# 함수: 특정 구간의 DOSCAR 데이터를 읽어 PDOS 계산
def read_doscar_pdos(filename, start_line, end_line, fermi_energy):
    data = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if start_line <= i + 1 <= end_line:
                data.append(line.split())
    data = np.array(data, dtype=float)
    energy = data[:, 0] - fermi_energy  # Fermi 에너지 기준 이동
    dos_values = data[:, 1:19]          # DOS 데이터
    spin_up = np.sum(dos_values[:, ::2], axis=1)    # 짝수 열 합산 (Spin Up)
    spin_down = np.sum(dos_values[:, 1::2], axis=1) # 홀수 열 합산 (Spin Down)
    return energy, spin_up, spin_down

# 각 원자별 PDOS 계산 및 플롯
plt.figure(figsize=(12, 8))
current_start_line = initial_start_line
current_end_line = initial_end_line

for atom, count in zip(atom_types, atom_counts):
    total_spin_up = None
    total_spin_down = None
    for _ in range(count):  # 해당 원자의 개수만큼 반복
        energy, spin_up, spin_down = read_doscar_pdos(doscar_file, current_start_line, current_end_line, Fermi_E)
        if total_spin_up is None:
            total_spin_up = spin_up
            total_spin_down = spin_down
        else:
            total_spin_up += spin_up
            total_spin_down += spin_down
        # 라인 범위 갱신
        current_start_line += lines_per_atom
        current_end_line += lines_per_atom
    # 원자별 Spin Up/Down 플롯 및 내부 색 채우기
    plt.fill_between(energy, total_spin_up, color=atom_colors[atom], linewidth=0.8, alpha=0.2, label=f'{atom}')
    plt.fill_between(energy, -total_spin_down, color=atom_colors[atom], linewidth=0.8, alpha=0.2)

# Fermi 에너지 위치 표시
plt.axvline(x=0, color='black', linestyle='--', label='Fermi_E (0 eV)')

# 그래프 설정
plt.xlabel('E - E_Fermi) (eV)')
plt.ylabel('DOS (States/eV)')
plt.title('pristine')
plt.legend(loc='best', frameon=False)
plt.grid(True)

# 그래프 표시
plt.show()

