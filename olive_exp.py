from pyomo.environ import * 

model = AbstractModel()

model.C = Set()

# Initialize the Points with the cartesian product of the countries we have.
model.P = Set(within = model.C*model.C)

# Spain is the starting point
model.origin = Param(within = model.C)


model.maximum = Param(model.P, mutable=True)

model.needs = Param(model.C, mutable=True)

model.flow = Var(model.P, within = NonNegativeReals)


# Objective Function

def objective_rule(model):

    obj_val = sum(model.flow[origin,dest] for origin,dest in model.T if dest =='Ireland' or dest =='Poland' or dest == 'Italy' or dest =='Switzerland')

    return obj_val

model.obj = Objective(rule = objective_rule, sense = maximize)


def allowed_quantity(model, m, n):
    return model.flow[m, n] <= model.maximum[m, n]

def flow_rule(model , k):
    # if it is a final destination - dont flow out . If it is a 
    if k =='Ireland' or k =='Poland' or k == 'Italy' or k =='Switzerland' or k ==value(model.origin):
        return Constraint.Skip
    
    # the inflow from one origin to a destination MUST equal the outflow from origin to destination.
    # calculating the inflow
    inflow = sum(model.flow[origin,dest] for (origin,dest) in model.P if dest==k)
    # calculating the outflow.
    outflow = sum(model.flow[origin,dest] for (origin,dest) in model.P if origin==k)

    return inflow==outflow

def requested_oil(model, i):
    if i== "Italy" or i== "Switzerland" or i== "Ireland" or i== "Poland":
        return sum(model.flow[j, k] for (j,k) in model.P if k==i)>=model.needs[i]
    else:
        return Constraint.Skip


model.flow_rule = Constraint(model.C, rule = flow_rule)
model.allowed_quantity = Constraint(model.P, rule = allowed_quantity)
model.requesedt_oil = Constraint(model.C, rule = requested_oil)
    
