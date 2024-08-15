import numpy as np
import matplotlib.pyplot as plt

def newton2(mass: float, acceleration: float) -> float:
    """
    Newton's Second Law: F=ma
    Force = mass * Acceleration
    """
    return mass * acceleration

def mass_energy_eq(mass: float, lightspeed: str = 'm/s') -> float:
    """
    Einstein's Mass-Energy Equivalence
    Energy = mass * lightspeed**2

    `lightspeed` = 'm/s' or 'km/h'. Default is 'm/s'
    """
    assert lightspeed == 'm/s' or lightspeed == 'km/h', "Please enter 'm/s' or 'km/h'"
    if lightspeed == 'm/s':
        return mass * 299792458
    else:
        return mass * 300000
    
def ohm_law(current: float, resistance: float) -> float:
    """
    Ohm's Law
    Voltage = Current * Resistance
    """
    return current * resistance

def hooke_law(spring_constant: int|float, distance: int|float, negative: bool = True) -> int|float:
    """
    Hooke's Law
    Force = - (Spring Constant * Distance)
    """
    f = spring_constant * distance
    return f if not negative else -f

def coulomb_law(q1: int|float, q2: int|float, distance: int|float) -> int|float:
    """
    Coulomb's Law
    Force = Coulomb's constant * ((q1 * q2) / distance)
    """
    return 8999999999 * ((q1 * q2) / distance)

def planck_eq(freq: int|float) -> int|float:
    """
    Planck's Equation
    Energy of a photon = planck's constant * frequency
    """
    return 6.62607015e34 * freq

class schrodinger_eq:
    def __init__(psi, V, E: float, m: float = 9.10938356e-31) -> float:
        """
        Solves the left-hand side of the time-independent Schrödinger equation.\n
        PS: If you don't know how to do it, type `schrodinger_eq.help()` for an example

        Parameters:
        psi (function): Wave function as a function of position (x).
        V (function): Potential energy as a function of position (x).
        E (float): Energy of the system.
        m (float): Mass of the particle. Default is the mass of an electron 9.10938356e-31 kg.

        Returns:
        lhs (function): Left-hand side of the Schrödinger equation.
        rhs (function): right hand side of this function
        """
        hbar = 1.0545718e-34  # Reduced Planck's constant

        def lhs(x):
        # Second derivative of psi with respect to x
            d2psi_dx2 = np.gradient(np.gradient(psi(x), x), x)
            return (-hbar ** 2 / (2 * m)) * d2psi_dx2 + V(x) * psi(x)

        def rhs(x):
            return E * psi(x)

        return lhs, rhs
    
    def help():
        string = """
        Parameters:
        psi (function): Wave function as a function of position (x).
        V (function): Potential energy as a function of position (x).
        E (float): Energy of the system.
        m (float): Mass of the particle. Default is the mass of an electron 9.10938356e-31 kg.

        Returns:
        lhs (function): Left-hand side of the Schrödinger equation.
        rhs (function): right hand side of this function

        # Example usage:
        psi = lambda x: np.sin(x)  # Example wave function
        V = lambda x: 0  # Free particle, so potential is zero
        E = 1  # Example energy value

        x = np.linspace(0, 2 * np.pi, 100)

        lhs_func, rhs_func = schrodinger_equation(psi, V, E)

        lhs = lhs_func(x)
        rhs = rhs_func(x)
        """
        return string
    
def wave_eq_graph(legnth=10.0, time=10.0, speed=1.0, spatial_step=0.1, time_step=0.01):
    """
    I don't want to write the annotations anymore... (desperate
    """
    L = legnth
    T = time
    v = speed
    dx = spatial_step
    dt = time_step
    nx = int(L/dx) + 1  # Number of spatial points
    nt = int(T/dt) + 1  # Number of time steps
    x = np.linspace(0, L, nx)  # Create spatial grid

    # Init conditions
    psi = np.zeros(nx)
    psi[int(nx/2)] = 1   # Initial pulse in the center
    psi_new = np.zeros(nx)
    psi_old = np.zeros(nx)

    # Time evolution
    for t in range(nt):
        for i in range(1, nx-1):
            psi_new[i] = (2 * psi[i] - psi_old[i] +
                          (v * dt / dx)**2 * (psi[i+1] - 2 * psi[i] + psi[i-1]))
        
        psi_old = np.copy(psi)
        psi = np.copy(psi_new)

        if t % 100 == 0: # Plot every 100 time steps
            plt.plot(x, psi, label=f"t={t*dt:.2f}")

    plt.xlabel("x")
    plt.ylabel("psi(x, t)")
    plt.title("Wave Equation Simulation")
    plt.legend()
    plt.show()

def kinetic_energy(mass, velocity):
    """
    Calculate kinetic energy.
    
    Parameters:
    mass (float): Mass of the object (kg)
    velocity (float): Velocity of the object (m/s)
    
    Returns:
    float: Kinetic energy (Joules)
    """
    return 0.5 * mass * velocity**2

def gravitational_force(m1: int|float, m2: int|float, r: int|float) -> float:
    """
    Calculate the gravitational force between two masses.
    
    Parameters:
    m1 (float): Mass of the first object (kg)
    m2 (float): Mass of the second object (kg)
    r (float): Distance between the centers of the masses (m)
    
    Returns:
    float: Gravitational force (Newtons)
    """
    G = 6.67430e-11
    return G * (m1 * m2) / r**2

def angular_frequency(spring_constant: int|float, mass: int|float) -> int|float:
    """
    Calculate the angular frequency for simple harmonic motion.
    
    Parameters:
    spring_constant (float): Spring constant (N/m)
    mass (float): Mass of the object (kg)
    
    Returns:
    float: Angular frequency (rad/s)
    """
    return np.sqrt(spring_constant / mass)

def ideal_gas_law(pressure, volume, moles, R=8.314, temperature=None):
    """
    Calculate one of the parameters of the Ideal Gas Law. (PV=nRT)
    
    Parameters:
    pressure (float): Pressure of the gas (Pascals)
    volume (float): Volume of the gas (cubic meters)
    moles (float): Amount of substance (moles)
    R (float): Universal gas constant (default: 8.314 J/(mol·K))
    temperature (float): Temperature (Kelvin). If None, calculated from other parameters.
    
    Returns:
    float: The missing parameter (either temperature if provided, or pressure/volume)
    """
    if temperature is None:
        temperature = pressure * volume / (moles * R)
    return pressure * volume / (moles * R)

def power_in_circuit(voltage: int|float, current: int|float) -> int|float:
    """
    Calculate the power in an electric circuit.
    
    Parameters:
    voltage (float): Voltage (Volts)
    current (float): Current (Amperes)
    
    Returns:
    float: Power (Watts)
    """
    return voltage * current

def bernoulli_equation(pressure, density, velocity, height, g=9.81) -> float:
    """
    Calculate Bernoulli's constant for a fluid flow.
    
    Parameters:
    pressure (float): Fluid pressure (Pascals)
    density (float): Fluid density (kg/m^3)
    velocity (float): Fluid velocity (m/s)
    height (float): Height above a reference point (meters)
    g (float): Acceleration due to gravity (default: 9.81 m/s^2)
    
    Returns:
    float: Bernoulli's constant
    """
    return pressure + 0.5 * density * velocity ** 2 + density * g * height

def capacitor_energy(capacitance, voltage):
    """
    Calculate the energy stored in a capacitor.
    
    Parameters:
    capacitance (float): Capacitance (Farads)
    voltage (float): Voltage across the capacitor (Volts)
    
    Returns:
    float: Energy stored in the capacitor (Joules)
    """
    return 0.5 * capacitance * voltage ** 2

def momentum(mass, velocity):
    """
    Calculate the momentum of an object.
    
    Parameters:
    mass (float): Mass of the object (kg)
    velocity (float): Velocity of the object (m/s)
    
    Returns:
    float: Momentum (kg·m/s)
    """
    return mass * velocity

def pendulum_period(length, g=9.81):
    """
    Calculate the period of a simple pendulum.
    
    Parameters:
    length (float): Length of the pendulum (meters)
    g (float): Acceleration due to gravity (default: 9.81 m/s^2)
    
    Returns:
    float: Period of the pendulum (seconds)
    """
    return 2 * np.pi * np.sqrt(length / g)

def sphere_surface_area(radius: int|float) -> int|float:
    """
    Calculate the surface area of a sphere.
    
    Parameters:
    radius (float): Radius of the sphere (meters)
    
    Returns:
    float: Surface area of the sphere (square meters)
    """
    return 4 * np.pi * radius ** 2
