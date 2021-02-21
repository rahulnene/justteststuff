#### A simple 1-dimensional solver of the Kohn-Sham equation using DFT and a self-consistent loop
#### by Rahul Nene, I17PH012

import numpy as np
import matplotlib.pyplot as plt


is_harmonic = int(input("Enter 0 for a potential well or 1 for a harmonic oscillator: \n"))
if not is_harmonic:
    well_width = float(input("Please enter width of potential well (0-10 units):  \n")) / 2

# Generates grid and spacing
num_electron= int(input("How many electrons are present?  \n"))
n_grid = int(input("What is the resolution of the simulation?  \n"))
x = np.linspace(-5,5,n_grid)
h = x[1] - x[0]

t0 = perf_counter()


# Defines the differential operator: D_ij = (del_i+1,j - del_i,j)/h
D = np.diagflat(np.ones(n_grid-1),1) - np.eye(n_grid)
D /= h

# Defines the second differential operator: D2_i,j = - -D_i,k * D_j,k
D2=D.dot(-D.T) #Dot product of D with its transpose
D2[-1,-1] = D2[0,0] #Ensures the edge is well defined

# Defines integral function ydx
def integral(x,y):
    dx=x[1]-x[0]
    return np.sum(y*dx, axis=0) #Sum along column

#The potential energy (currently using a harmonic oscillator)
V = np.diagflat(x*x)


# Generates the density function n(x) given number of electrons and wavefunction
def get_nx(num_electron, psi, x):
    # Normalization of the wavefunction
    I = integral(x, psi ** 2)
    normed_psi = psi / np.sqrt(I)

    # Pairs electrons using Pauli's exclusion princtiple
    occ_num = [2 for _ in range(num_electron // 2)]
    if num_electron % 2:
        occ_num.append(1)

    # density
    res = np.zeros_like(normed_psi[:, 0])   # Creates a zero array the size of the number of rows in the wavefunction
    for ne, psi in zip(occ_num, normed_psi.T):
        res += ne * (psi ** 2)  # Adds the charge density contribution by each eigenfunction
    return res

# Calculates the exchange energy and potential in a tuple
def get_exchange(nx,x):
    energy=-3./4.*(3./np.pi)**(1./3.)*integral(x,nx**(4./3.))
    potential=-(3./np.pi)**(1./3.)*nx**(1./3.)
    return energy, potential

# Calculates the electrostatic potential and energy (using an epsilon to ensure convergence)
def get_hatree(nx,x, eps=1e-1):
    h=x[1]-x[0]
    energy=np.sum(nx[None,:]*nx[:,None]*h**2/np.sqrt((x[None,:]-x[:,None])**2+eps)/2)
    potential=np.sum(nx[None,:]*h/np.sqrt((x[None,:]-x[:,None])**2+eps),axis=-1)
    return energy, potential

# Calculates the free and non-interacting energies and eigenfunctions
eig_non, psi_non = np.linalg.eigh(-D2/2) # Gets the wavefunction for freely moving electrons
if is_harmonic:
    eig_harm, psi_harm = np.linalg.eigh(-D2/2 + V) # Gets the wavefunction for non-interacting electrons in a harmonic oscillator
else:
    w = np.full_like(x, 1e12)
    w[np.logical_and(x > -well_width, x < well_width)] = 0  # Defines a potential well
    eig_well, psi_well = np.linalg.eigh(-D2 / 2 + np.diagflat(w))  # Gets the wavefunction for non-interacting electrons in a potential well


#### Solving KS Equations using self-consistent loop ####

# Debug, used to check convergence
def print_log(i,log):
    print(f"step: {i:<5} energy: {log['energy'][-1]:<10.4f} energy_diff: {log['energy_diff'][-1]:.10f}")


# Defines iteration limit and tolerance for iterative calculation of energy
max_iter=1000
energy_tolerance=1e-5

# Debug
log={"energy":[float("inf")], "energy_diff":[float("inf")]}


# Initializes the density as zero
nx = np.zeros(n_grid)

# Start iterations
for i in range(max_iter):
    # Calculate Exchange and Hartree energies and potentials
    ex_energy, ex_potential = get_exchange(nx, x)
    ha_energy, ha_potential = get_hatree(nx, x)

    # Calculate Hamiltonian
    if is_harmonic:
        H_temp = ex_potential + ha_potential + x*x
    else:
        H_temp = ex_potential + ha_potential + w

    H = -D2 / 2 + np.diagflat(H_temp)

    # Calculate energy and eigenfunctions
    energy, psi = np.linalg.eigh(H)

    # Debug
    log["energy"].append(energy[0])
    energy_diff = energy[0] - log["energy"][-2]
    log["energy_diff"].append(energy_diff)
    print_log(i, log)

    # Check for convergence
    if abs(energy_diff) < energy_tolerance:
        print("Converged succesfully.") # Debug
        break

    # Update the density if not converged and restart with new density
    nx = get_nx(num_electron, psi, x)
else:
    print("Diverged. Try a different setup.") # Debug

print("Energy of ground state is: ", energy[0])
print("TIME TAKEN: ", perf_counter()- t0)

# Display Eigenfunctions
for i in range(int(input("Lower eigenstate:  \n")), int(input("Higher eigenstate:  \n"))+1):
    plt.plot(x,psi[:,i], label=f"{energy[i]:.4f}")
    plt.legend(loc=1)
plt.show()

# Display density function
plt.plot(nx, label="Actual")
plt.plot(get_nx(num_electron,psi_non,x), label="Free Electrons")
if is_harmonic:
    plt.plot(get_nx(num_electron, psi_harm, x), label="Non-Interacting")
else:
    plt.plot(get_nx(num_electron,psi_well,x), label="Non-Interacting")
plt.legend()
plt.show()

