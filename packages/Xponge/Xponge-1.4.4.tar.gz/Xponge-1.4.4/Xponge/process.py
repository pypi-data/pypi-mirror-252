"""
This **module** is used to process topology and conformations
"""
import os.path
from abc import ABC, abstractmethod
from itertools import product

import numpy as np
from .helper import get_rotate_matrix, ResidueType, Molecule, Residue, set_global_alternative_names, Xdict, \
    GlobalSetting, Xopen, Xprint
from .helper.math import get_basis_vectors_from_length_and_angle
from .build import save_sponge_input
from .load import load_coordinate
from .forcefield.special.min import save_min_bonded_parameters, do_not_save_min_bonded_parameters
from .mdrun import run


def impose_bond(molecule, atom1, atom2, length):
    """
    This **function** is used to impose the distance in ``molecule`` between ``atom1`` and ``atom2`` to ``length``

    usage example::

        import Xponge
        import Xponge.forcefield.amber.ff14sb
        mol = ALA*10
        Impose_Bond(mol, mol.residues[0].CA, mol.residues[0].C, 1.2)

    .. ATTENTION::

        `atom1` and `atom2` should be bonded if they are in one residue

    :param molecule: a ``Molecule`` instance
    :param atom1: the base atom, which will not change its coordinate
    :param atom2: the atom to change its coordinate to fit the length
    :param length: distance in the unit of angstrom
    :return: None
    """
    crd = molecule.get_atom_coordinates()
    _, atom2_friends = molecule.divide_into_two_parts(atom1, atom2)
    r0 = crd[molecule.atom_index[atom2]] - crd[molecule.atom_index[atom1]]
    l0 = np.linalg.norm(r0)
    if l0 == 0:
        crd[molecule.atom_index[atom2]] += (1 / 3) ** (0.5)
        r0 = crd[molecule.atom_index[atom2]] - crd[molecule.atom_index[atom1]]
        l0 = np.linalg.norm(r0)
    dr = (length / l0 - 1) * r0
    crd[atom2_friends] += dr
    for atom in molecule.atoms:
        i = molecule.atom_index[atom]
        atom.x = crd[i][0]
        atom.y = crd[i][1]
        atom.z = crd[i][2]


def impose_angle(molecule, atom1, atom2, atom3, angle):
    """
    This **function** is used to impose the angle in ``molecule`` between ``atom1``, ``atom2`` and ``atom3`` \
 to ``angle``.

    .. ATTENTION::

        The pairs of ``atom1`` - ``atom2`` and ``atom2`` - ``atom3``  should be bonded.

    :param molecule: a ``Molecule`` instance
    :param atom1: the base atom, which will not change its coordinate
    :param atom2: the base atom, which will not change its coordinate
    :param atom3: the atom to change its coordinate to fit the angle
    :param angle: angle in the unit of rad
    :return: None
    """
    crd = molecule.get_atom_coordinates()
    _, atom3_friends = molecule.divide_into_two_parts(atom2, atom3)
    r12 = crd[molecule.atom_index[atom1]] - crd[molecule.atom_index[atom2]]
    r23 = crd[molecule.atom_index[atom3]] - crd[molecule.atom_index[atom2]]
    angle0 = np.arccos(np.dot(r12, r23) / np.linalg.norm(r23) / np.linalg.norm(r12))
    delta_angle = angle - angle0
    crd[atom3_friends] = np.dot(crd[atom3_friends] - crd[molecule.atom_index[atom2]],
                                get_rotate_matrix(np.cross(r12, r23), delta_angle)) + crd[molecule.atom_index[atom2]]
    for atom in molecule.atoms:
        i = molecule.atom_index[atom]
        atom.x = crd[i][0]
        atom.y = crd[i][1]
        atom.z = crd[i][2]


def impose_dihedral(molecule, atom1, atom2, atom3, atom4, dihedral, keep_atom3=False):
    """
    This **function** is used to impose the dihedral in ``molecule`` between ``atom1``, ``atom2``, ``atom3`` \
 and ``atom4`` to ``dihedral``.

    .. ATTENTION::

        The pairs of ``atom1`` - ``atom2``,  ``atom2`` - ``atom3``  and ``atom3`` - ``atom4`` should be bonded.

    :param molecule: a ``Molecule`` instance
    :param atom1: the base atom, which will not change its coordinate
    :param atom2: the base atom, which will not change its coordinate
    :param atom3: the atom to change its coordinate to fit the angle
    :param atom4: the atom to change its coordinate to fit the angle
    :param dihedral: dihedral angle in the unit of rad
    :param keep_atom3: whether the other atoms linked to atom3 will be rotated
    :return: None
    """
    crd = molecule.get_atom_coordinates()
    if not keep_atom3:
        _, rotate_friends = molecule.divide_into_two_parts(atom2, atom3)
    else:
        _, rotate_friends = molecule.divide_into_two_parts(atom3, atom4)
    r12 = crd[molecule.atom_index[atom1]] - crd[molecule.atom_index[atom2]]
    r23 = crd[molecule.atom_index[atom3]] - crd[molecule.atom_index[atom2]]
    r34 = crd[molecule.atom_index[atom3]] - crd[molecule.atom_index[atom4]]
    r12xr23 = np.cross(r12, r23)
    r34xr23 = np.cross(r34, r23)
    cos = np.dot(r12xr23, r34xr23) / np.linalg.norm(r12xr23) / np.linalg.norm(r34xr23)
    cos = max(-0.999999, min(cos, 0.999999))
    dihedral0 = np.arccos(cos)
    dihedral0 = np.pi - np.copysign(dihedral0, np.cross(r34xr23, r12xr23).dot(r23))
    delta_angle = dihedral - dihedral0
    crd[rotate_friends] = np.dot(crd[rotate_friends] - crd[molecule.atom_index[atom3]],
                                get_rotate_matrix(r23, delta_angle)) + crd[molecule.atom_index[atom3]]
    for atom in molecule.atoms:
        i = molecule.atom_index[atom]
        atom.x = crd[i][0]
        atom.y = crd[i][1]
        atom.z = crd[i][2]


def _add_inner_solvents(molecule, new_molecule, molcrd, molmin, molmax, solshape, solcrd, n_solvent):
    """
        add the solvents around the molecule
    """
    n_grid = np.floor((molmax - molmin) / solshape).astype(np.int32)
    if np.prod(n_grid) == 0:
        return 0
    grids = np.ones(n_grid, dtype=np.int32)
    for crd in molcrd:
        index = np.floor((crd - molmin) / solshape).astype(np.int32)
        for i, j, k in product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
            indexi = max(min(index[0] + i, n_grid[0] - 1), 0)
            indexj = max(min(index[1] + j, n_grid[1] - 1), 0)
            indexk = max(min(index[2] + k, n_grid[2] - 1), 0)
            grids[indexi][indexj][indexk] = 0
    n_add = np.sum(grids)
    if n_solvent is not None and n_solvent < n_add:
        Xprint(f"The parameter 'n_solvent' is too small. At least {n_add} solvents \
are required to fully solvate the molecule. This parameter will be ignored.", "WARNING")
    for i, j, k in product(np.arange(n_grid[0]), np.arange(n_grid[1]), np.arange(n_grid[2])):
        if grids[i][j][k] == 0:
            continue
        for atom in new_molecule.atoms:
            atom_crd = solcrd[new_molecule.atom_index[atom]]
            atom.x = atom_crd[0] + i * solshape[0] + molmin[0]
            atom.y = atom_crd[1] + j * solshape[1] + molmin[1]
            atom.z = atom_crd[2] + k * solshape[2] + molmin[2]
        molecule |= new_molecule
    return n_add


def _add_outer_solvents(molecule, new_molecule, molmin, molmax,
    solshape, solcrd, solbox, n_solvent, n_added):
    """
        add the solvents at a distance from the molecule
    """
    boxmin = molmin - np.array(solbox[:3])
    n_grid = np.ceil((molmax + np.array(solbox[3:]) - boxmin) / solshape).astype(np.int32)
    grids = np.ones(n_grid, dtype=np.int32)
    in_min = np.floor((molmin - boxmin) / solshape).astype(np.int32)
    in_max = np.ceil((molmax - boxmin) / solshape).astype(np.int32)
    grids[in_min[0]:in_max[0], in_min[1]:in_max[1], in_min[2]:in_max[2]] = 0
    n_add = np.sum(grids) + n_added
    if n_solvent is not None and n_solvent > n_add:
        n_solvent = None
        Xprint(f"The parameter 'n_solvent' is too big. The box can accommodate up to {n_add} solvents.\
 This parameter will be ignored.", "WARNING")
    if n_solvent is not None:
        ones_indices = np.argwhere(grids == 1)
        random_indices = np.random.choice(len(ones_indices), n_solvent - n_added, replace=False)
        random_ones_indices = ones_indices[random_indices]
        grids[:, :, :] = 0
        grids[tuple(random_ones_indices.T)] = 1
    for i, j, k in product(np.arange(n_grid[0]), np.arange(n_grid[1]), np.arange(n_grid[2])):
        if grids[i][j][k] == 0:
            continue
        for atom in new_molecule.atoms:
            atom_crd = solcrd[new_molecule.atom_index[atom]]
            atom.x = atom_crd[0] + i * solshape[0] + boxmin[0]
            atom.y = atom_crd[1] + j * solshape[1] + boxmin[1]
            atom.z = atom_crd[2] + k * solshape[2] + boxmin[2]
        molecule |= new_molecule
    return molecule


def add_solvent_box(molecule, solvent, distance, tolerance=2.5, n_solvent=None):
    """
    This **function** adds a box full of solvents to a molecule.
    This will be performed in place for a Molecule and out of place for a ResidueType.

    :param molecule: the molecule to add the box, either a ``Molecule`` or a ``ResidueType``
    :param solvent: the solvent molecule, either a ``Molecule`` or a ``ResidueType``
    :param distance: the distance between the ``molecule`` and the box in the unit of Angstrom. \
 This can be an ``int`` or a ``float``, and it can be also a list of them with the length 3 or 6, \
 which represents the 3 or 6 directions respectively.
    :param tolerance: the distance between two molecules. 2.5 for default.
    :param n_solvent: the number of solvent molecules.
    :return: the Molecule instance
    """
    if isinstance(distance, (float, int)):
        distance = [distance] * 6
    elif not isinstance(distance, list):
        raise TypeError("parameter distance should be a list, an int or a float")

    if len(distance) == 3:
        distance = distance + distance
    elif len(distance) != 6:
        raise TypeError("the length of parameter distance should be 3 or 6")

    if isinstance(molecule, ResidueType):
        new_molecule = Molecule(molecule.name)
        res_a = Residue(molecule)
        for atom in molecule.atoms:
            res_a.Add_Atom(atom)
        new_molecule.Add_Residue(res_a)
        molecule = new_molecule

    molcrd = molecule.get_atom_coordinates()
    molmin = np.min(molcrd, axis=0)
    molmax = np.max(molcrd, axis=0)
    if isinstance(solvent, ResidueType):
        new_molecule = Molecule(solvent.name)
        res_a = Residue(solvent)
        for atom in solvent.atoms:
            res_a.Add_Atom(atom)
        new_molecule.Add_Residue(res_a)
    else:
        new_molecule = solvent.deepcopy()
    solcrd = new_molecule.get_atom_coordinates()
    solmin = np.min(solcrd, axis=0)
    solmax = np.max(solcrd, axis=0)
    solshape = solmax - solmin + tolerance

    n_added = _add_inner_solvents(molecule, new_molecule, molcrd, molmin, molmax, solshape, solcrd, n_solvent)
    return _add_outer_solvents(molecule, new_molecule, molmin, molmax, solshape, solcrd, distance, n_solvent, n_added)


def h_mass_repartition(molecules, repartition_mass=1.1, repartition_rate=3, exclude_residue_name="WAT"):
    """
    This **function** repartition the mass of light atoms to the connected heavy atoms. \
 This can help the simulation run with a time step of 4 fs.

    .. ATTENTION::

        Many functions use mass to guess the element, the mass repartition may cause error. So call this function \
 at the final step please unless you know what you are doing.

    :param molecules: a ``Molecule``
    :param repartition_mass: if the mass of the atom is not greater than this value, it will be seen as a light atom. \
 1.1 for default and in the unit of Dalton.
    :param repartition_rate: The mass of the light atom will multiplied by this value.
    :param exclude_residue_name: the residue name which will not do the repartition. "WAT" for default.
    :return: None
    """
    for res in molecules.residues:
        if res.name == exclude_residue_name:
            continue
        for atom in res.atoms:
            if atom.mass <= repartition_mass:
                connect_atoms = res.type.connectivity[res.type.name2atom(atom.name)]
                assert len(connect_atoms) == 1, "The atom to repartition mass can have at most 1 bond"
                origin_mass = atom.mass
                atom.mass *= repartition_rate
                delta_mass = atom.mass - origin_mass
                for heavy_atom in connect_atoms:
                    res.name2atom(heavy_atom.name).mass -= delta_mass


def solvent_replace(molecule, select, toreplace, sort=True):
    """
    This **function** replaces the solvent to some other molecules randomly.

    usage example::

        import Xponge
        import Xponge.forcefield.amber.ff14sb
        import Xponge.forcefield.amber.tip3p
        mol = ALA*10
        Add_Solvent_Box(mol, WAT, 10)
        Solvent_Replace(mol, WAT, {K:10, CL:10})
        #Solvent_Replace(mol, lambda res:res.name == "WAT", {K:10, CL:10})

    :param molecule: a ``Molecule`` instance
    :param select: a **function** to decide which residues should be replaced, \
or a Residue, a ResidueType or a Molecule with only one Residue, \
which the residues to be replaced have the same name
    :param toreplace: a dict, which stores the mapping of molecules to replace and the number of molecules. \
 Every molecule should be a ``ResidueType``, a ``Residue`` or a ``Molecule`` with only one ``Residue``.
    :param sort: whether to sort the residues after replacing
    :return: None
    """
    solvents = []
    for_sort = Xdict()
    if not callable(select):
        if isinstance(select, Molecule):
            select = select.residues[0]
        resname = select.name
        # pylint: disable=unnecessary-lambda-assignment
        select = lambda res: res.name == resname
    for i, resi in enumerate(molecule.residues):
        if select(resi):
            solvents.append(i)
            for_sort[resi] = float("inf")
        else:
            for_sort[resi] = float("-inf")

    np.random.shuffle(solvents)
    count = 0
    for key, value in toreplace.items():
        assert isinstance(key, ResidueType) or (isinstance(key, Molecule) and len(key.residues) == 1)
        if isinstance(key, Molecule):
            key = key.residues[0].type

        tempi = solvents[count:count + value]
        count += value
        for i in tempi:
            new_residue = Residue(key)
            crd_o = [molecule.residues[i].atoms[0].x, molecule.residues[i].atoms[0].y, molecule.residues[i].atoms[0].z]
            crd0 = [key.atoms[0].x, key.atoms[0].y, key.atoms[0].z]
            for atom in key.atoms:
                new_residue.Add_Atom(atom, x=atom.x + crd_o[0] - crd0[0],
                                     y=atom.y + crd_o[1] - crd0[1], z=atom.z + crd_o[2] - crd0[2])
            molecule.residues[i] = new_residue
            for_sort[new_residue] = count
    if sort:
        molecule.residues.sort(key=lambda res: for_sort[res])


def main_axis_rotate(molecule, direction_long=None, direction_middle=None, direction_short=None):
    """
    This **function** rotates the main axis of the molecule to the desired direction

    :param molecule: a ``Molecule`` instance
    :param direction_long: a list of three ``int`` or ``float`` to represent the direction vector. \
The long main axis will rotate to this direction.
    :param direction_middle: a list of three ``int`` or ``float`` to represent the direction vector. \
The middle main axis will rotate to this direction.
    :param direction_short: a list of three ``int`` or ``float`` to represent the direction vector. \
The short main axis will rotate to this direction.
    :return: None
    """
    if direction_long is None:
        direction_long = [0, 0, 1]
    if direction_middle is None:
        direction_middle = [0, 1, 0]
    if direction_short is None:
        direction_short = [1, 0, 0]
    molcrd = molecule.get_atom_coordinates()
    eye = np.zeros((3, 3))
    mass_of_center = np.zeros(3)
    total_mass = 0
    for i, atom in enumerate(molecule.atoms):
        xi, yi, zi = molcrd[i]
        total_mass += atom.mass
        mass_of_center += atom.mass * np.array([xi, yi, zi])
    mass_of_center /= total_mass

    for i, atom in enumerate(molecule.atoms):
        xi, yi, zi = molcrd[i] - mass_of_center
        eye += atom.mass * np.array([[yi * yi + zi * zi, -xi * yi, -xi * zi],
                                     [-xi * yi, xi * xi + zi * zi, -yi * zi],
                                     [-xi * zi, -yi * zi, xi * xi + yi * yi]])

    eigval, eigvec = np.linalg.eig(eye)
    t = np.argsort(eigval)
    matrix0 = np.vstack([direction_short, direction_middle, direction_long])
    rotation_matrix = np.dot(matrix0, np.linalg.inv(np.vstack((eigvec[:, t[2]], eigvec[:, t[1]], eigvec[:, t[0]]))))
    molcrd = np.dot(molcrd - mass_of_center, rotation_matrix) + mass_of_center
    for i, atom in enumerate(molecule.atoms):
        atom.x = molcrd[i][0]
        atom.y = molcrd[i][1]
        atom.z = molcrd[i][2]


def get_peptide_from_sequence(sequence, charged_terminal=True):
    """
    This **function** is used to get a peptide from the sequence

    :param sequence: a string, the serial
    :param charged_terminal: whether to change the terminal residues to the corresponding charged residue
    :return: a Molecule instance, the peptide
    """
    assert isinstance(sequence, str) and len(sequence) > 1
    temp_dict = Xdict({"A": "ALA", "G": "GLY", "V": "VAL", "L": "LEU", "I": "ILE", "P": "PRO",
                       "F": "PHE", "Y": "TYR", "W": "TRP", "S": "SER", "T": "THR", "C": "CYS",
                       "M": "MET", "N": "ASN", "Q": "GLN", "D": "ASP", "E": "GLU", "K": "LYS",
                       "R": "ARG", "H": "HIS"}, not_found_message="{} is not an abbreviation for an amino acid")
    temp_dict2 = Xdict({key: ResidueType.get_type(value) for key, value in temp_dict.items()},
                       not_found_message="{} is not an abbreviation for an amino acid")
    if charged_terminal:
        head = "N" + temp_dict[sequence[0]]
        tail = "C" + temp_dict[sequence[-1]]
    else:
        head = temp_dict[sequence[0]]
        tail = temp_dict[sequence[-1]]

    toret = ResidueType.get_type(head)

    for i in sequence[1:-1]:
        toret = toret + temp_dict2[i]
    toret += ResidueType.get_type(tail)
    return toret


def optimize(mol, step=2000, only_bad_coordinate=True, dt=1e-8, pbc=True, extra_commands=None):
    """
    This **function** is used to optimize the structure of the Molecule instance

    :param mol: the molecule to optimize
    :param step: the limited step for each epoch for minimization, 2000 for default
    :param only_bad_coordinate: whether to optimize all the atoms or the atoms whose coordinates are bad
    :param dt: the start dt for minimization
    :param pbc: whether to use the periodic box condition
    :param extra_commands: a dict, with the extra commands to pass to the MD engine
    :return: None
    """
    from tempfile import TemporaryDirectory
    Xprint("Optimizing")
    with TemporaryDirectory() as tempdir:
        temp_prefix = os.path.join(tempdir, "temp")
        temp_out = os.path.join(tempdir, "min")
        Xprint("    Parametering")
        save_min_bonded_parameters()
        if not pbc:
            box_length_backup = mol.box_length if hasattr(mol, "box_length") else None
            mol.box_length = [999, 999, 999]
        save_sponge_input(mol, temp_prefix)
        if not pbc:
            mol.box_length = box_length_backup
        do_not_save_min_bonded_parameters()
        temp_mdin_name = os.path.join(tempdir, "mdin.txt")
        mdin = Xopen(temp_mdin_name, "w")
        mdin.write(f"""temp
default_in_file_prefix = {temp_prefix}
rst = {temp_out}
crd = {temp_prefix}.dat
box = {temp_prefix}.box
mdout = {temp_out}.out
mdinfo = {temp_out}.info
mode = minimization
minimization_dynamic_dt = 1
step_limit = {step}
write_information_interval = {step}
molecule_map_output = 1
dont_check_input = 1
""")
        towrite = ""
        if extra_commands:
            for command, value in extra_commands.items():
                towrite += f"{command} = {value}\n"
        mdin.write(towrite)
        mdin.close()
        if pbc:
            all_to_use = f"SPONGE -mdin {temp_mdin_name} "
        else:
            all_to_use = f"SPONGE_NOPBC -mdin {temp_mdin_name} "
        if only_bad_coordinate:
            all_to_use += f"-mass_in_file {temp_prefix + '_fake_mass.txt'} "
        if GlobalSetting.verbose > 10:
            print_to = f" > {os.devnull}"
        else:
            print_to = ""
        Xprint("    Running")
        out = run(all_to_use + f"-dt {dt} {print_to}")
        if out == 0:
            load_coordinate(temp_out+'_coordinate.txt', mol)
        else:
            Xprint("The optimization failed", "ERROR")
        Xprint("Optimization Finished")


class Region(ABC):
    """
    This **abstract class** is used to define a region
    **New From 1.2.6.4**
    """
    def __init__(self, side="in", boundary=False):
        self._side = True
        self.side = side
        self.boundary = boundary

    @abstractmethod
    def __contains__(self, item):
        pass

    @property
    def side(self):
        return "in" if self._side else "out"

    @side.setter
    def side(self, side):
        """
        This **function** is used to set the side of the region"

        :param side: either "in" or "out"
        :return: None
        """
        if side == "in":
            self._side = True
        elif side == "out":
            self._side = False
        else:
            raise ValueError("side should be 'in' or 'out'")


class IntersectRegion:
    """
    This **class** is used to get the interset region of some regions
    **New From 1.2.6.4**

    :param *regions: the regions
    """
    def __init__(self, *regions):
        self.regions = regions

    def __contains__(self, item):
        for region in self.regions:
            if item not in region:
                return False
        return True


class UnionRegion:
    """
    This **class** is used to get the union region of some regions
    **New From 1.2.6.4**

    :param *regions: the regions
    """
    def __init__(self, *regions):
        self.regions = regions

    def __contains__(self, item):
        for region in self.regions:
            if item in region:
                return True
        return False


Region.register(UnionRegion)
Region.register(IntersectRegion)


class BlockRegion(Region):
    """
    This **class** is used to define a block region
    **New From 1.2.6.4**

    :param x_low: the lowest x coordinate of the block region
    :param y_low: the lowest y coordinate of the block region
    :param z_low: the lowest z coordinate of the block region
    :param x_high: the highest x coordinate of the block region
    :param y_high: the highest y coordinate of the block region
    :param z_high: the highest z coordinate of the block region
    :param side: either "in" or "out"
    :param boundary: whether the boudary is seen as in the region
    """
    def __init__(self, x_low, y_low, z_low, x_high, y_high, z_high, side="in", boundary=False):
        self.x_low = x_low
        self.y_low = y_low
        self.z_low = z_low
        self.x_high = x_high
        self.y_high = y_high
        self.z_high = z_high
        super().__init__(side, boundary)

    def __contains__(self, item):
        if self.boundary:
            ans = self.x_low <= item[0] <= self.x_high and self.y_low <= item[1] <= self.y_high \
                  and self.z_low <= item[2] <= self.z_high
        else:
            ans = self.x_low < item[0] < self.x_high and self.y_low < item[1] < self.y_high \
                  and self.z_low < item[2] < self.z_high
        return ans if self._side else not ans


class SphereRegion(Region):
    """
    This **class** is used to define a sphere region
    **New From 1.2.6.4**

    :param x: the x coordinate of the sphere origin
    :param y: the y coordinate of the sphere origin
    :param z: the z coordinate of the sphere origin
    :param r: the radius of the sphere
    :param side: either "in" or "out"
    :param boundary: whether the boudary is seen as in the region
    """
    def __init__(self, x, y, z, r, side="in", boundary=False):
        self.x = x
        self.y = y
        self.z = z
        self._r2 = r * r
        super().__init__(side, boundary)

    def __contains__(self, item):
        ans = (item[0] - self.x) ** 2 + (item[1] - self.y) ** 2 + (item[2] - self.z) ** 2
        if self.boundary:
            ans = ans <= self._r2
        else:
            ans = ans < self._r2
        return ans if self._side else not ans


class FrustumRegion(Region):
    """
    This **class** is used to define a frustum region
    **New From 1.2.6.4**

    :param x1: the x coordinate of the first circle origin
    :param y1: the y coordinate of the first circle origin
    :param z1: the z coordinate of the first circle origin
    :param r1: the radius of the first circle origin
    :param x2: the x coordinate of the second circle origin
    :param y2: the y coordinate of the second circle origin
    :param z2: the z coordinate of the second circle origin
    :param r2: the radius of the second circle origin
    :param side: either "in" or "out"
    :param boundary: whether the boudary is seen as in the region
    """
    def __init__(self, x1, y1, z1, r1, x2, y2, z2, r2, side="in", boundary=False):
        self.r1 = r1
        self.r2 = r2
        self.o1 = np.array([x1, y1, z1], dtype=np.float32)
        self.o2 = np.array([x2, y2, z2], dtype=np.float32)
        self.axis = self.o2 - self.o1
        self.length = np.linalg.norm(self.axis)
        self.axis /= self.length
        self.k = (r2 - r1) / self.length
        super().__init__(side, boundary)

    def __contains__(self, item):
        crd = np.array(item) - self.o1
        length = np.linalg.norm(crd)
        projection = np.dot(crd, self.axis)
        distance = length * length - projection * projection
        r = self.r1 + self.k * projection
        if self.boundary:
            ans = self.length >= projection >= 0 and distance <= r * r
        else:
            ans = self.length > projection > 0 and distance < r * r
        return ans if self._side else not ans


class PrismRegion(Region):
    """
    This **class** is used to define a prism (parallelepiped) region
    **New From 1.2.6.4**

    :param x0: the x coordinate of the origin
    :param y0: the y coordinate of the origin
    :param z0: the z coordinate of the origin
    :param x1: the x coordinate of the first basis vector
    :param y1: the y coordinate of the first basis vector
    :param z1: the z coordinate of the first basis vector
    :param x2: the x coordinate of the second basis vector
    :param y2: the y coordinate of the second basis vector
    :param zz: the z coordinate of the second basis vector
    :param x3: the x coordinate of the third basis vector
    :param y3: the y coordinate of the third basis vector
    :param z3: the z coordinate of the third basis vector
    :param side: either "in" or "out"
    :param boundary: whether the boudary is seen as in the region
    """
    def __init__(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3, side="in", boundary=False):
        self.l0 = np.array([x0, y0, z0], dtype=np.float32)
        self.l1 = np.array([x1, y1, z1], dtype=np.float32)
        self.l2 = np.array([x2, y2, z2], dtype=np.float32)
        self.l3 = np.array([x3, y3, z3], dtype=np.float32)
        self.n3 = np.cross(self.l1, self.l2)
        self.n3 /= np.linalg.norm(self.n3)
        self.n2 = np.cross(self.l3, self.l1)
        self.n2 /= np.linalg.norm(self.n2)
        self.n1 = np.cross(self.l2, self.l3)
        self.n1 /= np.linalg.norm(self.n1)
        self.length = np.array([np.dot(self.l1, self.n1), np.dot(self.l2, self.n2), np.dot(self.l3, self.n3)])
        assert np.all(self.length > 0), "The basis vectors should mmet the right-handed axis system requirements"
        super().__init__(side, boundary)

    def __contains__(self, item):
        crd = np.array(item) - self.l0
        if self.boundary:
            ans = 0 <= np.dot(crd, self.n1) <= self.length[0] and 0 <= np.dot(crd, self.n2) <= self.length[1] and \
                  0 <= np.dot(crd, self.n3) <= self.length[2]
        else:
            ans = 0 < np.dot(crd, self.n1) < self.length[0] and 0 < np.dot(crd, self.n2) < self.length[1] and \
                  0 < np.dot(crd, self.n3) < self.length[2]
        return ans if self._side else not ans


class Lattice:
    """
    This **class** is used to help with the process of the lattice
    **New From 1.2.6.4**

    :param style: the style of the lattice. "custom", "template:NAME" or the key values in Lattice.styles
        "sc", "fcc", "bcc", "hcp", "diamond" are in the default template styles.
    :param basis_molecule: the unit to repeat, a Residue, a ResidueType or a Molecule
    :param scale: the scale of the lattice
    :param origin: a list with 3 numbers, the origin of the lattice. [0,0,0] for default.
    :param cell_length: the length of the unit cell. [1,1,1] for default.
    :param cell_angle: the angle of the unit cell. [90,90,90] for default.
    :param basis_position: a list of lists, every sublist has 3 numbers for coordinates.
    :param spacing: a list with 3 numbers, the spacing distance in three cell basis vectors.
    :param periodic_bonds: a set of atom pair names. This can be from ResidueType.remove_periodic_connectivity
    :param periodic_cutoff: a float. 3 for default. The cutoff of the bond to be recognized as periodic or not
    """
    styles = Xdict(not_found_message="There is no lattice style named {}")

    def __init__(self, style="custom", basis_molecule=None, scale=None, origin=None, cell_length=None,
                 cell_angle=None, basis_position=None, spacing=None, periodic_bonds=None, periodic_cutoff=3):
        self.basis_molecule = basis_molecule
        if style == "custom" or style.startswith("template:"):
            self.scale = 1
            self.origin = [0, 0, 0]
            self.cell_length = [1, 1, 1]
            self.cell_angle = np.array([90, 90, 90], dtype=float)
            self.spacing = [0, 0, 0]
            self.basis_position = []
            if self.scale is not None:
                self.scale = scale
            if origin is not None:
                self.origin = origin
            if cell_length is not None:
                self.cell_length = cell_length
            if cell_angle is not None:
                self.cell_angle = np.array(cell_angle)
            assert np.all(self.cell_angle <= 90), "the cell angle should be not greater than 90 degree"
            if spacing is not None:
                self.spacing = spacing
            if basis_position is not None:
                self.basis_position = basis_position
        else:
            old_style = Lattice.styles[style]
            self.scale = scale
            self.origin = old_style.origin
            self.cell_length = old_style.cell_length
            self.cell_angle = old_style.cell_angle
            self.basis_position = old_style.basis_position
            self.spacing = old_style.spacing
        if not style.startswith("template:") and self.basis_molecule is None:
            raise ValueError("basis molecule should not be None for a non-template lattice")
        if not style.startswith("template:") and self.scale is None:
            raise ValueError("scale should not be None for a non-template lattice")
        if style.startswith("template:"):
            style_name = style.split(":")[1].strip()
            Lattice.styles[style_name] = self
        self.periodic_bonds = periodic_bonds
        if periodic_bonds and not isinstance(self.basis_molecule, ResidueType):
            raise TypeError("Only ResidueType can process the periodic_bonds")
        self.current_unbonded_periodic_atoms = set()
        self.periodic_cutoff = periodic_cutoff * periodic_cutoff

    def _process_periodic_bonds(self, mol, res, box):
        """
            process the periodicity
        """
        if not self.periodic_bonds:
            return
        for (name1, name2) in self.periodic_bonds:
            self.current_unbonded_periodic_atoms.add((res.name2atom(name1), name2))
            self.current_unbonded_periodic_atoms.add((res.name2atom(name2), name1))
        remove_key = set()
        for (atom, name) in self.current_unbonded_periodic_atoms:
            atom2 = res.name2atom(name)
            dx = atom.x - atom2.x
            dx -= np.floor(dx / (box.x_high - box.x_low) + 0.5) * (box.x_high - box.x_low)
            dy = atom.y - atom2.y
            dy -= np.floor(dy / (box.y_high - box.y_low) + 0.5) * (box.y_high - box.y_low)
            dz = atom.z - atom2.z
            dz -= np.floor(dz / (box.z_high - box.z_low) + 0.5) * (box.z_high - box.z_low)
            if dx * dx + dy * dy + dz * dz < self.periodic_cutoff:
                mol.add_residue_link(atom, atom2)
                remove_key.add((atom, name))
                remove_key.add((atom2, atom.name))
        self.current_unbonded_periodic_atoms -= remove_key

    def _judge_region(self, x1, y1, z1, x2, y2, z2, region, mol, basis_mol, res_len, box):
        """
            judge whether (x2, y2, z2) in the region. 
            If so, the basis mol will be added to mol, and coordinates will be modified
        """
        if (x2, y2, z2) in region:
            mol |= basis_mol
            for res in mol.residues[res_len:]:
                for atom in res.atoms:
                    atom.x = atom.x - x1 + x2
                    atom.y = atom.y - y1 + y2
                    atom.z = atom.z - z1 + z2
            res = mol.residues[-1]
            self._process_periodic_bonds(mol, res, box)

    def create(self, box, region, mol=None):
        """
        This **function** is used to create basis molecules to the region in the box

        :param box: the box of the system
        :param region: the region to create the basis_molecule
        :param mol: if ``mol`` the Molecule instance is provided, basis molecules will be added to ``mol``
        :return: a new Molecule instance, or the Molecule instance ``mol``
        """
        if not isinstance(box, BlockRegion) or box.side == "out":
            raise ValueError("Box should only be a BlockRegion with side == 'in' !")
        if not mol:
            mol = Molecule("unnamed")
        mol.box_length = [box.x_high - box.x_low, box.y_high - box.y_low, box.z_high - box.z_low]
        basis_mol = self.basis_molecule
        res_len = -1
        if isinstance(basis_mol, Molecule):
            basis_mol.get_atoms()
            res_len = -len(basis_mol.residues)
        bvs = get_basis_vectors_from_length_and_angle(self.cell_length[0] + self.spacing[0],
                                                      self.cell_length[1] + self.spacing[1],
                                                      self.cell_length[2] + self.spacing[2],
                                                      self.cell_angle[0], self.cell_angle[1],
                                                      self.cell_angle[2]) * self.scale
        bps = np.array([[bvs[0][0] * basis[0] + bvs[1][0] * basis[1] + bvs[2][0] * basis[2],
                         bvs[1][1] * basis[1] + bvs[2][1] * basis[2],  bvs[2][2] * basis[2]]
                         for basis in self.basis_position])
        x_init = box.x_low + self.origin[0]
        y_init = box.y_low + self.origin[1]
        z0 = box.z_low + self.origin[2]
        x1, y1, z1 = np.min([[atom.x, atom.y, atom.z] for atom in basis_mol.atoms], axis=0)
        while z0 < box.z_high:
            y0 = y_init
            while y0 < box.y_high:
                x0 = x_init
                while x0 < box.x_high:
                    for basis in bps:
                        x2 = basis[0] + x0
                        y2 = basis[1] + y0
                        z2 = basis[2] + z0
                        self._judge_region(x1, y1, z1, x2, y2, z2, region, mol, basis_mol, res_len, box)
                    x0 += bvs[0][0]
                x_init += bvs[1][0]
                x_init %= bvs[0][0]
                y0 += bvs[1][1]
            x_init += bvs[2][0]
            x_init %= bvs[0][0]
            y_init += bvs[2][1]
            y_init %= bvs[1][1]
            z0 += bvs[2][2]
        if self.current_unbonded_periodic_atoms:
            Xprint(f"Not all atoms which can form periodic bonds form periodic bonds: \
{self.current_unbonded_periodic_atoms}", "WARNING")
        return mol


SIMPLE_CUBIC_LATTICE = Lattice("template:sc", basis_position=[[0, 0, 0]])

BODY_CENTERED_CUBIC_LATTICE = Lattice("template:bcc", basis_position=[[0, 0, 0], [0.5, 0.5, 0.5]])

FACE_CENTERED_CUBIC_LATTICE = Lattice("template:fcc", basis_position=[[0, 0, 0], [0.5, 0, 0.5],
                                                                      [0, 0.5, 0.5], [0.5, 0.5, 0]])

HEXAGONAL_CLOSE_PACKED_LATTICE = Lattice("template:hcp",
                                         basis_position=[[0, 0, 0], [1/3, 1/3, 0.5]],
                                         cell_angle=[90, 90, 60],
                                         cell_length=[1, 1, 2/3*np.sqrt(6)])

DIAMOND_LATTICE = Lattice("template:diamond", basis_position=[[0, 0, 0], [0, 0.5, 0.5],
                                                              [0.5, 0, 0.5], [0.5, 0.5, 0],
                                                              [0.25, 0.25, 0.25], [0.25, 0.75, 0.75],
                                                              [0.75, 0.25, 0.75], [0.75, 0.75, 0.25]])

set_global_alternative_names()
