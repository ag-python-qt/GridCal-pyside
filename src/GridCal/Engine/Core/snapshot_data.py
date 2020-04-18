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

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.sparse import diags, hstack as hstack_s, vstack as vstack_s
from scipy.sparse.linalg import factorized
from scipy.sparse import csc_matrix
from typing import List, Dict

from GridCal.Engine.basic_structures import Logger
import GridCal.Engine.Core.topology as tp
from GridCal.Engine.Core.multi_circuit import MultiCircuit
from GridCal.Engine.basic_structures import BranchImpedanceMode
from GridCal.Engine.basic_structures import BusMode
from GridCal.Engine.Simulations.PowerFlow.jacobian_based_power_flow import Jacobian
from GridCal.Engine.Simulations.PowerFlow.power_flow_results import PowerFlowResults
from GridCal.Engine.Simulations.PowerFlow.power_flow_aux import compile_types
from GridCal.Engine.Simulations.sparse_solve import get_sparse_type


# def calc_connectivity(idx_pi, idx_hvdc, idx_vsc,
#                       C_branch_bus_f, C_branch_bus_t, branch_active, bus_active,  # common to all branches
#
#                       # just for the pi-branch model
#                       apply_temperature, R_corrected,
#                       R, X, G, B, branch_tolerance_mode: BranchImpedanceMode, impedance_tolerance,
#                       tap_mod, tap_ang, tap_t, tap_f, Ysh,
#
#                       # for the HVDC lines
#                       Rdc,
#
#                       # for the VSC lines
#                       R1, X1, Gsw, Beq, m, theta):
#     """
#     Build all the admittance related objects
#     :param branch_active: array of branch active
#     :param bus_active: array of bus active
#     :param C_branch_bus_f: branch-bus from connectivity matrix
#     :param C_branch_bus_t: branch-bus to connectivity matrix
#     :param apply_temperature: apply temperature correction?
#     :param R_corrected: Use the corrected resistance?
#     :param R: array of resistance
#     :param X: array of reactance
#     :param G: array of conductance
#     :param B: array of susceptance
#     :param branch_tolerance_mode: branch tolerance mode (enum: BranchImpedanceMode)
#     :param impedance_tolerance: impedance tolerance
#     :param tap_mod: tap modules array
#     :param tap_ang: tap angles array
#     :param tap_t: virtual tap to array
#     :param tap_f: virtual tap from array
#     :param Ysh: shunt admittance injections
#     :return: Ybus: Admittance matrix
#              Yf: Admittance matrix of the from buses
#              Yt: Admittance matrix of the to buses
#              B1: Fast decoupled B' matrix
#              B2: Fast decoupled B'' matrix
#              Yseries: Admittance matrix of the series elements
#              Ys: array of series admittances
#              GBc: array of shunt conductances
#              Cf: Branch-bus from connectivity matrix
#              Ct: Branch-to from connectivity matrix
#              C_bus_bus: Adjacency matrix
#              C_branch_bus: branch-bus connectivity matrix
#              islands: List of islands bus indices (each list element is a list of bus indices of the island)
#     """
#
#     sparse = get_sparse_type()
#
#     # form the connectivity matrices with the states applied -----------------------------------------------------------
#     br_states_diag = sp.diags(branch_active)
#     Cf = br_states_diag * C_branch_bus_f
#     Ct = br_states_diag * C_branch_bus_t
#
#     # Declare the empty primitives -------------------------------------------------------------------------------------
#
#     # The composition order is and will be: Pi model, HVDC, VSC
#
#     n_pi = len(idx_pi)
#     n_hvdc = len(idx_hvdc)
#     n_vsc = len(idx_vsc)
#
#     mm = n_pi + n_hvdc + n_vsc
#     Ytt = np.empty(mm, dtype=complex)
#     Yff = np.empty(mm, dtype=complex)
#     Yft = np.empty(mm, dtype=complex)
#     Ytf = np.empty(mm, dtype=complex)
#
#     # Branch primitives in vector form, for Yseries
#     Ytts = np.empty(mm, dtype=complex)
#     Yffs = np.empty(mm, dtype=complex)
#     Yfts = np.empty(mm, dtype=complex)
#     Ytfs = np.empty(mm, dtype=complex)
#
#     # PI BRANCH MODEL --------------------------------------------------------------------------------------------------
#
#     # use the specified of the temperature-corrected resistance
#     if apply_temperature:
#         R = R_corrected
#
#     # modify the branches impedance with the lower, upper tolerance values
#     if branch_tolerance_mode == BranchImpedanceMode.Lower:
#         R *= (1 - impedance_tolerance / 100.0)
#     elif branch_tolerance_mode == BranchImpedanceMode.Upper:
#         R *= (1 + impedance_tolerance / 100.0)
#
#     Ys = 1.0 / (R + 1.0j * X)
#     GBc = G + 1.0j * B
#     Ys2 = (Ys + GBc / 2.0)
#     tap = tap_mod * np.exp(1.0j * tap_ang)
#
#     # branch primitives in vector form for Ybus
#     Ytt[idx_pi] = Ys2 / (tap_t * tap_t)
#     Yff[idx_pi] = Ys2 / (tap_f * tap_f * tap * np.conj(tap))
#     Yft[idx_pi] = - Ys / (tap_f * tap_t * np.conj(tap))
#     Ytf[idx_pi] = - Ys / (tap_t * tap_f * tap)
#
#     # branch primitives in vector form, for Yseries
#     Ytts[idx_pi] = Ys
#     Yffs[idx_pi] = Ys / (tap * np.conj(tap))
#     Yfts[idx_pi] = - Ys / np.conj(tap)
#     Ytfs[idx_pi] = - Ys / tap
#
#     # HVDC LINE MODEL --------------------------------------------------------------------------------------------------
#     Ydc = 1 / Rdc
#     Ytt[idx_hvdc] = Ydc
#     Yff[idx_hvdc] = Ydc
#     Yft[idx_hvdc] = - Ydc
#     Ytf[idx_hvdc] = - Ydc
#
#     Ytts[idx_hvdc] = Ydc
#     Yffs[idx_hvdc] = Ydc
#     Yfts[idx_hvdc] = - Ydc
#     Ytfs[idx_hvdc] = - Ydc
#
#     # VSC MODEL --------------------------------------------------------------------------------------------------------
#     Y_vsc = 1.0 / (R1 + 1.0j * X1)  # Y1
#     Yff[idx_vsc] = Y_vsc
#     Yft[idx_vsc] = -m * np.exp(1.0j * theta) * Y_vsc
#     Ytf[idx_vsc] = -m * np.exp(-1.0j * theta) * Y_vsc
#     Ytt[idx_vsc] = Gsw + m * m * (Y_vsc + 1.0j * Beq)
#
#     Yffs[idx_vsc] = Y_vsc
#     Yfts[idx_vsc] = -m * np.exp(1.0j * theta) * Y_vsc
#     Ytfs[idx_vsc] = -m * np.exp(-1.0j * theta) * Y_vsc
#     Ytts[idx_vsc] = m * m * (Y_vsc + 1.0j)
#
#     # form the admittance matrices -------------------------------------------------------------------------------------
#     Yf = sp.diags(Yff) * Cf + sp.diags(Yft) * Ct
#     Yt = sp.diags(Ytf) * Cf + sp.diags(Ytt) * Ct
#     Ybus = sparse(Cf.T * Yf + Ct.T * Yt + sp.diags(Ysh))
#
#     # form the admittance matrices of the series and shunt elements ----------------------------------------------------
#     Yfs = sp.diags(Yffs) * Cf + sp.diags(Yfts) * Ct
#     Yts = sp.diags(Ytfs) * Cf + sp.diags(Ytts) * Ct
#     Yseries = sparse(Cf.T * Yfs + Ct.T * Yts)
#
#     Gsh = np.zeros(mm, dtype=complex)
#     Gsh[idx_pi] = GBc
#     Gsh[idx_vsc] = Gsw + 1j * Beq
#     Yshunt = Ysh + Cf.T * Gsh + Ct.T * Gsh
#
#     # Form the matrices for fast decoupled -----------------------------------------------------------------------------
#     reactances = np.zeros(mm, dtype=float)
#     reactances[idx_pi] = X
#     reactances[idx_vsc] = X1
#
#     susceptances = np.zeros(mm, dtype=float)
#     susceptances[idx_pi] = B
#     susceptances[idx_vsc] = Beq
#
#     all_taps = np.ones(mm, dtype=complex)
#     all_taps[idx_pi] = tap
#     all_taps[idx_vsc] = m * np.exp(1j * theta)
#
#     b1 = 1.0 / (reactances + 1e-20)
#     b1_tt = sp.diags(b1)
#     B1f = b1_tt * Cf - b1_tt * Ct
#     B1t = -b1_tt * Cf + b1_tt * Ct
#     B1 = sparse(Cf.T * B1f + Ct.T * B1t)
#
#     b2 = b1 + susceptances
#     b2_ff = -(b2 / (all_taps * np.conj(all_taps))).real
#     b2_ft = -(b1 / np.conj(all_taps)).real
#     b2_tf = -(b1 / all_taps).real
#     b2_tt = - b2
#
#     B2f = -sp.diags(b2_ff) * Cf + sp.diags(b2_ft) * Ct
#     B2t = sp.diags(b2_tf) * Cf + -sp.diags(b2_tt) * Ct
#     B2 = sparse(Cf.T * B2f + Ct.T * B2t)
#
#     # Bus connectivity -------------------------------------------------------------------------------------------------
#
#     # branch - bus connectivity
#     C_branch_bus = Cf + Ct
#
#     # Connectivity node - Connectivity node connectivity matrix
#     bus_states_diag = sp.diags(bus_active)
#     C_bus_bus = bus_states_diag * (C_branch_bus.T * C_branch_bus)
#
#     return Ybus, Yf, Yt, B1, B2, Yseries, Yshunt, Ys, GBc, Cf, Ct, C_bus_bus, C_branch_bus
#
#
# def calc_islands(circuit: "SnapshotIsland", bus_active, C_bus_bus, C_branch_bus, C_bus_gen, C_bus_batt,
#                  nbus, nbr, ignore_single_node_islands=False) -> List["SnapshotIsland"]:
#     """
#     Partition the circuit in islands for the designated time intervals
#     :param circuit: CalculationInputs instance with all the data regardless of the islands and the branch states
#     :param C_bus_bus: bus-bus connectivity matrix
#     :param C_branch_bus: branch-bus connectivity matrix
#     :param C_bus_gen: gen-bus connectivity matrix
#     :param C_bus_batt: battery-bus connectivity matrix
#     :param nbus: number of buses
#     :param nbr: number of branches
#     :param ignore_single_node_islands: Ignore the single node islands
#     :return: list of CalculationInputs instances
#     """
#     # find the islands of the circuit
#     g = Graph(C_bus_bus=sp.csc_matrix(C_bus_bus),
#               C_branch_bus=sp.csc_matrix(C_branch_bus),
#               bus_states=bus_active)
#
#     islands = g.find_islands()
#
#     # clear the list of circuits
#     calculation_islands = list()
#
#     # find the branches that belong to each island
#     island_branches = list()
#
#     if len(islands) > 1:
#
#         # there are islands, pack the islands into sub circuits
#         for island_bus_idx in islands:
#
#             if ignore_single_node_islands and len(island_bus_idx) <= 1:
#                 keep = False
#             else:
#                 keep = True
#
#             if keep:
#                 # get the branch indices of the island
#                 island_br_idx = g.get_branches_of_the_island(island_bus_idx)
#                 island_br_idx = np.sort(island_br_idx)  # sort
#                 island_branches.append(island_br_idx)
#
#                 # indices of batteries and controlled generators that belong to this island
#                 gen_idx = np.where(C_bus_gen[island_bus_idx, :].sum(axis=0) > 0)[0]
#                 bat_idx = np.where(C_bus_batt[island_bus_idx, :].sum(axis=0) > 0)[0]
#
#                 # Get the island circuit (the bus types are computed automatically)
#                 # The island original indices are generated within the get_island function
#                 circuit_island = circuit.get_island(island_bus_idx, island_br_idx, gen_idx, bat_idx)
#
#                 # store the island
#                 calculation_islands.append(circuit_island)
#
#     else:
#         # Only one island
#
#         # compile bus types
#         circuit.consolidate()
#
#         # only one island, no need to split anything
#         calculation_islands.append(circuit)
#
#         island_bus_idx = np.arange(start=0, stop=nbus, step=1, dtype=int)
#         island_br_idx = np.arange(start=0, stop=nbr, step=1, dtype=int)
#
#         # set the indices in the island too
#         circuit.original_bus_idx = island_bus_idx
#         circuit.original_branch_idx = island_br_idx
#
#         # append a list with all the branch indices for completeness
#         island_branches.append(island_br_idx)
#
#     # return the list of islands
#     return calculation_islands
#
#
# class SnapshotIsland:
#     """
#     This class represents a SnapshotData for a single island
#     """
#
#     def __init__(self, nbus, nbr, nhvdc, nvsc, nbat, nctrlgen, Sbase=100):
#         """
#
#         :param nbus:
#         :param nbr:
#         :param nbat:
#         :param nctrlgen:
#         :param Sbase:
#         """
#         self.nbus = nbus
#         self.nbr = nbr
#         self.nhvdc = nhvdc
#         self.nvsc = nvsc
#
#         self.Sbase = Sbase
#
#         self.original_bus_idx = list()
#         self.original_branch_idx = list()
#         self.original_time_idx = list()
#
#         self.bus_names = np.empty(self.nbus, dtype=object)
#
#         # common to all branches
#         mm = nbr + nhvdc + nvsc
#         self.branch_names = np.empty(mm, dtype=object)
#         self.F = np.zeros(mm, dtype=int)
#         self.T = np.zeros(mm, dtype=int)
#         self.C_branch_bus_f = csc_matrix((mm, nbus), dtype=int)
#         self.C_branch_bus_t = csc_matrix((mm, nbus), dtype=int)
#
#         # resulting matrices (calculation)
#         self.Yf = csc_matrix((nbr, nbus), dtype=complex)
#         self.Yt = csc_matrix((nbr, nbus), dtype=complex)
#         self.Ybus = csc_matrix((nbus, nbus), dtype=complex)
#         self.Yseries = csc_matrix((nbus, nbus), dtype=complex)
#         self.B1 = csc_matrix((nbus, nbus), dtype=float)
#         self.B2 = csc_matrix((nbus, nbus), dtype=float)
#         self.Bpqpv = None
#         self.Bref = None
#
#         self.Ysh_helm = np.zeros(nbus, dtype=complex)
#         self.Ysh = np.zeros(nbus, dtype=complex)
#         self.Sbus = np.zeros(nbus, dtype=complex)
#         self.Ibus = np.zeros(nbus, dtype=complex)
#
#         self.Vbus = np.ones(nbus, dtype=complex)
#         self.Vmin = np.ones(nbus, dtype=float)
#         self.Vmax = np.ones(nbus, dtype=float)
#         self.types = np.zeros(nbus, dtype=int)
#         self.Qmin = np.zeros(nbus, dtype=float)
#         self.Qmax = np.zeros(nbus, dtype=float)
#         self.Sinstalled = np.zeros(nbus, dtype=float)
#
#         # vectors to re-calculate the admittance matrices
#         self.Ys = np.zeros(nbr, dtype=complex)
#         self.GBc = np.zeros(nbr, dtype=complex)
#         self.tap_f = np.zeros(nbr, dtype=float)
#         self.tap_t = np.zeros(nbr, dtype=float)
#         self.tap_ang = np.zeros(nbr, dtype=float)
#         self.tap_mod = np.ones(nbr, dtype=float)
#
#         # needed fot the tap changer
#         self.is_bus_to_regulated = np.zeros(nbr, dtype=int)
#         self.bus_to_regulated_idx = None
#         self.tap_position = np.zeros(nbr, dtype=int)
#         self.min_tap = np.zeros(nbr, dtype=int)
#         self.max_tap = np.zeros(nbr, dtype=int)
#         self.tap_inc_reg_up = np.zeros(nbr, dtype=float)
#         self.tap_inc_reg_down = np.zeros(nbr, dtype=float)
#         self.vset = np.zeros(nbr, dtype=float)
#
#         # vsc
#         self.vsc_m = np.ones(nvsc, dtype=float)
#
#         # Active power control
#         self.controlled_gen_pmin = np.zeros(nctrlgen, dtype=float)
#         self.controlled_gen_pmax = np.zeros(nctrlgen, dtype=float)
#         self.controlled_gen_enabled = np.zeros(nctrlgen, dtype=bool)
#         self.controlled_gen_dispatchable = np.zeros(nctrlgen, dtype=bool)
#
#         self.battery_pmin = np.zeros(nbat, dtype=float)
#         self.battery_pmax = np.zeros(nbat, dtype=float)
#         self.battery_Enom = np.zeros(nbat, dtype=float)
#         self.battery_soc_0 = np.zeros(nbat, dtype=float)
#         self.battery_discharge_efficiency = np.zeros(nbat, dtype=float)
#         self.battery_charge_efficiency = np.zeros(nbat, dtype=float)
#         self.battery_min_soc = np.zeros(nbat, dtype=float)
#         self.battery_max_soc = np.zeros(nbat, dtype=float)
#         self.battery_enabled = np.zeros(nbat, dtype=bool)
#         self.battery_dispatchable = np.zeros(nbat, dtype=bool)
#
#         # computed on consolidation
#         self.dispatcheable_batteries_bus_idx = list()
#
#         # connectivity matrices used to formulate OPF problems
#         self.C_bus_load = None
#         self.C_bus_batt = None
#         self.C_bus_sta_gen = None
#         self.C_bus_gen = None
#         self.C_bus_shunt = None
#
#         # ACPF system matrix factorization
#         self.Asys = None
#
#         self.branch_rates = np.zeros(nbr)
#
#         self.pq = list()
#         self.pv = list()
#         self.ref = list()
#         self.sto = list()
#         self.pqpv = list()  # it is sorted
#
#         self.logger = Logger()
#
#         self.available_structures = ['Vbus', 'Sbus', 'Ibus', 'Ybus', 'Yshunt', 'Yseries',
#                                      "B'", "B''", 'Types', 'Jacobian', 'Qmin', 'Qmax']
#
#     def consolidate(self):
#         """
#         Compute the magnitudes that cannot be computed vector-wise
#         """
#         self.bus_to_regulated_idx = np.where(self.is_bus_to_regulated == True)[0]
#
#         dispatcheable_batteries_idx = np.where(self.battery_dispatchable == True)[0]
#
#         self.dispatcheable_batteries_bus_idx = np.where(np.array(self.C_bus_batt[:, dispatcheable_batteries_idx].sum(axis=0))[0] > 0)[0]
#
#         #
#         self.ref, self.pq, self.pv, self.pqpv = compile_types(self.Sbus, self.types)
#
#         #
#         self.Bpqpv = self.Ybus.imag[np.ix_(self.pqpv, self.pqpv)]
#         self.Bref = self.Ybus.imag[np.ix_(self.pqpv, self.ref)]
#
#     def get_island(self, bus_idx, branch_idx, gen_idx, bat_idx) -> "SnapshotIsland":
#         """
#         Get a sub-island
#         :param bus_idx: bus indices of the island
#         :param branch_idx: branch indices of the island
#         :return: CalculationInputs instance
#         """
#         obj = SnapshotIsland(len(bus_idx), len(branch_idx), 0, 0, len(bat_idx), len(gen_idx))
#
#         # remember the island original indices
#         obj.original_bus_idx = bus_idx
#         obj.original_branch_idx = branch_idx
#
#         obj.Yf = self.Yf[np.ix_(branch_idx, bus_idx)]
#         obj.Yt = self.Yt[np.ix_(branch_idx, bus_idx)]
#         obj.Ybus = self.Ybus[np.ix_(bus_idx, bus_idx)]
#         obj.Yseries = self.Yseries[np.ix_(bus_idx, bus_idx)]
#         obj.B1 = self.B1[np.ix_(bus_idx, bus_idx)]
#         obj.B2 = self.B2[np.ix_(bus_idx, bus_idx)]
#
#         obj.Ysh = self.Ysh[bus_idx]
#         obj.Sbus = self.Sbus[bus_idx]
#         obj.Ibus = self.Ibus[bus_idx]
#         obj.Vbus = self.Vbus[bus_idx]
#         obj.types = self.types[bus_idx]
#         obj.Qmin = self.Qmin[bus_idx]
#         obj.Qmax = self.Qmax[bus_idx]
#         obj.Vmin = self.Vmin[bus_idx]
#         obj.Vmax = self.Vmax[bus_idx]
#         obj.Sinstalled = self.Sinstalled[bus_idx]
#
#         obj.F = self.F[branch_idx]
#         obj.T = self.T[branch_idx]
#         obj.branch_rates = self.branch_rates[branch_idx]
#         obj.bus_names = self.bus_names[bus_idx]
#         obj.branch_names = self.branch_names[branch_idx]
#
#         obj.C_branch_bus_f = self.C_branch_bus_f[np.ix_(branch_idx, bus_idx)]
#         obj.C_branch_bus_t = self.C_branch_bus_t[np.ix_(branch_idx, bus_idx)]
#
#         obj.C_bus_load = self.C_bus_load[bus_idx, :]
#         obj.C_bus_batt = self.C_bus_batt[bus_idx, :]
#         obj.C_bus_sta_gen = self.C_bus_sta_gen[bus_idx, :]
#         obj.C_bus_gen = self.C_bus_gen[bus_idx, :]
#         obj.C_bus_shunt = self.C_bus_shunt[bus_idx, :]
#
#         obj.is_bus_to_regulated = self.is_bus_to_regulated[branch_idx]
#         obj.tap_position = self.tap_position[branch_idx]
#         obj.min_tap = self.min_tap[branch_idx]
#         obj.max_tap = self.max_tap[branch_idx]
#         obj.tap_inc_reg_up = self.tap_inc_reg_up[branch_idx]
#         obj.tap_inc_reg_down = self.tap_inc_reg_down[branch_idx]
#         obj.vset = self.vset[branch_idx]
#         obj.tap_ang = self.tap_ang[branch_idx]
#         obj.tap_mod = self.tap_mod[branch_idx]
#
#         obj.Ys = self.Ys
#         obj.GBc = self.GBc
#         obj.tap_f = self.tap_f
#         obj.tap_t = self.tap_t
#
#         obj.controlled_gen_pmin = self.controlled_gen_pmin[gen_idx]
#         obj.controlled_gen_pmax = self.controlled_gen_pmax[gen_idx]
#         obj.controlled_gen_enabled = self.controlled_gen_enabled[gen_idx]
#         obj.controlled_gen_dispatchable = self.controlled_gen_dispatchable[gen_idx]
#         obj.battery_pmin = self.battery_pmin[bat_idx]
#         obj.battery_pmax = self.battery_pmax[bat_idx]
#         obj.battery_Enom = self.battery_Enom[bat_idx]
#         obj.battery_soc_0 = self.battery_soc_0[bat_idx]
#         obj.battery_discharge_efficiency = self.battery_discharge_efficiency[bat_idx]
#         obj.battery_charge_efficiency = self.battery_charge_efficiency[bat_idx]
#         obj.battery_min_soc = self.battery_min_soc[bat_idx]
#         obj.battery_max_soc = self.battery_max_soc[bat_idx]
#         obj.battery_enabled = self.battery_enabled[bat_idx]
#         obj.battery_dispatchable = self.battery_dispatchable[bat_idx]
#
#         obj.consolidate()
#
#         return obj
#
#     # def compute_branch_results(self, V) -> "PowerFlowResults":
#     #     """
#     #     Compute the branch magnitudes from the voltages
#     #     :param V: Voltage vector solution in p.u.
#     #     :return: PowerFlowResults instance
#     #     """
#     #
#     #     # declare circuit results
#     #     data = PowerFlowResults(self.nbus, self.nbr)
#     #
#     #     # copy the voltage
#     #     data.V = V
#     #
#     #     # power at the slack nodes
#     #     data.Sbus = self.Sbus.copy()
#     #     data.Sbus[self.ref] = V[self.ref] * np.conj(self.Ybus[self.ref, :].dot(V))
#     #
#     #     # Reactive power at the pv nodes: keep the original P injection and set the calculated reactive power
#     #     Q = (V[self.pv] * np.conj(self.Ybus[self.pv, :].dot(V))).imag
#     #
#     #     data.Sbus[self.pv] = self.Sbus[self.pv].real + 1j * Q
#     #
#     #     # Branches current, loading, etc
#     #     data.If = self.Yf * V
#     #     data.It = self.Yt * V
#     #     data.Sf = self.C_branch_bus_f * V * np.conj(data.If)
#     #     data.St = self.C_branch_bus_t * V * np.conj(data.It)
#     #
#     #     # Branch losses in MVA
#     #     data.losses = (data.Sf + data.St)
#     #
#     #     # Branch current in p.u.
#     #     data.Ibranch = np.maximum(data.If, data.It)
#     #
#     #     # Branch power in MVA
#     #     data.Sbranch = np.maximum(data.Sf, data.St)
#     #
#     #     # Branch loading in p.u.
#     #     data.loading = data.Sbranch / (self.branch_rates + 1e-9)
#     #
#     #     return data
#
#     def re_calc_admittance_matrices(self, tap_mod):
#         """
#         Recalculate the admittance matrices as the tap changes
#         :param tap_mod: tap modules per bus
#         :return: Nothing, the matrices are changed in-place
#         """
#         # here the branch_bus matrices do have the states embedded
#         Cf = self.C_branch_bus_f
#         Ct = self.C_branch_bus_t
#
#         tap = np.r_[tap_mod * np.exp(1.0j * self.tap_ang), ]
#
#         # branch primitives in vector form
#         Ytt = (self.Ys + self.GBc / 2.0) / (self.tap_t * self.tap_t)
#         Yff = (self.Ys + self.GBc / 2.0) / (self.tap_f * self.tap_f * tap * np.conj(tap))
#         Yft = - self.Ys / (self.tap_f * self.tap_t * np.conj(tap))
#         Ytf = - self.Ys / (self.tap_t * self.tap_f * tap)
#
#         # form the admittance matrices
#         self.Yf = diags(Yff) * Cf + diags(Yft) * Ct
#         self.Yt = diags(Ytf) * Cf + diags(Ytt) * Ct
#         self.Ybus = csc_matrix(Cf.T * self.Yf + Ct.T * self.Yt + diags(self.Ysh))
#
#         # branch primitives in vector form
#         Ytts = self.Ys
#         Yffs = Ytts / (tap * np.conj(tap))
#         Yfts = - self.Ys / np.conj(tap)
#         Ytfs = - self.Ys / tap
#
#         # form the admittance matrices of the series elements
#         Yfs = diags(Yffs) * Cf + diags(Yfts) * Ct
#         Yts = diags(Ytfs) * Cf + diags(Ytts) * Ct
#         self.Yseries = csc_matrix(Cf.T * Yfs + Ct.T * Yts)
#         Gsh = self.GBc / 2.0
#         self.Ysh += Cf.T * Gsh + Ct.T * Gsh
#
#         X = (1 / self.Ys).imag
#         b1 = 1.0 / (X + 1e-20)
#         B1f = diags(-b1) * Cf + diags(-b1) * Ct
#         B1t = diags(-b1) * Cf + diags(-b1) * Ct
#         self.B1 = csc_matrix(Cf.T * B1f + Ct.T * B1t)
#
#         b2 = b1 + self.GBc.imag  # B == GBc.imag
#         b2_ff = -(b2 / (tap * np.conj(tap))).real
#         b2_ft = -(b1 / np.conj(tap)).real
#         b2_tf = -(b1 / tap).real
#         b2_tt = - b2
#         B2f = diags(b2_ff) * Cf + diags(b2_ft) * Ct
#         B2t = diags(b2_tf) * Cf + diags(b2_tt) * Ct
#         self.B2 = csc_matrix(Cf.T * B2f + Ct.T * B2t)
#
#     def build_linear_ac_sys_mat(self):
#         """
#         Get the AC linear approximation matrices
#         :return:
#         """
#         A11 = -self.Yseries.imag[np.ix_(self.pqpv, self.pqpv)]
#         A12 = self.Ybus.real[np.ix_(self.pqpv, self.pq)]
#         A21 = -self.Yseries.real[np.ix_(self.pq, self.pqpv)]
#         A22 = -self.Ybus.imag[np.ix_(self.pq, self.pq)]
#
#         A = vstack_s([hstack_s([A11, A12]),
#                       hstack_s([A21, A22])], format="csc")
#
#         # form the slack system matrix
#         A11s = -self.Yseries.imag[np.ix_(self.ref, self.pqpv)]
#         A12s = self.Ybus.real[np.ix_(self.ref, self.pq)]
#         A_slack = hstack_s([A11s, A12s], format="csr")
#
#         self.Asys = factorized(A)
#         return A, A_slack
#
#     def get_structure(self, structure_type) -> pd.DataFrame:
#         """
#         Get a DataFrame with the input.
#
#         Arguments:
#
#             **structure_type** (str): 'Vbus', 'Sbus', 'Ibus', 'Ybus', 'Yshunt', 'Yseries' or 'Types'
#
#         Returns:
#
#             pandas DataFrame
#
#         """
#
#         if structure_type == 'Vbus':
#
#             df = pd.DataFrame(data=self.Vbus, columns=['Voltage (p.u.)'], index=self.bus_names)
#
#         elif structure_type == 'Sbus':
#             df = pd.DataFrame(data=self.Sbus, columns=['Power (p.u.)'], index=self.bus_names)
#
#         elif structure_type == 'Ibus':
#             df = pd.DataFrame(data=self.Ibus, columns=['Current (p.u.)'], index=self.bus_names)
#
#         elif structure_type == 'Ybus':
#             df = pd.DataFrame(data=self.Ybus.toarray(), columns=self.bus_names, index=self.bus_names)
#
#         elif structure_type == 'Yshunt':
#             df = pd.DataFrame(data=self.Ysh, columns=['Shunt admittance (p.u.)'], index=self.bus_names)
#
#         elif structure_type == 'Yseries':
#             df = pd.DataFrame(data=self.Yseries.toarray(), columns=self.bus_names, index=self.bus_names)
#
#         elif structure_type == "B'":
#             df = pd.DataFrame(data=self.B1.toarray(), columns=self.bus_names, index=self.bus_names)
#
#         elif structure_type == "B''":
#             df = pd.DataFrame(data=self.B2.toarray(), columns=self.bus_names, index=self.bus_names)
#
#         elif structure_type == 'Types':
#             df = pd.DataFrame(data=self.types, columns=['Bus types'], index=self.bus_names)
#
#         elif structure_type == 'Qmin':
#             df = pd.DataFrame(data=self.Qmin, columns=['Qmin'], index=self.bus_names)
#
#         elif structure_type == 'Qmax':
#             df = pd.DataFrame(data=self.Qmax, columns=['Qmax'], index=self.bus_names)
#
#         elif structure_type == 'Jacobian':
#
#             J = Jacobian(self.Ybus, self.Vbus, self.Ibus, self.pq, self.pqpv)
#
#             """
#             J11 = dS_dVa[array([pvpq]).T, pvpq].real
#             J12 = dS_dVm[array([pvpq]).T, pq].real
#             J21 = dS_dVa[array([pq]).T, pvpq].imag
#             J22 = dS_dVm[array([pq]).T, pq].imag
#             """
#             npq = len(self.pq)
#             npv = len(self.pv)
#             npqpv = npq + npv
#             cols = ['dS/dVa'] * npqpv + ['dS/dVm'] * npq
#             rows = cols
#             df = pd.DataFrame(data=J.toarray(), columns=cols, index=rows)
#
#         else:
#
#             raise Exception('PF input: structure type not found')
#
#         return df
#
#     def print(self, bus_names):
#         """
#         print in console
#         :return:
#         """
#         df_bus = pd.DataFrame(
#             np.c_[self.types, np.abs(self.Vbus), np.angle(self.Vbus), self.Vbus.real, self.Vbus.imag,
#                   self.Sbus.real, self.Sbus.imag, self.Ysh.real, self.Ysh.imag],
#             index=bus_names, columns=['Type', '|V|', 'angle', 're{V}', 'im{V}', 'P', 'Q', 'Gsh', 'Bsh'])
#         # df_bus.sort_index(inplace=True)
#
#         print('\nBus info\n', df_bus)
#
#         if self.nbus < 100:
#             print('\nYbus\n', pd.DataFrame(self.Ybus.todense(), columns=bus_names, index=bus_names))
#
#         print('PQ:', self.pq)
#         print('PV:', self.pv)
#         print('REF:', self.ref)
#
#
# class SnapshotData:
#     """
#     This class represents the set of numerical inputs for simulations that require
#     static values from the snapshot mode (power flow, short circuit, voltage collapse, PTDF, etc.)
#     """
#
#     def __init__(self, n_bus, n_pi, n_hvdc, n_vsc, n_ld, n_gen, n_sta_gen, n_batt, n_sh,
#                  idx_pi, idx_hvdc, idx_vsc, Sbase):
#         """
#         Topology constructor
#         :param n_bus: number of nodes
#         :param n_pi: number of branches
#         :param n_ld: number of loads
#         :param n_gen: number of generators
#         :param n_sta_gen: number of generators
#         :param n_batt: number of generators
#         :param n_sh: number of shunts
#         :param n_hvdc: number of dc lines
#         :param n_vsc: number of VSC converters
#         :param idx_pi: pi model branch indices
#         :param idx_hvdc: hvdc model branch indices
#         :param idx_vsc: vsc model branch indices
#         :param Sbase: circuit base power
#         """
#
#         # number of buses
#         self.nbus = n_bus
#
#         # number of branches
#         self.nbr = n_pi
#
#         self.n_hvdc = n_hvdc
#
#         self.n_vsc = n_vsc
#
#         self.n_batt = n_batt
#
#         self.n_gen = n_gen
#
#         self.n_ld = n_ld
#
#         self.idx_pi = idx_pi
#
#         self.idx_hvdc = idx_hvdc
#
#         self.idx_vsc = idx_vsc
#
#         # base power
#         self.Sbase = Sbase
#
#         self.time_array = None
#
#         # bus ----------------------------------------------------------------------------------------------------------
#         self.bus_names = np.empty(n_bus, dtype=object)
#         self.bus_vnom = np.zeros(n_bus, dtype=float)
#         self.bus_active = np.ones(n_bus, dtype=int)
#         self.V0 = np.ones(n_bus, dtype=complex)
#         self.Vmin = np.ones(n_bus, dtype=float)
#         self.Vmax = np.ones(n_bus, dtype=float)
#         self.bus_types = np.empty(n_bus, dtype=int)
#
#         # branch common ------------------------------------------------------------------------------------------------
#         mm = n_pi + n_hvdc + n_vsc
#         self.branch_names = np.empty(mm, dtype=object)
#         self.branch_active = np.zeros(mm, dtype=int)
#         self.F = np.zeros(mm, dtype=int)
#         self.T = np.zeros(mm, dtype=int)
#         self.branch_rates = np.zeros(mm, dtype=float)
#         self.C_branch_bus_f = sp.lil_matrix((mm, n_bus), dtype=int)
#         self.C_branch_bus_t = sp.lil_matrix((mm, n_bus), dtype=int)
#
#         # pi model -----------------------------------------------------------------------------------------------------
#         self.branch_R = np.zeros(n_pi, dtype=float)
#         self.branch_X = np.zeros(n_pi, dtype=float)
#         self.branch_G = np.zeros(n_pi, dtype=float)
#         self.branch_B = np.zeros(n_pi, dtype=float)
#         self.branch_impedance_tolerance = np.zeros(n_pi, dtype=float)
#         self.branch_tap_f = np.ones(n_pi, dtype=float)  # tap generated by the difference in nominal voltage at the form side
#         self.branch_tap_t = np.ones(n_pi, dtype=float)  # tap generated by the difference in nominal voltage at the to side
#         self.branch_tap_mod = np.zeros(n_pi, dtype=float)  # normal tap module
#         self.branch_tap_ang = np.zeros(n_pi, dtype=float)  # normal tap angle
#
#         self.branch_cost = np.zeros(n_pi, dtype=float)
#
#         self.branch_mttf = np.zeros(n_pi, dtype=float)
#         self.branch_mttr = np.zeros(n_pi, dtype=float)
#
#         self.branch_temp_base = np.zeros(n_pi, dtype=float)
#         self.branch_temp_oper = np.zeros(n_pi, dtype=float)
#         self.branch_alpha = np.zeros(n_pi, dtype=float)
#
#         self.branch_is_bus_to_regulated = np.zeros(n_pi, dtype=bool)
#         self.branch_tap_position = np.zeros(n_pi, dtype=int)
#         self.branch_min_tap = np.zeros(n_pi, dtype=int)
#         self.branch_max_tap = np.zeros(n_pi, dtype=int)
#         self.branch_tap_inc_reg_up = np.zeros(n_pi, dtype=float)
#         self.branch_tap_inc_reg_down = np.zeros(n_pi, dtype=float)
#         self.branch_vset = np.zeros(n_pi, dtype=float)
#         self.branch_switch_indices = list()
#
#         # hvdc line ----------------------------------------------------------------------------------------------------
#         self.hvdc_R = np.zeros(n_hvdc, dtype=float)
#         self.hvdc_Pset = np.zeros(n_hvdc, dtype=float)
#
#         # vsc converter ------------------------------------------------------------------------------------------------
#         self.vsc_R1 = np.zeros(n_vsc, dtype=float)
#         self.vsc_X1 = np.zeros(n_vsc, dtype=float)
#         self.vsc_G0 = np.zeros(n_vsc, dtype=float)
#         self.vsc_Beq = np.zeros(n_vsc, dtype=float)
#         self.vsc_m = np.zeros(n_vsc, dtype=float)
#         self.vsc_theta = np.zeros(n_vsc, dtype=float)
#
#         # load ---------------------------------------------------------------------------------------------------------
#         self.load_names = np.empty(n_ld, dtype=object)
#         self.load_power = np.zeros(n_ld, dtype=complex)
#         self.load_current = np.zeros(n_ld, dtype=complex)
#         self.load_admittance = np.zeros(n_ld, dtype=complex)
#         self.load_active = np.zeros(n_ld, dtype=bool)
#
#         self.load_cost = np.zeros(n_ld, dtype=float)
#
#         self.load_mttf = np.zeros(n_ld, dtype=float)
#         self.load_mttr = np.zeros(n_ld, dtype=float)
#
#         self.C_bus_load = sp.lil_matrix((n_bus, n_ld), dtype=int)
#
#         # battery ------------------------------------------------------------------------------------------------------
#         self.battery_names = np.empty(n_batt, dtype=object)
#         self.battery_power = np.zeros(n_batt, dtype=float)
#         self.battery_voltage = np.zeros(n_batt, dtype=float)
#         self.battery_qmin = np.zeros(n_batt, dtype=float)
#         self.battery_qmax = np.zeros(n_batt, dtype=float)
#         self.battery_pmin = np.zeros(n_batt, dtype=float)
#         self.battery_pmax = np.zeros(n_batt, dtype=float)
#         self.battery_Enom = np.zeros(n_batt, dtype=float)
#         self.battery_soc_0 = np.zeros(n_batt, dtype=float)
#         self.battery_discharge_efficiency = np.zeros(n_batt, dtype=float)
#         self.battery_charge_efficiency = np.zeros(n_batt, dtype=float)
#         self.battery_min_soc = np.zeros(n_batt, dtype=float)
#         self.battery_max_soc = np.zeros(n_batt, dtype=float)
#         self.battery_cost = np.zeros(n_batt, dtype=float)
#
#         self.battery_dispatchable = np.zeros(n_batt, dtype=bool)
#         self.battery_active = np.zeros(n_batt, dtype=bool)
#         self.battery_mttf = np.zeros(n_batt, dtype=float)
#         self.battery_mttr = np.zeros(n_batt, dtype=float)
#
#         self.C_bus_batt = sp.lil_matrix((n_bus, n_batt), dtype=int)
#
#         # static generator ---------------------------------------------------------------------------------------------
#         self.static_gen_names = np.empty(n_sta_gen, dtype=object)
#         self.static_gen_power = np.zeros(n_sta_gen, dtype=complex)
#         self.static_gen_dispatchable = np.zeros(n_sta_gen, dtype=bool)
#
#         self.static_gen_active = np.zeros(n_sta_gen, dtype=bool)
#
#         self.static_gen_mttf = np.zeros(n_sta_gen, dtype=float)
#         self.static_gen_mttr = np.zeros(n_sta_gen, dtype=float)
#
#         self.C_bus_sta_gen = sp.lil_matrix((n_bus, n_sta_gen), dtype=int)
#
#         # controlled generator -----------------------------------------------------------------------------------------
#         self.generator_names = np.empty(n_gen, dtype=object)
#         self.generator_power = np.zeros(n_gen, dtype=float)
#         self.generator_power_factor = np.zeros(n_gen, dtype=float)
#         self.generator_voltage = np.zeros(n_gen, dtype=float)
#         self.generator_qmin = np.zeros(n_gen, dtype=float)
#         self.generator_qmax = np.zeros(n_gen, dtype=float)
#         self.generator_pmin = np.zeros(n_gen, dtype=float)
#         self.generator_pmax = np.zeros(n_gen, dtype=float)
#         self.generator_dispatchable = np.zeros(n_gen, dtype=bool)
#         self.generator_controllable = np.zeros(n_gen, dtype=bool)
#         self.generator_cost = np.zeros(n_gen, dtype=float)
#         self.generator_nominal_power = np.zeros(n_gen, dtype=float)
#
#         self.generator_active = np.zeros(n_gen, dtype=bool)
#
#         self.generator_mttf = np.zeros(n_gen, dtype=float)
#         self.generator_mttr = np.zeros(n_gen, dtype=float)
#
#         self.C_bus_gen = sp.lil_matrix((n_bus, n_gen), dtype=int)
#
#         # shunt --------------------------------------------------------------------------------------------------------
#         self.shunt_names = np.empty(n_sh, dtype=object)
#         self.shunt_admittance = np.zeros(n_sh, dtype=complex)
#
#         self.shunt_active = np.zeros(n_sh, dtype=bool)
#
#         self.shunt_mttf = np.zeros(n_sh, dtype=float)
#         self.shunt_mttr = np.zeros(n_sh, dtype=float)
#
#         self.C_bus_shunt = sp.lil_matrix((n_bus, n_sh), dtype=int)
#
#     def get_power_injections(self):
#         """
#         returns the complex power injections in MW+jMVAr
#         """
#         Sbus = - self.C_bus_load * self.load_power.T  # MW
#         Sbus += self.C_bus_gen * self.generator_power.T
#         Sbus += self.C_bus_batt * self.battery_power.T
#         Sbus += self.C_bus_sta_gen * self.static_gen_power.T
#         # HVDC forced power
#         Sbus += self.hvdc_Pset * self.C_branch_bus_f[self.idx_hvdc, :]
#         Sbus -= self.hvdc_Pset * self.C_branch_bus_t[self.idx_hvdc, :]
#
#         return Sbus
#
#     def get_branch_number(self):
#         """
#         Get the number of branches
#         :return:
#         """
#         return self.nbr + self.n_hvdc + self.n_vsc
#
#     def get_raw_circuit(self, add_generation, add_storage) -> SnapshotIsland:
#         """
#
#         :param add_generation:
#         :param add_storage:
#         :return:
#         """
#         # Declare object to store the calculation inputs
#         circuit = SnapshotIsland(nbus=self.nbus,
#                                  nbr=self.nbr,
#                                  nhvdc=self.n_hvdc,
#                                  nvsc=self.n_vsc,
#                                  nbat=self.n_batt,
#                                  nctrlgen=self.n_gen)
#
#         # branches
#         circuit.branch_rates = self.branch_rates
#         circuit.F = self.F
#         circuit.T = self.T
#         circuit.tap_f = self.branch_tap_f
#         circuit.tap_t = self.branch_tap_t
#         circuit.bus_names = self.bus_names
#         circuit.branch_names = self.branch_names
#
#         # connectivity matrices
#         circuit.C_bus_load = self.C_bus_load
#         circuit.C_bus_batt = self.C_bus_batt
#         circuit.C_bus_sta_gen = self.C_bus_sta_gen
#         circuit.C_bus_gen = self.C_bus_gen
#         circuit.C_bus_shunt = self.C_bus_shunt
#
#         # needed for the tap changer
#         circuit.is_bus_to_regulated = self.branch_is_bus_to_regulated
#         circuit.tap_position = self.branch_tap_position
#         circuit.min_tap = self.branch_min_tap
#         circuit.max_tap = self.branch_max_tap
#         circuit.tap_inc_reg_up = self.branch_tap_inc_reg_up
#         circuit.tap_inc_reg_down = self.branch_tap_inc_reg_down
#         circuit.vset = self.branch_vset
#         circuit.tap_ang = self.branch_tap_ang
#         circuit.tap_mod = self.branch_tap_mod
#
#         # active power control
#         circuit.controlled_gen_pmin = self.generator_pmin
#         circuit.controlled_gen_pmax = self.generator_pmax
#         circuit.controlled_gen_enabled = self.generator_active
#         circuit.controlled_gen_dispatchable = self.generator_dispatchable
#         circuit.battery_pmin = self.battery_pmin
#         circuit.battery_pmax = self.battery_pmax
#         circuit.battery_Enom = self.battery_Enom
#         circuit.battery_soc_0 = self.battery_soc_0
#         circuit.battery_discharge_efficiency = self.battery_discharge_efficiency
#         circuit.battery_charge_efficiency = self.battery_charge_efficiency
#         circuit.battery_min_soc = self.battery_min_soc
#         circuit.battery_max_soc = self.battery_max_soc
#         circuit.battery_enabled = self.battery_active
#         circuit.battery_dispatchable = self.battery_dispatchable
#
#         ################################################################################################################
#         # loads, generators, batteries, etc...
#         ################################################################################################################
#
#         # Shunts
#         Ysh = self.C_bus_shunt * (self.shunt_admittance / self.Sbase)
#
#         # Loads
#         S = self.C_bus_load * (- self.load_power / self.Sbase * self.load_active)
#         I = self.C_bus_load * (- self.load_current / self.Sbase * self.load_active)
#         Ysh += self.C_bus_load * (self.load_admittance / self.Sbase * self.load_active)
#
#         if add_generation:
#             # static generators
#             S += self.C_bus_sta_gen * (self.static_gen_power / self.Sbase * self.static_gen_active)
#
#             # generators
#             pf2 = np.power(self.generator_power_factor, 2.0)
#             # compute the reactive power from the active power and the power factor
#             pf_sign = (self.generator_power_factor + 1e-20) / np.abs(self.generator_power_factor + 1e-20)
#             Q = pf_sign * self.generator_power * np.sqrt((1.0 - pf2) / (pf2 + 1e-20))
#             gen_S = self.generator_power + 1j * Q
#             S += self.C_bus_gen * (gen_S / self.Sbase * self.generator_active)
#
#         installed_generation_per_bus = self.C_bus_gen * (self.generator_nominal_power * self.generator_active)
#
#         # batteries
#         if add_storage:
#             S += self.C_bus_batt * (self.battery_power / self.Sbase * self.battery_active)
#
#         # HVDC forced power
#         S += (self.hvdc_Pset / self.Sbase) * self.C_branch_bus_f[self.idx_hvdc, :]
#         S -= (self.hvdc_Pset / self.Sbase) * self.C_branch_bus_t[self.idx_hvdc, :]
#
#         # Qmax
#         q_max = self.C_bus_gen * (self.generator_qmax / self.Sbase) + self.C_bus_batt * (self.battery_qmax / self.Sbase)
#
#         # Qmin
#         q_min = self.C_bus_gen * (self.generator_qmin / self.Sbase) + self.C_bus_batt * (self.battery_qmin / self.Sbase)
#
#         # assign the values
#         circuit.Ysh = Ysh
#         circuit.Sbus = S
#         circuit.Ibus = I
#         circuit.Vbus = self.V0
#         circuit.Sbase = self.Sbase
#         circuit.types = self.bus_types
#         circuit.Qmax = q_max
#         circuit.Qmin = q_min
#         circuit.Sinstalled = installed_generation_per_bus
#
#         return circuit
#
#     def compute(self, add_storage=True, add_generation=True, apply_temperature=False,
#                 branch_tolerance_mode=BranchImpedanceMode.Specified,
#                 ignore_single_node_islands=False) -> List[SnapshotIsland]:
#         """
#         Compute the cross connectivity matrices to determine the circuit connectivity
#         towards the calculation. Additionally, compute the calculation matrices.
#         :param add_storage:
#         :param add_generation:
#         :param apply_temperature:
#         :param branch_tolerance_mode:
#         :param ignore_single_node_islands: If True, the single node islands are omitted
#         :return: list of CalculationInputs instances where each one is a circuit island
#         """
#
#         # get the raw circuit with the inner arrays computed
#         circuit = self.get_raw_circuit(add_generation=add_generation, add_storage=add_storage)
#
#         """
#           n_br, n_hvdc, n_vsc,
#           C_branch_bus_f, C_branch_bus_t,  branch_active,  bus_active,  # common to all branches
#
#           # just for the pi-branch model
#           apply_temperature, R_corrected,
#           R, X, G, B, branch_tolerance_mode: BranchImpedanceMode, impedance_tolerance,
#           tap_mod, tap_ang, tap_t, tap_f, Ysh,
#
#           # for the HVDC lines
#           Rdc,
#
#           # for the VSC lines
#           R1, X1, Gsw, Beq, m, theta
#         """
#
#         # compute the connectivity and the different admittance matrices
#         circuit.Ybus, \
#         circuit.Yf, \
#         circuit.Yt, \
#         circuit.B1, \
#         circuit.B2, \
#         circuit.Yseries, \
#         circuit.Ysh_helm, \
#         circuit.Ys, \
#         circuit.GBc, \
#         circuit.C_branch_bus_f, \
#         circuit.C_branch_bus_t, \
#         C_bus_bus, \
#         C_branch_bus = calc_connectivity(idx_pi=self.idx_pi,
#                                          idx_hvdc=self.idx_hvdc,
#                                          idx_vsc=self.idx_vsc,
#                                          C_branch_bus_f=self.C_branch_bus_f,
#                                          C_branch_bus_t=self.C_branch_bus_t,
#                                          branch_active=self.branch_active,
#                                          bus_active=self.bus_active,
#
#                                          # pi model
#                                          apply_temperature=apply_temperature,
#                                          R_corrected=self.R_corrected(),
#                                          R=self.branch_R,
#                                          X=self.branch_X,
#                                          G=self.branch_G,
#                                          B=self.branch_B,
#                                          branch_tolerance_mode=branch_tolerance_mode,
#                                          impedance_tolerance=self.branch_impedance_tolerance,
#                                          tap_mod=self.branch_tap_mod,
#                                          tap_ang=self.branch_tap_ang,
#                                          tap_t=self.branch_tap_t,
#                                          tap_f=self.branch_tap_f,
#                                          Ysh=circuit.Ysh,
#
#                                          # HVDC line
#                                          Rdc=self.hvdc_R,
#
#                                          # VSC model
#                                          R1=self.vsc_R1,
#                                          X1=self.vsc_X1,
#                                          Gsw=self.vsc_G0,
#                                          Beq=self.vsc_Beq,
#                                          m=self.vsc_m,
#                                          theta=self.vsc_theta
#                                          )
#
#         #  split the circuit object into the individual circuits that may arise from the topological islands
#         calculation_islands = calc_islands(circuit=circuit,
#                                            bus_active=self.bus_active,
#                                            C_bus_bus=C_bus_bus,
#                                            C_branch_bus=C_branch_bus,
#                                            C_bus_gen=self.C_bus_gen,
#                                            C_bus_batt=self.C_bus_batt,
#                                            nbus=self.nbus,
#                                            nbr=self.get_branch_number(),
#                                            ignore_single_node_islands=ignore_single_node_islands)
#
#         for island in calculation_islands:
#             self.bus_types[island.original_bus_idx] = island.types
#
#         # return the list of islands
#         return calculation_islands
#
#     def R_corrected(self):
#         """
#         Returns temperature corrected resistances (numpy array) based on a formula
#         provided by: NFPA 70-2005, National Electrical Code, Table 8, footnote #2; and
#         https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity#Linear_approximation
#         (version of 2019-01-03 at 15:20 EST).
#         """
#         return self.branch_R * (1.0 + self.branch_alpha * (self.branch_temp_oper - self.branch_temp_base))
#
#     def get_B(self, apply_temperature=False):
#         """
#
#         :param apply_temperature:
#         :return:
#         """
#
#         # Shunts
#         Ysh = self.C_bus_shunt.T * (self.shunt_admittance / self.Sbase)
#
#         # Loads
#         Ysh += self.C_bus_load.T * (self.load_admittance / self.Sbase * self.load_active)
#
#         # form the connectivity matrices with the states applied
#         states_dia = sp.diags(self.branch_active)
#         Cf = states_dia * self.C_branch_bus_f
#         Ct = states_dia * self.C_branch_bus_t
#
#         if apply_temperature:
#             R = self.R_corrected()
#         else:
#             R = self.branch_R
#
#         Ys = 1.0 / (R + 1.0j * self.branch_X)
#         GBc = self.branch_G + 1.0j * self.branch_B
#         tap = self.branch_tap_mod * np.exp(1.0j * self.branch_tap_ang)
#
#         # branch primitives in vector form
#         Ytt = (Ys + GBc / 2.0) / (self.branch_tap_t * self.branch_tap_t)
#         Yff = (Ys + GBc / 2.0) / (self.branch_tap_f * self.branch_tap_f * tap * np.conj(tap))
#         Yft = - Ys / (self.branch_tap_f * self.branch_tap_t * np.conj(tap))
#         Ytf = - Ys / (self.branch_tap_t * self.branch_tap_f * tap)
#
#         # form the admittance matrices
#         Yf = sp.diags(Yff) * Cf + sp.diags(Yft) * Ct
#         Yt = sp.diags(Ytf) * Cf + sp.diags(Ytt) * Ct
#         Ybus = sp.csc_matrix(Cf.T * Yf + Ct.T * Yt + sp.diags(Ysh))
#
#         return Ybus.imag
#


def compile_types(Sbus, types, logger=Logger()):
    """
    Compile the types.
    :param Sbus: array of power injections per node
    :param types: array of tentative node types
    :param logger: logger where to store the errors
    :return: ref, pq, pv, pqpv
    """

    pq = np.where(types == BusMode.PQ.value)[0]
    pv = np.where(types == BusMode.PV.value)[0]
    ref = np.where(types == BusMode.REF.value)[0]

    if len(ref) == 0:  # there is no slack!

        if len(pv) == 0:  # there are no pv neither -> blackout grid

            logger.add('There are no slack nodes selected')

        else:  # select the first PV generator as the slack

            mx = max(Sbus[pv])
            if mx > 0:
                # find the generator that is injecting the most
                i = np.where(Sbus == mx)[0][0]

            else:
                # all the generators are injecting zero, pick the first pv
                i = pv[0]

            # delete the selected pv bus from the pv list and put it in the slack list
            pv = np.delete(pv, np.where(pv == i)[0])
            ref = [i]
            # print('Setting bus', i, 'as slack')

        ref = np.ndarray.flatten(np.array(ref))
        types[ref] = BusMode.REF.value
    else:
        pass  # no problem :)

    pqpv = np.r_[pq, pv]
    pqpv.sort()

    return ref, pq, pv, pqpv


class SnapshotCircuit:

    def __init__(self, nbus, nline, ntr, nvsc, nhvdc, nload, ngen, nbatt, nshunt, sbase,
                 apply_temperature=False, impedance_tolerance=0.0,
                 branch_tolerance_mode: BranchImpedanceMode = BranchImpedanceMode.Specified):
        """

        :param nbus: number of buses
        :param nline: number of lines
        :param ntr: number of transformers
        :param nvsc:
        :param nhvdc:
        :param nload:
        :param ngen:
        :param nbatt:
        :param nshunt:
        """

        self.nbus = nbus
        self.nline = nline
        self.ntr = ntr
        self.nvsc = nvsc
        self.nhvdc = nhvdc
        self.nload = nload
        self.ngen = ngen
        self.nbatt = nbatt
        self.nshunt = nshunt

        self.Sbase = sbase

        self.apply_temperature = apply_temperature
        self.branch_tolerance_mode = branch_tolerance_mode
        self.impedance_tolerance = impedance_tolerance

        # bus ----------------------------------------------------------------------------------------------------------
        self.bus_names = np.empty(nbus, dtype=object)
        self.bus_active = np.ones(nbus, dtype=int)
        self.Vbus = np.ones(nbus, dtype=complex)
        self.bus_types = np.empty(nbus, dtype=int)
        self.bus_installed_power = np.zeros(nbus, dtype=float)

        # branch common ------------------------------------------------------------------------------------------------
        self.nbr = nline + ntr + nhvdc + nvsc  # compute the number of branches

        self.branch_names = np.empty(self.nbr, dtype=object)
        self.branch_active = np.zeros(self.nbr, dtype=int)
        self.F = np.zeros(self.nbr, dtype=int)  # indices of the "from" buses
        self.T = np.zeros(self.nbr, dtype=int)  # indices of the "to" buses
        self.branch_rates = np.zeros(self.nbr, dtype=float)
        self.C_branch_bus_f = sp.lil_matrix((self.nbr, nbus), dtype=int)  # connectivity branch with their "from" bus
        self.C_branch_bus_t = sp.lil_matrix((self.nbr, nbus), dtype=int)  # connectivity branch with their "to" bus

        # lines --------------------------------------------------------------------------------------------------------
        self.line_names = np.zeros(nline, dtype=object)
        self.line_R = np.zeros(nline, dtype=float)
        self.line_X = np.zeros(nline, dtype=float)
        self.line_B = np.zeros(nline, dtype=float)
        self.line_temp_base = np.zeros(nline, dtype=float)
        self.line_temp_oper = np.zeros(nline, dtype=float)
        self.line_alpha = np.zeros(nline, dtype=float)
        self.line_impedance_tolerance = np.zeros(nline, dtype=float)

        self.C_line_bus = sp.lil_matrix((nline, nbus), dtype=int)  # this ons is just for splitting islands

        # transformer 2W + 3W ------------------------------------------------------------------------------------------
        self.tr_names = np.zeros(ntr, dtype=object)
        self.tr_R = np.zeros(ntr, dtype=float)
        self.tr_X = np.zeros(ntr, dtype=float)
        self.tr_G = np.zeros(ntr, dtype=float)
        self.tr_B = np.zeros(ntr)

        self.tr_tap_f = np.ones(ntr)  # tap generated by the difference in nominal voltage at the form side
        self.tr_tap_t = np.ones(ntr)  # tap generated by the difference in nominal voltage at the to side
        self.tr_tap_mod = np.ones(ntr)  # normal tap module
        self.tr_tap_ang = np.zeros(ntr)  # normal tap angle
        self.tr_is_bus_to_regulated = np.zeros(ntr, dtype=bool)
        self.tr_tap_position = np.zeros(ntr, dtype=int)
        self.tr_min_tap = np.zeros(ntr, dtype=int)
        self.tr_max_tap = np.zeros(ntr, dtype=int)
        self.tr_tap_inc_reg_up = np.zeros(ntr)
        self.tr_tap_inc_reg_down = np.zeros(ntr)
        self.tr_vset = np.ones(ntr)

        self.C_tr_bus = sp.lil_matrix((ntr, nbus), dtype=int)  # this ons is just for splitting islands

        # hvdc line ----------------------------------------------------------------------------------------------------
        self.hvdc_names = np.zeros(nhvdc, dtype=object)
        self.hvdc_active = np.zeros(nhvdc, dtype=bool)
        self.hvdc_rate = np.zeros(nhvdc, dtype=float)

        self.hvdc_Pset = np.zeros(nhvdc)
        self.hvdc_Vset_f = np.zeros(nhvdc)
        self.hvdc_Vset_t = np.zeros(nhvdc)
        self.hvdc_Qmin_f = np.zeros(nhvdc)
        self.hvdc_Qmax_f = np.zeros(nhvdc)
        self.hvdc_Qmin_t = np.zeros(nhvdc)
        self.hvdc_Qmax_t = np.zeros(nhvdc)

        self.C_hvdc_bus_f = sp.lil_matrix((nhvdc, nbus), dtype=int)  # this ons is just for splitting islands
        self.C_hvdc_bus_t = sp.lil_matrix((nhvdc, nbus), dtype=int)  # this ons is just for splitting islands

        # vsc converter ------------------------------------------------------------------------------------------------
        self.vsc_names = np.zeros(nvsc, dtype=object)
        self.vsc_R1 = np.zeros(nvsc)
        self.vsc_X1 = np.zeros(nvsc)
        self.vsc_Gsw = np.zeros(nvsc)
        self.vsc_Beq = np.zeros(nvsc)
        self.vsc_m = np.zeros(nvsc)
        self.vsc_theta = np.zeros(nvsc)

        self.C_vsc_bus = sp.lil_matrix((nvsc, nbus), dtype=int)  # this ons is just for splitting islands

        # load ---------------------------------------------------------------------------------------------------------
        self.load_names = np.empty(nload, dtype=object)
        self.load_active = np.zeros(nload, dtype=bool)
        self.load_s = np.zeros(nload, dtype=complex)

        self.C_bus_load = sp.lil_matrix((nbus, nload), dtype=int)

        # battery ------------------------------------------------------------------------------------------------------
        self.battery_names = np.empty(nbatt, dtype=object)
        self.battery_active = np.zeros(nbatt, dtype=bool)
        self.battery_controllable = np.zeros(nbatt, dtype=bool)
        self.battery_installed_p = np.zeros(nbatt)
        self.battery_p = np.zeros(nbatt)
        self.battery_pf = np.zeros(nbatt)
        self.battery_v = np.zeros(nbatt)
        self.battery_qmin = np.zeros(nbatt)
        self.battery_qmax = np.zeros(nbatt)

        self.C_bus_batt = sp.lil_matrix((nbus, nbatt), dtype=int)

        # generator ----------------------------------------------------------------------------------------------------
        self.generator_names = np.empty(ngen, dtype=object)
        self.generator_active = np.zeros(ngen, dtype=bool)
        self.generator_controllable = np.zeros(ngen, dtype=bool)
        self.generator_installed_p = np.zeros(ngen)
        self.generator_p = np.zeros(ngen)
        self.generator_pf = np.zeros(ngen)
        self.generator_v = np.zeros(ngen)
        self.generator_qmin = np.zeros(ngen)
        self.generator_qmax = np.zeros(ngen)

        self.C_bus_gen = sp.lil_matrix((nbus, ngen), dtype=int)

        # shunt --------------------------------------------------------------------------------------------------------
        self.shunt_names = np.empty(nshunt, dtype=object)
        self.shunt_active = np.zeros(nshunt, dtype=bool)
        self.shunt_admittance = np.zeros(nshunt, dtype=complex)

        self.C_bus_shunt = sp.lil_matrix((nbus, nshunt), dtype=int)

    def consolidate(self):
        """
        Consolidates the information of this object
        :return:
        """
        self.C_branch_bus_f = self.C_branch_bus_f.tocsc()
        self.C_branch_bus_t = self.C_branch_bus_t.tocsc()

        self.C_line_bus = self.C_line_bus.tocsc()
        self.C_tr_bus = self.C_tr_bus.tocsc()
        self.C_hvdc_bus_f = self.C_hvdc_bus_f.tocsc()
        self.C_hvdc_bus_t = self.C_hvdc_bus_t.tocsc()
        self.C_vsc_bus = self.C_vsc_bus.tocsc()

        self.C_bus_load = self.C_bus_load.tocsr()
        self.C_bus_batt = self.C_bus_batt.tocsr()
        self.C_bus_gen = self.C_bus_gen.tocsr()
        self.C_bus_shunt = self.C_bus_shunt.tocsr()

        self.bus_installed_power = self.C_bus_gen * self.generator_installed_p
        self.bus_installed_power += self.C_bus_batt * self.battery_installed_p

    def to_island(self) -> "SnapshotIsland":
        """
        copy theis circuit as an island device
        :return: NumericIsland instance
        """
        island = SnapshotIsland(nbus=self.nbus,
                                nline=self.nline,
                                ntr=self.ntr,
                                nvsc=self.nvsc,
                                nhvdc=self.nhvdc,
                                nload=self.nload,
                                ngen=self.ngen,
                                nbatt=self.nbatt,
                                nshunt=self.nshunt,
                                sbase=self.Sbase,
                                apply_temperature=self.apply_temperature,
                                impedance_tolerance=self.impedance_tolerance,
                                branch_tolerance_mode=self.branch_tolerance_mode)

        island.original_bus_idx = np.arange(self.nbus)
        island.original_branch_idx = np.arange(self.nbr)
        island.original_tr_idx = np.arange(self.ntr)
        island.original_gen_idx = np.arange(self.ngen)
        island.original_bat_idx = np.arange(self.nbatt)

        # bus ----------------------------------------------------------------------------------------------------------
        island.bus_names = self.bus_names
        island.bus_active = self.bus_active
        island.Vbus = self.Vbus
        island.bus_types = self.bus_types

        # branches common ----------------------------------------------------------------------------------------------
        island.branch_names = self.branch_names
        island.branch_active = self.branch_active
        island.F = self.F
        island.T = self.T
        island.branch_rates = self.branch_rates
        island.C_branch_bus_f = self.C_branch_bus_f
        island.C_branch_bus_t = self.C_branch_bus_t

        # lines --------------------------------------------------------------------------------------------------------
        island.line_names = self.line_names
        island.line_R = self.line_R
        island.line_X = self.line_X
        island.line_B = self.line_B
        island.line_temp_base = self.line_temp_base
        island.line_temp_oper = self.line_temp_oper
        island.line_alpha = self.line_alpha
        island.line_impedance_tolerance = self.line_impedance_tolerance

        island.C_line_bus = self.C_line_bus

        # transformer 2W + 3W ------------------------------------------------------------------------------------------
        island.tr_names = self.tr_names
        island.tr_R = self.tr_R
        island.tr_X = self.tr_X
        island.tr_G = self.tr_G
        island.tr_B = self.tr_B

        island.tr_tap_f = self.tr_tap_f
        island.tr_tap_t = self.tr_tap_t
        island.tr_tap_mod = self.tr_tap_mod
        island.tr_tap_ang = self.tr_tap_ang
        island.tr_is_bus_to_regulated = self.tr_is_bus_to_regulated
        island.tr_tap_position = self.tr_tap_position
        island.tr_min_tap = self.tr_min_tap
        island.tr_max_tap = self.tr_max_tap
        island.tr_tap_inc_reg_up = self.tr_tap_inc_reg_up
        island.tr_tap_inc_reg_down = self.tr_tap_inc_reg_down
        island.tr_vset = self.tr_vset

        island.C_tr_bus = self.C_tr_bus

        # hvdc line ----------------------------------------------------------------------------------------------------
        island.hvdc_names = self.hvdc_names
        island.hvdc_active = self.hvdc_active
        island.hvdc_rate = self.hvdc_rate

        island.hvdc_Pset = self.hvdc_Pset

        island.hvdc_Vset_f = self.hvdc_Vset_f
        island.hvdc_Vset_t = self.hvdc_Vset_t

        island.hvdc_Qmin_f = self.hvdc_Qmin_f
        island.hvdc_Qmax_f = self.hvdc_Qmax_f
        island.hvdc_Qmin_t = self.hvdc_Qmin_t
        island.hvdc_Qmax_t = self.hvdc_Qmax_t

        island.C_hvdc_bus_f = self.C_hvdc_bus_f
        island.C_hvdc_bus_f = self.C_hvdc_bus_t

        # vsc converter ------------------------------------------------------------------------------------------------
        island.vsc_names = self.vsc_names
        island.vsc_R1 = self.vsc_R1
        island.vsc_X1 = self.vsc_X1
        island.vsc_Gsw = self.vsc_Gsw
        island.vsc_Beq = self.vsc_Beq
        island.vsc_m = self.vsc_m
        island.vsc_theta = self.vsc_theta

        island.C_vsc_bus = self.C_vsc_bus

        # load ---------------------------------------------------------------------------------------------------------
        island.load_names = self.load_names
        island.load_active = self.load_active
        island.load_s = self.load_s

        island.C_bus_load = self.C_bus_load

        # battery ------------------------------------------------------------------------------------------------------
        island.battery_names = self.battery_names
        island.battery_active = self.battery_active
        island.battery_controllable = self.battery_controllable
        island.battery_p = self.battery_p
        island.battery_pf = self.battery_pf
        island.battery_v = self.battery_v
        island.battery_qmin = self.battery_qmin
        island.battery_qmax = self.battery_qmax

        island.C_bus_batt = self.C_bus_batt

        # generator ----------------------------------------------------------------------------------------------------
        island.generator_names = self.generator_names
        island.generator_active = self.generator_active
        island.generator_controllable = self.generator_controllable
        island.generator_p = self.generator_p
        island.generator_pf = self.generator_pf
        island.generator_v = self.generator_v
        island.generator_qmin = self.generator_qmin
        island.generator_qmax = self.generator_qmax

        island.C_bus_gen = self.C_bus_gen

        # shunt --------------------------------------------------------------------------------------------------------
        island.shunt_names = self.shunt_names
        island.shunt_active = self.shunt_active
        island.shunt_admittance = self.shunt_admittance

        island.C_bus_shunt = self.C_bus_shunt

        return island

    def get_island(self, bus_idx) -> "SnapshotIsland":
        """
        Get the island corresponding to the given buses
        :param bus_idx: array of bus indices
        :return: NumericIsland
        """

        # find the indices of the devices of the island
        line_idx = tp.get_elements_of_the_island(self.C_line_bus, bus_idx)
        tr_idx = tp.get_elements_of_the_island(self.C_tr_bus, bus_idx)
        vsc_idx = tp.get_elements_of_the_island(self.C_vsc_bus, bus_idx)
        hvdc_idx = tp.get_elements_of_the_island(self.C_hvdc_bus_f + self.C_hvdc_bus_t, bus_idx)
        br_idx = tp.get_elements_of_the_island(self.C_branch_bus_f + self.C_branch_bus_t, bus_idx)

        load_idx = tp.get_elements_of_the_island(self.C_bus_load.T, bus_idx)
        gen_idx = tp.get_elements_of_the_island(self.C_bus_gen.T, bus_idx)
        batt_idx = tp.get_elements_of_the_island(self.C_bus_batt.T, bus_idx)
        shunt_idx = tp.get_elements_of_the_island(self.C_bus_shunt.T, bus_idx)

        nc = SnapshotIsland(nbus=len(bus_idx),
                            nline=len(line_idx),
                            ntr=len(tr_idx),
                            nvsc=len(vsc_idx),
                            nhvdc=len(hvdc_idx),
                            nload=len(load_idx),
                            ngen=len(gen_idx),
                            nbatt=len(batt_idx),
                            nshunt=len(shunt_idx),
                            sbase=self.Sbase,
                            apply_temperature=self.apply_temperature,
                            impedance_tolerance=self.impedance_tolerance,
                            branch_tolerance_mode=self.branch_tolerance_mode)

        nc.original_bus_idx = bus_idx
        nc.original_branch_idx = br_idx

        nc.original_tr_idx = tr_idx
        nc.original_gen_idx = gen_idx
        nc.original_bat_idx = batt_idx

        # bus ----------------------------------------------------------------------------------------------------------
        nc.bus_names = self.bus_names[bus_idx]
        nc.bus_active = self.bus_active[bus_idx]
        nc.Vbus = self.Vbus[bus_idx]
        nc.bus_types = self.bus_types[bus_idx]

        # branch common ------------------------------------------------------------------------------------------------
        nc.branch_names = self.branch_names[br_idx]
        nc.branch_active = self.branch_active[br_idx]
        nc.F = self.F[br_idx]
        nc.T = self.T[br_idx]
        nc.branch_rates = self.branch_rates[br_idx]
        nc.C_branch_bus_f = self.C_branch_bus_f[np.ix_(br_idx, bus_idx)]
        nc.C_branch_bus_t = self.C_branch_bus_t[np.ix_(br_idx, bus_idx)]

        # lines --------------------------------------------------------------------------------------------------------
        nc.line_names = self.line_names[line_idx]
        nc.line_R = self.line_R[line_idx]
        nc.line_X = self.line_X[line_idx]
        nc.line_B = self.line_B[line_idx]
        nc.line_temp_base = self.line_temp_base[line_idx]
        nc.line_temp_oper = self.line_temp_oper[line_idx]
        nc.line_alpha = self.line_alpha[line_idx]
        nc.line_impedance_tolerance = self.line_impedance_tolerance[line_idx]

        nc.C_line_bus = self.C_line_bus[np.ix_(line_idx, bus_idx)]

        # transformer 2W + 3W ------------------------------------------------------------------------------------------
        nc.tr_names = self.tr_names[tr_idx]
        nc.tr_R = self.tr_R[tr_idx]
        nc.tr_X = self.tr_X[tr_idx]
        nc.tr_G = self.tr_G[tr_idx]
        nc.tr_B = self.tr_B[tr_idx]

        nc.tr_tap_f = self.tr_tap_f[tr_idx]
        nc.tr_tap_t = self.tr_tap_t[tr_idx]
        nc.tr_tap_mod = self.tr_tap_mod[tr_idx]
        nc.tr_tap_ang = self.tr_tap_ang[tr_idx]
        nc.tr_is_bus_to_regulated = self.tr_is_bus_to_regulated[tr_idx]
        nc.tr_tap_position = self.tr_tap_position[tr_idx]
        nc.tr_min_tap = self.tr_min_tap[tr_idx]
        nc.tr_max_tap = self.tr_max_tap[tr_idx]
        nc.tr_tap_inc_reg_up = self.tr_tap_inc_reg_up[tr_idx]
        nc.tr_tap_inc_reg_down = self.tr_tap_inc_reg_down[tr_idx]
        nc.tr_vset = self.tr_vset[tr_idx]

        nc.C_tr_bus = self.C_tr_bus[np.ix_(tr_idx, bus_idx)]

        # hvdc line ----------------------------------------------------------------------------------------------------
        nc.hvdc_names = self.hvdc_names[hvdc_idx]
        nc.hvdc_active = self.hvdc_active[hvdc_idx]
        nc.hvdc_rate = self.hvdc_rate[hvdc_idx]

        nc.hvdc_Pset = self.hvdc_Pset[hvdc_idx]
        nc.hvdc_Vset_f = self.hvdc_Vset_f[hvdc_idx]
        nc.hvdc_Vset_t = self.hvdc_Vset_t[hvdc_idx]
        nc.hvdc_Qmin_f = self.hvdc_Qmin_f[hvdc_idx]
        nc.hvdc_Qmax_f = self.hvdc_Qmax_f[hvdc_idx]
        nc.hvdc_Qmin_t = self.hvdc_Qmin_t[hvdc_idx]
        nc.hvdc_Qmax_t = self.hvdc_Qmax_t[hvdc_idx]

        nc.C_hvdc_bus_f = self.C_hvdc_bus_f[np.ix_(hvdc_idx, bus_idx)]
        nc.C_hvdc_bus_t = self.C_hvdc_bus_t[np.ix_(hvdc_idx, bus_idx)]

        # vsc converter ------------------------------------------------------------------------------------------------
        nc.vsc_names = self.vsc_names[vsc_idx]
        nc.vsc_R1 = self.vsc_R1[vsc_idx]
        nc.vsc_X1 = self.vsc_X1[vsc_idx]
        nc.vsc_Gsw = self.vsc_Gsw[vsc_idx]
        nc.vsc_Beq = self.vsc_Beq[vsc_idx]
        nc.vsc_m = self.vsc_m[vsc_idx]
        nc.vsc_theta = self.vsc_theta[vsc_idx]

        nc.C_vsc_bus = self.C_vsc_bus[np.ix_(vsc_idx, bus_idx)]

        # load ---------------------------------------------------------------------------------------------------------
        nc.load_names = self.load_names[load_idx]
        nc.load_active = self.load_active[load_idx]
        nc.load_s = self.load_s[load_idx]

        nc.C_bus_load = self.C_bus_load[np.ix_(bus_idx, load_idx)]

        # battery ------------------------------------------------------------------------------------------------------
        nc.battery_names = self.battery_names[batt_idx]
        nc.battery_active = self.battery_active[batt_idx]
        nc.battery_controllable = self.battery_controllable[batt_idx]
        nc.battery_p = self.battery_p[batt_idx]
        nc.battery_pf = self.battery_pf[batt_idx]
        nc.battery_v = self.battery_v[batt_idx]
        nc.battery_qmin = self.battery_qmin[batt_idx]
        nc.battery_qmax = self.battery_qmax[batt_idx]

        nc.C_bus_batt = self.C_bus_batt[np.ix_(bus_idx, batt_idx)]

        # generator ----------------------------------------------------------------------------------------------------
        nc.generator_names = self.generator_names[gen_idx]
        nc.generator_active = self.generator_active[gen_idx]
        nc.generator_controllable = self.generator_controllable[gen_idx]
        nc.generator_p = self.generator_p[gen_idx]
        nc.generator_pf = self.generator_pf[gen_idx]
        nc.generator_v = self.generator_v[gen_idx]
        nc.generator_qmin = self.generator_qmin[gen_idx]
        nc.generator_qmax = self.generator_qmax[gen_idx]

        nc.C_bus_gen = self.C_bus_gen[np.ix_(bus_idx, gen_idx)]

        # shunt --------------------------------------------------------------------------------------------------------
        nc.shunt_names = self.shunt_names[shunt_idx]
        nc.shunt_active = self.shunt_active[shunt_idx]
        nc.shunt_admittance = self.shunt_admittance[shunt_idx]

        nc.C_bus_shunt = self.C_bus_shunt[np.ix_(bus_idx, shunt_idx)]

        return nc


class SnapshotIsland(SnapshotCircuit):

    def __init__(self, nbus, nline, ntr, nvsc, nhvdc, nload, ngen, nbatt, nshunt, sbase,
                 apply_temperature=False, impedance_tolerance=0.0,
                 branch_tolerance_mode: BranchImpedanceMode = BranchImpedanceMode.Specified):
        """

        :param nbus:
        :param nline:
        :param ntr:
        :param nvsc:
        :param nhvdc:
        :param nload:
        :param ngen:
        :param nbatt:
        :param nshunt:
        :param sbase:
        :param apply_temperature:
        :param impedance_tolerance:
        :param branch_tolerance_mode:
        """
        SnapshotCircuit.__init__(self, nbus=nbus, nline=nline, ntr=ntr, nvsc=nvsc, nhvdc=nhvdc,
                                 nload=nload, ngen=ngen, nbatt=nbatt, nshunt=nshunt, sbase=sbase,
                                 apply_temperature=apply_temperature, branch_tolerance_mode=branch_tolerance_mode,
                                 impedance_tolerance=impedance_tolerance)

        self.Sbus = np.zeros(self.nbus, dtype=complex)
        self.Ibus = np.zeros(self.nbus, dtype=complex)

        self.Qmax_bus = np.zeros(self.nbus)
        self.Qmin_bus = np.zeros(self.nbus)

        self.Ybus = None
        self.Yf = None
        self.Yt = None
        self.Yseries = None
        self.Yshunt = None
        # self.Ysh_helm = None
        self.B1 = None
        self.B2 = None
        self.Bpqpv = None
        self.Bref = None

        self.original_bus_idx = list()
        self.original_branch_idx = list()
        self.original_tr_idx = list()
        self.original_gen_idx = list()
        self.original_bat_idx = list()

        self.pq = list()
        self.pv = list()
        self.vd = list()
        self.pqpv = list()

        self.available_structures = ['Vbus', 'Sbus', 'Ibus', 'Ybus', 'Yshunt', 'Yseries',
                                     "B'", "B''", 'Types', 'Jacobian', 'Qmin', 'Qmax']

    def R_corrected(self):
        """
        Returns temperature corrected resistances (numpy array) based on a formula
        provided by: NFPA 70-2005, National Electrical Code, Table 8, footnote #2; and
        https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity#Linear_approximation
        (version of 2019-01-03 at 15:20 EST).
        """
        return self.line_R * (1.0 + self.line_alpha * (self.line_temp_oper - self.line_temp_base))

    def compute_admittance_matrices(self):
        """
        Compute the admittance matrices
        :return: Ybus, Yseries, Yshunt
        """
        # form the connectivity matrices with the states applied -------------------------------------------------------
        br_states_diag = sp.diags(self.branch_active)
        Cf = br_states_diag * self.C_branch_bus_f
        Ct = br_states_diag * self.C_branch_bus_t

        # Declare the empty primitives ---------------------------------------------------------------------------------

        # The composition order is and will be: Pi model, HVDC, VSC
        Ytt = np.empty(self.nbr, dtype=complex)
        Yff = np.empty(self.nbr, dtype=complex)
        Yft = np.empty(self.nbr, dtype=complex)
        Ytf = np.empty(self.nbr, dtype=complex)

        # Branch primitives in vector form, for Yseries
        Ytts = np.empty(self.nbr, dtype=complex)
        Yffs = np.empty(self.nbr, dtype=complex)
        Yfts = np.empty(self.nbr, dtype=complex)
        Ytfs = np.empty(self.nbr, dtype=complex)

        ysh_br = np.empty(self.nbr, dtype=complex)

        # line ---------------------------------------------------------------------------------------------------------
        a = 0
        b = self.nline

        # use the specified of the temperature-corrected resistance
        if self.apply_temperature:
            line_R = self.R_corrected()
        else:
            line_R = self.line_R

        # modify the branches impedance with the lower, upper tolerance values
        if self.branch_tolerance_mode == BranchImpedanceMode.Lower:
            line_R *= (1 - self.impedance_tolerance / 100.0)
        elif self.branch_tolerance_mode == BranchImpedanceMode.Upper:
            line_R *= (1 + self.impedance_tolerance / 100.0)

        Ys_line = 1.0 / (line_R + 1.0j * self.line_X)
        Ysh_line = 1.0j * self.line_B
        Ys_line2 = Ys_line + Ysh_line / 2.0

        # branch primitives in vector form for Ybus
        Ytt[a:b] = Ys_line2
        Yff[a:b] = Ys_line2
        Yft[a:b] = - Ys_line
        Ytf[a:b] = - Ys_line

        # branch primitives in vector form, for Yseries
        Ytts[a:b] = Ys_line
        Yffs[a:b] = Ys_line
        Yfts[a:b] = - Ys_line
        Ytfs[a:b] = - Ys_line
        ysh_br[a:b] = Ysh_line / 2.0

        # transformer models -------------------------------------------------------------------------------------------

        a = self.nline
        b = a + self.ntr

        Ys_tr = 1.0 / (self.tr_R + 1.0j * self.tr_X)
        Ysh_tr = 1.0j * self.tr_B
        Ys_tr2 = Ys_tr + Ysh_tr / 2.0
        tap = self.tr_tap_mod * np.exp(1.0j * self.tr_tap_ang)

        # branch primitives in vector form for Ybus
        Ytt[a:b] = Ys_tr2 / (self.tr_tap_t * self.tr_tap_t)
        Yff[a:b] = Ys_tr2 / (self.tr_tap_f * self.tr_tap_f * tap * np.conj(tap))
        Yft[a:b] = - Ys_tr / (self.tr_tap_f * self.tr_tap_t * np.conj(tap))
        Ytf[a:b] = - Ys_tr / (self.tr_tap_t * self.tr_tap_f * tap)

        # branch primitives in vector form, for Yseries
        Ytts[a:b] = Ys_tr
        Yffs[a:b] = Ys_tr / (tap * np.conj(tap))
        Yfts[a:b] = - Ys_tr / np.conj(tap)
        Ytfs[a:b] = - Ys_tr / tap
        ysh_br[a:b] = Ysh_tr / 2.0

        # VSC MODEL ----------------------------------------------------------------------------------------------------
        a = self.nline + self.ntr
        b = a + self.nvsc

        Y_vsc = 1.0 / (self.vsc_R1 + 1.0j * self.vsc_X1)  # Y1
        Yff[a:b] = Y_vsc
        Yft[a:b] = -self.vsc_m * np.exp(1.0j * self.vsc_theta) * Y_vsc
        Ytf[a:b] = -self.vsc_m * np.exp(-1.0j * self.vsc_theta) * Y_vsc
        Ytt[a:b] = self.vsc_Gsw + self.vsc_m * self.vsc_m * (Y_vsc + 1.0j * self.vsc_Beq)

        Yffs[a:b] = Y_vsc
        Yfts[a:b] = -self.vsc_m * np.exp(1.0j * self.vsc_theta) * Y_vsc
        Ytfs[a:b] = -self.vsc_m * np.exp(-1.0j * self.vsc_theta) * Y_vsc
        Ytts[a:b] = self.vsc_m * self.vsc_m * (Y_vsc + 1.0j)

        # HVDC LINE MODEL ----------------------------------------------------------------------------------------------
        # does not apply since the HVDC-line model is the simplistic 2-generator model

        # SHUNT --------------------------------------------------------------------------------------------------------
        Yshunt_from_devices = self.C_bus_shunt * (self.shunt_admittance * self.shunt_active / self.Sbase)

        # form the admittance matrices ---------------------------------------------------------------------------------
        self.Yf = sp.diags(Yff) * Cf + sp.diags(Yft) * Ct
        self.Yt = sp.diags(Ytf) * Cf + sp.diags(Ytt) * Ct
        self.Ybus = sp.csc_matrix(Cf.T * self.Yf + Ct.T * self.Yt + sp.diags(Yshunt_from_devices))

        # form the admittance matrices of the series and shunt elements ------------------------------------------------
        Yfs = sp.diags(Yffs) * Cf + sp.diags(Yfts) * Ct
        Yts = sp.diags(Ytfs) * Cf + sp.diags(Ytts) * Ct
        self.Yseries = sp.csc_matrix(Cf.T * Yfs + Ct.T * Yts)

        self.Yshunt = Yshunt_from_devices + Cf.T * ysh_br + Ct.T * ysh_br

    def get_generator_injections(self):
        """
        Compute the active and reactive power of non-controlled generators (assuming all)
        :return:
        """
        pf2 = np.power(self.generator_pf, 2.0)
        pf_sign = (self.generator_pf + 1e-20) / np.abs(self.generator_pf + 1e-20)
        Q = pf_sign * self.generator_p * np.sqrt((1.0 - pf2) / (pf2 + 1e-20))
        return self.generator_p + 1.0j * Q

    def get_battery_injections(self):
        """
        Compute the active and reactive power of non-controlled batteries (assuming all)
        :return:
        """
        pf2 = np.power(self.battery_pf, 2.0)
        pf_sign = (self.battery_pf + 1e-20) / np.abs(self.battery_pf + 1e-20)
        Q = pf_sign * self.battery_p * np.sqrt((1.0 - pf2) / (pf2 + 1e-20))
        return self.battery_p + 1.0j * Q

    def compute_injections(self):
        """
        Compute the power
        :return: nothing, the results are stored in the class
        """
        self.Sbus = - self.C_bus_load * (self.load_s * self.load_active)  # MW

        # generators
        self.Sbus += self.C_bus_gen * (self.get_generator_injections() * self.generator_active)

        # battery
        self.Sbus += self.C_bus_batt * (self.get_battery_injections() * self.battery_active)

        # HVDC forced power
        if self.nhvdc:
            self.Sbus += self.hvdc_active * self.hvdc_Pset * self.C_hvdc_bus_f
            self.Sbus -= self.hvdc_active * self.hvdc_Pset * self.C_hvdc_bus_t

        self.Sbus /= self.Sbase

    def compute_reactive_power_limits(self):
        # generators
        self.Qmax_bus = self.C_bus_gen * (self.generator_qmax * self.generator_active)
        self.Qmin_bus = self.C_bus_gen * (self.generator_qmin * self.generator_active)

        if self.nbatt > 0:
            # batteries
            self.Qmax_bus += self.C_bus_batt * (self.battery_qmax * self.battery_active)
            self.Qmin_bus += self.C_bus_batt * (self.battery_qmin * self.battery_active)

        if self.nhvdc > 0:
            # hvdc from
            self.Qmax_bus += (self.hvdc_Qmax_f * self.hvdc_active) * self.C_hvdc_bus_f
            self.Qmin_bus += (self.hvdc_Qmin_f * self.hvdc_active) * self.C_hvdc_bus_f

            # hvdc to
            self.Qmax_bus += (self.hvdc_Qmax_t * self.hvdc_active) * self.C_hvdc_bus_t
            self.Qmin_bus += (self.hvdc_Qmin_t * self.hvdc_active) * self.C_hvdc_bus_t

    def consolidate(self):
        """
        Computes the parameters given the filled-in information
        :return:
        """
        self.compute_injections()

        self.vd, self.pq, self.pv, self.pqpv = compile_types(Sbus=self.Sbus, types=self.bus_types)

        self.compute_admittance_matrices()

        self.compute_reactive_power_limits()

    def get_structure(self, structure_type) -> pd.DataFrame:
        """
        Get a DataFrame with the input.

        Arguments:

            **structure_type** (str): 'Vbus', 'Sbus', 'Ibus', 'Ybus', 'Yshunt', 'Yseries' or 'Types'

        Returns:

            pandas DataFrame

        """

        if structure_type == 'Vbus':

            df = pd.DataFrame(data=self.Vbus, columns=['Voltage (p.u.)'], index=self.bus_names)

        elif structure_type == 'Sbus':
            df = pd.DataFrame(data=self.Sbus, columns=['Power (p.u.)'], index=self.bus_names)

        elif structure_type == 'Ibus':
            df = pd.DataFrame(data=self.Ibus, columns=['Current (p.u.)'], index=self.bus_names)

        elif structure_type == 'Ybus':
            df = pd.DataFrame(data=self.Ybus.toarray(), columns=self.bus_names, index=self.bus_names)

        elif structure_type == 'Yshunt':
            df = pd.DataFrame(data=self.Yshunt, columns=['Shunt admittance (p.u.)'], index=self.bus_names)

        elif structure_type == 'Yseries':
            df = pd.DataFrame(data=self.Yseries.toarray(), columns=self.bus_names, index=self.bus_names)

        elif structure_type == "B'":
            df = pd.DataFrame(data=self.B1.toarray(), columns=self.bus_names, index=self.bus_names)

        elif structure_type == "B''":
            df = pd.DataFrame(data=self.B2.toarray(), columns=self.bus_names, index=self.bus_names)

        elif structure_type == 'Types':
            df = pd.DataFrame(data=self.bus_types, columns=['Bus types'], index=self.bus_names)

        elif structure_type == 'Qmin':
            df = pd.DataFrame(data=self.Qmin_bus, columns=['Qmin'], index=self.bus_names)

        elif structure_type == 'Qmax':
            df = pd.DataFrame(data=self.Qmax_bus, columns=['Qmax'], index=self.bus_names)

        elif structure_type == 'Jacobian':

            J = Jacobian(self.Ybus, self.Vbus, self.Ibus, self.pq, self.pqpv)

            """
            J11 = dS_dVa[array([pvpq]).T, pvpq].real
            J12 = dS_dVm[array([pvpq]).T, pq].real
            J21 = dS_dVa[array([pq]).T, pvpq].imag
            J22 = dS_dVm[array([pq]).T, pq].imag
            """
            npq = len(self.pq)
            npv = len(self.pv)
            npqpv = npq + npv
            cols = ['dS/dVa'] * npqpv + ['dS/dVm'] * npq
            rows = cols
            df = pd.DataFrame(data=J.toarray(), columns=cols, index=rows)

        else:

            raise Exception('PF input: structure type not found')

        return df


def split_into_islands(numeric_circuit: SnapshotCircuit, ignore_single_node_islands=False) -> List[SnapshotIsland]:
    """
    Split circuit into islands
    :param numeric_circuit: NumericCircuit instance
    :param ignore_single_node_islands: ignore islands composed of only one bus
    :return: List[NumericCircuit]
    """

    # compute the adjacency matrix
    A = tp.get_adjacency_matrix(C_branch_bus_f=numeric_circuit.C_branch_bus_f,
                                C_branch_bus_t=numeric_circuit.C_branch_bus_t,
                                branch_active=numeric_circuit.branch_active,
                                bus_active=numeric_circuit.bus_active)

    # find the matching islands
    idx_islands = tp.find_islands(A)

    if len(idx_islands) == 1:
        island = numeric_circuit.to_island()  # convert the circuit to an island
        island.consolidate()  # compute the internal magnitudes
        return [island]

    else:

        circuit_islands = list()  # type: List[SnapshotIsland]

        for bus_idx in idx_islands:

            if ignore_single_node_islands:

                if len(bus_idx) > 1:
                    island = numeric_circuit.get_island(bus_idx)
                    island.consolidate()  # compute the internal magnitudes
                    circuit_islands.append(island)

            else:
                island = numeric_circuit.get_island(bus_idx)
                island.consolidate()  # compute the internal magnitudes
                circuit_islands.append(island)

        return circuit_islands


def compile_snapshot_circuit(circuit: MultiCircuit, apply_temperature=False,
                             branch_tolerance_mode=BranchImpedanceMode.Specified,
                             impedance_tolerance=0.0,
                             opf_results=None) -> SnapshotCircuit:
    """
    Compile the information of a circuit and generate the pertinent power flow islands
    :param circuit: Circuit instance
    :param apply_temperature:
    :param branch_tolerance_mode:
    :param impedance_tolerance:
    :return: list of NumericIslands
    """

    logger = Logger()

    bus_dictionary = dict()

    # Element count
    nbus = len(circuit.buses)
    nload = 0
    ngen = 0
    n_batt = 0
    nshunt = 0
    for bus in circuit.buses:
        nload += len(bus.loads)
        ngen += len(bus.controlled_generators)
        n_batt += len(bus.batteries)
        nshunt += len(bus.shunts)

    nline = len(circuit.lines)
    ntr2w = len(circuit.transformers2w)
    nvsc = len(circuit.vsc_converters)
    nhvdc = len(circuit.hvdc_lines)

    # declare the numerical circuit
    nc = SnapshotCircuit(nbus=nbus,
                         nline=nline,
                         ntr=ntr2w,
                         nvsc=nvsc,
                         nhvdc=nhvdc,
                         nload=nload,
                         ngen=ngen,
                         nbatt=n_batt,
                         nshunt=nshunt,
                         sbase=circuit.Sbase,
                         apply_temperature=apply_temperature,
                         impedance_tolerance=impedance_tolerance,
                         branch_tolerance_mode=branch_tolerance_mode
                         )

    # buses and it's connected elements (loads, generators, etc...)
    i_ld = 0
    i_gen = 0
    i_batt = 0
    i_sh = 0
    for i, bus in enumerate(circuit.buses):

        # bus parameters
        nc.bus_names[i] = bus.name
        nc.bus_active[i] = bus.active
        nc.bus_types[i] = bus.determine_bus_type().value

        # Add buses dictionary entry
        bus_dictionary[bus] = i

        for elm in bus.loads:
            nc.load_names[i_ld] = elm.name
            nc.load_active[i_ld] = elm.active
            nc.load_s[i_ld] = complex(elm.P, elm.Q)
            nc.C_bus_load[i, i_ld] = 1
            i_ld += 1

        for elm in bus.controlled_generators:
            nc.generator_names[i_gen] = elm.name
            nc.generator_pf[i_gen] = elm.Pf
            nc.generator_v[i_gen] = elm.Vset
            nc.generator_qmin[i_gen] = elm.Qmin
            nc.generator_qmax[i_gen] = elm.Qmax
            nc.generator_active[i_gen] = elm.active
            nc.generator_controllable[i_gen] = elm.is_controlled
            nc.generator_p[i_gen] = elm.P
            nc.generator_installed_p[i_gen] = elm.Snom

            nc.C_bus_gen[i, i_gen] = 1

            if nc.Vbus[i].real == 1.0:
                nc.Vbus[i] = complex(elm.Vset, 0)
            elif elm.Vset != nc.Vbus[i]:
                logger.append('Different set points at ' + bus.name + ': ' + str(elm.Vset) + ' !=' + str(nc.Vbus[i]))
            i_gen += 1

        for elm in bus.batteries:
            nc.battery_names[i_batt] = elm.name
            nc.battery_p[i_batt] = elm.P
            nc.battery_pf[i_batt] = elm.Pf
            nc.battery_v[i_batt] = elm.Vset
            nc.battery_qmin[i_batt] = elm.Qmin
            nc.battery_qmax[i_batt] = elm.Qmax
            nc.battery_active[i_batt] = elm.active
            nc.battery_controllable[i_batt] = elm.is_controlled
            nc.battery_installed_p[i_batt] = elm.Snom

            nc.C_bus_batt[i, i_batt] = 1
            nc.Vbus[i] *= elm.Vset
            i_batt += 1

        for elm in bus.shunts:
            nc.shunt_names[i_sh] = elm.name
            nc.shunt_active[i_sh] = elm.active
            nc.shunt_admittance[i_sh] = complex(elm.G, elm.B)

            nc.C_bus_shunt[i, i_sh] = 1
            i_sh += 1

    # Compile the lines
    for i, elm in enumerate(circuit.lines):
        # generic stuff
        nc.branch_names[i] = elm.name
        nc.branch_active[i] = elm.active
        nc.branch_rates[i] = elm.rate
        f = bus_dictionary[elm.bus_from]
        t = bus_dictionary[elm.bus_to]
        nc.C_branch_bus_f[i, f] = 1
        nc.C_branch_bus_t[i, t] = 1
        nc.F[i] = f
        nc.T[i] = t

        # impedance
        nc.line_names[i] = elm.name
        nc.line_R[i] = elm.R
        nc.line_X[i] = elm.X
        nc.line_B[i] = elm.B
        nc.line_impedance_tolerance[i] = elm.tolerance
        nc.C_line_bus[i, f] = 1
        nc.C_line_bus[i, t] = 1

        # Thermal correction
        nc.line_temp_base[i] = elm.temp_base
        nc.line_temp_oper[i] = elm.temp_oper
        nc.line_alpha[i] = elm.alpha

    # 2-winding transformers
    for i, elm in enumerate(circuit.transformers2w):
        ii = i + nline

        # generic stuff
        f = bus_dictionary[elm.bus_from]
        t = bus_dictionary[elm.bus_to]

        nc.branch_names[ii] = elm.name
        nc.branch_active[ii] = elm.active
        nc.branch_rates[ii] = elm.rate
        nc.C_branch_bus_f[ii, f] = 1
        nc.C_branch_bus_t[ii, t] = 1
        nc.F[ii] = f
        nc.T[ii] = t

        # impedance
        nc.tr_names[i] = elm.name
        nc.tr_R[i] = elm.R
        nc.tr_X[i] = elm.X
        nc.tr_G[i] = elm.G
        nc.tr_B[i] = elm.B

        nc.C_tr_bus[i, f] = 1
        nc.C_tr_bus[i, t] = 1

        # tap changer
        nc.tr_tap_mod[i] = elm.tap_module
        nc.tr_tap_ang[i] = elm.angle
        nc.tr_is_bus_to_regulated[i] = elm.bus_to_regulated
        nc.tr_tap_position[i] = elm.tap_changer.tap
        nc.tr_min_tap[i] = elm.tap_changer.min_tap
        nc.tr_max_tap[i] = elm.tap_changer.max_tap
        nc.tr_tap_inc_reg_up[i] = elm.tap_changer.inc_reg_up
        nc.tr_tap_inc_reg_down[i] = elm.tap_changer.inc_reg_down
        nc.tr_vset[i] = elm.vset

        # virtual taps for transformers where the connection voltage is off
        nc.tr_tap_f[i], nc.tr_tap_t[i] = elm.get_virtual_taps()

    # VSC
    for i, elm in enumerate(circuit.vsc_converters):
        ii = i + nline + ntr2w

        # generic stuff
        f = bus_dictionary[elm.bus_from]
        t = bus_dictionary[elm.bus_to]

        nc.branch_names[ii] = elm.name
        nc.branch_active[ii] = elm.active
        nc.branch_rates[ii] = elm.rate
        nc.C_branch_bus_f[ii, f] = 1
        nc.C_branch_bus_t[ii, t] = 1
        nc.F[ii] = f
        nc.T[ii] = t

        # vsc values
        nc.vsc_names[i] = elm.name
        nc.vsc_R1[i] = elm.R1
        nc.vsc_X1[i] = elm.X1
        nc.vsc_Gsw[i] = elm.Gsw
        nc.vsc_Beq[i] = elm.Beq
        nc.vsc_m[i] = elm.m
        nc.vsc_theta[i] = elm.theta

        nc.C_vsc_bus[i, f] = 1
        nc.C_vsc_bus[i, t] = 1

    # HVDC
    for i, elm in enumerate(circuit.hvdc_lines):
        ii = i + nline + ntr2w + nvsc

        # generic stuff
        f = bus_dictionary[elm.bus_from]
        t = bus_dictionary[elm.bus_to]

        # hvdc values
        nc.hvdc_names[i] = elm.name
        nc.hvdc_active[i] = elm.active
        nc.hvdc_rate[i] = elm.rate

        nc.hvdc_Pset[i] = elm.Pset
        nc.hvdc_Vset_f[i] = elm.Vset_f
        nc.hvdc_Vset_t[i] = elm.Vset_t
        nc.hvdc_Qmin_f[i] = elm.Qmin_f
        nc.hvdc_Qmax_f[i] = elm.Qmax_f
        nc.hvdc_Qmin_t[i] = elm.Qmin_t
        nc.hvdc_Qmax_t[i] = elm.Qmax_t

        # hack the bus types to believe they are PV
        nc.bus_types[f] = BusMode.PV.value
        nc.bus_types[t] = BusMode.PV.value

        # the the bus-hvdc line connectivity
        nc.C_hvdc_bus_f[i, f] = 1
        nc.C_hvdc_bus_t[i, t] = 1

    # consolidate the information
    nc.consolidate()

    return nc

