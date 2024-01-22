import numpy as np
from pydantic import BaseModel

k = 0.01720209895
def kepToCart(kepler, m0):
    """
    This function transforms an objects kepler coordinates to cartesian coordinates provided by Max Zimmermann
    
    Args:
        kepler (numpy.array): orbital elements and mass of object
        m0 (float): mass of primary object
    
    Returns:
        (tuple): tuple containing:
            pos (numpy.array): transformed cartesian position of object
            vel (numpy.array): transformed cartesian velocity of object
    """

    k2 = np.square(0.01720209895)
    igrad = 180/np.pi
    
    M = kepler[5]/igrad
    ecentric = M
    pos = np.zeros(3)
    vel = np.zeros(3)
    
    acc=1.
    e = kepler[1]
    
    while(acc>1e-13):
        ecentric =  e * np.sin(ecentric) + M
        acc = np.absolute(ecentric - e * np.sin(ecentric) - M)

    nu = 2 * np.arctan(np.sqrt((1+e)/(1-e)) * np.tan(ecentric/2))
    a = kepler[0]
    r = a * (1-e * np.cos(ecentric))
    mu = k2 * (m0 + kepler[6])
    h = np.sqrt(mu * a * (1 - np.square(e)))
    p = a * (1 - np.square(e))

    node = kepler[4]/igrad
    per = kepler[3]/igrad
    inc = kepler[2]/igrad
    
    pos[0] = r * (np.cos(node) * np.cos(per + nu) - np.sin(node) * np.sin(per + nu) * np.cos(inc))
    pos[1] = r * (np.sin(node) * np.cos(per + nu) + np.cos(node) * np.sin(per + nu) * np.cos(inc))
    pos[2] = r * (np.sin(inc) * np.sin(per + nu))

    vel[0] = (pos[0] * h * e * np.sin(nu)) / (r * p) - (h/r) * (np.cos(node) * np.sin(per + nu) + np.sin(node) * np.cos(per + nu) * np.cos(inc))
    vel[1] = (pos[1] * h * e * np.sin(nu)) / (r * p) - (h/r) * (np.sin(node) * np.sin(per + nu) - np.cos(node) * np.cos(per + nu) * np.cos(inc))
    vel[2] = (pos[2] * h * e * np.sin(nu)) / (r * p) + (h/r) * (np.sin(inc) * np.cos(per + nu))

    return pos, vel

#def cartToKep(x1,v1,x0,v0,m0,m1):
def cartToKep(x1,v1,m0,m1):
    """
    This function transforms an objects cartesian coordinates to kepler coordinates provided by Max Zimmermann
    
    Args:
        x1 (numpy.array): position of object in cartesian coordinates
        v1 (numpy.array): velocity of object in cartesian coordinates
        m0 (float): mass of primary object
        m1 (float): mass of object
    
    Returns:
        numpy.array: orbital elements of object
    """

    k2 = np.square(k)
    igrad = 180/np.pi
    
    kepler = np.zeros(7)
    
    u = np.zeros((3,3))
    #r = x1-x0
    #v = v1-v0
    r = x1
    v = v1

    cappaq = m0 + m1

    l = np.cross(r,v)
    rscal = np.linalg.norm(r)
    l2 = np.dot(l,l)
    lprojxy = np.sqrt(np.square(l[0]) + np.square(l[1]))
    lrl = np.cross(v,l)

    lrl = [lrl[i]/(k2*cappaq)-r[i]/rscal for i in range(len(lrl))]
    oM = np.arctan2(l[0],-l[1]) * igrad
    if(oM < 0):
        oM = oM + 360
    inc = np.arctan2(lprojxy, l[2]) * igrad

    e = np.linalg.norm(lrl)

    if(e < 1e-11):
        e = 0
        e2 = 0
        om = 0
    else:
        e2 = np.square(e)

    a = l2/(cappaq * k2 * (1-e2))
    node = np.zeros(3)
    node[0] = -l[1] * l[2]
    node[1] = l[0] * l[2]
    node[2] = 0
    nscal = np.linalg.norm(node)

    if(inc < 1e-11):
        oM = 0
        om = np.arccos(lrl[0]/np.linalg.norm(lrl))
        if(lrl[1] < 0):
            om = 360 - om * igrad
        else:
            om = om * igrad
    else:
        h = np.cross(l,node)
        hnorm = np.linalg.norm(h)
        om = np.arctan2(np.dot(lrl,h) * nscal, np.dot(lrl,node) * hnorm) * igrad
        #if(om < 0):
            #om = om + 360

    if(e < 1e-11 and inc <= 1e-11):
        oM = 0
        om = 0
        mmm = np.arctan2(r[1],r[0]) * igrad
        #if (mmm < 0):
            #mmm = mmm + 360
    elif (e < 1e-11 and inc > 1e-11):
        h = np.cross(l,node)
        hnorm = np.linalg.norm(h)
        for j in range(len(node)):
            u[j][0] = node[j]/nscal
            u[j][1] = h[j]/hnorm
            u[j][2] = l[j]/np.sqrt(l2)

        ru = np.linalg.solve(u,r)
        tAn = np.arctan2(ru[1],ru[0])
        mmm = tAn * igrad
        #if (mmm < 0):
            #mmm = mmm + 360
    elif(inc < 1e-11 and e > 1e-11):
        h = np.cross(l,lrl)
        hnorm = np.linalg.norm(h)
        tAn = np.arctan2(np.dot(h,r) * e, np.dot(lrl,r) * hnorm)
        cosen = (e + np.cos(tAn))/(1+e*np.cos(tAn))
        sinen = np.sqrt(1 - e2) * np.sin(tAn)/(1 + e * np.cos(tAn))
        eanom = np.arctan2(sinen,cosen)

        mmm = (eanom - e * sinen) * igrad
        #if(mmm<0):
            #mmm = mmm + 360
    else:

        h = np.cross(l,lrl)
        hnorm = np.linalg.norm(h)
        for j in range(len(lrl)):
            u[j][0] = lrl[j]/e
            u[j][1] = h[j]/hnorm
            u[j][2] = l[j]/np.sqrt(l2)

        ru = np.linalg.solve(u,r)
        tAn = np.arctan2(ru[1],ru[0])
        cosen = (e + np.cos(tAn))/(1 + e * np.cos(tAn))
        sinen = np.sqrt(1 - e2) * np.sin(tAn)/(1 + e * np.cos(tAn))
        eanom = np.arctan2(sinen, cosen)

        mmm = (eanom - e * sinen) * igrad
        #if(mmm < 0):
            #mmm = mmm + 360

    #if (om >= 360):
        #om = om - 360
    #if (oM >= 360):
        #oM = oM - 360

    #if (mmm >= 360):
        #mmm = mmm - 360
            
    #kepler[0] = a
    #kepler[1] = e
    #kepler[2] = inc
    #kepler[3] = om
    #kepler[4] = oM
    #kepler[5] = mmm
    #kepler[6] = m1
    kepler = a,e,inc,om,oM,mmm,m1

    return kepler

def calculate_acceleration(positions, masses):
    """
    This function calculates the accelerations of the objects involved in the N-body problem
    
    Args:
        positions (numpy.array): positions of objects
        masses (numpy.array): masses of objects
    
    Returns:
        numpy.array: accelerations of objects
    """
    k = 0.01720209895
    G = k * k
    acceleration = np.zeros((len(positions), 3))
    for i in range(len(positions)):
        for j in range(len(positions)):
            if i != j and masses[j] != 0:  # if not massless
                r = positions[i] - positions[j]
                acceleration[i] -= G * masses[j] * r/np.linalg.norm(r)**3
                
    return acceleration

def calculate_derivatives(state, masses):
    """
    This function calculates the derivative quantities of the objects involved in the N-body problem
    
    Args:
        state (numpy.array): states of objects (positions, velocities)
        masses (numpy.array): masses of objects
    
    Returns:
        numpy.array: derivative quantities of objects
    """
    num_bodies = len(masses)
    positions = state[:num_bodies]
    velocities = state[num_bodies:]
    accelerations = calculate_acceleration(positions, masses) 
    return np.concatenate([velocities, accelerations])

def move_to_barycenter(positions, velocities, masses):
    """
    This function corrects the positions of the objects involved in the N-body problem to barycenter positions
    
    Args:
        positions (numpy.array): positions of objects
        velocities (numpy.array): velocities of objects
        masses (numpy.array): masses of objects
    
    Returns:
        (tuple): tuple containing:
            positions (numpy.array): barycenter corrected positions of objects
            velocities (numpy.array): barycenter corrected velocities of objects
    """
    total_mass = np.sum(masses)
    barycenter = np.sum(positions * masses[:, np.newaxis], axis = 0)/total_mass
    positions -= barycenter
    velocities -= np.sum(velocities * masses[:, np.newaxis], axis = 0)/total_mass
    return positions, velocities

def rk4_n_body(time_step, num_steps, initial_positions, initial_velocities, masses):
    """
    This function calculates the Runge-Kutta 4th order scheme of the objects involved in the N-body problem
    
    Args:
        time_step (float): time-step of integration
        num_steps (int): number of steps of integration
        initial_positions (numpy.array): initial positions of objects
        initial_velocities (numpy.array): initial velocities of objects
        masses (numpy.array): masses of objects
    
    Returns:
        (tuple): tuple containing:
            positions (numpy.array): positions of objects after integration
            velocities (numpy.array): velocities of objects after integration
    """
    num_bodies = len(masses)
    state = np.zeros((num_steps + 1, 2 * num_bodies, 3))
    state[0, :num_bodies] = initial_positions
    state[0, num_bodies:] = initial_velocities
    positions = state[0, :num_bodies]
    velocities = state[0, num_bodies:]

    positions, velocities = move_to_barycenter(positions, velocities, masses)

    for step in range(num_steps):
        k_1 = calculate_derivatives(state[step], masses)
        k_2 = calculate_derivatives(state[step] + 0.5 * time_step * k_1, masses)
        k_3 = calculate_derivatives(state[step] + 0.5 * time_step * k_2, masses)
        k_4 = calculate_derivatives(state[step] + time_step * k_3, masses)

        state[step + 1] = state[step] + time_step * (k_1 + 2 * k_2 + 2 * k_3 + k_4)/6

    positions = state[:, :num_bodies]
    velocities = state[:, num_bodies:]
    return positions, velocities


class NOrbit(BaseModel):
    """
    Class that keeps track of NOrbit functions
    
    Attributes:
        object_elements (numpy.array): orbital elements and mass of objects (e.g. planets)
        m_primary (float): mass of primary object (e.g. star) in solar masses
    """
    object_elements: list
    m_primary: float

    def orbit(self, dt: float, n_orbits: int) -> tuple:
        """
        This function calculates the orbit of the objects involved in the N-body problem
    
        Args:
            dt (float): time-step of integration
            n_orbits (int): number of total orbits of first object around primary object
    
        Returns:
            (tuple): tuple containing:
                positions (numpy.array): orbital positions of objects
                velocities (numpy.array): orbital velocities of objects
        """
        
        k = 0.01720209895
        G = k * k

        # Kepler
        primary = np.array((0, 0, 0, 0, 0, 0, self.m_primary))
        n_objects = len(self.object_elements)

        positions = [np.array([0, 0, 0])]
        velocities = [np.array([0, 0, 0])]
        mass = [self.m_primary]

        # Cartesian
        for i in range(0, n_objects):
            pos = kepToCart(self.object_elements[i][0], self.m_primary)[0]
            vel = kepToCart(self.object_elements[i][0], self.m_primary)[1]

            positions.append(pos)
            velocities.append(vel)
            mass.append(self.object_elements[i][0][-1])

        # Set initial positions and velocities for the Sun and objects
        initial_positions =  np.array(positions)
        initial_velocities = np.array(velocities)
        masses = np.array(mass)

        # calculate the number of steps of one single orbit
        a_object = self.object_elements[0][0][0]
        M_object = self.object_elements[0][0][-1]
        T = 2 * np.pi * np.sqrt(a_object**3/G * (self.m_primary + M_object))
        time_step = T * dt  # time step
        num_steps = int(n_orbits/dt)

        # Runge-Kutta 4
        positions, velocities = rk4_n_body(time_step, num_steps, initial_positions, initial_velocities, masses)
        return positions, velocities


class Object():
    """
    Class that makes objects of the solar system available for simple import
    """
    mercury = [np.array((0.3871, 0.2056, 7.0049, 48.3317, 77.4565, 252.2508, 1.659e-7))]
    venus = [np.array((0.7233, 0.0068, 3.3947, 76.6807, 131.5330, 181.9797, 2.447e-6))]
    earth = [np.array((1.0, 0.0167, 0.0001, -11.2606, 102.9472, 100.4644, 3.039e-6))]
    mars = [np.array((1.5237, 0.0934, 1.8506, 49.5785, 336.0408, 355.4533, 3.226e-7))]
    jupiter = [np.array((5.2034, 0.0484, 1.3053, 100.5562, 14.7539, 34.4044, 9.542e-4))]
    saturn = [np.array((9.5371, 0.0542, 2.4845, 113.7150, 92.4319, 49.9443, 2.857e-4))]
    uranus = [np.array((19.1913, 0.0472, 0.7699, 74.2299, 170.9642, 313.2322, 4.353e-5))]
    neptune = [np.array((30.0690, 0.0086, 1.7692, 131.7217, 44.9714, 304.8800, 5.165e-5))]
    planets_solar_system = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    planets_solar_system_names = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    planets_inner_solar_system = [mercury, venus, earth, mars]
    planets_inner_solar_system_names = ["Mercury", "Venus", "Earth", "Mars"]
    planets_outer_solar_system = [jupiter, saturn, uranus, neptune]
    planets_outer_solar_system_names = ["Jupiter", "Saturn", "Uranus", "Neptune"]
