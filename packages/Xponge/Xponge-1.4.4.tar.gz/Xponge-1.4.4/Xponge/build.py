"""
This **module** is used to build and save
"""
import os
from itertools import product
from warnings import warn
from . import assign
from .helper import AbstractMolecule, ResidueType, Molecule, Residue, GlobalSetting, Xopen, Xdict, \
    set_global_alternative_names


def _analyze_connectivity(cls):
    """

    :param cls:
    :return:
    """
    for atom0, c in cls.connectivity.items():
        index_dict = Xdict().fromkeys(c, atom0)
        for i in range(2, GlobalSetting.farthest_bonded_force + 1):
            index_next = Xdict()
            for atom1, from_atom in index_dict.items():
                atom0.Link_Atom(i, atom1)
                index_temp = Xdict().fromkeys(cls.connectivity[atom1], atom1)
                index_temp.pop(from_atom, None)
                index_temp.update(index_temp.fromkeys(index_temp.keys() & index_next.keys()))
                index_next.update(index_temp)
            index_dict = index_next



def _check_backup(backups, atom1, top_matrix, i, d):
    """

    :param backups:
    :param atom1:
    :param top_matrix:
    :param d:
    :return:
    """
    for backup in backups[i - 1]:
        good_backup = True
        for j, atomj in enumerate(backup):
            if atomj == atom1 or abs(top_matrix[j][i]) <= 1 \
                    or atom1 not in atomj.linked_atoms[abs(top_matrix[j][i])]:
                good_backup = False
                break
            if top_matrix[j][i] <= -1:
                for d2 in range(2, d):
                    if atom1 in atomj.linked_atoms[d2]:
                        good_backup = False
                        break
        if good_backup:
            backups[i].append([*backup, atom1])


def _get_frc_all(frc, cls):
    """

    :param frc:
    :param cls:
    :return:
    """
    top = frc.topology_like
    top_matrix = frc.topology_matrix
    frc_all = []
    for atom0 in cls.atoms:
        backups = {i: [] for i in range(len(top))}
        backups[0].append([atom0])
        for i, d in enumerate(top):
            if i == 0:
                continue
            for atom1 in atom0.linked_atoms[d]:
                _check_backup(backups, atom1, top_matrix, i, d)
        frc_all.extend(backups[len(top) - 1])
    cls.checked_list[frc.get_class_name()] = [[atom.name for atom in pairs] for pairs in frc_all]
    return frc_all


def _get_frc_all_final(frc, frc_all):
    """

    :param frc:
    :param frc_all:
    :return:
    """
    frc_all_final = []
    frc_keys = Xdict()
    for frc_one in frc_all:
        frc_one_name = "".join([str(hash(atom)) for atom in frc_one])
        if frc_one_name in frc_keys.keys():
            frc_keys[frc_one_name].append(frc_one)
        else:
            temp_list = [frc_one]
            frc_all_final.append(temp_list)
            for atom_permutation in frc.Same_Force(frc_one):
                frc_one_name = "".join([str(hash(atom)) for atom in atom_permutation])
                frc_keys[frc_one_name] = temp_list
    return frc_all_final


def _find_the_force(frc, frc_all_final, cls):
    """

    :param frc:
    :param frc_all_final:
    :param cls:
    :return:
    """
    frc_all_types = frc.get_all_types()
    for frc_ones in frc_all_final:
        finded = Xdict()
        # 先直接找
        for frc_one in frc_ones:
            tofindname = frc.Get_Type_Name(frc_one)
            if tofindname in frc_all_types:
                finded[tofindname] = [frc.get_type(tofindname), frc_one]
                break
        # 没找到再找通用的
        if not finded:
            leastfinded_x = 999
            for frc_one in frc_ones:
                tofind = frc.Get_Type_Name(frc_one).split("-")
                tofind = [[atom, "X"] for atom in tofind]
                for p in product(*tofind):
                    pcountx = p.count("X")
                    if pcountx > leastfinded_x:
                        continue
                    tofindname = "-".join(p)
                    if tofindname in frc_all_types:
                        finded = {tofindname: [frc.get_type(tofindname), frc_one]}
                        leastfinded_x = pcountx
                        break

        assert (not frc.compulsory or len(finded) == 1), "None of %s type found for %s" % (
            frc.get_class_name(), "-".join([atom.type.name for atom in frc_one]))

        if finded:
            for finded_type, finded_atoms in finded.values(): #pylint: disable=unbalanced-dict-unpacking
                cls.Add_Bonded_Force(frc.entity(finded_atoms, finded_type))


def _build_residue_type(cls):
    """

    :param cls:
    :return:
    """
    _analyze_connectivity(cls)
    for frc in GlobalSetting.BondedForces:
        if len(frc.get_all_types()) < 2:
            continue
        frc_all = _get_frc_all(frc, cls)
        frc_all_final = _get_frc_all_final(frc, frc_all)
        _find_the_force(frc, frc_all_final, cls)


def _build_residue(cls, checked):
    """

    :param cls:
    :return:
    """
    if not cls.type.built:
        _build_residue_type(cls.type)

    try:
        res_type_atom_map = Xdict({atom : cls.name2atom(atom.name) for atom in cls.type.atoms},
            not_found_message="{} in the ResidueType is not in the Residue. \
            You need to add the missing atoms before building.")
    except KeyError as ke:
        ke.args += ("Maybe there are missing atoms in your residue",)
        raise ke

    for atom0, atom in res_type_atom_map.items():
        for key in atom0.linked_atoms.keys():
            for atomi in atom0.linked_atoms[key]:
                atom.Link_Atom(key, res_type_atom_map[atomi])

    for key, frc_entities in cls.type.bonded_forces.items():
        for frc_entity in frc_entities:
            finded_atoms = [res_type_atom_map[atom] for atom in frc_entity.atoms]
            finded_type = frc_entity.type
            frc_name = finded_type.get_class_name()
            cls.Add_Bonded_Force(finded_type.entity(finded_atoms, finded_type))
            cls.bonded_forces[frc_name][-1].contents = frc_entity.contents
        for pair in cls.type.checked_list.get(key, []):
            checked[key].add("-".join([repr(cls.name2atom(name)) for name in pair]))


def _build_reslink_preprosess(atom1, atom2):
    """ modify the linkage according to residue links """
    atom1_friends, atom2_friends = set([atom1]), set([atom2])
    b1, b2 = Xdict(not_found_method=lambda x: set()), Xdict(not_found_method=lambda x: set())
    far = GlobalSetting.farthest_bonded_force
    for i in range(far - 1, 1, -1):
        for atom in atom1.linked_atoms[i]:
            atom.Link_Atom(i + 1, atom2)
            b2[i+1].add(atom)
            atom1_friends.add(atom)
        for atom in atom2.linked_atoms[i]:
            atom.Link_Atom(i + 1, atom1)
            b1[i+1].add(atom)
            atom2_friends.add(atom)

    for i, atoms in b1.items():
        for atom in atoms:
            atom1.Link_Atom(i, atom)

    for i, atoms in b2.items():
        for atom in atoms:
            atom2.Link_Atom(i, atom)

    atom1.Link_Atom(2, atom2)
    atom2.Link_Atom(2, atom1)

    for i in range(2, far):
        for j in range(2, far + 1 - i):
            for atom1_linked_atom in atom1.linked_atoms[i]:
                for atom2_linked_atom in atom2.linked_atoms[j]:
                    if atom1_linked_atom not in atom2_friends and atom2_linked_atom not in atom1_friends:
                        atom1_linked_atom.Link_Atom(i + j, atom2_linked_atom)
                        atom2_linked_atom.Link_Atom(i + j, atom1_linked_atom)

def _build_residue_link(cls, checked):
    """
        build bonded force for residue link
    """
    for frc in GlobalSetting.BondedForces:
        far = frc.far
        atom1_friends = { atom for i in range(2, far + 1) for atom in cls.atom1.linked_atoms[i]}
        atom2_friends = { atom for i in range(2, far + 1) for atom in cls.atom2.linked_atoms[i]}
        atom12_friends = atom1_friends | atom2_friends
        if len(frc.get_all_types()) < 2:
            continue
        top = frc.topology_like
        top_matrix = frc.topology_matrix
        frc_all = []
        for atom0 in atom12_friends:
            backups = {i: [] for i in range(len(top))}
            backups[0].append([atom0])
            for i, d in enumerate(top):
                if i == 0:
                    continue
                for atom1 in atom12_friends:
                    _check_backup(backups, atom1, top_matrix, i, d)
            for backup in backups[len(top) - 1]:
                backuphash = "-".join([repr(atom) for atom in backup])
                if backuphash not in checked[frc.get_class_name()]:
                    frc_all.append(backup)
                    checked[frc.get_class_name()].add(backuphash)
        frc_all_final = _get_frc_all_final(frc, frc_all)
        _find_the_force(frc, frc_all_final, cls)


def _build_molecule(cls):
    """

    :param cls:
    :return:
    """
    checked = {frc.get_class_name(): set() for frc in GlobalSetting.BondedForces}
    cls.get_atoms()
    for res in cls.residues:
        if not res.type.built:
            build_bonded_force(res.type)
        _build_residue(res, checked)
    for link in cls.residue_links:
        atom1, atom2 = link.atom1, link.atom2
        _build_reslink_preprosess(atom1, atom2)
    for link in cls.residue_links:
        _build_residue_link(link, checked)

    cls.bonded_forces = {frc.get_class_name(): [] for frc in GlobalSetting.BondedForces}
    for key in cls.bonded_forces:
        for res in cls.residues:
            cls.bonded_forces[key].extend(res.bonded_forces.get(key, []))
        for link in cls.residue_links:
            cls.bonded_forces[key].extend(link.bonded_forces.get(key, []))

    cls.atom_index = {cls.atoms[i]: i for i in range(len(cls.atoms))}
    for vatom_type_name, vatom_type_atom_numbers in GlobalSetting.VirtualAtomTypes.items():
        for vatom in cls.bonded_forces.get(vatom_type_name, []):
            this_vatoms = [vatom.atoms[0]]
            for i in range(vatom_type_atom_numbers):
                this_vatoms.append(cls.atoms[cls.atom_index[vatom.atoms[0]] + getattr(vatom, "atom%d" % i)])
            this_vatoms.sort(key=lambda x: cls.atom_index[x])
            while this_vatoms:
                tolink = this_vatoms.pop(0)
                for i in this_vatoms:
                    tolink.Link_Atom("v", i)


def build_bonded_force(cls):
    """
    This **function** build the bonded force for the input object

    :param cls: the object to build
    :return: None
    """
    if cls.built:
        return

    if isinstance(cls, ResidueType):
        _build_residue_type(cls)
        cls.built = True
    elif isinstance(cls, Molecule):
        _build_molecule(cls)
        cls.built = True
    else:
        raise NotImplementedError


def _get_single_system_energy(scls, sys_kwarg, ene_kwarg, use_pbc):
    """

    :param scls:
    :return:
    """
    for todo in getattr(scls, "_mindsponge_todo").values():
        todo(scls, sys_kwarg, ene_kwarg, use_pbc)


def get_mindsponge_system_energy(cls, use_pbc=False):
    """
    This **function** gets the system and energy for mindsponge

    :param cls: the object to save, or a list of object to save
    :param use_pbc: whether to use the periodic box conditions
    :return: a tuple, including the system and energy for mindsponge
    """
    from mindsponge import set_global_units
    from mindsponge import Molecule as mMolecule
    from mindsponge import ForceFieldBase
    from collections.abc import Iterable
    if not isinstance(cls, Iterable):
        cls = [cls]
    sys_kwarg = Xdict()
    ene_kwarg = Xdict()
    for scls in cls:
        if isinstance(scls, AbstractMolecule):
            mol = Molecule.cast(scls, deepcopy=False)
            build_bonded_force(mol)
            _get_single_system_energy(mol, sys_kwarg, ene_kwarg, use_pbc)
        else:
            raise TypeError(f"The type should be a Molecule, Residue, ResidueType, but we get {str(type(scls))}")
    set_global_units("A", "kcal/mol")
    toremove = []
    for key, value in sys_kwarg.items():
        if not value[0]:
            toremove.append(key)
    for key in toremove:
        sys_kwarg.pop(key)
    system = mMolecule(**sys_kwarg)
    system.multi_system = len(cls)
    energies = []
    sys_kwarg["exclude"] = ene_kwarg.pop("exclude")
    for todo in ene_kwarg.values():
        try:
            energies.append(todo["function"](system, ene_kwarg))
        except (TypeError, ValueError) as e:
            if 'NoneType' not in e.args[0] and 'zero dimension' not in e.args[0]:
                raise e

    try:
        energy = ForceFieldBase(energy=energies, exclude_index=sys_kwarg["exclude"])
    except ValueError as e:
        if 'zero dimension' not in e.args[0]:
            raise e
        energy = ForceFieldBase(energy=energies)

    return system, energy


def save_sponge_input(cls, prefix=None, dirname="."):
    """
    This **function** saves the iput object as SPONGE inputs

    :param cls: the object to save
    :param prefix: the prefix of the output files
    :param dirname: the directory to save the output files
    :return: the molecule instance built
    """
    if isinstance(cls, Molecule):
        mol = cls
        build_bonded_force(cls)

        if not prefix:
            prefix = cls.name

        for key, func in getattr(Molecule, "_save_functions").items():
            towrite = func(cls)
            if towrite:
                f = Xopen(os.path.join(dirname, prefix + "_" + key + ".txt"), "w")
                f.write(towrite)
                f.close()

    elif isinstance(cls, Residue):
        mol = Molecule(name=cls.name)
        mol.Add_Residue(cls)
        save_sponge_input(mol, prefix, dirname)

    elif isinstance(cls, ResidueType):
        residue = Residue(cls, name=cls.name)
        for atom in cls.atoms:
            residue.Add_Atom(atom)
        mol = save_sponge_input(residue, prefix, dirname)

    return mol


def _pdb_chain(cls: Molecule):
    """
        get all chains in the pdb
    """
    chains = Xdict()
    chain_ids = [" "] * len(cls.residues)
    start = 0
    alphabet = "A"
    i = 0
    for i, res in enumerate(cls.residues):
        if i == start:
            continue
        pre_res = cls.residues[i-1]
        new_chain = False
        if pre_res.type.tail is None or res.type.head is None:
            new_chain = True
        if not new_chain:
            tail = pre_res.name2atom(pre_res.type.tail)
            head = res.name2atom(res.type.head)
            reslink = cls.get_residue_link(tail, head)
            if reslink is None:
                new_chain = True
        if new_chain:
            length = i - start
            if length > 1:
                chains[alphabet] = {j + 1: start + j + 1 for j in range(length)}
                chain_ids[start: start + length] = alphabet * length
                alphabet = chr(ord(alphabet) + 1)
            start = i
    length = i - start + 1
    if length > 1:
        chains[alphabet] = {j + 1: start + j + 1 for j in range(length)}
        chain_ids[start: start + length] = alphabet * length
    return chains, chain_ids


def _pdb_connection(connects):
    """
        process the CONECT part
    """
    templist = []
    for connect, atoms in connects.items():
        atoms.sort()
        atom_groups = [atoms[i:i + 4] for i in range(0, len(atoms), 4)]
        for four_atoms in atom_groups:
            templist.append("CONECT" + "{:5d}".format(connect + 1)
                            + "".join(["{:5d}".format(i + 1) for i in four_atoms]) + "\n")
    templist.sort()
    return "".join(templist)


def _pdb_sequence(cls: Molecule, chains: Xdict):
    """
        process the SEQRES part
    """
    towrite = ""
    chain_ids = list(chains.keys())
    chain_ids.sort()
    for chain_id in chain_ids:
        index_map = chains[chain_id]
        pdb_index = list(index_map.keys())
        pdb_index.sort()
        names = []
        for i in pdb_index:
            mol_index = index_map[i] - 1
            name = cls.residues[mol_index].name
            name = GlobalSetting.PDBResidueNameMap["save"][name] \
                if name in GlobalSetting.PDBResidueNameMap["save"] else name
            if len(name) > 3:
                warn(f"The residue name {name} is more than 3 characters.")
            names.append(name)
        lines = [" ".join(["{:3s}".format(name) for name in names[j:j+13]])  for j in range(0, len(names), 13)]
        lines = ["SEQRES {0:3d} {1:1s} {2:4d}  {3:s}\n".format(
            i + 1, chain_id, len(names), line) for i, line in enumerate(lines)]
        towrite += "".join(lines)
    return towrite


def _pdb_residue_link(cls: Molecule, chain_ids: Xdict, chains: Xdict, r2i: Xdict):
    """
        Process the residue links
    """
    towrite = ""
    connects = Xdict(not_found_method=lambda key: [])
    ssbonds = []
    links = []
    chains_inverse = Xdict({chain_id: Xdict({value: key for key, value in chains[chain_id].items()})
                            for chain_id in chains})
    for reslink in cls.residue_links:
        a, b = reslink.atom1, reslink.atom2
        index_a = cls.atom_index[a]
        index_b = cls.atom_index[b]
        if index_a > index_b:
            a, b = b, a
            index_a, index_b = index_b, index_a
        res_a, res_b = a.residue, b.residue
        res_index_a, res_index_b = r2i[res_a], r2i[res_b]
        chain_a, chain_b = chain_ids[res_index_a], chain_ids[res_index_b]
        if res_index_b - res_index_a == 1 and chain_a == chain_b != " ":
            continue
        if chain_a == " " or chain_b == " ":
            connects[index_a].append(index_b)
            connects[index_b].append(index_a)
        elif res_a.name == "CYX" and res_b.name == "CYX" and \
                a.name == res_a.type.connect_atoms["ssbond"] and \
                b.name == res_b.type.connect_atoms["ssbond"]:
            ssbonds.append("CYX {0:1s} {1:4d}    CYX {2:1s} {3:4d}\n".format(
                chain_a, chains_inverse[chain_a][res_index_a] + 1, chain_b, chains_inverse[chain_b][res_index_b] + 1))
        else:
            save_names = GlobalSetting.PDBResidueNameMap["save"]
            name_a = save_names[res_a.name] if res_a.name in save_names else res_a.name
            name_b = save_names[res_b.name] if res_b.name in save_names else res_b.name
            links.append("LINK        {0:^4s} {1:3s} {2:1s}{3:4d}                \
{4:^4s} {5:3s} {6:1s}{7:4d}\n".format(
    a.name, name_a, chain_a, chains_inverse[chain_a][res_index_a],
    b.name, name_b, chain_b, chains_inverse[chain_b][res_index_b]))
    if ssbonds:
        ssbonds.sort()
        towrite += "".join(["SSBOND {0:3d} ".format(i + 1) + ssbond for i, ssbond in enumerate(ssbonds)])
    if links:
        links.sort(key=lambda line: (line[21], int(line[22:26]), line[51], int(line[52:56])))
        towrite += "".join(links)
    return connects, towrite


def save_pdb(cls, filename=None):
    """
    This **function** saves the iput object as a pdb file

    :param cls: the object to save
    :param filename: the name of the output file
    :return: None
    """
    if isinstance(cls, AbstractMolecule):
        cls = Molecule.cast(cls, deepcopy=False)
        cls.atoms = []
        for res in cls.residues:
            cls.atoms.extend(res.atoms)
        cls.atom_index.clear()
        cls.atom_index.update({atom : i for i, atom in enumerate(cls.atoms)})
        a2i = cls.atom_index
        r2i = {cls.residues[i]: i for i in range(len(cls.residues))}

        chains, chain_ids = _pdb_chain(cls)
        towrite = "REMARK   Generated By Xponge (Molecule)\n"
        towrite += _pdb_sequence(cls, chains)
        connects, temp_towrite = _pdb_residue_link(cls, chain_ids, chains, r2i)
        towrite += temp_towrite
        chain_residue0 = -1
        real_chain_residue0 = -1
        ter_res = set()
        for i, code in enumerate(chain_ids):
            if i == len(chain_ids) - 1:
                ter_res.add(i)
                break
            if chain_ids[i + 1] != code or code == " ":
                ter_res.add(i)
        for atom in cls.atoms:
            resname = atom.residue.name
            resid = r2i[atom.residue]
            if resname in GlobalSetting.PDBResidueNameMap["save"]:
                resname = GlobalSetting.PDBResidueNameMap["save"][resname]
            towrite += "ATOM  %5d %4s %3s %1s%4d    %8.3f%8.3f%8.3f%17s%2s\n" % (
                (a2i[atom] + 1) % 100000, atom.name,
                resname, chain_ids[resid],
                (resid - chain_residue0) % 10000,
                atom.x, atom.y, atom.z, " ", " ")
            if atom == atom.residue.atoms[-1] and resid in ter_res:
                towrite += "TER\n"
                if resid - real_chain_residue0 != 1 or resid + 1 in ter_res:
                    real_chain_residue0 = chain_residue0
                else:
                    chain_residue0 = resid
                    real_chain_residue0 = resid
        if not filename:
            filename = cls.name + ".pdb"
        towrite += _pdb_connection(connects)
        towrite += "END\n"
        f = Xopen(filename, "w")
        f.write(towrite)
        f.close()
    elif isinstance(cls, assign.Assign):
        cls.Save_As_PDB(filename)
    else:
        raise TypeError("Only Molecule, Residue, ResidueType and Assign can be saved as a pdb file")


def save_mol2(cls, filename=None):
    """
    This **function** saves the iput object as a mol2 file

    :param cls: the object to save
    :param filename: the name of the output file
    :return: None
    """
    if isinstance(cls, AbstractMolecule):
        cls = Molecule.cast(cls, deepcopy=False)
        cls.atoms = []
        for res in cls.residues:
            cls.atoms.extend(res.atoms)
        cls.atom_index = {cls.atoms[i]: i for i in range(len(cls.atoms))}
        bonds = []
        for res in cls.residues:
            for atom1, atom1_con in res.type.connectivity.items():
                atom1_index = cls.atom_index[res.name2atom(atom1.name)] + 1
                for atom2 in atom1_con:
                    atom2_index = cls.atom_index[res.name2atom(atom2.name)] + 1
                    if atom1_index < atom2_index:
                        bonds.append("%6d %6d" % (atom1_index, atom2_index))

        for link in cls.residue_links:
            atom1_index = cls.atom_index[link.atom1] + 1
            atom2_index = cls.atom_index[link.atom2] + 1
            if atom1_index < atom2_index:
                bonds.append("%6d %6d" % (atom1_index, atom2_index))
            else:
                bonds.append("%6d %6d" % (atom2_index, atom1_index))
        bonds.sort(key=lambda x: list(map(int, x.split())))
        towrite = "@<TRIPOS>MOLECULE\n"
        towrite += "%s\n" % (cls.name)
        towrite += " %d %d %d 0 1\n" % (len(cls.atoms), len(bonds), len(cls.residues))
        towrite += "SMALL\n"
        towrite += "USER_CHARGES\n"

        towrite += "@<TRIPOS>ATOM\n"
        count = 0
        res_count = 0
        residue_start = []
        for atom in cls.atoms:
            count += 1
            if atom == atom.residue.atoms[0]:
                res_count += 1
                residue_start.append(count)
            resname = atom.residue.name
            towrite += "%6d %4s %8.3f %8.3f %8.3f %4s %5d %8s %10.6f\n" % (
                count, atom.name, atom.x, atom.y, atom.z, atom.type.name, res_count, resname, atom.charge)

        towrite += "@<TRIPOS>BOND\n"
        for i, bond in enumerate(bonds):
            towrite += "%6d %s 1\n" % (i + 1, bond)
        towrite += "@<TRIPOS>SUBSTRUCTURE\n"
        for i, residue in enumerate(cls.residues):
            towrite += "%5d %8s %6d ****               0 ****  **** \n" % (i + 1, residue.name, residue_start[i])

        if not filename:
            filename = cls.name + ".mol2"

        f = Xopen(filename, "w")
        f.write(towrite)
        f.close()
    elif isinstance(cls, assign.Assign):
        cls.Save_As_Mol2(filename)
    else:
        raise TypeError("Only Molecule, Residue, ResidueType and Assign can be saved as a mol2 file")


def save_gro(cls, filename):
    """
    This **function** saves the iput object as a gro file

    :param cls: the object to save
    :param filename: the name of the output file
    :return: None
    """
    towrite = "Generated By Xponge\n"
    cls = Molecule.cast(cls, deepcopy=False)
    cls.atoms = []
    for res in cls.residues:
        cls.atoms.extend(res.atoms)
    cls.residue_index = {cls.residues[i]: i for i in range(len(cls.residues))}

    boxlength = [0, 0, 0]
    maxi = [-float("inf"), -float("inf"), -float("inf")]
    mini = [float("inf"), float("inf"), float("inf")]
    for atom in cls.atoms:
        if atom.x > maxi[0]:
            maxi[0] = atom.x
        if atom.y > maxi[1]:
            maxi[1] = atom.y
        if atom.z > maxi[2]:
            maxi[2] = atom.z
        if atom.x < mini[0]:
            mini[0] = atom.x
        if atom.y < mini[1]:
            mini[1] = atom.y
        if atom.z < mini[2]:
            mini[2] = atom.z

    towrite += "%d\n" % len(cls.atoms)
    for i, atom in enumerate(cls.atoms):
        residue = atom.residue
        if not GlobalSetting.nocenter:
            x = atom.x - mini[0] + GlobalSetting.boxspace
            y = atom.y - mini[1] + GlobalSetting.boxspace
            z = atom.z - mini[2] + GlobalSetting.boxspace
        else:
            x, y, z = atom.x, atom.y, atom.z

        towrite += "%5d%-5s%5s%5d%8.3f%8.3f%8.3f\n" % (
            cls.residue_index[residue] + 1, residue.name, atom.name, i + 1, x / 10, y / 10, z / 10)
    if cls.box_length is None:
        boxlength[0] = maxi[0] - mini[0] + GlobalSetting.boxspace * 2
        boxlength[1] = maxi[1] - mini[1] + GlobalSetting.boxspace * 2
        boxlength[2] = maxi[2] - mini[2] + GlobalSetting.boxspace * 2
        cls.box_length = [boxlength[0], boxlength[1], boxlength[2]]
    else:
        boxlength[0] = cls.box_length[0]
        boxlength[1] = cls.box_length[1]
        boxlength[2] = cls.box_length[2]
    towrite += "%8.3f %8.3f %8.3f" % (
        cls.box_length[0] / 10, cls.box_length[1] / 10, cls.box_length[2] / 10)
    f = Xopen(filename, "w")
    f.write(towrite)
    f.close()

set_global_alternative_names()
