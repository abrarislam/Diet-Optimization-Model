# The diet problem is one of the first large-scale optimization problems to be studied in practice.
# Back in the 1930’s and 40’s, the Army wanted to meet the nutritional requirements of its soldiers
#  while minimizing the cost.) In this homework you get to solve a diet problem with real data.

# 1. The following is an optimization model (a linear program) to find the cheapest diet that satisfies the maximum and minimum daily
#    nutrition constraints, and is solved using PuLP.  (The optimal solution should be a diet of air-popped popcorn,
#    poached eggs, oranges, raw iceberg lettuce, raw celery, and frozen broccoli. UGH!)

# Import pulp and pandas
from pulp import *
import pandas as pd

# Read in data
foodData = pd.read_excel("data 15.2/diet.xls")
print(foodData.head())

# All food is stored in rows 1-65
foodData = foodData[0:64]

# Convert data frame into a list
foodData = foodData.values.tolist()

# Store food names from column A of spreadsheet
foods = [x[0] for x in foodData]

# Create a dictionary for the costs of the foods
cost   = dict([(x[0], float(x[1])) for x in foodData])
cals   = dict([(x[0], float(x[3])) for x in foodData])
chol   = dict([(x[0], float(x[4])) for x in foodData])
fat    = dict([(x[0], float(x[5])) for x in foodData])
sodium = dict([(x[0], float(x[6])) for x in foodData])
carbs  = dict([(x[0], float(x[7])) for x in foodData])
fiber  = dict([(x[0], float(x[8])) for x in foodData])
prot   = dict([(x[0], float(x[9])) for x in foodData])
vitA   = dict([(x[0], float(x[10])) for x in foodData])
vitC   = dict([(x[0], float(x[11])) for x in foodData])
calc   = dict([(x[0], float(x[12])) for x in foodData])
iron   = dict([(x[0], float(x[13])) for x in foodData])

# Define optimization problem by naming & specifying max or min
problem = LpProblem("DietProblem", LpMinimize)

# Define primary variables (amount food in each diet)
# and give the amounts a natural lower bound of 0
amountVars = LpVariable.dicts("Amounts", foods, 0)

# Add objective function (inner product of cost & amountVars vectors)
problem += lpSum([cost[i] * amountVars[i] for i in foods]), 'total cost'

# Hard code all min/max constraints
problem += lpSum([cals[i] * amountVars[i] for i in foods]) >= 1500, 'min cals'
problem += lpSum([cals[i] * amountVars[i] for i in foods]) <= 2500, 'max cals'

problem += lpSum([chol[i] * amountVars[i] for i in foods]) >= 30, 'min chol'
problem += lpSum([chol[i] * amountVars[i] for i in foods]) <= 240, 'max chol'

problem += lpSum([fat[i] * amountVars[i] for i in foods]) >= 20, 'min fat'
problem += lpSum([fat[i] * amountVars[i] for i in foods]) <= 70, 'max fat'

problem += lpSum([sodium[i] * amountVars[i] for i in foods]) >= 800, 'min sodium'
problem += lpSum([sodium[i] * amountVars[i] for i in foods]) <= 2000, 'max sodium'

problem += lpSum([carbs[i] * amountVars[i] for i in foods]) >= 130, 'min carbs'
problem += lpSum([carbs[i] * amountVars[i] for i in foods]) <= 450, 'max carbs'

problem += lpSum([fiber[i] * amountVars[i] for i in foods]) >= 125, 'min fiber'
problem += lpSum([fiber[i] * amountVars[i] for i in foods]) <= 250, 'max fiber'

problem += lpSum([prot[i] * amountVars[i] for i in foods]) >= 60, 'min prot'
problem += lpSum([prot[i] * amountVars[i] for i in foods]) <= 100, 'max prot'

problem += lpSum([vitA[i] * amountVars[i] for i in foods]) >= 1000, 'min vitA'
problem += lpSum([vitA[i] * amountVars[i] for i in foods]) <= 10000, 'max vitA'

problem += lpSum([vitC[i] * amountVars[i] for i in foods]) >= 400, 'min vitC'
problem += lpSum([vitC[i] * amountVars[i] for i in foods]) <= 5000, 'max vitC'

problem += lpSum([calc[i] * amountVars[i] for i in foods]) >= 700, 'min calc'
problem += lpSum([calc[i] * amountVars[i] for i in foods]) <= 1500, 'max calc'

problem += lpSum([iron[i] * amountVars[i] for i in foods]) >= 10, 'min iron'
problem += lpSum([iron[i] * amountVars[i] for i in foods]) <= 40, 'max iron'

# Function to solve the LP
problem.solve()

# Print status
print("Status", LpStatus[problem.status])

# Print out amount values from optimal solution
for v in problem.variables():
    print(v.name, "=", v.varValue)

# Print optimized objective function value
print("\nTotal cost per person: ", value(problem.objective))


# 2. Adding to the model the following constraints (which might require adding more variables):
#    a. If a food is selected, then a minimum of 1/10 serving must be chosen. 
#       (This will require two variables for each food i: whether it is chosen, and how much is part of the diet. 
#       May need to write a constraint to link them.)
#    b. Many people dislike celery and frozen broccoli. So at most one, but not both, can be selected.
#    c. To get day-to-day variety in protein, at least 3 kinds of meat/poultry/fish/eggs must be selected. [If something is
#       ambiguous (e.g., should bean-and-bacon soup be considered meat?), just call it whatever you think is appropriate]

# Create binary variable
selectVars = pulp.LpVariable.dicts("Select", foods, cat = pulp.LpBinary)

# 2a - add constraints
for i in foods:
    problem += amountVars[i] <= 1000 * selectVars[i], ""

for i in foods:
    problem += amountVars[i] >= 0.1 * selectVars[i], ""

# 2b - add constraints
problem += selectVars["Frozen Broccoli"] + selectVars["Celery, Raw"] <= 1, ""

# 2c - add constraints
problem += (selectVars['Roasted Chicken']
            + selectVars['Poached Eggs']  
            + selectVars['Scrambled Eggs']
            + selectVars['Bologna,Turkey'] 
            + selectVars['Frankfurter, Beef']
            + selectVars['Ham,Sliced,Extralean']
            + selectVars['Kielbasa,Prk']
            + selectVars['Pizza W/Pepperoni']
            + selectVars['Hamburger W/Toppings']
            + selectVars['Hotdog, Plain']
            + selectVars['Pork']
            + selectVars['Sardines in Oil']            
            + selectVars['White Tuna in Water']
            ) >=3, ""

# Function to solve the LP
problem.solve()

# Print status
print("Status", LpStatus[problem.status])

# Print out amount values from optimal solution
for v in problem.variables():
    print(v.name, "=", v.varValue)

# Print optimized objective function value
print("\nTotal cost per person: ", value(problem.objective))