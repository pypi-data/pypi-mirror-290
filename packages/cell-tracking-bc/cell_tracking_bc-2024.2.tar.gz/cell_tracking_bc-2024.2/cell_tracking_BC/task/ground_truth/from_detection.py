# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

"""
Quick and dirty work done for a one-shot use in a project.
"""

import networkx as ntwx
from cell_tracking_BC.in_out.file.load import (
    INFINITY,
    AddEdgeToTrack,
    MarkDividingCells,
    fake_cell_t,
)
from cell_tracking_BC.task.tracking.constant import TRACKING_AFFINITY_LABEL
from cell_tracking_BC.type.compartment.cell import state_e
from cell_tracking_BC.type.track.single.forking import forking_track_t
from cell_tracking_BC.type.track.single.unstructured import (
    TIME_POINT,
    unstructured_track_t,
)


def CorrectTracks(
    valid_tracks,
    next_label_for_valid_s,
    label_conversions,
    correction_path,
    dividing_cells,
    new_status_sheet,
    next_thread_label,
    invalid_tracks,
):
    """"""
    unwanted = []
    overlapping = []

    new_thread_tracks = {}
    with open(correction_path) as accessor:
        for line in accessor.readlines():
            true_label, time_point, action = line.split()

            try:
                true_label = int(true_label)
            except ValueError:
                while true_label in new_thread_tracks:
                    true_label = new_thread_tracks[true_label]
                if not isinstance(true_label, int):
                    raise ValueError(true_label)
                # if not isinstance(true_label, int):
                #     print(
                #         f"! Invalid label {true_label}; Skipped Correction: ",
                #         true_label,
                #         time_point,
                #         action,
                #     )
                #     continue
                # label_conversions[true_label] = true_label

            time_point = int(time_point)
            operation = action[0]
            if action.__len__() > 1:
                try:
                    operand = int(action[1:])
                except ValueError:
                    operand = action[1:]
            else:
                print(
                    "! Missing operand; Skipped Correction: ",
                    true_label,
                    time_point,
                    action,
                )
                continue

            label = None
            for key, value in label_conversions.items():
                if value == true_label:
                    label = key
                    break
            if label is None:
                print(
                    "! Invalid label; Skipped Correction: ",
                    true_label,
                    time_point,
                    action,
                )
                continue

            assert label_conversions[label] == true_label

            if operation == "-":
                PruneTrack(
                    valid_tracks,
                    true_label,
                    label,
                    time_point,
                    action,
                    operand,
                    unwanted,
                    overlapping,
                )
            elif operation == "+":
                if AddTrack(
                    valid_tracks,
                    next_label_for_valid_s,
                    true_label,
                    label,
                    time_point,
                    action,
                    operand,
                    next_thread_label,
                    new_thread_tracks,
                    dividing_cells,
                    label_conversions,
                ):
                    new_status_sheet.append("Valid")
                    next_label_for_valid_s += 1
                    next_thread_label += 1
            else:
                print(
                    f"! Invalid operation {operation}; Skipped Correction: ",
                    true_label,
                    time_point,
                    action,
                )
                continue

    assert sorted(label_conversions.keys()) == list(
        range(1, max(label_conversions.keys()) + 1)
    )
    assert sorted(label_conversions.values()) == sorted(
        set(range(1, max(label_conversions.values()) + 1)).difference(
            _elm[0] for _elm in invalid_tracks
        )
    ), (
        sorted(label_conversions.values()),
        sorted(
            set(range(1, max(label_conversions.values()) + 1)).difference(
                _elm[0] for _elm in invalid_tracks
            )
        ),
    )
    assert valid_tracks.topologic_labels == list(
        range(1, max(label_conversions.keys()) + 1)
    ), (
        valid_tracks.topologic_labels,
        list(range(1, max(label_conversions.keys()) + 1)),
    )

    dividing_cells.clear()
    for valid_track in valid_tracks:
        MarkDividingCells(valid_track, dividing_cells)
    #
    #     for cells, label in valid_track.LabeledThreadIterator():
    #         for cell in cells:
    #             if (cell.uid in dividing_cells[label]) and (
    #                 valid_track.CellSuccessors(cell).__len__() < 2
    #             ):
    #                 dividing_cells[label].remove(cell.uid)
    #                 cell.state = state_e.living
    #
    # to_be_removed = []
    # for _key, _vle in dividing_cells.items():
    #     if _vle.__len__() == 0:
    #         to_be_removed.append(_key)
    # for key in to_be_removed:
    #     del dividing_cells[key]

    return unwanted, overlapping


def PruneTrack(
    valid_tracks, true_label, label, time_point, action, operand, unwanted, overlapping
):
    """"""
    target_track = None
    target_node = None
    for valid_track in valid_tracks:
        if target_track is not None:
            break

        for nodes, thread_label in valid_track.LabeledThreadIterator():
            if target_track is not None:
                break
            if thread_label != label:
                continue

            for node in nodes:
                if target_track is not None:
                    break
                if node.time_point != time_point:
                    continue

                if operand in ("u", "o"):
                    target_track = valid_track
                    target_node = node
                    break
                else:
                    for successor in valid_track.CellSuccessors(node):
                        if operand in successor.all_labels:
                            target_track = valid_track
                            target_node = successor
                            break

    if target_node is None:
        print(
            "! No target node found; Skipped Correction: ",
            true_label,
            time_point,
            action,
        )
        return

    if operand in ("u", "o"):
        if operand == "u":
            which = "UNWANTED"
        else:
            which = "OVERLAP "
        which_2 = "s   "
    else:
        which = "PRUNED  "
        which_2 = f" {operand:3}"
    # print(
    #     f"{which} thread track{which_2} along thread track {true_label:3} "
    #     f"(tmp_lbl={label:3}) from t={time_point:3}"
    # )

    new_potential_leaf = tuple(target_track.predecessors(target_node))
    if new_potential_leaf.__len__() == 0:
        new_leaf = None
    elif new_potential_leaf.__len__() == 1:
        new_leaf = new_potential_leaf[0]
    else:
        print("! More than one predecessor to {target_node}")
        return

    to_be_removed = [target_node]
    successors = list(target_track.CellSuccessors(target_node))
    while successors.__len__() > 0:
        current = successors.pop()
        to_be_removed.append(current)
        successors.extend(target_track.CellSuccessors(current))
    for node in to_be_removed:
        node.state = state_e.discarded
        if node in target_track.leaves:
            new_leaves = list(target_track.leaves)
            new_leaves.remove(node)
            target_track.leaves = tuple(new_leaves)
        if operand in ("u", "o"):
            if operand == "u":
                unwanted.append(node.uid)
            else:
                overlapping.append(node.uid)
    if new_leaf is None:
        target_track.leaves = ()
    elif target_track.CellSuccessors(new_leaf).__len__() == 0:
        target_track.leaves = target_track.leaves + (new_leaf,)
        new_leaf.state = state_e.living


def AddTrack(
    valid_tracks,
    next_label_for_valid_s,
    true_label,
    label,
    time_point,
    action,
    operand,
    next_thread_label,
    new_thread_tracks,
    _,
    label_conversions,
):
    """"""
    target_track = None
    target_track_idx = None
    predecessors = None
    previous_node = None
    next_node = None
    issues = []
    for t_idx, valid_track in enumerate(valid_tracks):
        if target_track is not None:
            break

        for nodes, thread_label in valid_track.LabeledThreadIterator():
            if target_track is not None:
                break
            if thread_label != label:
                continue

            if nodes.__len__() < 2:
                issues.append(f"Track with less than 2 nodes: {thread_label}")
                # print(f"! Track with less than 2 nodes: {thread_label}: {valid_track}")
                # if isinstance(valid_track, ntwx.DiGraph):
                #     ntwx.write_network_text(valid_track)
                # else:
                #     print(tuple(valid_track))
                continue

            predecessors = []
            previous_node = nodes[0]
            next_node = nodes[1]
            n_idx = 1
            while next_node is not None:
                if (previous_node.time_point < time_point) and (
                    next_node.time_point > time_point
                ):
                    target_track = valid_track
                    target_track_idx = t_idx
                    break

                predecessors.append(previous_node)
                previous_node = next_node
                n_idx += 1
                if n_idx < nodes.__len__():
                    next_node = nodes[n_idx]
                else:
                    next_node = None
            assert not any(_elm.label == previous_node.label for _elm in predecessors)
            predecessors.append(previous_node)

    if target_track is None:
        if issues.__len__() > 0:
            issues = ", ".join(issues)
        else:
            issues = ""
        print(
            "! No target track found; Skipped Correction: ",
            true_label,
            time_point,
            action,
            issues,
        )
        return False

    # print(
    #     f"ADDED on thread track {true_label:3} (tmp_lbl={label:3}) "
    #     f"@ t={time_point:3} with label {operand:3}={next_thread_label:3} "
    #     f"(tmp_lbl={next_label_for_valid_s:3})"
    # )

    if isinstance(target_track, ntwx.DiGraph):
        should_replace_track = False
    else:
        assert (previous_node is target_track[0]) and (next_node is target_track[-1])

        should_replace_track = True

        unstructured = unstructured_track_t()
        AddEdgeToTrack(
            (previous_node.all_labels, previous_node.time_point),
            (next_node.all_labels, next_node.time_point),
            unstructured,
        )
        target_track, _ = forking_track_t.NewFromUnstructuredTrack(unstructured, label)
        previous_node = target_track.root
        next_node = target_track.leaves[0]
        predecessors[-1] = previous_node
        # for node in target_track.nodes:
        #     if node.uid == previous_node.uid:
        #         previous_node = node
        #         predecessors[-1] = node
        #     elif node.uid == next_node.uid:
        #         next_node = node

    # print("BEFORE ----", target_track_idx)
    # ntwx.write_network_text(target_track)

    new_junction_node = (next_node.all_labels + (next_thread_label,), time_point)
    new_leaf_node = ((next_thread_label,), INFINITY)
    target_track.remove_edge(previous_node, next_node)
    AddEdgeToTrack(previous_node, new_junction_node, target_track)
    AddEdgeToTrack(new_junction_node, next_node, target_track)
    AddEdgeToTrack(new_junction_node, new_leaf_node, target_track)
    for node in target_track:
        if node.all_labels == new_leaf_node[0]:
            target_track.nodes[node][
                forking_track_t.THREAD_LABEL
            ] = next_label_for_valid_s
            target_track.leaves = target_track.leaves + (node,)
            target_track.topologic_leaves = target_track.topologic_leaves + (node,)
            target_track.topologic_labels = target_track.topologic_labels + (
                next_label_for_valid_s,
            )
            break

    while predecessors.__len__() > 0:
        old_node = predecessors.pop()
        old_is_root = old_node.uid == target_track.root.uid
        # new_node_uid = tuple(old_node.uid[:-1]) + (
        #     next_label_for_valid_s,
        #     old_node.uid[-1],
        # )
        new_node = fake_cell_t.NewFromLabelsAndTimePoint(
            old_node.all_labels + (next_thread_label,), old_node.time_point
        )
        new_node.state = old_node.state
        # if old_node.uid == previous_node.uid:
        #     previous_node = new_node
        # old_node = None
        # for node in target_track.nodes:
        #     print(node, predecessor, node is predecessor)
        # if node.uid == predecessor.uid:
        #     old_node = node
        #     break
        ancestors = tuple(target_track.predecessors(old_node))
        successors = tuple(target_track.successors(old_node))
        target_track.remove_node(old_node)
        time_point_src = {TIME_POINT: new_node.time_point}
        target_track.add_node(new_node, **time_point_src)
        if old_is_root:
            target_track.root = target_track.topologic_root = new_node
        affinity = {TRACKING_AFFINITY_LABEL: 1.0}
        for ancestor in ancestors:
            target_track.add_edge(ancestor, new_node, **affinity)
        for successor in successors:
            target_track.add_edge(new_node, successor, **affinity)

    # MarkDividingCells(target_track, dividing_cells)
    label_conversions[next_label_for_valid_s] = next_thread_label
    # for cells, label in target_track.LabeledThreadIterator():
    #     if label not in label_conversions:
    #         assert label == cells[-1].uid[0], (label, cells[-1].uid[0], cells[-1])
    #         label_conversions[label] = label  # cells[-1].uid[0]  # Leaf cell label.

    if should_replace_track:
        valid_tracks[target_track_idx] = target_track
    new_thread_tracks[operand] = next_thread_label

    # ntwx.write_network_text(target_track)
    # print("AFTER ----")

    return True
