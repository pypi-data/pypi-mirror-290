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

Launch:
python cell_tracking_BC/produce-gt-from-dn.py test/ground-truth/tracks.xlsx test/ground-truth/cell_events.xlsx test/ground-truth/corrections.txt
or
python -m cell_tracking_BC.produce-gt-from-dn test/ground-truth/tracks.xlsx test/ground-truth/cell_events.xlsx test/ground-truth/corrections.txt
"""

import difflib as diff
import sys as sstm
import tempfile as temp
import typing as h
from pathlib import Path as path_t

import matplotlib.pyplot as pypl
import networkx as ntwx
import numpy as nmpy
import xlsxwriter as xlsx
from cell_tracking_BC.in_out.file.load import (
    RebuiltTracks,
    SaveAndReloadDivisions,
    SaveAndReloadTracks,
)
from cell_tracking_BC.in_out.file.table.sheet import SheetNameFromLongName
from cell_tracking_BC.task.ground_truth.from_detection import CorrectTracks
from cell_tracking_BC.type.analysis import analysis_t
from cell_tracking_BC.type.compartment.cell import state_e
from cell_tracking_BC.type.track.single.unstructured import TIME_POINT


def Main(
    tracks_path, events_path, correction_path, should_show_tracks, should_plot_divisions
):
    """"""
    folder = path_t(tracks_path).parent
    tmp_folder = path_t(temp.mkdtemp())
    # print(f"Test documents in: {tmp_folder}\n")

    (
        thread_tracks_sheet,
        divisions_sheet,
        dividing_cells,
        valid_tracks,
        next_label_for_valid_s,
        label_conversions,
        invalid_tracks,
    ) = RebuiltTracks(tracks_path, events_path)
    new_status_sheet = list(thread_tracks_sheet["status"])
    next_thread_label = thread_tracks_sheet["siblings"].__len__() + 1

    original_siblings = OriginalAsList(
        thread_tracks_sheet, thread_tracks_sheet, "siblings"
    )
    original_divisions = OriginalAsList(
        divisions_sheet, thread_tracks_sheet, "division times"
    )

    analysis = analysis_t()
    analysis.tracks = valid_tracks

    rebuilt_siblings = SaveAndReloadTracks(
        analysis, label_conversions, tmp_folder, "test"
    )
    rebuilt_siblings, _ = RebuiltAsList(
        thread_tracks_sheet["status"],
        invalid_tracks,
        rebuilt_siblings,
        "siblings",
        None,
        None,
    )

    rebuilt_divisions = SaveAndReloadDivisions(
        analysis, label_conversions, dividing_cells, None, None, tmp_folder, "test"
    )
    rebuilt_divisions, _ = RebuiltAsList(
        thread_tracks_sheet["status"],
        invalid_tracks,
        rebuilt_divisions,
        "division times",
        None,
        None,
    )

    if should_show_tracks:
        import pprint

        pprint.pprint(label_conversions)
        pprint.pprint(dividing_cells)
        for valid_track in valid_tracks:
            if isinstance(valid_track, ntwx.DiGraph):
                ntwx.write_network_text(valid_track)

    if rebuilt_siblings != original_siblings:
        print("---- Rebuilt Siblings ----")
        CompareWithOriginal(original_siblings, rebuilt_siblings)
        print("----")
        return
    if rebuilt_divisions != original_divisions:
        print("---- Rebuilt Divisions ----")
        CompareWithOriginal(original_divisions, rebuilt_divisions)
        print("----")
        return

    unwanted, overlapping = CorrectTracks(
        valid_tracks,
        next_label_for_valid_s,
        label_conversions,
        correction_path,
        dividing_cells,
        new_status_sheet,
        next_thread_label,
        invalid_tracks,
    )

    if should_show_tracks:
        for valid_track in valid_tracks:
            if isinstance(valid_track, ntwx.DiGraph):
                ntwx.write_network_text(valid_track)

    SaveDivisions(valid_tracks, folder, should_plot_divisions)

    corrected_siblings = SaveAndReloadTracks(
        analysis, label_conversions, tmp_folder, "test-corrected"
    )
    corrected_siblings, corrected_siblings_raw = RebuiltAsList(
        new_status_sheet,
        invalid_tracks,
        corrected_siblings,
        "siblings",
        unwanted,
        overlapping,
    )

    corrected_divisions = SaveAndReloadDivisions(
        analysis,
        label_conversions,
        dividing_cells,
        unwanted,
        overlapping,
        tmp_folder,
        "test-corrected",
    )
    corrected_divisions, corrected_divisions_raw = RebuiltAsList(
        new_status_sheet,
        invalid_tracks,
        corrected_divisions,
        "division times",
        unwanted,
        overlapping,
    )

    # if corrected_siblings != original_siblings:
    #     print("#### Corrected Siblings ####")
    #     print("############################")
    #     CompareWithOriginal(original_siblings, corrected_siblings)
    #     print("")
    # if corrected_divisions != original_divisions:
    #     print("#### Corrected Divisions ####")
    #     print("#############################")
    #     CompareWithOriginal(original_divisions, corrected_divisions)

    SaveCorrected(
        corrected_siblings_raw, new_status_sheet, corrected_divisions_raw, folder
    )


def OriginalAsList(content_sheet, status_sheet, what):
    """"""
    original = []

    if what == "siblings":
        for label, (content, status) in enumerate(
            zip(content_sheet[what], status_sheet["status"]), start=1
        ):
            original.append(f"{label}: {content} {status}")
    elif what == "division times":
        for label, (content, status) in enumerate(
            zip(content_sheet, status_sheet["status"]), start=1
        ):
            original.append(f"{label}: {content} {status}")
    else:
        raise ValueError(what)

    return original


def RebuiltAsList(status_sheet, invalid_tracks, new_content_sheet, what, _, __):
    """"""
    rebuilt = []
    rebuilt_raw = []

    valid_idx = 0
    invalid_idx = 0
    if what == "siblings":
        for label, status in enumerate(status_sheet, start=1):
            if status == "Valid":
                content = new_content_sheet[what][valid_idx]
                rebuilt.append(f"{label}: {content} Valid")
                rebuilt_raw.append(content)
                valid_idx += 1
            else:
                _, content, status = invalid_tracks[invalid_idx]
                rebuilt.append(f"{label}: {content} {status}")
                rebuilt_raw.append(content)
                invalid_idx += 1
    elif what == "division times":
        for label, status in enumerate(status_sheet, start=1):
            if status == "Valid":
                content = new_content_sheet[valid_idx]
                if isinstance(content, str):
                    if content in ("Unwanted", "Overlap"):
                        rebuilt.append(f"{label}: {content} Valid")
                        rebuilt_raw.append(content)
                    else:
                        rebuilt.append(f"{label}: No Divisions Valid")
                        rebuilt_raw.append("No Divisions")
                else:
                    rebuilt.append(f"{label}: {content} Valid")
                    rebuilt_raw.append(content)
                valid_idx += 1
            else:
                _, content, status = invalid_tracks[invalid_idx]
                rebuilt.append(f"{label}: Invalid or Pruned {status}")
                rebuilt_raw.append("Invalid or Pruned")
                invalid_idx += 1
    else:
        raise ValueError(what)

    return rebuilt, rebuilt_raw


def CompareWithOriginal(original, other):
    """"""
    original_new_line = [_elm + "\n" for _elm in original]
    corrected_new_line = [_elm + "\n" for _elm in other]
    sstm.stdout.writelines(
        diff.context_diff(
            original_new_line,
            corrected_new_line,
            fromfile="Detection",
            tofile="Ground-truth",
            n=0,
        )
    )


def SaveCorrected(corrected_siblings, status_sheet, corrected_divisions, folder):
    """"""
    for content, basename, sheet_name, should_convert_to_str in (
        (corrected_siblings, "tracks", "siblings", True),
        (corrected_divisions, "cell_events", "division times", False),
    ):
        path = folder / f"{basename}-corrected.xlsx"
        workbook = xlsx.Workbook(str(path))

        sheet_name = SheetNameFromLongName(sheet_name)
        worksheet = workbook.add_worksheet(sheet_name)
        for row, value in enumerate(content):
            if isinstance(value, str):
                worksheet.write_string(row, 0, value)
            elif isinstance(value, h.Sequence):
                if should_convert_to_str:
                    value = str(value)[1:-1]
                    worksheet.write_string(row, 0, value)
                else:
                    worksheet.write_row(row, 0, value)
            elif should_convert_to_str:
                worksheet.write_string(row, 0, str(value))
            else:
                worksheet.write_number(row, 0, value)
        worksheet.write_string(content.__len__(), 0, "END")

        if basename == "tracks":
            sheet_name = SheetNameFromLongName("status")
            worksheet = workbook.add_worksheet(sheet_name)
            for row, status in enumerate(status_sheet):
                worksheet.write_string(row, 0, status)
            worksheet.write_string(content.__len__(), 0, "END")

        workbook.close()


def SaveDivisions(valid_tracks, folder, should_plot_divisions):
    """"""
    division_time_points = []
    for valid_track in valid_tracks:
        for node in valid_track:
            if node.state == state_e.dividing:
                division_time_points.append(valid_track.nodes[node][TIME_POINT])
    division_time_points = sorted(division_time_points)

    # print(f"\nDivisions: {division_time_points.__len__()} {division_time_points}\n")

    with open(folder / "division_times.txt", "w") as accessor:
        accessor.writelines(str(_elm) + "\n" for _elm in division_time_points)

    n_divisions_per_time_point = nmpy.bincount(division_time_points)
    with open(folder / "n_divisions_per_time_point.txt", "w") as accessor:
        accessor.writelines(str(_elm) + "\n" for _elm in n_divisions_per_time_point)

    if should_plot_divisions:
        MAX_BIN_SIZE = 40
        BIN_SIZE_STEP = 10

        with open(folder / "division_times.txt") as accessor:
            division_time_points = accessor.readlines()
        division_time_points = tuple(int(_elm) for _elm in division_time_points)
        last_time_point = max(division_time_points)

        with open(folder / "n_divisions_per_time_point.txt") as accessor:
            n_divisions_per_time_point = accessor.readlines()
        n_divisions_per_time_point = tuple(
            int(_elm) for _elm in n_divisions_per_time_point
        )

        bin_sizes = tuple(range(1, MAX_BIN_SIZE + 1, BIN_SIZE_STEP))
        _, all_axes = pypl.subplots(ncols=bin_sizes.__len__())
        for bin_size, axes in zip(bin_sizes, all_axes):
            if bin_size == 1:
                abscissa = tuple(range(last_time_point + 1))
                histogram = n_divisions_per_time_point
            else:
                bin_edges = tuple(range(0, last_time_point + 1, bin_size))
                if bin_edges[-1] != last_time_point:
                    bin_edges = bin_edges + (last_time_point,)
                abscissa = 0.5 * (
                    nmpy.array(bin_edges[1:]) + nmpy.array(bin_edges[:-1])
                )
                histogram, _ = nmpy.histogram(division_time_points, bins=bin_edges)
            axes.bar(abscissa, histogram, width=max(5, 0.75 * bin_size))
            axes.set_title(f"Bin size: {bin_size}")
        pypl.show()


if __name__ == "__main__":
    #
    if sstm.argv.__len__() == 4:
        error_has_occurred = False
        for a_idx, extension in enumerate(("xlsx", "xlsx", "txt"), start=1):
            arg_path = path_t(sstm.argv[a_idx])
            if not arg_path.is_file() or (arg_path.suffix[1:] != extension):
                error_has_occurred = True
                print(
                    f'Argument {a_idx} "{arg_path}": Not a(n existing) file, '
                    f"or wrong extension {arg_path.suffix}; Expected=.{extension}"
                )
        if not error_has_occurred:
            Main(sstm.argv[1], sstm.argv[2], sstm.argv[3], False, False)
    else:
        print("Parameters: tracks XLSX, cell events XLSX, corrections TXT")
