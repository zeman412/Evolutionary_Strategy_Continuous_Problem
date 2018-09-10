import numpy as np
import random
sigma = 0.05
alpha = 0.82
mu = 100
l_mu = 6
lamda = l_mu*mu
len_soln = 4
num_gen = 1000
np.random.seed(999)
range_x = [-5, 10]
range_y = [0, 15]

def fitness_score(population):
    x = population[0]
    y = population[1]
    return ((y - (5.1 * x ** 2) / (4 * np.pi ** 2) + ((5 * x / np.pi) - 6)) ** 2 + 10 * np.cos(x) * (1 - 1 / (8 * np.pi)) + 10)

new_parent = np.zeros((mu, len_soln), dtype=np.float64)
new_children = np.zeros((lamda, len_soln))

def compute_succes_rate():
    global sigma, alpha, success_count
    # compute success rate of children
    for i in range(lamda):
        for j in range(mu):
            if fitness_score(new_children[i, :]) > fitness_score(new_parent[j, :]):
                success_count = success_count + 1
                break
    # print("success count:", success_count)
    succes_rate = success_count / lamda
    # print("success rate:", succes_rate)
    if succes_rate > 0.2:
        sigma = sigma + 1/alpha
    elif succes_rate < 0.2:
        sigma = sigma * alpha

def select_fittest(parnt, childrn):
    global new_parent
    combind = np.concatenate((parnt, childrn))
    fitness = np.zeros((len(combind)))  # holds the fitness of the combined parent and children
    for i in range(len(combind)):
        fitness[i] = fitness_score(combind[i, :])  # store the fitness of the combined parent and children
    # print (fitness)
    fittest = np.argsort(fitness)  # sorted index based on the fitness value (ascending)
    # print(fitness)
    combind = combind[fittest]  # holds the sorted fitness based on the index
    # print(combined)
    new_parent = combind[:mu, :]  # slice the top from combined and replace the parents
    # print("selected", new_parent)
    #return new_parent

def globl_interm_recomb(parent, indx1, indx2, indx3):
    # take X1 & X2 from parent1, sigmal 1 from parent 2, sigma2 from parent 3
    x = parent[indx1][0]
    y = parent[indx1][1]
    sigma1 = (parent[indx2][2] + parent[indx1][2])/2
    sigma2 = (parent[indx3][3] + parent[indx1][2])/2
    x = x + sigma1 * np.random.normal(0, 1)
    y = y + sigma1 * np.random.normal(0, 1)
    parent4 = [x, y, sigma1, sigma2]
    return  parent4

def dual_discrt_recomb(parent, indx1, indx2):

    # For elements if rondom number is less than 0.5 take from parent1 else from parent 2, return

    if (random.random() < 0.5):
        x = parent[indx1][0]
    else:
        x = parent[indx2][0]

    if (random.random() < 0.5):
        y = parent[indx1][0]
    else:
        y = parent[indx2][0]

    if (random.random() < 0.5):
        sigma1 = parent[indx1][2]
    else:
        sigma1 = parent[indx2][2]
    if (random.random() < 0.5):
        sigma2 = parent[indx1][3]
    else:
        sigma2 = parent[indx2][3]

    parent3 = [x, y, sigma1, sigma2]

    return  parent3

def create_parent():
    for i in range (mu):
        new_parent[i][0] = np.random.uniform(-5, 10, size=None)
        new_parent [i][1]= np.random.uniform(0, 15, size=None)
        new_parent [i][2] = sigma * np.random.normal(0, 1)
        new_parent[i][3] = sigma * np.random.normal(0, 1)
        #new_parent [idx] =  new_parent [i]
        #print(new_parent)

temp_child = np.zeros((l_mu, len_soln)) # six children container for each parent

def create_children_recomb(parent):
    global idx
    for j in range (l_mu):
        idx = idx + 1
        temp_child[j][0] = parent[0] + sigma * np.random.normal(0, 1)
        temp_child[j][1] = parent[1] + sigma * np.random.normal(0, 1)
        temp_child[j][2] = parent[2]
        temp_child[j][3] = parent[3]

        temp_child[j][0] = np.clip(temp_child[j][0], *range_x)
        temp_child[j][1] = np.clip(temp_child[j][1], *range_y)

        new_children[idx] = temp_child[j]

#for i in range (mu):
def create_children(parent, i):
    global idx
    for j in range (l_mu):
        idx = idx + 1
        temp_child[j][0] = new_parent[i,0] + sigma * np.random.normal(0, 1)
        temp_child[j][1] =  new_parent[i][1] + sigma * np.random.normal(0, 1)
        #temp_child[j][2] = new_parent[i][2]

        temp_child[j][0] = np.clip(temp_child[j][0], *range_x)
        temp_child[j][1] = np.clip(temp_child[j][1], *range_y)

        new_children[idx] = temp_child[j]

def run_ES():   # The main ES function
    global idx, success_count
    create_parent()
    #print("random", new_parent)
    for g in range (num_gen):
        success_count = 0
        idx = -1
        # create children by randomly selecting population
        for index in range(mu):
            # recombination
            #1. Call the global intermidiete ====================================
            index1 = np.random.randint(low=0, high=mu)
            index2 = np.random.randint(low=0, high=mu)
            index3 = np.random.randint(low=0, high=mu)
            parent = globl_interm_recomb(new_parent, index1, index2, index3)
            #create_children_recomb(parent)

            # 2. Call the dual discrete ==========================================
            indx1 = np.random.randint(low=0, high=mu)
            indx2 = np.random.randint(low=0, high=mu)
            parent = dual_discrt_recomb(new_parent, indx1, indx2)
            create_children_recomb(parent)

            # Mutation
            index = np.random.randint(low=0, high=mu) # randomly select population
            #create_children(new_parent, index)

        select_fittest(new_parent, new_children)
        #compute_succes_rate() # compute 1/5 rule
        #print("Number of success", success_count)
        print("best soln at Generaion", g, "is :", fitness_score(new_parent[0, :]))
        print("best parent", new_parent[0, :])
        #print("Sigma=========", sigma)
if __name__== "__main__":  # calling the main function, where the program starts running
    run_ES()
