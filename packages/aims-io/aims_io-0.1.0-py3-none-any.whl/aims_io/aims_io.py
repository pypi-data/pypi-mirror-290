import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Tuple, Optional

from ase import Atoms
from ase.io import write, read
from ase.calculators.singlepoint import SinglePointCalculator
from ase import units
from dataclasses import dataclass, field
import os


@dataclass
class AimsIO:
    """A class to read in a AIMS output directory and generate a nequip compatible dataset."""

    path: Path
    control_dat: str = "Control.dat"
    fms_out: str = "FMS.out"

    ex_shift: float = field(init=False)
    atoms_list: List[str] = field(init=False)
    masses: dict = field(init=False)

    def __post_init__(self):
        self.get_ex_shift()
        self.extract_masses_and_symbols()
        self.gen_extxyz_for_trajdump_files()

    def get_ex_shift(self):
        with open(self.path / self.control_dat) as f:
            for line in f:
                if "ExShift" in line:
                    self.ex_shift = float(line.split()[0].split("=")[1])
                    break

    def extract_masses_and_symbols(self):
        masses = {}
        atoms_list = []
        element = None
        reading_particles = False

        with open(self.path / self.fms_out) as f:
            file_content = f.read()

        for line in file_content.splitlines():
            line = line.strip()

            if "Propagate until:" in line:
                break  # Stop processing once we reach the "Propagate until" line

            if line.startswith("Particle #"):
                reading_particles = True
                continue

            if reading_particles:
                if "Element:" in line:
                    element = line.split()[1]  # Extract the element symbol
                    atoms_list.append(element)
                elif "Mass:" in line and element is not None:
                    mass = float(line.split()[1])  # Extract the mass
                    if element not in masses:
                        masses[element] = mass  # Add to dictionary

        self.atoms_list = atoms_list
        self.masses = masses

    def gen_extxyz_for_trajdump_files(self):
        for file in sorted(self.path.glob("TrajDump*")):
            print(file)
            filename = str(file) + ".extxyz"
            positions, momenta, states, time = self.read_trajdump(file)
            energy = self.read_energy(file, state=states[0])
            forces = self.calc_forces(momenta, time)
            # print(positions.shape, momenta.shape, states.shape, time.shape)
            self.write_extxyz(filename, positions, forces, energy, self.atoms_list)

    def write_extxyz(self, filename, positions, forces, energy, atoms_list):
        for i in range(forces.shape[0]):
            curr_atoms = Atoms(
                # set atomic positions
                positions=positions[i] * units.Bohr,
                # set chemical symbols / species
                symbols=atoms_list,
                # assuming data with periodic boundary conditions, set to false for e.g. for molecules in vacuum
                pbc=False,
            )

            # set calculator to assign targets
            calculator = SinglePointCalculator(
                curr_atoms, energy=energy[i], forces=forces[i]
            )
            curr_atoms.calc = calculator

            write(self.path / filename, curr_atoms, format="extxyz", append=True)

    def read_trajdump(self, file):
        # remove "#" character inside the file
        os.system(f"gsed -i 's/\#//' {file}")
        # os.system(f"sed -i 's/\#//' {file}")
        traj_dump = pd.read_table(file, sep="\s+", header=0)

        position_indices = traj_dump.columns.str.contains("pos")
        momentum_indices = traj_dump.columns.str.contains("mom")
        state_indices = traj_dump.columns.str.contains("StateID")
        time = traj_dump["Time"].values

        positions = traj_dump.loc[:, position_indices].values.reshape(
            traj_dump.shape[0], -1, 3
        )
        momenta = traj_dump.loc[:, momentum_indices].values.reshape(
            traj_dump.shape[0], -1, 3
        )
        states = traj_dump.loc[:, state_indices].values.astype(int)
        time = time

        return positions, momenta, states, time

    def read_energy(self, file, state):
        file = "PotEn." + str(file).split(".")[-1]
        poten_dump = pd.read_table(file, sep="\s+", header=0)
        print(poten_dump)
        energies = poten_dump.iloc[:, state].values

        return energies - self.ex_shift

    def calc_forces(self, momenta, time):
        forces = []
        for timestep in range(len(momenta) - 1):
            forces.append(
                (momenta[timestep + 1] - momenta[timestep])
                / (time[timestep + 1] - time[timestep])
            )

        return np.array(forces)


def test_AimsIO():
    path = Path("/Users/pablo/test-aims/0000")
    aims = AimsIO(path)
    assert aims.path is path


if __name__ == "__main__":
    test_AimsIO()
    print("All tests passed!")
