import capytaine as cpt
import xarray as xr
import numpy as np
from capytaine.post_pro import rao

#cpt.set_logging('INFO')

# ------------ Loading the mesh ---------------
hull = cpt.mesh_sphere(radius=1.0, center=(0, 0, -2), name="hull")

# ------------ Displaying the mesh ---------------

#hull.show()

# ------------ Defining the body ---------------

body = cpt.FloatingBody(mesh=hull,
                        dofs=cpt.rigid_body_dofs(rotation_center=(0, 0, -2)),
                        center_of_mass=(0, 0, -2))

# ------------ Names of DOFs ----------------

#print(body.dofs.keys()) # dict_keys(['Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw'])

# ------------ Hydrostatics ----------------

hydrostatics = body.compute_hydrostatics(rho=1025.0)

print(hydrostatics["disp_volume"])
# 3.82267415555807

print(hydrostatics["hydrostatic_stiffness"])
# <xarray.DataArray 'hydrostatic_stiffness' (influenced_dof: 6, radiating_dof: 6)> Size: 288B
# [...]
# Coordinates:
#   * influenced_dof  (influenced_dof) <U5 120B 'Surge' 'Sway' ... 'Pitch' 'Yaw'
#   * radiating_dof   (radiating_dof) <U5 120B 'Surge' 'Sway' ... 'Pitch' 'Yaw'

print(hydrostatics["inertia_matrix"])
# <xarray.DataArray 'inertia_matrix' (influenced_dof: 6, radiating_dof: 6)> Size: 288B
# [...]
# Coordinates:
#   * influenced_dof  (influenced_dof) <U5 120B 'Surge' 'Sway' ... 'Pitch' 'Yaw'
#   * radiating_dof   (radiating_dof) <U5 120B 'Surge' 'Sway' ... 'Pitch' 'Yaw'

# ---------------- Defining frequencies and direction to solve for -----------------

omega = np.linspace(0.1, 4, 40)

test_matrix = xr.Dataset(coords={
    'omega': omega,
    'wave_direction': [0, np.pi/2],
    'radiating_dof': list(body.dofs),
    'water_depth': [np.inf],
})

# ---------------- Defining linear potential flow problem ---------------------

radiation_problem = cpt.RadiationProblem(body=body, radiating_dof="Heave", omega=1.0, water_depth=np.inf, g=9.81, rho=1025)

diffraction_problem = cpt.DiffractionProblem(body=body, wave_direction=np.pi/2, omega=1.0)

# ----------------- Solving the problem ---------------------

solver = cpt.BEMSolver()

result_rad = solver.solve(radiation_problem)
result_diff = solver.solve(diffraction_problem)

dataset = solver.fill_dataset(test_matrix, body)

print(dataset['added_mass'].sel(omega=0.1))

rao = rao(dataset)

print(rao)