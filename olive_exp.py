from pyomo.environ import * 

model = AbstractModel()

model.C = Set()

# Initialize the Points with the cartesian product of the countries we have.
model.P = Set(within = model.C*model.C)

# Spain is the starting point
model.origin = Param(within = model.C)


model.maximum = Param(model.P)

model.needs = Param(model.C)

model.flow = Var(model.P, within=Binary)



# Objective Function

def objective_rule(model):

    obj_val = sum(model.flow[origin,dest] for origin,dest in model.P if dest =='Ireland' or dest =='Poland' or dest == 'Italy' or dest =='Switzerland')

    return obj_val

model.obj = Objective(rule = objective_rule, sense = minimize)


def allowed_quantity(model, m, n):
    return model.flow[m, n] <= model.maximum[m, n]

def flow_rule(model, k):
    if k in ["Italy", "Switzerland", "Ireland", "Poland", value(model.origin)]:
        return Constraint.Skip

    # The inflow and outflow are binary variables, so you don't need to sum them
    inflow = sum(model.flow[origin, dest] for (origin, dest) in model.P if dest == k)
    outflow = sum(model.flow[origin, dest] for (origin, dest) in model.P if origin == k)

    return inflow == outflow

def requested_oil(model, i):
    if i in ["Italy", "Switzerland", "Ireland", "Poland"]:
        # Requested oil constraint for binary variables
        return sum(model.flow[j, k] for (j, k) in model.P if k == i) >= model.needs[i]
    else:
        return Constraint.Skip


model.flow_rule = Constraint(model.C, rule = flow_rule)
model.allowed_quantity = Constraint(model.P, rule = allowed_quantity)
model.requested_oil = Constraint(model.C, rule = requested_oil)
