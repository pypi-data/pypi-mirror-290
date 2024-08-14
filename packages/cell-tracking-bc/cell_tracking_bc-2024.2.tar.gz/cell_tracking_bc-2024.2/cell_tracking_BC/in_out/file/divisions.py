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

from pathlib import Path as path_t
from typing import Union

import networkx as ntwx
import xlsxwriter as xlsx
from cell_tracking_BC.in_out.file.event import _SaveDivisionEvents
from cell_tracking_BC.type.analysis import analysis_t
from logger_36 import LOGGER


def SaveCellDivisionsToXLSX(
    path: Union[str, path_t],
    analysis: analysis_t,
    dividing_cells,
    unwanted,
    overlapping,
    label_conversions,
    /,
) -> None:
    """"""
    if isinstance(path, str):
        path = path_t(path)

    workbook = xlsx.Workbook(str(path))

    csv_path = path.with_suffix(".csv")
    csv_accessor = open(csv_path, mode="w")

    dummy_feature_book = {}

    tracks = analysis.tracks
    if (tracks is None) or (tracks.__len__() == 0):
        LOGGER.warning("Sequence with no valid tracks.")
    else:
        division_time_points = {}  # tracks.DivisionTimePoints()
        for _key, _vle in dividing_cells.items():
            division_time_points[_key] = [_elm[-1] for _elm in _vle]
        AddUnwanted(
            division_time_points, tracks, unwanted, overlapping, label_conversions
        )
        _SaveDivisionEvents(
            workbook, csv_accessor, dummy_feature_book, division_time_points, tracks
        )

    workbook.close()
    csv_accessor.close()


def AddUnwanted(division_time_points, tracks, unwanted, overlapping, label_conversions):
    """"""
    if unwanted is None:
        unwanted = []
    if overlapping is None:
        overlapping = []

    for track in tracks:
        if not isinstance(track, ntwx.DiGraph):
            continue

        for node in track:
            if (node.uid in unwanted) or (node.uid in overlapping):
                if node.uid in unwanted:
                    marker = "Unwanted"
                else:
                    marker = "Overlap"
                for true_label in node.all_labels:
                    label = None
                    for key, value in label_conversions.items():
                        if value == true_label:
                            label = key
                            break
                    division_time_points[label] = [marker]
