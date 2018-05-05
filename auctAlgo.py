import random
import time

agents = {}
prices = {}
unassigned = []
values_matrix = []
averages = []

def findUnmatchedAgent():
    for key, value in agents.items():
        if value is None:
            return key

def executeAuction(N, M):

    sequence = []
    for i in range(0, int(M)):
        sequence.append(i)

    for i in range(0, int(N)):
        sublist = []
        for k in range(0, int(N)):
            val = random.choice(sequence)
            sublist.append(val)
        values_matrix.append(sublist)

    for p in range(0, int(N)):
        agents[p] = None
        prices[p] = 0

    while (None in agents.values()):

        unassigned_agent = findUnmatchedAgent()
        agents_row = values_matrix[unassigned_agent]

        max_diff = 0
        max_obj = 0
        for j in range(0, int(N)):
            value = agents_row[j] - prices[j]
            if value > max_diff:
                max_diff = value
                max_obj = j

        next_max_diff = 0
        for l in range(0, int(N)):
            value = agents_row[l] - prices[l]
            if value > next_max_diff and value < max_diff:
                next_max_diff = value

        bid_increment = max_diff - next_max_diff
        agents[unassigned_agent] = max_obj

        for key, value in agents.items():
            if value is max_obj and key is not unassigned_agent:
                agents[k] = None
                unassigned.append(key)

        prices[max_obj] += bid_increment

def calculateAssignmentValue(matrix, assignment = {}):
    totalValue = 0
    for key, value in assignment.items():
        totalValue += values_matrix[key][value]
    return totalValue

def calculateAvgSolveTime():
    s = 0;
    for time in averages:
        s += time
    avgSolveTime = s / len(averages)
    return avgSolveTime

if __name__ == '__main__':
    for i in range(100):
        start = time.process_time()
        executeAuction(256, 10)
        end = time.process_time() - start
        averages.append(end)
        print(agents)
    print("Overall Avg. Solve Time " + str(calculateAssignmentValue(values_matrix, agents)))

