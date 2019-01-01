import numpy as np
import pytest

from nbody.forces.numpy_forces import calculate_forces, calculate_potentials
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import floats


@pytest.mark.parametrize(
    "r2, expected_force_on_1, expected_potential_on_1",
    [
        [0.5, 24192, 16128],
        [1, 0, 0],
        [2, -0.369_140_625, -0.061_523_437_5],  # regression test
        [-1, 0, 0],
        [-2, 0.369_140_625, -0.061_523_437_5],  # regression test
        [-0.5, -24192, 16128],
    ],
)
def test_lenard_jones_1d(r2, expected_force_on_1, expected_potential_on_1):
    r1 = 0
    r = np.vstack([(r1, 0, 0), (r2, 0, 0)])
    forces = calculate_forces(r)
    potential_energy = calculate_potentials(r)
    # check force value
    np.testing.assert_allclose(forces[0, 0], expected_force_on_1)
    print(potential_energy)
    np.testing.assert_allclose(potential_energy, expected_potential_on_1)

    # check reciprocity (Newton's third law)
    np.testing.assert_allclose(forces[1], -forces[0])


@given(r=arrays(np.float, (2, 3), floats(allow_infinity=False, allow_nan=False)))
def test_lenard_jones_3d_reciprocity(r):
    forces = calculate_forces(r)
    # check reciprocity (Newton's third law)
    np.testing.assert_allclose(forces[1], -forces[0])
