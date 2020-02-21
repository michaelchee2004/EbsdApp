from pyomo.environ import *

class OptiModel():
    
    def __init__(self, i_op, i_t, p_capital, p_opcost, p_capacity, p_demand):
        self.run_status = 0

        self.m = ConcreteModel()
        self.m.i_op = Set(initialize=i_op)
        self.m.i_t = Set(initialize=i_t)
        self.m.p_capital = Param(self.m.i_op, self.m.i_t, initialize=p_capital)
        self.m.p_opcost = Param(self.m.i_op, self.m.i_t, initialize=p_opcost)
        self.m.p_capacity = Param(self.m.i_op, initialize=p_capacity)
        self.m.p_demand = Param(self.m.i_t, initialize=p_demand)

        self.m.v_B = Var(self.m.i_op, self.m.i_t, within=Binary)
        self.m.v_CAPEX = Var(self.m.i_op, self.m.i_t, domain=NonNegativeReals)
        self.m.v_VOPEX = Var(self.m.i_op, self.m.i_t, domain=NonNegativeReals)
        self.m.v_F = Var(self.m.i_op, self.m.i_t, domain=NonNegativeReals)

        self.m.obj = Objective(expr=
            sum(sum(self.m.v_CAPEX[op, t] for op in self.m.i_op) for t in self.m.i_t)
            + sum(sum(self.m.v_VOPEX[op, t] for op in self.m.i_op) for t in self.m.i_t)
        )

        self.m.c_sum_b_is_zero = ConstraintList()
        for op in self.m.i_op:
            self.m.c_sum_b_is_zero.add(
                sum(self.m.v_B[op, t] for t in self.m.i_t) <= 1.0
            )

        self.m.c_SDB = ConstraintList()
        for t in self.m.i_t:
            self.m.c_SDB.add(
                sum(self.m.v_F[op, t] for op in self.m.i_op) >= self.m.p_demand[t]
            )

        self.m.c_capex = ConstraintList()
        for op in self.m.i_op:
            for t in self.m.i_t:
                self.m.c_capex.add(
                    self.m.v_CAPEX[op, t] == self.m.p_capital[op, t] * self.m.v_B[op, t]
                )

        self.m.c_vopex = ConstraintList()
        for op in self.m.i_op:
            for t in self.m.i_t:
                self.m.c_vopex.add(
                    self.m.v_VOPEX[op, t] == self.m.p_opcost[op, t] * self.m.v_F[op, t]
                )

        self.m.c_capacity = ConstraintList()
        for op in self.m.i_op:
            for t in self.m.i_t:
                self.m.c_capacity.add(
                    self.m.v_F[op, t] <= self.m.p_capacity[op] * sum(self.m.v_B[op, t2] for t2 in self.m.i_t if value(t2) <= t)
                )

        solverpath = 'C:\\w64\\glpsol'
        self.solver = SolverFactory('glpk', executable=solverpath)

    def run_model(self):
        run = self.solver.solve(self.m, tee=True)
        self.run_status = 1

    def write_results(self):
        if self.run_status == 1:
            output_dict = {}
            for op in self.m.i_op:
                for t in self.m.i_t:
                    output_dict[(op, t)] = self.m.v_F[op, t].value
        return output_dict



