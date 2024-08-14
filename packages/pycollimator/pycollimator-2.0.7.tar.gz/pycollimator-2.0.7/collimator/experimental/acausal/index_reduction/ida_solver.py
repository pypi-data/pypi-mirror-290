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

import numpy as np
import sympy as sp
from collimator.backend import numpy_api as cnp
from collimator.experimental.acausal.index_reduction import IndexReduction


class IDASolver:
    """
    Solve an 'Acausal system without any causal inputs' with IDA solver.
    The semi-explicit system is converted into an explicit form for IDA.
    ```
    s = [x, y]^T
    F(t, s, sdot) = 0
    ```
    """

    def __init__(
        self,
        ir: IndexReduction,
        compute_ydot0: bool = False,  # False for index-1 semi-explicit systems
        leaf_backend: str = "jax",
    ):
        self.ir = ir
        self.compute_ydot0 = compute_ydot0
        self.leaf_backend = leaf_backend

        self.n_ode = len(self.ir.se_x)
        self.n_alg = len(self.ir.se_y)

        self.knowns_symbols, self.knowns_vals = zip(*ir.knowns.items())

    def compute_initial_conditions(self):
        """
        Compute initial conditions for s(t=0)=s0 and sdot(t=0)=sdot0, where s=[x, y]^T.
        """
        self.ir.compute_initial_conditions()
        self.se_x_ic = [
            self.ir.X_ic_mapping[self.ir.dae_X_to_X_mapping[var]]
            for var in self.ir.se_x
        ]
        self.se_x_dot_ic = [
            self.ir.X_ic_mapping[self.ir.dae_X_to_X_mapping[var]]
            for var in self.ir.se_x_dot
        ]
        self.se_y_ic = [
            self.ir.X_ic_mapping[self.ir.dae_X_to_X_mapping[var]]
            for var in self.ir.se_y
        ]

        s0 = self.se_x_ic + self.se_y_ic
        if self.compute_ydot0:
            ydot0 = self.get_ydot0(self.se_x_ic, self.se_y_ic)
        else:
            ydot0 = [0.0] * len(self.se_y_ic)
        sdot0 = self.se_x_dot_ic + list(ydot0)
        return s0, sdot0

    def get_ydot0(self, x0, y0):
        """
        Compute ydot0. This doesn't need to be called for semi-explicit index-1 systems
        as the solution won't be affected by the choice of ydot0.
        Needs modification for higher index (>1) systems.
        """
        args = (self.ir.t, self.ir.se_x, self.ir.se_y, self.knowns_symbols)

        self.gy = sp.Matrix(self.ir.se_alg_eqs).jacobian(self.ir.se_y)
        self.gx = sp.Matrix(self.ir.se_alg_eqs).jacobian(self.ir.se_x)

        gy = sp.lambdify(
            args,
            self.gy,
            modules=[self.leaf_backend, {"cnp": cnp}],
        )
        gx = sp.lambdify(
            args,
            self.gx,
            modules=[self.leaf_backend, {"cnp": cnp}],
        )

        ydot0 = np.linalg.solve(
            gy(0.0, x0, y0, self.knowns_vals),
            -gx(0.0, x0, y0, self.knowns_vals) @ np.array(self.se_x_ic),
        )
        return ydot0

    def create_residual_and_jacobian(self):
        """
        For the system `F(t, s, sdot) = 0`, create functions for the the residual `F`
        and its jacobian w.r.t `s` and `sdot` for the IDA solver.
        """
        self.s = self.ir.se_x + self.ir.se_y
        self.sdot = self.ir.se_x_dot + [
            sp.Derivative(y, self.ir.t) for y in self.ir.se_y
        ]

        self.F = [
            xdot - fx for xdot, fx in zip(self.ir.se_x_dot, self.ir.se_x_dot_rhs)
        ] + self.ir.se_alg_eqs

        self.dF_ds = sp.Matrix(self.F).jacobian(self.s)
        self.dF_dsdot = sp.Matrix(self.F).jacobian(self.sdot)

        self.lambda_args = (self.ir.t, self.s, self.sdot, self.knowns_symbols)

        F = sp.lambdify(
            self.lambda_args,
            self.F,
            modules=[self.leaf_backend, {"cnp": cnp}],
        )

        dF_ds = sp.lambdify(
            self.lambda_args,
            self.dF_ds,
            modules=[self.leaf_backend, {"cnp": cnp}],
        )

        dF_dsdot = sp.lambdify(
            self.lambda_args,
            self.dF_dsdot,
            modules=[self.leaf_backend, {"cnp": cnp}],
        )

        return F, dF_ds, dF_dsdot

    def solve(
        self,
        sim_time: float = 1.0,
        dt: float = 0.1,
        rtol: float = 1e-6,
        atol: float = 1e-8,
        first_step_size: float = 1e-18,
        max_steps: int = 500,
    ):
        from scikits.odes import dae

        s0, sdot0 = self.compute_initial_conditions()
        F, dF_ds, dF_dsdot = self.create_residual_and_jacobian()

        def dae_residual(t, s, sdot, result):
            result[:] = F(t, s, sdot, self.knowns_vals)
            return 0

        def dae_jacobian(t, s, sdot, residual, cj, result):
            result[:, :] = dF_ds(t, s, sdot, self.knowns_vals) + cj * dF_dsdot(
                t, s, sdot, self.knowns_vals
            )
            return 0

        solver = dae(
            "ida",
            dae_residual,
            jacfn=dae_jacobian,
            first_step_size=first_step_size,
            rtol=rtol,
            atol=atol,
            algebraic_vars_idx=list(range(self.n_ode, self.n_ode + self.n_alg)),
            exclude_algvar_from_error=False,
            max_steps=max_steps,
            old_api=False,
        )

        time = 0.0
        solver.init_step(time, s0, sdot0)

        t_sol = [time]
        s_sol = [s0]
        while True:
            time += dt
            solution = solver.step(time)
            if solution.errors.t:
                print(f"Error: {solution.message} at time {solution.errors.t}")
                break
            t_sol.append(solution.values.t)
            s_sol.append(solution.values.y)
            if time >= sim_time:
                break

        return cnp.array(t_sol), cnp.array(s_sol)
