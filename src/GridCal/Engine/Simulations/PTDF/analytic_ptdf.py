# This file is part of GridCal.
#
# GridCal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GridCal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GridCal.  If not, see <http://www.gnu.org/licenses/>.
import time
import multiprocessing
from PySide2.QtCore import QThread, Signal

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve

from GridCal.Engine.basic_structures import Logger
from GridCal.Engine.Core.multi_circuit import MultiCircuit
from GridCal.Engine.Simulations.result_types import ResultTypes
from GridCal.Gui.GuiFunctions import ResultsModel
from GridCal.Engine.Core.snapshot_pf_data import compile_snapshot_circuit, split_into_islands


def make_ptdf(Bbus, Bf, pqpv, vd, distribute_slack=True):
    """
    Build the PTDF matrix
    :param Bbus: DC-linear susceptance matrix
    :param Bf: Bus-branch "from" susceptance matrix
    :param pqpv: array of sorted pq and pv node indices
    :param vd: array of slack node indices
    :param distribute_slack: distribute the slack?
    :return: PTDF matrix. It is a full matrix of dimensions branches x buses
    """

    n = Bbus.shape[0]
    dP = sp.eye(n, n).tocsc()
    nb = n
    nbi = n
    noref = np.arange(1, nb)
    noslack = pqpv

    # solve for change in voltage angles
    dTheta = np.zeros((nb, nbi))
    Bref = Bbus[noslack, :][:, noref].tocsc()
    dTheta[noref, :] = spsolve(Bref,  dP[noslack, :]).toarray()

    # compute corresponding change in branch flows
    # Bf is a sparse matrix
    H = Bf * dTheta

    # normalize the slack
    if distribute_slack:
        slack = vd + 1  # the +1 is to avoid zero divisions
        w_slack = slack / np.sum(slack)
        mod = sp.eye(nb, nb).toarray() - w_slack * np.ones((1, nb))
        H = np.dot(H, mod)

    return H


def make_lodf(Cf, Ct, PTDF):
    """
    Compute the LODF matrix
    :param Cf: Branch "from" -bus connectivity matrix
    :param Ct: Branch "to" -bus connectivity matrix
    :param PTDF: PTDF matrix in numpy array form (branches, buses)
    :return: LODF matrix of dimensions (branches, branches)
    """
    nl = PTDF.shape[0]

    # compute the connectivity matrix
    Cft = Cf - Ct

    H = PTDF * Cft.T

    # old code
    # h = sp.diags(H.diagonal())
    # LODF = H / (np.ones((nl, nl)) - h * np.ones(nl))

    # divide each row of H by the vector 1 - H.diagonal
    LODF = H / (1 - H.diagonal())

    # replace possible nan and inf
    LODF[LODF == -np.inf] = 0
    LODF[LODF == np.inf] = 0
    LODF = np.nan_to_num(LODF)

    # replace the diagonal elements by -1
    # old code
    # LODF = LODF - sp.diags(LODF.diagonal()) - sp.eye(nl, nl), replaced by:
    for i in range(nl):
        LODF[i, i] = - 1.0

    return LODF


class LinearAnalysisResults:

    def __init__(self, n_br=0, n_bus=0, br_names=(), bus_names=(), bus_types=()):
        """
        PTDF and LODF results class
        :param n_br: number of branches
        :param n_bus: number of buses
        :param br_names: branch names
        :param bus_names: bus names
        :param bus_types: bus types array
        """

        self.name = 'Linear Analysis'

        # number of branches
        self.n_br = n_br

        self.n_bus = n_bus

        # names of the branches
        self.br_names = br_names

        self.bus_names = bus_names

        self.bus_types = bus_types

        self.logger = Logger()

        self.PTDF = np.zeros((n_br, n_bus))
        self.LODF = np.zeros((n_br, n_br))

        self.available_results = [ResultTypes.PTDFBranchesSensitivity,
                                  ResultTypes.OTDF]

    def mdl(self, result_type: ResultTypes) -> ResultsModel:
        """
        Plot the results.

        Arguments:

            **result_type**: ResultTypes

        Returns: ResultsModel
        """

        if result_type == ResultTypes.PTDFBranchesSensitivity:
            labels = self.bus_names
            y = self.PTDF
            y_label = '(p.u.)'
            title = 'Branches sensitivity'

        elif result_type == ResultTypes.OTDF:
            labels = self.br_names
            y = self.LODF
            y_label = '(p.u.)'
            title = 'Branch failure sensitivity'

        else:
            labels = []
            y = np.zeros(0)
            y_label = ''
            title = ''

        # assemble model
        mdl = ResultsModel(data=y,
                           index=self.br_names,
                           columns=labels,
                           title=title,
                           ylabel=y_label,
                           units=y_label)
        return mdl


class LinearAnalysis:

    def __init__(self, grid: MultiCircuit, distributed_slack=True):
        """

        :param grid:
        :param distributed_slack:
        """

        self.grid = grid

        self.distributed_slack = distributed_slack

        self.numerical_circuit = None

        self.results = LinearAnalysisResults(n_br=0,
                                             n_bus=0,
                                             br_names=[],
                                             bus_names=[],
                                             bus_types=[])

    def run(self):
        """
        Run the PTDF and LODF
        """
        self.numerical_circuit = compile_snapshot_circuit(self.grid)
        islands = split_into_islands(self.numerical_circuit)

        self.results = LinearAnalysisResults(n_br=self.numerical_circuit.nbr,
                                             n_bus=self.numerical_circuit.nbus,
                                             br_names=self.numerical_circuit.branch_names,
                                             bus_names=self.numerical_circuit.bus_names,
                                             bus_types=self.numerical_circuit.bus_types)

        # compute the PTDF per islands
        if len(islands) > 0:
            for island in islands:

                # compute the linear-DC matrices
                Bbus, Bf = island.get_linear_matrices()

                # compute the PTDF of the island
                ptdf_island = make_ptdf(Bbus=Bbus,
                                        Bf=Bf,
                                        pqpv=island.pqpv,
                                        vd=island.vd,
                                        distribute_slack=self.distributed_slack)

                # assign the PTDF to the matrix
                self.results.PTDF[np.ix_(island.original_branch_idx, island.original_bus_idx)] = ptdf_island

        else:

            # compute the linear-DC matrices
            Bbus, Bf = islands[0].get_linear_matrices()

            # there is only 1 island, compute the PTDF
            self.results.PTDF = make_ptdf(Bbus=Bbus,
                                          Bf=Bf,
                                          pqpv=islands[0].pqpv,
                                          vd=islands[0].vd,
                                          distribute_slack=self.distributed_slack)

        # the LODF algorithm doesn't seem to solve any circuit, hence there is no need of island splitting
        self.results.LODF = make_lodf(Cf=self.numerical_circuit.C_branch_bus_f,
                                      Ct=self.numerical_circuit.C_branch_bus_t,
                                      PTDF=self.results.PTDF)

    def get_branch_time_series(self, Sbus):
        """
        Compute the time series PTDF
        :param Sbus: Power injections time series array
        :return:
        """

        # option 2: call the power directly
        P = Sbus.real
        PTDF = self.results.PTDF
        Pbr = np.dot(PTDF, P).T * self.grid.Sbase

        return Pbr
