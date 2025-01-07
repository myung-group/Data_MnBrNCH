import numpy as np
import matplotlib.pyplot as plt

def read_doscar(filename):
    """
    Read DOSCAR file and extract energy, total DOS, and partial DOS (if available).
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Skip the header (first 6 lines)
    header = lines[:6]
    num_atoms = int(header[0].split()[0])
    e_fermi = float(header[5].split()[3])  # Fermi energy

    # Extract grid data
    nedos = int(header[5].split()[2])  # Number of DOS points
    dos_data = np.array([list(map(float, line.split())) for line in lines[6:6+nedos]])

    energy = dos_data[:, 0]  # Energy values
    total_dos_up = dos_data[:, 1]  # Total DOS (spin-up)
    total_dos_down = dos_data[:, 2] if dos_data.shape[1] > 2 else None  # Total DOS (spin-down)

    return energy, total_dos_up, total_dos_down, e_fermi

def plot_dos(energy1, total_dos_up1, total_dos_down1, e_fermi1,
             energy2, total_dos_up2, total_dos_down2, e_fermi2):
    """
    Plot DOS for two different DOSCAR files with energy aligned to the Fermi level.
    The DOS for both files will be plotted on the same graph.
    """
    #energy1_shifted = energy1 - e_fermi1  # Shift energy relative to Fermi level for first file
    #energy2_shifted = energy2 - e_fermi2  # Shift energy relative to Fermi level for second file
    energy1_shifted = energy1
    energy2_shifted = energy2

    plt.figure(figsize=(8, 6))

    # Fill the area under the spin-up DOS curve for the first file
    plt.fill_between(energy1_shifted, total_dos_up1, color='blue', alpha=0.1, label='pristine')
    if total_dos_down1 is not None:
        plt.fill_between(energy1_shifted, -total_dos_down1, color='blue', alpha=0.1)

    # Fill the area under the spin-up DOS curve for the second file
    plt.fill_between(energy2_shifted, total_dos_up2, color='orange', alpha=0.1, label='remove_Br')
    if total_dos_down2 is not None:
        plt.fill_between(energy2_shifted, -total_dos_down2, color='orange', alpha=0.1)

    # Plot the outlines of the DOS curves for both files
    plt.plot(energy1_shifted, total_dos_up1, color='blue', linewidth=0.5)
    if total_dos_down1 is not None:
        plt.plot(energy1_shifted, -total_dos_down1, color='blue', linewidth=0.5)

    plt.plot(energy2_shifted, total_dos_up2, color='orange', linewidth=0.5)
    if total_dos_down2 is not None:
        plt.plot(energy2_shifted, -total_dos_down2, color='orange', linewidth=0.5)

    # Plot the Fermi levels for both files
    #plt.axvline(0, color='red', linestyle='--', label='Fermi Level')
    #plt.axhline(0, color='red', linewidth=0.3)
    # Plot the Fermi levels for both files with labels
    plt.axvline(e_fermi1, color='blue', linestyle='--', linewidth=0.8, label=f'Fermi Level (pristine): {e_fermi1:.3f} eV')
    plt.axvline(e_fermi2, color='orange', linestyle='--', linewidth=0.8, label=f'Fermi Level (remove_Br): {e_fermi2:.3f} eV')

    
    plt.xlabel('Energy (eV)')
    plt.ylabel('DOS (states/eV)')
    plt.title('Density of States (MnBrNCH)')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

# Example usage
filename1 = "./pristine/DOS_calc_magmom/DOSCAR"  # Path to the first DOSCAR file
filename2 = "./remove_Br/DOS_calc_magmom/DOSCAR"  # Path to the second DOSCAR file

# Read data from both DOSCAR files
energy1, total_dos_up1, total_dos_down1, e_fermi1 = read_doscar(filename1)
energy2, total_dos_up2, total_dos_down2, e_fermi2 = read_doscar(filename2)

# Plot the DOS from both files on the same graph
plot_dos(energy1, total_dos_up1, total_dos_down1, e_fermi1,
         energy2, total_dos_up2, total_dos_down2, e_fermi2)
