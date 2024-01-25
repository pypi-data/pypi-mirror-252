"""
This **module** gives the basic functions for fep calculations
"""
import re
from ...helper import source, set_global_alternative_names, Xdict, Xopen, Xprint, kabsch
from ..base import lj_base, exclude_base, bond_base, angle_base, dihedral_base, nb14_extra_base

source("....")

lj_type = lj_base.LJType

lj_type.New_From_String("""name A  B
ZERO_LJ_ATOM-ZERO_LJ_ATOM  0  0
""")

AtomType.Add_Property({"LJtypeB": str})
AtomType.Add_Property({"subsys": int})


def _find_common_forces(forcetype, aforces, bforces, mol_b2mol_a):
    """

    :param forcetype:
    :param aforces:
    :param bforces:
    :param mol_b2mol_a:
    :return:
    """
    toret = []
    temp_map = Xdict()
    temp_map2 = Xdict()
    for force in bforces:
        temp_map2[force] = True
        for fatoms in forcetype.Same_Force(force.atoms):
            temp_map["-".join(list(map(lambda atom: str(mol_b2mol_a[atom]), fatoms)))] = force
    for force in aforces:
        tofind = "-".join(list(map(str, force.atoms)))
        bforce = temp_map.get(tofind, None)
        toret.append([force, bforce])
        temp_map2[bforce] = False
    for force in bforces:
        if temp_map2[force]:
            toret.append([None, force])
    return toret


FEP_BONDED_FORCE_MERGE_RULE = Xdict()
TINY = 1e-10 / 18.2223


# pylint: disable=unused-argument
def _nb14_extra_merge_rule(mol_r, mol_a, mol_b, forcetype, rforces, bforces, lambda_, mol_r2mol_a, mol_a2mol_r,
                           mol_r2mol_b, mol_b2mol_r):
    """

    :param mol_r:
    :param mol_a:
    :param mol_b:
    :param forcetype:
    :param rforces:
    :param bforces:
    :param lambda_:
    :param mol_r2mol_a:
    :param mol_a2mol_r:
    :param mol_r2mol_b:
    :param mol_b2mol_r:
    :return:
    """
    forcepair = _find_common_forces(forcetype, rforces, bforces, mol_b2mol_r)
    for f_r, f_b in forcepair:
        if f_b is None:
            temp_charge0 = f_r.atoms[0].charge if abs(f_r.atoms[0].charge) > TINY else TINY
            temp_charge1 = f_r.atoms[1].charge if abs(f_r.atoms[1].charge) > TINY else TINY

            if f_r.nb14_ee_factor is not None:
                nb14_ee_factor = f_r.nb14_ee_factor
            else:
                nb14_ee_factor = f_r.kee * mol_r2mol_a[f_r.atoms[0]].charge * \
                                 mol_r2mol_a[f_r.atoms[1]].charge
            f_r.kee = nb14_ee_factor / temp_charge0 / temp_charge1

            f_r.kee *= 1 - lambda_
            f_r.A *= 1 - lambda_
            f_r.B *= 1 - lambda_
        elif f_r is None:
            f_r = nb14_extra_base.NB14Type.entity(list(map(lambda x: mol_b2mol_r[x], f_b.atoms)), f_b.type, f_b.name)

            temp_charge0 = f_r.atoms[0].charge if abs(f_r.atoms[0].charge) > TINY else TINY
            temp_charge1 = f_r.atoms[1].charge if abs(f_r.atoms[1].charge) > TINY else TINY

            if f_b.nb14_ee_factor is not None:
                nb14_ee_factor = f_b.nb14_ee_factor
            else:
                nb14_ee_factor = f_b.kee * f_b.atoms[0].charge * \
                                 f_b.atoms[1].charge
            f_r.kee = nb14_ee_factor / temp_charge0 / temp_charge1

            f_r.A = f_b.A * lambda_
            f_r.B = f_b.B * lambda_
            f_r.kee = f_b.kee * lambda_
            mol_r.Add_Bonded_Force(f_r)
        else:
            temp_charge0 = f_r.atoms[0].charge if abs(f_r.atoms[0].charge) > TINY else TINY
            temp_charge1 = f_r.atoms[1].charge if abs(f_r.atoms[1].charge) > TINY else TINY

            if f_r.nb14_ee_factor is not None:
                nb14_ee_factor = f_r.nb14_ee_factor
            else:
                nb14_ee_factor = f_r.kee * mol_r2mol_a[f_r.atoms[0]].charge * \
                                 mol_r2mol_a[f_r.atoms[1]].charge
            f_r.kee = nb14_ee_factor / temp_charge0 / temp_charge1

            if f_b.nb14_ee_factor is not None:
                nb14_ee_factor = f_b.nb14_ee_factor
            else:
                nb14_ee_factor = f_b.kee * f_b.atoms[0].charge * \
                                 f_b.atoms[1].charge
            kee = nb14_ee_factor / temp_charge0 / temp_charge1

            f_r.kee = f_r.kee * (1 - lambda_) + kee * lambda_
            f_r.A = f_r.A * (1 - lambda_) + f_b.A * lambda_
            f_r.B = f_r.B * (1 - lambda_) + f_b.B * lambda_


FEP_BONDED_FORCE_MERGE_RULE["nb14_extra"] = {"lambda_name": "dihedral", "merge_function": _nb14_extra_merge_rule}


def _bond_base_merge_rule(mol_r, mol_a, mol_b, forcetype, rforces, bforces, lambda_,
                          mol_r2mol_a, mol_a2mol_r, mol_r2mol_b, mol_b2mol_r):
    """

    :param mol_r:
    :param mol_a:
    :param mol_b:
    :param forcetype:
    :param rforces:
    :param bforces:
    :param lambda_:
    :param mol_r2mol_a:
    :param mol_a2mol_r:
    :param mol_r2mol_b:
    :param mol_b2mol_r:
    :return:
    """
    forcepair = _find_common_forces(forcetype, rforces, bforces, mol_b2mol_r)
    for f_r, f_b in forcepair:
        if f_b is None:
            mol_r.bonded_forces["bond_base"].remove(f_r)
            f_r.from_AorB = 0
            mol_r.Add_Bonded_Force(f_r, "soft_bond_base")
        elif f_r is None:
            f_r = bond_base.BondType.entity(list(map(lambda x: mol_b2mol_r[x], f_b.atoms)), f_b.type, f_b.name)
            f_r.k = f_b.k
            f_r.b = f_b.b
            f_r.from_AorB = 1
            mol_r.Add_Bonded_Force(f_r, "soft_bond_base")
        elif abs(f_r.b - f_b.b) < 1e-5:
            f_r.k = f_r.k * (1 - lambda_) + f_b.k * lambda_
        else:
            f_r2 = bond_base.BondType.entity(list(map(lambda x: mol_b2mol_r[x], f_b.atoms)), f_b.type, f_b.name)
            f_r2.k = f_b.k * lambda_
            f_r.b = f_b.b
            f_r.k *= (1 - lambda_)
            mol_r.Add_Bonded_Force(f_r2)


FEP_BONDED_FORCE_MERGE_RULE["bond"] = {"lambda_name": "bond_base", "merge_function": _bond_base_merge_rule}


def _angle_merge_rule(mol_r, mol_a, mol_b, forcetype, rforces, bforces, lambda_, mol_r2mol_a, mol_a2mol_r, mol_r2mol_b,
                      mol_b2mol_r):
    """

    :param mol_r:
    :param mol_a:
    :param mol_b:
    :param forcetype:
    :param rforces:
    :param bforces:
    :param lambda_:
    :param mol_r2mol_a:
    :param mol_a2mol_r:
    :param mol_r2mol_b:
    :param mol_b2mol_r:
    :return:
    """
    forcepair = _find_common_forces(forcetype, rforces, bforces, mol_b2mol_r)
    for f_r, f_b in forcepair:
        if f_b is None:
            f_r.k *= 1 - lambda_
        elif f_r is None:
            f_r = angle_base.AngleType.entity(list(map(lambda x: mol_b2mol_r[x], f_b.atoms)), f_b.type, f_b.name)
            f_r.k *= lambda_
            f_r.b = f_b.b
            mol_r.Add_Bonded_Force(f_r)
        elif abs(f_r.b - f_b.b) < 1e-5:
            f_r.k = f_r.k * (1 - lambda_) + f_b.k * lambda_
        else:
            f_r2 = angle_base.AngleType.entity(list(map(lambda x: mol_b2mol_r[x], f_b.atoms)), f_b.type, f_b.name)
            f_r2.k = f_b.k * lambda_
            f_r2.b = f_b.b
            f_r.k *= (1 - lambda_)
            mol_r.Add_Bonded_Force(f_r2)


FEP_BONDED_FORCE_MERGE_RULE["angle"] = {"lambda_name": "angle", "merge_function": _angle_merge_rule}


def _dihedral_merge_rule(mol_r, mol_a, mol_b, forcetype, rforces, bforces, lambda_, mol_r2mol_a, mol_a2mol_r,
                         mol_r2mol_b, mol_b2mol_r):
    """

    :param mol_r:
    :param mol_a:
    :param mol_b:
    :param forcetype:
    :param rforces:
    :param bforces:
    :param lambda_:
    :param mol_r2mol_a:
    :param mol_a2mol_r:
    :param mol_r2mol_b:
    :param mol_b2mol_r:
    :return:
    """
    forcepair = _find_common_forces(forcetype, rforces, bforces, mol_b2mol_r)
    for f_r, f_b in forcepair:
        if f_b is None:
            for i in range(f_r.multiple_numbers):
                f_r.ks[i] *= 1 - lambda_
        elif f_r is None:
            f_r2 = dihedral_base.ProperType.entity(list(map(lambda x: mol_b2mol_r[x], f_b.atoms)), f_b.type, f_b.name)
            f_r2.multiple_numbers = f_b.multiple_numbers
            for i in range(f_b.multiple_numbers):
                f_r2.ks.append(f_b.ks[i] * lambda_)
                f_r2.phi0s.append(f_b.phi0s[i])
                f_r2.periodicitys.append(f_b.periodicitys[i])
            mol_r.Add_Bonded_Force(f_r2)
        else:
            sameforce = f_r.multiple_numbers == f_b.multiple_numbers
            if sameforce:
                check_map = Xdict()
                for i in range(f_b.multiple_numbers):
                    check_map[f_b.periodicitys[i]] = f_b.phi0s[i]
                for i in range(f_r.multiple_numbers):
                    if abs(check_map.get(f_r.periodicitys[i], float("Inf")) - f_r.phi0s[i]) > 1e-5:
                        sameforce = False
                        break
            if sameforce:
                for i in range(f_r.multiple_numbers):
                    f_r.ks[i] = f_r.ks[i] * (1 - lambda_) + f_b.ks[i] * lambda_
            else:
                for i in range(f_r.multiple_numbers):
                    f_r.ks[i] *= (1 - lambda_)
                f_r2 = dihedral_base.ProperType.entity(list(map(lambda x: mol_b2mol_r[x], f_b.atoms)), f_b.type,
                                                       f_b.name)
                f_r2.multiple_numbers = f_b.multiple_numbers
                for i in range(f_b.multiple_numbers):
                    f_r2.ks.append(f_b.ks[i] * lambda_)
                    f_r2.phi0s.append(f_b.phi0s[i])
                    f_r2.periodicitys.append(f_b.periodicitys[i])
                mol_r.Add_Bonded_Force(f_r2)


FEP_BONDED_FORCE_MERGE_RULE["dihedral"] = {"lambda_name": "dihedral", "merge_function": _dihedral_merge_rule}


def _improper_merge_rule(mol_r, mol_a, mol_b, forcetype, rforces, bforces, lambda_, mol_r2mol_a, mol_a2mol_r,
                         mol_r2mol_b, mol_b2mol_r):
    """

    :param mol_r:
    :param mol_a:
    :param mol_b:
    :param forcetype:
    :param rforces:
    :param bforces:
    :param lambda_:
    :param mol_r2mol_a:
    :param mol_a2mol_r:
    :param mol_r2mol_b:
    :param mol_b2mol_r:
    :return:
    """
    forcepair = _find_common_forces(forcetype, rforces, bforces, mol_b2mol_r)
    for f_r, f_b in forcepair:
        if f_b is None:
            f_r.k *= 1 - lambda_
        elif f_r is None:
            f_r = dihedral_base.ImproperType.entity(list(map(lambda x: mol_b2mol_r[x], f_b.atoms)), f_b.type, f_b.name)
            f_r.k = f_b.k * lambda_
            f_r.phi0 = f_b.phi0
            f_r.periodicity = f_b.periodicity
            mol_r.Add_Bonded_Force(f_r)
        elif abs(f_r.phi0 - f_b.phi0) < 1e-5 and f_r.periodicity == f_b.periodicity:
            f_r.k = f_r.k * (1 - lambda_) + f_b.k * lambda_
        else:
            f_r2 = dihedral_base.ImproperType.entity(list(map(lambda x: mol_b2mol_r[x], f_b.atoms)), f_b.type, f_b.name)
            f_r2.k = f_b.k * lambda_
            f_r2.phi0 = f_b.phi0
            f_r2.periodicity = f_b.periodicity
            f_r.k *= (1 - lambda_)
            mol_r.Add_Bonded_Force(f_r2)


FEP_BONDED_FORCE_MERGE_RULE["improper"] = {"lambda_name": "dihedral", "merge_function": _improper_merge_rule}


def save_hard_core_lj():
    """
    This **function** is used to save hard core lj

    :return: None
    """
    Molecule.Set_Save_SPONGE_Input("LJ")(lj_base.write_zero_lj)
    Molecule.Del_Save_SPONGE_Input("LJ_soft_core")
    Molecule.Del_Save_SPONGE_Input("subsys_division")


def save_soft_core_lj():
    """
    This **function** is used to save soft core lj

    :return: None
    """
    Molecule.Del_Save_SPONGE_Input("LJ")

    def write_subsys_division(self):
        towrite = "%d\n" % len(self.atoms)
        for atom in self.atoms:
            if getattr(atom, "subsys", None) is None:
                towrite += "%d\n" % 0
            else:
                towrite += "%d\n" % atom.subsys
        return towrite

    Molecule.Set_Save_SPONGE_Input("subsys_division")(write_subsys_division)

    def write_soft_lj(self):
        """

        :param self:
        :return:
        """
        lj_types = []
        lj_typemap = Xdict()
        lj_typeb = []
        lj_typemapb = Xdict()
        for atom in self.atoms:
            if atom.LJtype not in lj_typemap.keys():
                lj_typemap[atom.LJtype] = len(lj_types)
                lj_types.append(atom.LJtype)
            if atom.LJtypeB is None:
                atom.LJtypeB = atom.LJtype
            if atom.LJtypeB not in lj_typemapb.keys():
                lj_typemapb[atom.LJtypeB] = len(lj_typeb)
                lj_typeb.append(atom.LJtypeB)

        # pylint: disable=protected-access
        lj_as, lj_bs = lj_base._find_ab_lj(lj_types)
        lj_asb, lj_bsb = lj_base._find_ab_lj(lj_typeb)
        checks = lj_base._get_checks(lj_types, lj_as, lj_bs)
        same_type = lj_base._judge_same_type(lj_types, checks)
        real_lj_types = lj_base._get_real_lj(lj_types, same_type)
        real_as, real_bs = lj_base._find_ab_lj(real_lj_types, False)

        checks = lj_base._get_checks(lj_typeb, lj_asb, lj_bsb)
        same_typeb = lj_base._judge_same_type(lj_typeb, checks)
        real_lj_typesb = lj_base._get_real_lj(lj_typeb, same_typeb)
        real_asb, real_bsb = lj_base._find_ab_lj(real_lj_typesb, False)

        towrite = "%d %d %d\n\n" % (len(self.atoms), len(real_lj_types), len(real_lj_typesb))
        count = 0
        for i in range(len(real_lj_types)):
            for _ in range(i + 1):
                towrite += "%16.7e" % real_as[count] + " "
                count += 1
            towrite += "\n"
        towrite += "\n"

        count = 0
        for i in range(len(real_lj_types)):
            for _ in range(i + 1):
                towrite += "%16.7e" % real_bs[count] + " "
                count += 1
            towrite += "\n"
        towrite += "\n"

        count = 0
        for i in range(len(real_lj_typesb)):
            for _ in range(i + 1):
                towrite += "%16.7e" % real_asb[count] + " "
                count += 1
            towrite += "\n"
        towrite += "\n"

        count = 0
        for i in range(len(real_lj_typesb)):
            for _ in range(i + 1):
                towrite += "%16.7e" % real_bsb[count] + " "
                count += 1
            towrite += "\n"

        towrite += "\n"
        towrite += "\n".join(
            ["%d %d" % (same_type[lj_typemap[atom.LJtype]], same_typeb[lj_typemapb[atom.LJtypeB]]) for atom in
             self.atoms])
        return towrite

    Molecule.Set_Save_SPONGE_Input("LJ_soft_core")(write_soft_lj)


def intramolecule_nb_to_nb14(mol_a, perturbating_residues):
    """
    This **function** convert the non bonded interactions to nb14 interactions within the molecule

    :param mol_a: the Molecule instance
    :param perturbating_residues: the residue(s) to be perturbed
    :return:
    """
    if isinstance(perturbating_residues, Residue):
        perturbating_residues = [perturbating_residues]
    build.Build_Bonded_Force(mol_a)
    a_exclude = exclude_base.Exclude.current.Get_Excluded_Atoms(mol_a)
    for residue1 in perturbating_residues:
        for atom_a1 in residue1.atoms:
            for residue2 in perturbating_residues:
                for atom_a2 in residue2.atoms:
                    if atom_a1 == atom_a2:
                        continue
                    if atom_a2 not in a_exclude[atom_a1]:
                        temp_a, temp_b = nb14_extra_base.get_nb14_extra_lj(atom_a1, atom_a2)
                        new_force = nb14_extra_base.NB14Type.entity([atom_a1, atom_a2],
                                                                    nb14_extra_base.NB14Type.get_type("UNKNOWNS"))
                        new_force.A = temp_a
                        new_force.B = temp_b
                        new_force.kee = 1
                        mol_a.Add_Bonded_Force(new_force)

                        atom_a1.Extra_Exclude_Atom(atom_a2)
                        a_exclude[atom_a1].add(atom_a2)
                        a_exclude[atom_a2].add(atom_a1)


def get_free_molecule(mol_a, perturbating_residues, intra_fep=False):
    """
    This **function** makes the molecule to be "free", having no interaction with other molecules

    :param mol_a: the Molecule instance
    :param perturbating_residues: the residues to be perturbed
    :param intra_fep: whether clear intramolecular non bonded interactions
    :return: a new Molecule instance
    """
    if isinstance(perturbating_residues, Residue):
        perturbating_residues = [perturbating_residues]
    build.Build_Bonded_Force(mol_a)
    nb14_extra_base.NB14_To_NB14EXTRA(mol_a)
    mol_b = mol_a.deepcopy()
    mol_a2mol_b = Xdict()
    for i, atom_a in enumerate(mol_a.atoms):
        mol_a2mol_b[atom_a] = mol_b.atoms[i]

    for residue in perturbating_residues:
        for atom_a in residue.atoms:
            atom = mol_a2mol_b[atom_a]
            atom.charge = 0
            atom.LJtype = "ZERO_LJ_ATOM"
            atom.subsys = 1
            atom_a.subsys = 1

    return mol_b


def _correct_residueb_coordinates(residue_a, residue_b, matchmap):
    """

    :param residue_a:
    :param residue_b:
    :param matchmap:
    :return:
    """
    template_positions = []
    certified_positions = []
    residue_type_a = residue_a.type
    for i, atom in enumerate(residue_b.atoms):
        if i in matchmap.keys():
            temp_atom = residue_a.name2atom(residue_type_a.atoms[matchmap[i]].name)
            template_positions.append([temp_atom.x, temp_atom.y, temp_atom.z])
            certified_positions.append([atom.x, atom.y, atom.z])

    rotation, center1, center2 = kabsch(template_positions, certified_positions)

    for atom in residue_b.atoms:
        temp_position = np.array([getattr(atom, xyz) for xyz in "xyz"])
        tnew_position = np.dot(rotation, (temp_position - center2)) + center1
        atom.x = tnew_position[0]
        atom.y = tnew_position[1]
        atom.z = tnew_position[2]


def _get_extra_atoms_and_rbmap(restype_ab, residue_type_a, residue_type_b, residue_a,
                               forcopy, matchmap, match_a, match_b):
    """
        get the extra atoms of the residue and the map from the mixed residue to residue b
    """
    extra_a = []
    extra_b = []
    rbmap = {value: key for key, value in matchmap.items()}
    for i, atom in enumerate(residue_type_a.atoms):
        atom.x = residue_a.name2atom(atom.name).x
        atom.y = residue_a.name2atom(atom.name).y
        atom.z = residue_a.name2atom(atom.name).z
        if i not in match_a:
            extra_a.append(atom.copied[forcopy])
            extra_a[-1].subsys = 1

    for i, atom in enumerate(residue_type_b.atoms):
        if i not in match_b:
            rbmap[len(restype_ab.atoms)] = i
            restype_ab.Add_Atom(atom.name + "R2", atom.type, atom.x, atom.y, atom.z)
            atom.copied[forcopy] = restype_ab.atoms[-1]
            atom.copied[forcopy].contents = dict(atom.contents.items())
            atom.copied[forcopy].name = atom.name + "R2"
            extra_b.append(atom.copied[forcopy])
            extra_b[-1].subsys = 2
        else:
            residue_type_b.atoms[i].copied[forcopy] = restype_ab.atoms[matchmap[i]]
    return extra_a, extra_b, rbmap


def _link_restypeb_atoms(residue_type_b, forcopy, matchmap):
    """

    :param residue_type_b:
    :param forcopy:
    :param matchmap:
    :return:
    """
    for atom in residue_type_b.atoms:
        for key, _ in atom.copied[forcopy].linked_atoms.items():
            for aton in atom.linked_atoms.get(key, []):
                if not (residue_type_b.atom2index(aton) in matchmap.keys()
                        and residue_type_b.atom2index(atom) in matchmap.keys()):
                    atom.copied[forcopy].Link_Atom(key, aton.copied[forcopy])


def _get_residue_ab(residue_type_a, residue_type_b, residue_a, forcopy, matchmap, match_a, match_b):
    """
        get the mixed residue type
    """
    restype_ab = residue_type_a.deepcopy(residue_type_a.name + "_" + residue_type_b.name, forcopy)

    extra_a, extra_b, rbmap = _get_extra_atoms_and_rbmap(restype_ab, residue_type_a, residue_type_b, residue_a, forcopy,
                                                         matchmap, match_a, match_b)

    for atomi in extra_a:
        for atomj in extra_b:
            atomi.Extra_Exclude_Atom(atomj)

    for atom, connect_set in residue_type_b.connectivity.items():
        for aton in connect_set:
            restype_ab.Add_Connectivity(atom.copied[forcopy], aton.copied[forcopy])

    for bond_entities in residue_type_b.bonded_forces.values():
        for bond_entity in bond_entities:
            tocopy = False
            for atom in bond_entity.atoms:
                if residue_type_b.atom2index(atom) not in matchmap.keys():
                    tocopy = True
                    break
            if tocopy:
                restype_ab.Add_Bonded_Force(bond_entity.deepcopy(forcopy))

    _link_restypeb_atoms(residue_type_b, forcopy, matchmap)

    return restype_ab, rbmap


def _nhydrogen(rdmol, j):
    """get the number of hydrogens of the j-th atom in an rdkit rdmol instance"""
    return rdmol.GetAtomWithIdx(j).GetTotalNumHs(includeNeighbors=True)


def merge_dual_topology(mol, residue_a, residue_b, assign_a, assign_b,
                        tmcs=60, image_path=None, similarity_limit=0, imcs=None):
    """
    This **function** perturbs a residue in the molecule into another type in the dual topology way

    :param mol: the Molecule instance
    :param residue_a: the Residue which needs to be perturbed
    :param residue_b: the Residue which is perturbed to
    :param assign_a: the Assign instance corresponding to ``residue_a``
    :param assign_b: the Assign instance corresponding to ``residue_b``
    :param tmcs: the max time to find the max common structure
    :param image_path: the path to save the mcs image
    :param similarity_limit: the limitation of the similarity. The similarity is calculated by \
the tanimoto coefficient of the max common structure.
    :param imcs: the input file to store the mcs information
    :return: two molecules in the initial and final lambda stat respectively, and the matchmap
    """
    build.Build_Bonded_Force(mol)
    build.Build_Bonded_Force(residue_b.type)

    from ...helper.rdkit import assign_to_rdmol
    from rdkit.Chem import rdFMCS as MCS
    from rdkit.Chem import Draw, AllChem, RemoveHs, SanitizeMol, rdmolops

    rdmol_a = assign_to_rdmol(assign_a)
    rdmol_b = assign_to_rdmol(assign_b)
    if imcs is None:
        Xprint("FINDING MAXIMUM COMMON SUBSTRUCTURE\n")
        flags = rdmolops.SanitizeFlags
        rdmol_a_no_h = RemoveHs(rdmol_a, sanitize=False)
        SanitizeMol(rdmol_a_no_h, flags.SANITIZE_ALL & ~flags.SANITIZE_PROPERTIES)
        rdmol_b_no_h = RemoveHs(rdmol_b, sanitize=False)
        SanitizeMol(rdmol_b_no_h, flags.SANITIZE_ALL & ~flags.SANITIZE_PROPERTIES)
        result = MCS.FindMCS([rdmol_a_no_h, rdmol_b_no_h],
                             completeRingsOnly=True,
                             bondCompare=MCS.BondCompare.CompareOrderExact,
                             timeout=tmcs)
        rdmol_mcs = result.queryMol
        if rdmol_mcs is None:
            raise OSError("No common substructure found")
        match_a = rdmol_a.GetSubstructMatch(rdmol_mcs)
        a_hydros = {i: _nhydrogen(rdmol_a, j) for i, j in enumerate(match_a)}
        match_b = sorted(rdmol_b.GetSubstructMatches(rdmol_mcs, uniquify=False),
                         key=lambda x: sum(min(_nhydrogen(rdmol_b, j), a_hydros[i]) for i,j in enumerate(x)))[-1]
        matchmap = {match_b[j]: match_a[j] for j in range(len(match_a))}
        extra_map = {}
        for j, i in matchmap.items():
            a = rdmol_a.GetAtomWithIdx(i)
            a_hydrogens = []
            for ai in a.GetNeighbors():
                if ai.GetAtomicNum() == 1:
                    a_hydrogens.append(ai.GetIdx())
            b = rdmol_b.GetAtomWithIdx(j)
            for bi in b.GetNeighbors():
                if not a_hydrogens:
                    break
                if bi.GetAtomicNum() == 1:
                    extra_map[bi.GetIdx()] = a_hydrogens.pop()
        matchmap.update(extra_map)
        match_a, match_b = zip(*[[value, key] for key, value in matchmap.items()])
        tanimoto = len(match_a)
        tanimoto /= len(assign_a.atoms) + len(assign_b.atoms) - tanimoto
        Xprint(f"similarity: {tanimoto}")
        if image_path:
            draw_a = assign_to_rdmol(assign_a)
            draw_b = assign_to_rdmol(assign_b)
            AllChem.Compute2DCoords(draw_a)
            AllChem.Compute2DCoords(draw_b)
            for atom in draw_a.GetAtoms():
                atom.SetProp("atomLabel", atom.GetSymbol())
            for atom in draw_b.GetAtoms():
                atom.SetProp("atomLabel", atom.GetSymbol())
            img = Draw.MolsToGridImage([draw_a, draw_b],
                                       molsPerRow=1,
                                       subImgSize=(1200, 600),
                                       highlightAtomLists=[match_a, match_b])
            img.save(image_path)
            f = Xopen(os.path.splitext(image_path)[0] + ".txt", "w")
            f.write(f"similarity: {tanimoto}\n")
            f.write(f"mcs atoms in r1: {match_a}\n\n")
            f.write(f"mcs atoms in r2: {match_b}\n\n")
            f.close()
    else:
        match_a = None
        match_b = None
        with open(imcs) as f:
            for line in f:
                if line.startswith("mcs atoms in"):
                    result = re.search(r"r(\d): (.*)", line)
                    if result is None or len(result.groups()) != 2:
                        raise ValueError(f"the format of the mcs file {imcs} is not right")
                    id_ = int(result.group(1))
                    atoms = tuple(int(i) for i in result.group(2).replace('(', "")
                                                            .replace(')', "")
                                                            .split(","))
                    if id_ == 1:
                        match_a = atoms
                    elif id_ == 2:
                        match_b = atoms
                    else:
                        raise ValueError(f"the format of the mcs file {imcs} is not right")
        if match_a is None or match_b is None or len(match_a) != len(match_b):
            raise ValueError(f"the format of the mcs file {imcs} is not right")
        matchmap = {match_b[j]: match_a[j] for j in range(len(match_a))}
        tanimoto = len(match_a)
        tanimoto /= len(assign_a.atoms) + len(assign_b.atoms) - tanimoto
        Xprint(f"similarity: {tanimoto}")
    if tanimoto <= similarity_limit:
        Xprint(f"similarity (={tanimoto}) should be greater than {similarity_limit}", "ERROR")
        sys.exit(2)
    Xprint("ALIGNING TOPOLOGY AND COORDINATE\n")

    residue_type_a = residue_a.type

    if isinstance(residue_b, Residue):
        residue_type_b = residue_b.type
    elif isinstance(residue_b, ResidueType):
        residue_type_b = residue_b
    else:
        raise TypeError

    _correct_residueb_coordinates(residue_a, residue_type_b, matchmap)

    forcopy = hash(str(time.time()))
    restype_ab, rbmap = _get_residue_ab(residue_type_a, residue_type_b, residue_a, forcopy, matchmap, match_a, match_b)

    restype_ba = restype_ab.deepcopy(residue_type_b.name + "_" + residue_type_a.name)

    build.Build_Bonded_Force(restype_ba)
    build.Build_Bonded_Force(restype_ab)

    nb14_extra_base.nb14_to_nb14_extra(restype_ba)
    nb14_extra_base.nb14_to_nb14_extra(restype_ab)
    for i, atomi in enumerate(restype_ab.atoms):
        if i < len(residue_type_a.atoms):
            atomi.contents.update(
                {key: value for key, value in residue_type_a.atoms[i].contents.items() if key != "name"})
        else:
            restype_ab.atoms[i].LJtype = "ZERO_LJ_ATOM"
            restype_ab.atoms[i].charge = 0
            restype_ab.atoms[i].subsys = 2
            restype_ba.atoms[i].subsys = 2

        if i in rbmap:
            restype_ba.atoms[i].contents.update(
                {key: value for key, value in residue_type_b.atoms[rbmap[i]].contents.items() if key != "name"})
        else:
            restype_ba.atoms[i].LJtype = "ZERO_LJ_ATOM"
            restype_ba.atoms[i].charge = 0
            restype_ab.atoms[i].subsys = 1
            restype_ba.atoms[i].subsys = 1

    mol_a = Molecule(mol.name + "A")
    mol_b = Molecule(mol.name + "B")

    ri = 0
    res2index = Xdict()
    for i, res in enumerate(mol.residues):
        res2index[res] = i
        if res == residue_a:
            mol_a.Add_Residue(restype_ab)
            mol_b.Add_Residue(restype_ba)
            ri = i
        else:
            mol_a.Add_Residue(res.deepcopy())
            mol_b.Add_Residue(res.deepcopy())

    for reslink in mol.residue_links:
        atom1 = reslink.atom1
        atom2 = reslink.atom2
        new_atom1_a = mol_a.residues[res2index[atom1.residue]].name2atom(atom1.name)
        new_atom1_b = mol_b.residues[res2index[atom1.residue]].name2atom(atom1.name)
        new_atom2_a = mol_a.residues[res2index[atom2.residue]].name2atom(atom2.name)
        new_atom2_b = mol_b.residues[res2index[atom2.residue]].name2atom(atom2.name)
        if atom1.residue == residue_a:
            new_atom1_a = mol_a.residues[ri].name2atom(new_atom1_a.name)
            new_atom1_b = mol_b.residues[ri].name2atom(new_atom1_b.name)
        if atom2.residue == residue_a:
            new_atom2_a = mol_a.residues[ri].name2atom(new_atom2_a.name)
            new_atom2_b = mol_b.residues[ri].name2atom(new_atom2_b.name)
        mol_a.add_residue_link(new_atom1_a, new_atom2_a)
        mol_b.add_residue_link(new_atom1_b, new_atom2_b)
    build.Build_Bonded_Force(mol_a)
    build.Build_Bonded_Force(mol_b)

    return mol_a, mol_b, matchmap


def merge_force_field(mol_a, mol_b, default_lambda, specific_lambda=None, intra_fep=False):
    """
    This **function** merges one molecule in two different force fields (two Molecule instances) into one

    :param mol_a: the Molecule instance in the initial lambda stat
    :param mol_b: the Molecule instance in the final lambda stat
    :param default_lambda: the lambda to scale the force if no ``specific_lambda`` is set for the force
    :param specific_lambda: a dict to map the force to its special scale factor lambda
    :param intra_fep: whether clear intramolecular non bonded interactions
    :return: the Molecule instance merged
    """
    if specific_lambda is None:
        specific_lambda = Xdict()
    build.Build_Bonded_Force(mol_a)
    build.Build_Bonded_Force(mol_b)

    nb14_extra_base.nb14_to_nb14_extra(mol_a)
    nb14_extra_base.nb14_to_nb14_extra(mol_b)

    assert len(mol_a.atoms) == len(mol_b.atoms)
    mol_a2mol_b = Xdict()
    for i, atom_a in enumerate(mol_a.atoms):
        mol_a2mol_b[atom_a] = mol_b.atoms[i]

    mol_r = mol_a.deepcopy()

    mol_r2mol_a = Xdict()
    mol_r2mol_b = Xdict()
    for i, atom_ret in enumerate(mol_r.atoms):
        mol_r2mol_a[atom_ret] = mol_a.atoms[i]
        mol_r2mol_b[atom_ret] = mol_b.atoms[i]
    mol_b2mol_r = {value: key for key, value in mol_r2mol_b.items()}
    mol_a2mol_r = {value: key for key, value in mol_r2mol_a.items()}

    charge_lambda = specific_lambda.get("charge", default_lambda)
    mass_lambda = specific_lambda.get("mass", default_lambda)

    for i, atom in enumerate(mol_r.atoms):
        atom.charge = mol_r2mol_a[atom].charge * (1 - charge_lambda) + mol_r2mol_b[atom].charge * charge_lambda
        atom.mass = mol_r2mol_a[atom].mass * (1 - mass_lambda) + mol_r2mol_b[atom].mass * mass_lambda
        atom.LJtypeB = mol_r2mol_b[atom].LJtype

    for forcename, rforces in mol_r.bonded_forces.items():
        if forcename in FEP_BONDED_FORCE_MERGE_RULE.keys():
            temp_lambda = specific_lambda.get(FEP_BONDED_FORCE_MERGE_RULE[forcename].get("lambda_name"),
                                              default_lambda)
            bforces = mol_b.bonded_forces.get(forcename, [])
            FEP_BONDED_FORCE_MERGE_RULE[forcename].get("merge_function")(mol_r, mol_a, mol_b,
                                                                         GlobalSetting.BondedForcesMap[forcename],
                                                                         rforces, bforces, temp_lambda, mol_r2mol_a,
                                                                         mol_a2mol_r, mol_r2mol_b, mol_b2mol_r)
        elif rforces:
            raise NotImplementedError(forcename + " is not supported for FEP to merge force field yet.")

    for forcename, parameters in FEP_BONDED_FORCE_MERGE_RULE.items():
        temp_lambda = specific_lambda.get(parameters["lambda_name"], default_lambda)

    return mol_r


set_global_alternative_names()
