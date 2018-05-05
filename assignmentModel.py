from ortools.linear_solver import pywraplp
import random

avg_across_diff_n = {}
averages = []
solver_times = []

def main(n, M):

    # Creating our mixed integer problem solver
    solver = pywraplp.Solver('SolveAssignmentProblemMIP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    possible_vals = []
    for i in range(0, int(M)):
        possible_vals.append(i)

    # create our value matrix, randomly assigning values from the sequence above
    value = []
    for j in range(0, int(n)):
        sublist = []
        for k in range(0, int(n)):
            val = random.choice(possible_vals)
            sublist.append(val)
        value.append(sublist)

    num_agents = len(value)
    num_objects = len(value[0])
    x = {}

    # insert decision variables into dictionary
    for i in range(num_agents):
        for j in range(num_objects):
            x[i,j] = solver.BoolVar('x[%i, %i]' % (i,j))

    # obj. function: we try to maximize value of the pairings
    solver.Maximize(solver.Sum([value[i][j] * x[i,j] for i in range(num_agents) for j in range(num_objects)]))

    # each agent is assigned to exactly one object
    for i in range(num_agents):
        solver.Add(solver.Sum([x[i, j] for j in range(num_objects)]) == 1)

    # each object is assigned to exactly one agent
    for j in range(num_objects):
        solver.Add(solver.Sum([x[i, j] for i in range(num_agents)]) == 1)

    solver.Solve()
    print('Total Value = ', solver.Objective().Value())
    print()

    value_sum = 0
    for i in range(num_agents):
        for j in range(num_objects):
            if x[i, j].solution_value() > 0:
                value_sum += value[i][j]
                print('Agent %d assigned to object %d. Value = %d' % (
                    i,
                    j,
                    value[i][j]
                ))

    average = value_sum / int(n)
    averages.append(average)
    print("Per-Agent Avg. Value of Assignments = " + str(average))
    print()
    print("Time = ", solver.WallTime(), " milliseconds")
    solver_times.append(solver.WallTime())
if __name__ == '__main__':
    M = 100
    for i in range(0, 100):
        n = 16
        print("Run: " + str(i))
        main(n, M)
        avg_across_diff_n[n] = averages
    s = 0
    c = 0
    for key in avg_across_diff_n:
        for val in avg_across_diff_n[key]:
            s += val
            c += 1
        average = s / c
        print("Per-Agent Avg. Assignment Value: " + str(average))

    su = 0
    tt = 0
    for time in solver_times:
        su += time
        tt += 1
    time_avg = su / tt
    print("Avg. Time for Solver to Solve Instance: " + str(time_avg))