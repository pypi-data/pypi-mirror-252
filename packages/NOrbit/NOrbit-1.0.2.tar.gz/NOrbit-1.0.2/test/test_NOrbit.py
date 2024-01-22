import sys
path = "src"
sys.path.append(path)

import numpy as np
import NOrbit
import pytest

def test_kepToCart():
    planet_elements = np.array((1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e-5))
    mass_star = 1.0

    result = NOrbit.kepToCart(planet_elements, mass_star)
    pos = np.array((1., 0., 0.))
    vel = np.array((0., 0.017, 0.))

    assert pytest.approx(result[0], 0.1) == pos
    assert pytest.approx(result[1], 0.1) == vel

def test_cartToKep():
    positions_1 = np.array((1.0, 1.0, 0.0))
    velocities_1 = np.array((0.1, 0.1, 0.0))
    positions_2 = np.array((-1.0, -1.0, 0.0))
    velocities_2 = np.array((0.1, 0.1, 0.0))
    positions_3 = np.array((1.0, 0.0, 0.0))
    velocities_3 = np.array((0.0, 0.017202184960279726, 0.0))
    positions_4 = np.array((1.0, 0.0, 0.0))
    velocities_4 = np.array((0.0, 0.017199564984189623, 0.0003002195235361275))
    positions_5 = np.array((0.9, 0.0, 0.0))
    velocities_5 = np.array((0.0, 0.019017731029180855, 0.0))
    positions_6 = np.array((1.0, 0.0, 1.0))
    velocities_6 = np.array((0.0, 0.017202184960279726, 0.0))
    mass_planet = 1e-5
    mass_star = 1.0

    result_1 = NOrbit.cartToKep(positions_1, velocities_1, mass_star, mass_planet)
    result_2 = NOrbit.cartToKep(positions_2, velocities_2, mass_star, mass_planet)
    result_3 = NOrbit.cartToKep(positions_3, velocities_3, mass_star, mass_planet)
    result_4 = NOrbit.cartToKep(positions_4, velocities_4, mass_star, mass_planet)
    result_5 = NOrbit.cartToKep(positions_5, velocities_5, mass_star, mass_planet)
    result_6 = NOrbit.cartToKep(positions_6, velocities_6, mass_star, mass_planet)
    assert pytest.approx(result_1, 0.1) == (0.0, 1.0, 0.0, 225.0, 0.0, 180.0, 1e-05)
    assert pytest.approx(result_2, 0.1) == (0.0, 1.0, 0.0, 45.0, 0.0, 180, 1e-05)
    assert pytest.approx(result_3, 0.1) == (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e-05)
    assert pytest.approx(result_4, 0.1) == (1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1e-05)
    assert pytest.approx(result_5, 0.1) == (1.0, 0.1, 0.0, 0.0, 0.0, 0.0, 1e-05)
    assert pytest.approx(result_6, 0.1) == (2.41, 0.41, 45.0, 90.0, 270.0, 0.0, 1e-05)

def test_calculate_acceleration():
    positions = np.array([[ 4.24986205e-03, -2.16147702e-03, -7.22871314e-05],
                        [-9.69141616e-01, -2.45313757e-01, -7.05363499e-05],
                        [-4.45076172e+00,  2.26600558e+00,  7.57570172e-02]])
    masses = np.array([ 1.000e+00, 3.039e-06, 9.542e-04])

    result = NOrbit.calculate_acceleration(positions, masses)
    assert pytest.approx(result) == np.array([[ -1.09315857e-08,  4.90777799e-09,  1.71316619e-10],
                                        [ 2.85191816e-04,  7.12527106e-05, -2.42462946e-10],
                                        [ 1.05479855e-05, -5.37027351e-06, -1.79538757e-07]])

def test_calculate_derivatives():
    state = np.array([[ 4.24986205e-03, -2.16147702e-03, -7.22871314e-05],
                        [-9.69141616e-01, -2.45313757e-01, -7.05363499e-05],
                        [-4.45076172e+00,  2.26600558e+00,  7.57570172e-02],
                        [ 3.57150614e-06,  6.61486878e-06,  1.23844670e-07],
                        [ 3.88593376e-03, -1.66934707e-02,  1.23771443e-07],
                        [-3.75530863e-03, -6.87920491e-03, -1.29789400e-04]])
    masses = np.array([1.000e+00, 3.039e-06, 9.542e-04])

    result = NOrbit.calculate_derivatives(state, masses)
    assert pytest.approx(result) == np.array([[ 3.57150614e-06,  6.61486878e-06,  1.23844670e-07],
                        [ 3.88593376e-03, -1.66934707e-02,  1.23771443e-07],
                        [-3.75530863e-03, -6.87920491e-03, -1.29789400e-04],
                        [-1.09315857e-08,  4.90777799e-09,  1.71316619e-10],
                        [ 2.85191816e-04,  7.12527106e-05, -2.42462946e-10],
                        [ 1.05479855e-05, -5.37027351e-06, -1.79538757e-07]])

def test_move_to_barycenter():
    positions = np.array([[0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                        [-9.73391478e-01, -2.43152280e-01, 1.75078150e-06],
                        [-4.45501158e+00, 2.26816706e+00, 7.58293043e-02]])

    velocities = np.array([[0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                        [3.88236225e-03, -1.67000855e-02, -7.32266254e-11],
                        [-3.75888013e-03, -6.88581978e-03, -1.29913245e-04]])
    masses = np.array([1.000e+00, 3.039e-06, 9.542e-04])

    result = NOrbit.move_to_barycenter(positions, velocities, masses)
    
    pos = np.array([[4.24986205e-03, -2.16147702e-03, -7.22871314e-05],
                        [-9.69141616e-01, -2.45313757e-01, -7.05363499e-05],
                        [-4.45076172e+00, 2.26600558e+00, 7.57570172e-02]])
    vel = np.array([[3.57150614e-06, 6.61486878e-06, 1.23844670e-07],
                        [3.88593376e-03, -1.66934707e-02, 1.23771443e-07],
                        [-3.75530863e-03, -6.87920491e-03, -1.29789400e-04]])
    
    assert pytest.approx(result[0]) == pos
    assert pytest.approx(result[1]) == vel

def test_rk4_n_body():
    time_step = 182.62872666688173
    num_steps = 2
    initial_positions = np.array([[0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                        [-9.73391478e-01, -2.43152280e-01, 1.75078150e-06],
                        [-4.45501158e+00, 2.26816706e+00, 7.58293043e-02]])
    initial_velocities = np.array([[0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                        [3.88236225e-03, -1.67000855e-02, -7.32266254e-11],
                        [-3.75888013e-03, -6.88581978e-03, -1.29913245e-04]])
    masses = np.array([1.000e+00, 3.039e-06, 9.542e-04])

    result = NOrbit.rk4_n_body(time_step, num_steps, initial_positions, initial_velocities, masses)

    pos = np.array([[[4.24986205e-03, -2.16147702e-03, -7.22871314e-05],
                        [-9.69141616e-01, -2.45313757e-01, -7.05363499e-05],
                        [-4.45076172e+00, 2.26600558e+00, 7.57570172e-02]],
                        
                        [[4.72395076e-03, -8.88013725e-04, -4.71501065e-05],
                        [1.17480287e+00, -2.25133700e+00, -4.84982224e-05],
                        [-4.95443406e+00, 9.37807103e-01, 4.94133870e-02]],
                        
                        [[4.83899013e-03, 4.49597689e-04, -1.84045467e-05],
                        [2.81225316e+00, -2.72423579e+00, -2.43528023e-05],
                        [-5.08021019e+00, -4.62501296e-01, 1.92880117e-02]]])

    vel = np.array([[[3.57150614e-06, 6.61486878e-06, 1.23844670e-07],
                        [3.88593376e-03, -1.66934707e-02, 1.23771443e-07],
                        [-3.75530863e-03, -6.87920491e-03, -1.29789400e-04]],
                        
                        [[1.62276300e-06, 7.23800186e-06, 1.49536484e-07],
                        [1.06780480e-02, -5.14841510e-03, 1.26958340e-07],
                        [-1.73466106e-03, -7.56901680e-03, -1.56714388e-04]],
                        
                        [[-3.60304790e-07, 7.32101319e-06, 1.63214129e-07],
                        [7.51275918e-03, -8.85004112e-04, 1.36526191e-07],
                        [3.53671677e-04, -7.66959093e-03, -1.71048569e-04]]])

    assert pytest.approx(result[0]) == pos
    assert pytest.approx(result[1]) == vel

def test_orbit():
    planet_elements = [
    [np.array([1.000000e+00, 1.670000e-02, 1.000000e-04, -1.126060e+01,
            1.029472e+02, 1.004644e+02, 3.039000e-06])],
    [np.array([5.203400e+00, 4.840000e-02, 1.305300e+00, 1.005562e+02,
            1.475390e+01, 3.440440e+01, 9.542000e-04])] ]
    m_star = 1.0
    dt = 0.5
    n_orbits = 1
    
    result = NOrbit.NOrbit(object_elements = planet_elements, m_primary = m_star).orbit(dt = dt, n_orbits = n_orbits)
    
    pos = np.array([[[4.24986205e-03, -2.16147702e-03, -7.22871314e-05],
                        [-9.69141616e-01, -2.45313757e-01, -7.05363499e-05],
                        [-4.45076172e+00, 2.26600558e+00, 7.57570172e-02]],
                        
                        [[4.72395076e-03, -8.88013725e-04, -4.71501065e-05],
                        [1.17480287e+00, -2.25133700e+00, -4.84982224e-05],
                        [-4.95443406e+00, 9.37807103e-01, 4.94133870e-02]],
                        
                        [[4.83899013e-03, 4.49597689e-04, -1.84045467e-05],
                        [2.81225316e+00, -2.72423579e+00, -2.43528023e-05],
                        [-5.08021019e+00, -4.62501296e-01, 1.92880117e-02]]])
    vel = np.array([[[3.57150614e-06, 6.61486878e-06, 1.23844670e-07],
                        [3.88593376e-03, -1.66934707e-02, 1.23771443e-07],
                        [-3.75530863e-03, -6.87920491e-03, -1.29789400e-04]],
                        
                        [[1.62276300e-06, 7.23800186e-06, 1.49536484e-07],
                        [1.06780480e-02, -5.14841510e-03, 1.26958340e-07],
                        [-1.73466106e-03, -7.56901680e-03, -1.56714388e-04]],
                        
                        [[-3.60304790e-07, 7.32101319e-06, 1.63214129e-07],
                        [7.51275918e-03, -8.85004112e-04, 1.36526191e-07],
                        [3.53671677e-04, -7.66959093e-03, -1.71048569e-04]]])

    assert pytest.approx(result[0]) == pos
    assert pytest.approx(result[1]) == vel
