# Compares the proportion of runs that end in an accurate guess of the secret rather than a guess because a player has no new shares to send.
# Compares across graph densities.
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy

tracker = np.zeros((5,2)) # each graph and [number success, number fail]

for runs in range(1000):

    # Parameters
    q = 1000 # Field size
    act = False # Activation check
    N = 100 # Population size
    Ns = [i for i in range(N)]
    t, m = 100, 150 # Threshold values
    ms = [i for i in range(m)]
    reps = {}
    minLambda, maxLambda = 1, 20 # Range of vertex values
    w1, w2, w3 = 0.2, 0.2, 0.5 # Reward and punishment values
    densities = [0.05, 0.1, 0.25, 0.75, 0.95]
    avgNum1, avgNum2, avgNum3, avgNum4, avgNum5, numberKnow, numRuns = [], [], [], [], [], np.zeros(5), np.zeros(5)

    # Generate graphs
    lambdai = [random.randint(minLambda, maxLambda) for i in range(N)]
    shares1, shares2, shares3, shares4, shares5 = {}, {}, {}, {}, {}
    G1, G2, G3, G4, G5 = nx.Graph(), nx.Graph(), nx.Graph(), nx.Graph(), nx.Graph()
    G1.add_nodes_from([(i, {"lambda": lambdai[i]}) for i in range(N)])
    G2.add_nodes_from([(i, {"lambda": lambdai[i]}) for i in range(N)])
    G3.add_nodes_from([(i, {"lambda": lambdai[i]}) for i in range(N)])
    G4.add_nodes_from([(i, {"lambda": lambdai[i]}) for i in range(N)])
    G5.add_nodes_from([(i, {"lambda": lambdai[i]}) for i in range(N)])
    for i in range(N):
        shares1[i] = random.sample(ms, lambdai[i])
        for j in range(i+1, N):
            if random.random()<densities[0]: G1.add_edge(i, j)
            if random.random()<densities[1]: G2.add_edge(i, j)
            if random.random()<densities[2]: G3.add_edge(i, j)
            if random.random()<densities[3]: G4.add_edge(i, j)
            if random.random()<densities[4]: G5.add_edge(i, j)

    #Distribute shares
    touse = [i for i in range(m)]
    for i in range(N):
        for j in range(len(shares1[i])):
            if shares1[i][j] in touse: touse.remove(shares1[i][j])
    for i in range(len(touse)): shares1[random.choice(Ns)].append(touse[i])
    sensknown = np.zeros(N)
    ps = random.sample(ms, 0)
    for i in range(N):
        for j in range(len(ps)):
            if ps[j] in shares1[i] :
                shares1[i].remove(ps[j])
                sensknown[i]+=1
    shares2, shares3, shares4, shares5 = deepcopy(shares1), deepcopy(shares1), deepcopy(shares1), deepcopy(shares1)

    if not nx.is_connected(G1):
        components = list(nx.connected_components(G1))
        for j in range(len(components)-1):
            node1, node2 = next(iter(components[j])), next(iter(components[j+1]))
            G1.add_edge(node1, node2)
    if not nx.is_connected(G2):
        components = list(nx.connected_components(G2))
        for j in range(len(components)-1):
            node1, node2 = next(iter(components[j])), next(iter(components[j+1]))
            G2.add_edge(node1, node2)
    if not nx.is_connected(G3):
        components = list(nx.connected_components(G3))
        for j in range(len(components)-1):
            node1, node2 = next(iter(components[j])), next(iter(components[j+1]))
            G3.add_edge(node1, node2)
    if not nx.is_connected(G4):
        components = list(nx.connected_components(G4))
        for j in range(len(components)-1):
            node1, node2 = next(iter(components[j])), next(iter(components[j+1]))
            G4.add_edge(node1, node2)
    if not nx.is_connected(G5):
        components = list(nx.connected_components(G5))
        for j in range(len(components)-1):
            node1, node2 = next(iter(components[j])), next(iter(components[j+1]))
            G5.add_edge(node1, node2)


    # Model
    # 1
    played, act = {}, False
    for i in range(N): played[i] = []
    for i in range(N): reps[i] = 0
    while act==False:
        numRuns[0] += 1
        reps = {k: v for k, v in sorted(reps.items(), key=lambda item: item[1])}
        for i in reps:
            if len(shares1[i])+sensknown[i] >= t:
                numberKnow[0]+=1
                for j in range(N):
                    if j!=i and random.random()<1/q: numberKnow[0]+=1  
                if act==False: tracker[0][0] += 1
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
                        if act==False: tracker[0][1] += 1
                        act = True
        avgNum1.append(np.mean([len(shares1[i])+sensknown[i] for i in range(N)]))

    # 2
    played, act = {}, False
    for i in range(N): played[i] = []
    for i in range(N): reps[i] = 0
    while act==False:
        numRuns[1] += 1
        reps = {k: v for k, v in sorted(reps.items(), key=lambda item: item[1])}
        for i in reps:
            if len(shares2[i])+sensknown[i] >= t:
                numberKnow[1]+=1
                for j in range(N):
                    if j!=i and random.random()<1/q: numberKnow[1]+=1  
                if act==False: tracker[1][0] += 1
                act = True
            else:
                c = [val for val in shares2[i] if val not in played[i]]
                if len(c)>0:
                    tosend = random.choice(c)
                    played[i].append(tosend)
                    reps[i] += w1
                    for j in G2[i]:
                        if tosend not in shares2[j]:
                            shares2[j].append(tosend)
                            reps[j]+=w2
                else:
                    for j in range(N):
                        if random.random()<1/q: numberKnow[1]+=1  
                        if act==False: tracker[1][1] += 1
                        act = True
        avgNum2.append(np.mean([len(shares2[i])+sensknown[i] for i in range(N)]))

    # 3
    played, act = {}, False
    for i in range(N): played[i] = []
    for i in range(N): reps[i] = 0
    while act==False:
        numRuns[2] += 1
        reps = {k: v for k, v in sorted(reps.items(), key=lambda item: item[1])}
        for i in reps:
            if len(shares3[i])+sensknown[i] >= t:
                numberKnow[2]+=1
                for j in range(N):
                    if j!=i and random.random()<1/q: numberKnow[2]+=1  
                if act==False: tracker[2][0] += 1
                act = True
            else:
                c = [val for val in shares3[i] if val not in played[i]]
                if len(c)>0:
                    tosend = random.choice(c)
                    played[i].append(tosend)
                    reps[i] += w1
                    for j in G3[i]:
                        if tosend not in shares3[j]:
                            shares3[j].append(tosend)
                            reps[j]+=w2
                else:
                    for j in range(N):
                        if random.random()<1/q: numberKnow[2]+=1  
                        if act==False: tracker[2][1] += 1
                        act = True
        avgNum3.append(np.mean([len(shares3[i])+sensknown[i] for i in range(N)]))

    # 4
    played, act = {}, False
    for i in range(N): played[i] = []
    for i in range(N): reps[i] = 0
    while act==False:
        numRuns[3] += 1
        reps = {k: v for k, v in sorted(reps.items(), key=lambda item: item[1])}
        for i in reps:
            if len(shares4[i])+sensknown[i] >= t:
                numberKnow[3]+=1
                for j in range(N):
                    if j!=i and random.random()<1/q: numberKnow[3]+=1  
                if act==False: tracker[3][0] += 1
                act = True
            else:
                c = [val for val in shares4[i] if val not in played[i]]
                if len(c)>0:
                    tosend = random.choice(c)
                    played[i].append(tosend)
                    reps[i] += w1
                    for j in G4[i]:
                        if tosend not in shares4[j]:
                            shares4[j].append(tosend)
                            reps[j]+=w2
                else:
                    for j in range(N):
                        if random.random()<1/q: numberKnow[3]+=1  
                        if act==False: tracker[3][1] += 1
                        act = True
        avgNum4.append(np.mean([len(shares4[i])+sensknown[i] for i in range(N)]))

    # 5
    played, act = {}, False
    for i in range(N): played[i] = []
    for i in range(N): reps[i] = 0
    while act==False:
        numRuns[4] += 1
        reps = {k: v for k, v in sorted(reps.items(), key=lambda item: item[1])}
        for i in reps:
            if len(shares5[i])+sensknown[i] >= t:
                numberKnow[4]+=1
                for j in range(N):
                    if j!=i and random.random()<1/q: numberKnow[4]+=1  
                if act==False: tracker[4][0] += 1
                act = True
            else:
                c = [val for val in shares5[i] if val not in played[i]]
                if len(c)>0:
                    tosend = random.choice(c)
                    played[i].append(tosend)
                    reps[i] += w1
                    for j in G5[i]:
                        if tosend not in shares5[j]:
                            shares5[j].append(tosend)
                            reps[j]+=w2
                else:
                    for j in range(N):
                        if random.random()<1/q: numberKnow[4]+=1  
                        if act==False: tracker[4][1] += 1
                        act = True
        avgNum5.append(np.mean([len(shares5[i])+sensknown[i] for i in range(N)]))

# Graph
# Bar plot of number of times each fails against density
print(tracker)
pt1, pt2 = np.array(tracker)[:,0], np.array(tracker)[:,1]
x = [r'$\rho_G$='+str(densities[0]), r'$\rho_G$='+str(densities[1]), r'$\rho_G$='+str(densities[2]), r'$\rho_G$='+str(densities[3]), r'$\rho_G$='+str(densities[4])]
plt.bar(x, pt1, color='purple')
plt.bar(x, pt2, bottom=pt1, color='lightgreen')
plt.legend(['Secret learned', 'Aborted'], loc=3)
plt.xlabel('Density')
plt.ylabel('Number of Rounds')
plt.title('Round Outcome by Graph Generated Density')
plt.show()