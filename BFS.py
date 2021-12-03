import copy

def getTuple(mat):
    return tuple(tuple(i) for i in mat)

def getValidOpt(mat):
    res = []
    for i, s in enumerate(mat):
        for j, t in enumerate(s):
            if t == 0:
                if i > 0:
                    res.append(1)
                if i < len(mat)-1:
                    res.append(2)
                if j > 0:
                    res.append(3)
                if j < len(s)-1:
                    res.append(4)
    return res

def moveState(state, opt):
    mat = state[0]
    pat = state[1]
    for i, s in enumerate(mat):
        for j, t in enumerate(s):
            if t == 0:
                res = copy.deepcopy(mat)
                nxt = copy.deepcopy(pat)
                if opt == 1:
                    res[i][j], res[i-1][j] = res[i-1][j], res[i][j]
                    nxt.append(1)
                if opt == 2:
                    res[i][j], res[i+1][j] = res[i+1][j], res[i][j]
                    nxt.append(2)
                if opt == 3:
                    res[i][j], res[i][j-1] = res[i][j-1], res[i][j]
                    nxt.append(3)
                if opt == 4:
                    res[i][j], res[i][j+1] = res[i][j+1], res[i][j]
                    nxt.append(4)
                return [res, nxt]
    return []

def search(origin, target):
    step = 0
    start = [origin, []]
    vis = set()
    st = []
    st.append(start)
    lastlen = 0
    while len(st):
        state = st[0]
        st.pop(0)
        mat = state[0]
        pat = state[1]
        vis.add(getTuple(mat))
        if len(pat) > lastlen:
            step += 1
        lastlen = len(pat)
        if mat == target:
            ans = [(pat, len(vis))]
            while len(st):
                tmp = st[0]
                st.pop(0)
                vis.add(getTuple(tmp[0]))
                if tmp[0] == target:
                    ans.append((tmp[1], len(vis)))
            return True, ans
        opt = getValidOpt(mat)
        if len(opt) == 0:
            return
        flag = False
        for i in opt:
            newState = moveState(state, i)
            tmp = getTuple(newState[0])
            if tmp not in vis:
                st.append(newState)
                flag = True
        if not flag:
            return False, [([], len(vis))]

def moveMat(mat, opt):
    for i, s in enumerate(mat):
        for j, t in enumerate(s):
            if t == 0:
                res = copy.deepcopy(mat)
                tar = ()
                if opt == 1:
                    res[i][j], res[i-1][j] = res[i-1][j], res[i][j]
                    tar = (i, j+1)
                if opt == 2:
                    res[i][j], res[i+1][j] = res[i+1][j], res[i][j]
                    tar = (i+2, j+1)
                if opt == 3:
                    res[i][j], res[i][j-1] = res[i][j-1], res[i][j]
                    tar = (i+1, j)
                if opt == 4:
                    res[i][j], res[i][j+1] = res[i][j+1], res[i][j]
                    tar = (i+1, j+2)
                return res, (i+1, j+1), tar
    return [], (), ()

def printMat(mat):
    print("-------------")
    for i in mat:
        for j in i:
            print("| %d " % j, end='')
        print("|")
    print("-------------")

origin = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
target = [[1, 0, 3], [4, 2, 5], [7, 8, 6]]
# target = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]

reachable, ans = search(origin, target)
print("\n最优解有%d个。" % (len(ans) if len(ans[0][0]) else 0))
if reachable:
    for tmp in ans:
        path = tmp[0]
        step = tmp[1]
        print("初始状态：")
        printMat(origin)
        for i, opt in enumerate(path):
            origin, a, b = moveMat(origin, opt)
            print("第%d步操作，交换(%d, %d)与(%d, %d)。" % (i+1, a[0], a[1], b[0], b[1]))
            printMat(origin)
        print("已达成目标状态。")
        print("搜过%d步可能的步数。\n" % (step-1))
else:
    step = ans[0][1]
    print("无解！")
    print("搜过%d步可能的步数。\n" % (step-1))