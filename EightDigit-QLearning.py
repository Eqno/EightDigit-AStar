import numpy
import random
import copy

def getValidOpt(state): # ↑ : 1, ↓ : 2, ← : 3, → : 4
    operation = []
    for i, p in enumerate(state):
        for j, q in enumerate(p):
            if q == 0:
                if i > 0:
                    operation.append(1)
                if i < len(state)-1:
                    operation.append(2)
                if j > 0:
                    operation.append(3)
                if j < len(p)-1:
                    operation.append(4)
                return operation
    return operation

def getTuple(state):
    return tuple(tuple(i) for i in state)

def move(state, opt):
    res = copy.deepcopy(state)
    for i, p in enumerate(res):
        for j, q in enumerate(p):
            if q == 0:
                if opt == 1:
                    res[i][j], res[i-1][j] = res[i-1][j], res[i][j]
                if opt == 2:
                    res[i][j], res[i+1][j] = res[i+1][j], res[i][j]
                if opt == 3:
                    res[i][j], res[i][j-1] = res[i][j-1], res[i][j]
                if opt == 4:
                    res[i][j], res[i][j+1] = res[i][j+1], res[i][j]
                return res
    return res

def epsilonGreedy(Q, state, epsilon):
    operation = getValidOpt(state)
    if numpy.random.uniform() < epsilon:
        randed = set()
        while True:
            rand = random.randint(0, len(operation)-1)
            opt = operation[rand]
            if (getTuple(state), opt) not in Q:
                return opt
            randed.add(rand)
            if len(randed) == len(operation):
                return opt
    else:
        Qs = numpy.array([Q.get((getTuple(state), i), 0) for i in operation])
        return operation[numpy.argmin(Qs)]

# repTime->重复次数, learnRate->学习率, decayFactor->衰减系数, origin->初始状态, target->目标状态
def trainQ(repTime, learnRate, decayFactor, origin, target):
    epsilon = 1.0
    stepNum = []
    Q = {}
    for _ in range(repTime):
        epsilon *= decayFactor
        step = 0
        lastState = []
        lastOpt = ()
        state = copy.deepcopy(origin)
        while True:
            step += 1
            opt = epsilonGreedy(Q, state, epsilon)
            newState = move(state, opt)
            if (getTuple(state), opt) not in Q:
                Q[(getTuple(state), opt)] = 0
            if newState == target:
                Q[(getTuple(state), opt)] = 1
                stepNum.append(step)
                break
            else:
                if step > 1:
                    Q[(getTuple(lastState), lastOpt)] += learnRate \
                        * (1 + Q[(getTuple(state), opt)] - Q[(getTuple(lastState), lastOpt)])
                lastState = copy.deepcopy(state)
                lastOpt = copy.deepcopy(opt)
                state = copy.deepcopy(newState)
    return Q, stepNum

def testQ(Q, maxStep, origin, target):
    state = origin
    path = [[state, 0]]
    step = 0
    while True:
        step += 1
        Qs = []
        operation = getValidOpt(state)
        for i in operation:
            Qs.append(Q.get((getTuple(state), i), 0xffffff))
        opt = operation[numpy.argmin(Qs)]
        newState = move(state, opt)
        path.append([newState, opt])
        if newState == target:
            return path
        elif step >= maxStep:
            print("%d步内无法达到目标状态。" % maxStep)
            return []
        state = copy.deepcopy(newState)

def getMinStep(repTime, step, minstep):
    delstep = 0
    step = list(step)
    while delstep != repTime:
        if numpy.mean(step) > 7:
            step.pop(0)
            delstep += 1
        else:
            if delstep < minstep:
                return delstep, True
            else:
                return minstep, False
    if delstep < minstep:
        return delstep, True
    else:
        return minstep, False

def findFactor(repTime, learnRate, decayFactor, origin, target):
    bestRate = 0.5
    bestFactor = 0.7
    _, step = trainQ(repTime, bestRate, bestFactor, origin, target)
    minstep, _ = getMinStep(50, step, 0xffffff)
    best = []
    for _ in range(10):
        for i in learnRate:
            for j in decayFactor:
                _, step = trainQ(repTime, i, j, origin, target)
                newMinstep, B = getMinStep(repTime, step, minstep)
                if B:
                    bestRate = i
                    bestFactor = j
                    minstep = copy.deepcopy(newMinstep)
        best.append([bestRate, bestFactor])
    return best

def printPath(path):
    print("共需要%d步。" % (len(path)-1))
    if not len(path):
        return
    print("\n初始状态：\n")
    for i in path:
        print(i)
    print("\n已达到目标状态。")

origin = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
target = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

Q, stepNum = trainQ(50, 0.5, 0.8, origin, target)
path = testQ(Q, 100, origin, target)
print(stepNum)
printPath(path)

# learnRate = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
# decayFactor = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
# best = findFactor(100, learnRate, decayFactor, origin, target)
# print(best)