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

def plot_dos(energy, total_dos_up, total_dos_down, e_fermi):
    """
    Plot DOS for a single DOSCAR file with energy aligned to the Fermi level.
    """
    #energy_shifted = energy - e_fermi  # Shift energy relative to Fermi level
    energy_shifted = energy  # Shift energy relative to Fermi level

    plt.figure(figsize=(8, 6))

    # Fill the area under the spin-up DOS curve
    plt.fill_between(energy_shifted, total_dos_up, color='blue', alpha=0.1, label='Spin-up DOS')
    if total_dos_down is not None:
        plt.fill_between(energy_shifted, -total_dos_down, color='blue', alpha=0.1, label='Spin-down DOS')

    # Plot the outlines of the DOS curves
    plt.plot(energy_shifted, total_dos_up, color='blue', linewidth=0.5)
    if total_dos_down is not None:
        plt.plot(energy_shifted, -total_dos_down, color='blue', linewidth=0.5)

    # Plot the Fermi level
    plt.axvline(e_fermi, color='red', linestyle='--', linewidth=0.8, label=f'Fermi Level: {e_fermi:.3f} eV')

    # Labels and title
    plt.xlabel('Energy (eV)')
    plt.ylabel('DOS (states/eV)')
    plt.title('Density of States')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

# Example usage
filename = "./pristine/DOS_calc_magmom/DOSCAR"  # Path to your DOSCAR file

# Read data from the DOSCAR file
energy, total_dos_up, total_dos_down, e_fermi = read_doscar(filename)

# Plot the DOS from the single file
plot_dos(energy, total_dos_up, total_dos_down, e_fermi)

