# Compare the number of iterations it takes for a player to guess the seceret as the threshold changes.
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


tracker=np.zeros(12)
for p in range(1,13):
    # Parameters
    q = 1000 # Field size
    act = False # Activation check
    N = 100 # Population size
    Ns = [i for i in range(N)]
    t, m = 10*p, 120 # Threshold values
    ms = [i for i in range(m)]
    reps = {}
    minLambda, maxLambda = 1, 20 # Range of vertex values
    w1, w2, w3 = 0.2, 0.2, 0.5 # Reward and punishment values
    densities = [0.1]
    avgNum1, numberKnow, numRuns = [], np.zeros(5), np.zeros(5)

    # Generate graphs
    lambdai = [random.randint(minLambda, maxLambda) for i in range(N)]
    shares1 = {}
    G1= nx.Graph()
    G1.add_nodes_from([(i, {"lambda": lambdai[i]}) for i in range(N)])
    for i in range(N):
        shares1[i] = random.sample(ms, lambdai[i])
        for j in range(i+1, N):
            if random.random()<densities[0]: G1.add_edge(i, j)
    
    # Distribute shares
    touse = [i for i in range(m)]
    for i in range(N):
        for j in range(len(shares1[i])):
            if shares1[i][j] in touse: touse.remove(shares1[i][j])
    for i in range(len(touse)): shares1[random.choice(Ns)].append(touse[i])
    sensknown = np.zeros(N)
    ps = random.sample(ms, 20)
    for i in range(N):
        for j in range(len(ps)):
            if ps[j] in shares1[i] :
                shares1[i].remove(ps[j])
                sensknown[i]+=1

    if not nx.is_connected(G1):
        components = list(nx.connected_components(G1))
        for j in range(len(components)-1):
            node1, node2 = next(iter(components[j])), next(iter(components[j+1]))
            G1.add_edge(node1, node2)

    # Model
    played, act = {}, False
    for i in range(N): played[i] = []
    for i in range(N): reps[i] = 0
    while act==False:
        numRuns[0] += 1
        tracker[p-1]+=1
        reps = {k: v for k, v in sorted(reps.items(), key=lambda item: item[1])}
        for i in reps:
            if len(shares1[i])+sensknown[i]  >= t:
                numberKnow[0]+=1
                for j in range(N):
                    if j!=i and random.random()<1/q: numberKnow[0]+=1 
                act = True
            else:
                c = [val for val in shares1[i] if val not in played[i]]
                if len(c)>0:
                    tosend = random.choice(c)
                    played[i].append(tosend)
                    reps[i] += w1
                    for j in G1[i]:
                        if tosend not in shares1[j]:
                            shares1[j].append(tosend)
                            reps[j]+=w2
                else:
                    for j in range(N):
                        if random.random()<1/q: numberKnow[0]+=1 
                        act = True
        avgNum1.append(np.mean([len(shares1[i])+sensknown[i]  for i in range(N)]))

# Graph
# Plot number of runs against number of people
plt.scatter([10+10*i for i in range(len(tracker))], tracker, color='purple')
plt.xlabel('Threshold')
plt.ylabel('Number of Iterations')
plt.title('Threshold vs Number of Iterations to Learn the Secret')
plt.show()
