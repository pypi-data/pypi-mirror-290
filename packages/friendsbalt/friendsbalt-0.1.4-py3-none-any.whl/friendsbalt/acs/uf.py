class QuickFind:
    def __init__(self, N):
        self.id = list(range(N))

    def connected(self, p, q):
        return self.id[p] == self.id[q]

    def union(self, p, q):
        pid = self.id[p]
        qid = self.id[q]
        for i in range(len(self.id)):
            if self.id[i] == pid:
                self.id[i] = qid

class QuickUnion:
    def __init__(self, N):
        self.id = list(range(N))

    def root(self, i):
        while i != self.id[i]:
            i = self.id[i]
        return i

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)
        self.id[i] = j

class WeightedQuickUnion:
    def __init__(self, N):
        self.id = list(range(N))
        self.sz = [1] * N

    def root(self, i):
        while i != self.id[i]:
            self.id[i] = self.id[self.id[i]]  # path compression
            i = self.id[i]
        return i

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)
        if i == j:
            return

        if self.sz[i] < self.sz[j]:
            self.id[i] = j
            self.sz[j] += self.sz[i]
        else:
            self.id[j] = i
            self.sz[i] += self.sz[j]