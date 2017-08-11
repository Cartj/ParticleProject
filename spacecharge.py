
# !/usr/bin/env synergia
import synergia

from synergia.foundation import Four_momentum, Reference_particle, pconstants
from synergia.lattice import Mad8_reader, Lattice
from synergia.bunch import Bunch, Diagnostics_basic
from synergia.simulation import Independent_stepper_elements, Bunch_simulator, Propagator

use_space_charge=1

turns=200

lattice= synergia.lattice.Mad8_reader().get_lattice("fodo", "fodo.lat")

x_emit = 3.9e-6 
y_emit = 3.9e-6
z_std = 2*.0018
z_period = 6.73E-02
dpop = 1e-3 
real_particles = 1.5e8
macro_particles = 50000

commxx = Commxx(True)
grid = [32,32,32]

if use_space_charge ==1:
	space_charge = Space_charge_2d_open_hockney(commxx, grid)
else:
	space_charge = Dummy_collective_operator("null space charge")

map_order = 1

steps_per_element = 1 

stepper = Split_operator_stepper_elements(lattice, map_order, space_charge, steps_per_elements)

lattice_simulator = stepper.get_lattice_simulator()

seed = 1415926

bunch = synergia.optics.generate_matched_bunch_transverse(
	lattice_simulator,
	x_emit, y_emit, z_std, dpop,
	real_particles, macro_particles,
	seed = seed, z_period_length = z_period)
z_period = bunch.get_z_period_length()
print z_period

bunch_simulator = Bunch_simulator(bunch)

diagnostics = Diagnostics_full2("diagnostics.h5")
bunch_simulator.add_per_step(diagnostics)

tracker = Diagnostics_particles("tracks.h5")
bunch_simulator.add_per_turn(tracker,10)

propagator = Propagator(stepper)
max_turns = 0

verbosity = 2

propagator.propagate(bunch_simulator, turns, max_turns, verbosity)
