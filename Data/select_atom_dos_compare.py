import numpy as np
import matplotlib.pyplot as plt

# DOSCAR 파일 경로 지정
doscar_file1 = './pristine/DOS_calc_magmom/DOSCAR'
doscar_file2 = './remove_Br/DOS_calc_magmom/DOSCAR'

# 각 파일의 Fermi 에너지 지정
Fermi_E1 = 0.14345278
Fermi_E2 = 2.50203548

# 데이터 읽기 함수 정의
def read_doscar(filename, Fermi_E, start_line=1008, end_line=2007):
    data = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if start_line <= i + 1 <= end_line:
                data.append(line.split())
    data = np.array(data, dtype=float)
    energy = data[:, 0]
    dos_values = data[:, 1:19]  # DOS 데이터는 2열부터 19열까지
    spin_up_sum = np.sum(dos_values[:, ::2], axis=1)  # 짝수 열 합산
    spin_down_sum = np.sum(dos_values[:, 1::2], axis=1)  # 홀수 열 합산
    #return energy - Fermi_E, spin_up_sum, spin_down_sum  # Fermi_E 기준으로 에너지 이동
    return energy, spin_up_sum, spin_down_sum  # Fermi_E 기준으로 에너지 이동

# 두 개의 DOSCAR 파일 데이터 읽기
energy1, spin_up1, spin_down1 = read_doscar(doscar_file1, Fermi_E1)
energy2, spin_up2, spin_down2 = read_doscar(doscar_file2, Fermi_E2)

# 그래프 그리기
plt.figure(figsize=(12, 8))

# 첫 번째 DOSCAR 데이터 플롯
plt.plot(energy1, spin_up1, label='pristine', color='blue', linewidth=0.5)
plt.plot(energy1, -spin_down1, color='blue', linewidth=0.5)

# 두 번째 DOSCAR 데이터 플롯
plt.plot(energy2, spin_up2, label='remove_Br', color='orange', linewidth=0.5)
plt.plot(energy2, -spin_down2, color='orange', linewidth=0.5)

# 공통 Fermi 에너지 축 표시
#plt.axvline(x=0, color='red', linestyle='--', label='Fermi_E (0 eV)')
# Plot the Fermi levels for both files with labels
plt.axvline(Fermi_E1, color='blue', linestyle='--', linewidth=0.8, label=f'Fermi Level (pristine): {Fermi_E1:.3f} eV')
plt.axvline(Fermi_E2, color='orange', linestyle='--', linewidth=0.8, label=f'Fermi Level (remove_Br): {Fermi_E2:.3f} eV')
#plt.axhline(0, color='red', linewidth=0.3)

# 그래프 설정
plt.fill_between(energy1, spin_up1, color='blue', alpha=0.2)
plt.fill_between(energy1, -spin_down1, color='blue', alpha=0.2)
plt.fill_between(energy2, spin_up2, color='orange', alpha=0.2)
plt.fill_between(energy2, -spin_down2, color='orange', alpha=0.2)

plt.xlabel('Energy (eV)')
plt.ylabel('DOS (states/eV)')
plt.title('Density of States (MnBrNCH)')
plt.legend(loc='best', frameon=False)
plt.grid(True)

# 그래프 표시
plt.show()

