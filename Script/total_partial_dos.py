import numpy as np
import matplotlib.pyplot as plt

# POSCAR 파일 경로 지정
poscar_file = './remove_Br/DOS_calc_magmom/POSCAR'

# DOSCAR 파일 경로 지정
doscar_file = './remove_Br/DOS_calc_magmom/DOSCAR'

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
# Fermi_E = 0.14345278   # pristine
Fermi_E = 2.50203548   # remove_Br

# 원자별 색상 지정
colors = ['blue', 'green', 'orange', 'orange', 'orange', 'magenta', 'yellow', 'red']
atom_colors = {atom: colors[i % len(colors)] for i, atom in enumerate(atom_types)}

# 함수: 특정 구간의 DOSCAR 데이터를 읽어 PDOS 계산
def read_doscar_pdos(filename, start_line, end_line, Fermi_E):
    data = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if start_line <= i + 1 <= end_line:
                data.append(line.split())
    data = np.array(data, dtype=float)
    energy = data[:, 0] - Fermi_E  # Fermi 에너지 기준 이동
    dos_values = data[:, 1:19]          # DOS 데이터
    spin_up = np.sum(dos_values[:, ::2], axis=1)    # 짝수 열 합산 (Spin Up)
    spin_down = np.sum(dos_values[:, 1::2], axis=1) # 홀수 열 합산 (Spin Down)
    return energy, spin_up, spin_down

# 전체 Total DOS 계산 함수
def calculate_total_dos(filename, Fermi_E):
    data = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if 7 <= i + 1 < 1007:  # Total DOS는 DOSCAR 파일의 7~1006행에 위치
                data.append(line.split())
    data = np.array(data, dtype=float)
    energy = data[:, 0] - Fermi_E  # Fermi 에너지 기준 이동
    total_spin_up = data[:, 1]    # 스핀 업
    total_spin_down = data[:, 2]  # 스핀 다운
    return energy, total_spin_up, total_spin_down

# Total DOS 계산
total_energy, total_spin_up, total_spin_down = calculate_total_dos(doscar_file, Fermi_E)

# 각 원자별 PDOS 계산 및 플롯
plt.figure(figsize=(10, 8))
current_start_line = initial_start_line
current_end_line = initial_end_line

for atom, count in zip(atom_types, atom_counts):
    total_spin_up_atom = None
    total_spin_down_atom = None
    for _ in range(count):  # 해당 원자의 개수만큼 반복
        energy, spin_up, spin_down = read_doscar_pdos(doscar_file, current_start_line, current_end_line, Fermi_E)
        if total_spin_up_atom is None:
            total_spin_up_atom = spin_up
            total_spin_down_atom = spin_down
        else:
            total_spin_up_atom += spin_up
            total_spin_down_atom += spin_down
        # 라인 범위 갱신
        current_start_line += lines_per_atom
        current_end_line += lines_per_atom
    # 원자별 Spin Up/Down 플롯 및 내부 색 채우기
    plt.fill_between(energy, total_spin_up_atom, color=atom_colors[atom], alpha=0.2, label=f'{atom}')
    plt.fill_between(energy, -total_spin_down_atom, color=atom_colors[atom], alpha=0.2)
    plt.plot(energy, total_spin_up_atom, color=atom_colors[atom], linewidth=0.5)
    plt.plot(energy, -total_spin_down_atom, color=atom_colors[atom], linewidth=0.5)

# Total DOS 플롯
plt.fill_between(total_energy, total_spin_up, color='black', label='Total DOS', alpha=0.1)
plt.fill_between(total_energy, -total_spin_down, color='black', alpha=0.1)
plt.plot(total_energy, total_spin_up, color='black', linewidth=0.5)
plt.plot(total_energy, -total_spin_down, color='black', linewidth=0.5)

# Plot the Fermi level
plt.axvline(0, color='red', linestyle='--', linewidth=0.8, label='Fermi Level')

# 그래프 설정
plt.xlabel(r'$E - E_F\ \mathrm{(eV)}$', fontsize=20)
plt.ylabel('DOS (states/eV)', fontsize=20)
plt.xlim(-4, 6)
plt.ylim(-80, 80)
plt.tick_params(axis='x', labelsize=13)  # X축 숫자 크기
plt.tick_params(axis='y', labelsize=13)  # Y축 숫자 크기
plt.legend(fontsize=15, loc='upper right')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

