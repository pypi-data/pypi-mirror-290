# Copyright (C) 2024 Collimator, Inc.
# SPDX-License-Identifier: AGPL-3.0-only
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, version 3. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General
# Public License for more details.  You should have received a copy of the GNU
# Affero General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

from dataclasses import dataclass
import sympy as sp
from enum import Enum
from .base import Sym, SymKind


"""
Fluid media specification classes.
based on the media modeling concepts in:
https://modelica.org/events/Conference2003/papers/h40_Elmqvist_fluid.pdf
"""

# "Base properties (p, d, T, h, u, R_s, MM and, if applicable, X and Xi) of a medium"
# SpecificHeatCapacity R_s "Gas constant (of mixture if applicable)";
# MolarMass MM "Molar mass (of mixture or single fluid)";

# 1] p = rho*R_s*T, ideal gas law in specific form
# 2] h = u + p/rho , specific enthalpy of uniform system, where u=specific internal energy, p=pressure, and rho=density.
# 3] u = Cv*T, specific in ternal energy

# find T = f(p,h):
# solve 1] for T. a] T = p/(rho*R_s)
# solve 2 for rho and substitute into a: rho = p/(h-u), T = p/(p*R_s/(h-u)) ..hmm, going in circles maybe.


class IdealGasAir:
    """
    class for air with only gaseous phase.
    https://www.engineeringtoolbox.com/air-properties-d_156.html
    """

    def __init__(
        self,
        ev,
        name="IdealGasAir_ph",
        P_ic=101325.0,
        T_ic=273.0,
    ):
        self.name = name

        # constants
        self.cp = Sym(
            ev,
            name=self.name + "_cp",
            kind=SymKind.param,
            val=1006.0,  # J/(kg*K)
        )
        self.cv = Sym(
            ev,
            name=self.name + "_cv",
            kind=SymKind.param,
            val=0.7171,  # FIXME: wrong value
        )
        self.Rs_air = Sym(
            ev,
            name=self.name + "_Rs_air",
            kind=SymKind.param,
            val=287.052874,
        )
        self.Tref = Sym(
            ev,
            name=self.name + "_Tref",
            kind=SymKind.param,
            val=0.0,
        )
        self.href = Sym(
            ev,
            name=self.name + "_href",
            kind=SymKind.param,
            val=274648.7,
        )

        self.syms = [
            self.cp,
            self.cv,
            self.Rs_air,
            self.Tref,
            self.href,
        ]

        # HACK: this is super hacky for now. I made this because we need some values
        # to initialize fluid BaseProp variables such that they dont get the default
        # weak_ic of 0.0. for exmaple, for density, a weak_ic of 0.0 results in div-by-zero
        # in the IC solving process.
        h_ic, u_ic, d_ic = self.get_h_u_d_ics(P_ic, T_ic)
        self.init = {"p": P_ic, "T": T_ic, "h": h_ic, "u": u_ic, "d": d_ic}

    def gen_eqs(self, p, h, T, u, d):
        eqs = [
            sp.Eq(p.s, d.s * self.Rs_air.s * T.s),
            sp.Eq(h.s, self.href.s + self.cp.s * T.s),
            sp.Eq(u.s, h.s - p.s / d.s),
        ]
        return eqs

    def get_T_u_d_ics(self, p, h):
        T = (h - self.href.val) / self.cp.val
        d = p / (self.Rs_air.val * T)
        u = h - p / d

        return T, u, d

    def get_h_u_d_ics(self, p, T):
        h = T * self.cp.val + self.href.val
        d = p / (self.Rs_air.val * T)
        u = h - p / d

        return h, u, d


class Water_ph:
    """
    class for water with only liquid phase, using pressure and enthalpy as the
    state variables. the following variables are computed, using functions:
        T (temperature K) = Tref + H/cp
        ...
        etc.
    """

    def __init__(self, ev, name="Water_ph"):
        self.name = name

        # constants
        self.cp = Sym(
            ev,
            name=self.name + "_cp",
            kind=SymKind.param,
            val=4.16,  # kJ/(kg*K)
        )
        self.Tref = Sym(
            ev,
            name=self.name + "_Tref",
            kind=SymKind.param,
            val=0.0,
        )
        self.href = Sym(
            ev,
            name=self.name + "_href",
            kind=SymKind.param,
            val=0.0,
        )
        self.density = Sym(
            ev,
            name=self.name + "_density",
            kind=SymKind.param,
            val=1000.0,
        )

        self.syms = [
            self.cp,
            self.Tref,
            self.href,
            self.density,
        ]

    def fT(self, p, h):
        return self.Tref + h / self.cp.s

    def fu(self, p, h):
        return h - p / self.density.s

    def fd(self, p, h):
        return self.density.s

    # unused
    def h_pT(self, p, T):
        return self.href.s + self.cp.s * (T - self.Tref.s)


class FluidName(Enum):
    """Enumeration class for the names of fluids for which property sets are
    provided.
    """

    water = 0
    hydraulic_fluid = 1


@dataclass
class Water:
    name = "water"
    density = 1000  # kg/m**3
    viscosity_dyn = 0.89e3  # Pa*s
    viscosity_kin = viscosity_dyn / density  # m^2/s


@dataclass
class HydraulicFluid:
    name = "hydraulic_fluid"
    density = 950  # kg/m**3
    viscosity_kin = 40e-6  # m^2/s
    viscosity_dyn = viscosity_kin * density  # Pa*s


class Fluid:
    """Class for holding the symbols for fluid properties."""

    def __init__(self, fluid="water"):
        if fluid == FluidName.water:
            fp = Water()
        elif fluid == FluidName.hydraulic_fluid:
            fp = HydraulicFluid()
        else:
            raise ValueError(
                f"Fluid class, {fluid} is incorrect input for arg 'fluid'."
            )

        self.density = Sym(
            None,  # eqn_env is not needed
            name=fp.name + "_density",
            kind=SymKind.param,
            val=fp.density,
        )
        self.viscosity_kin = Sym(
            None,  # eqn_env is not needed
            name=fp.name + "_viscosity",
            kind=SymKind.param,
            val=fp.viscosity_kin,
        )
        self.viscosity_dyn = Sym(
            None,  # eqn_env is not needed
            name=fp.name + "_viscosity",
            kind=SymKind.param,
            val=fp.viscosity_dyn,
        )
        self.syms = [self.density, self.viscosity_kin, self.viscosity_dyn]
