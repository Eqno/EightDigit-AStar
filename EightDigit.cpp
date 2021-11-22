#include <map>
#include <vector>
#include <utility>
#include <iostream>
#include <algorithm>
using namespace std;

int dx[] = {1, -1, 0, 0};
int dy[] = {0, 0, 1, -1};
class Mat
{
    private:
    int num[3][3];
    public:
    int val;
    Mat(int v)
    {
        val = v;
        for (int i=2; i>=0; i--)
            for (int j=2; j>=0; j--)
                num[i][j] = v%10, v /= 10;
    }
    bool operator ==(const Mat &a)
    const { return val == a.val; }
    int operator -(const Mat &a)
    const {
        int del = 0, vX = val, vY = a.val;
        for (int i=0; i<9; i++)
        {
            del += vX%10 != vY%10;
            vX /= 10, vY /= 10;
        }
        return del;
    }
    bool reachable(const Mat &a)
    const {
        int rX = 0, rY = 0;
        for (int i=0; i<9; i++)
            for (int j=0; j<i; j++)
            {
                rX += num[j/3][j%3] && num[j/3][j%3]<num[i/3][i%3];
                rY += a.num[j/3][j%3] && a.num[j/3][j%3]<a.num[i/3][i%3];
            }
        return (rX&1) == (rY&1);
    }
    pair <int, int> findZero()
    {
        for (int i=0; i<3; i++)
            for (int j=0; j<3; j++)
                if (num[i][j] == 0)
                    return make_pair(i, j);
        return make_pair(-1, -1);
    }
    void swapNum(int x1, int y1, int x2, int y2)
    {
        swap(num[x1][y1], num[x2][y2]);
        val = 0;
        for(int i=0; i<3; i++)
            for(int j=0; j<3; j++)
                val = val*10 + num[i][j];
    }
    void outputMat()
    {
        puts("-------");
        for (int i=0; i<3; i++)
        {
            putchar('|');
            for (int j=0; j<3; j++)
                printf("%d|", num[i][j]);
            putchar('\n');
        }
        puts("-------");
    }
};
struct State
{
    int s, g, h, t, p;
    bool operator <(const State &a) const { return s < a.s; }
    bool operator ==(const State &a) const { return s == a.s; }
    int getF() const { return g + h; };  // f->factor, g->step, h->diff(now, tar)
};

multimap <int, State> open;  // f->s，open表。
map <State, int> fact;  // s->f，逆open表。
map <int, bool> clos;  // 记录搜过的状态，closed表。
vector <State> path;  // 记录路径。
int search(const Mat &origin, const Mat &target)
{
    if (! origin.reachable(target)) return -1;
    int id = 0, H = target - origin;
    State start{origin.val, 0, H, id, id++};
    open.insert(make_pair(H, start));
    fact.insert(make_pair(start, H));
    while (open.size())
    {
        State p = open.begin()->second;
        open.erase(open.begin());
        fact.erase(fact.lower_bound(p));
        path.push_back(p);
        clos[p.s] = true;
        Mat mat(p.s);
        if (mat == target) return p.g;
        pair <int, int> zero = mat.findZero();
        int x = zero.first, y = zero.second;
        for (int i=0; i<4; i++)
        {
            int nx = x+dx[i], ny = y+dy[i];
            if (nx>=0 && nx<3 && ny>=0 && ny<3)
            {
                Mat newMat = mat;
                newMat.swapNum(x, y, nx, ny);
                State n{newMat.val, p.g+1, target-newMat, id++, p.t};
                if (clos.find(newMat.val) == clos.end())
                {
                    auto j = fact.lower_bound(n);
                    auto t = j->first;
                    if (j!=fact.end() && t==n && t.getF()>n.getF())
                    {
                        auto k=open.lower_bound(t.getF());
                        for (; k!=open.upper_bound(t.getF()); k++)
                            if (k->second == n) break;
                        open.erase(k);
                        fact.erase(j);
                        open.insert(make_pair(n.getF(), n));
                        fact.insert(make_pair(n, n.getF()));
                    }
                    else
                    {
                        open.insert(make_pair(n.getF(), n));
                        fact.insert(make_pair(n, n.getF()));
                    }
                }
            }
        }
    }
    return -1;
}
void restorePath(int p, int len, int step)
{
	if (step <= 0)
    {
        puts("\n初始状态：");
		Mat(path[len].s).outputMat();
		return;
	}
	for (int i=len; i>=0; i--)
		if (path[i].t == p)
		    restorePath(path[i].p, i, step-1);
	printf("第%d步操作：\n", step);
	Mat(path[len].s).outputMat();
}
int main()
{
    int origin = 0, target = 0;
    puts("请输入初始状态：");
    for (int i=0; i<3; i++)
        for (int j=0; j<3; j++)
        {
            int num;
            cin >> num;
            origin = origin*10 + num;
        }
    puts("请输入目标状态：");
    for (int i=0; i<3; i++)
        for (int j=0; j<3; j++)
        {
            int num;
            cin >> num;
            target = target*10 + num;
        }
    int step = search(Mat(origin), Mat(target));
    if (step != -1)
    {
        restorePath((path.end()-1)->p, path.size()-1, step);
        puts("已达到目标状态。\n");
    }
    else cout << "无解！" << endl;
    return 0;
}