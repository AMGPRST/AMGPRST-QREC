import math

from numpy import load
from spotify.Requester import Requester
from util.qmath import find_k_largest


class Predictor(object):
    def __init__(self, model):
        self.requester = Requester()

        data = load(model, allow_pickle=True)['arr_0']
        self.U = data[0]
        self.V = data[1]
        self.user_name2user_index = data[2]
        self.item_name2item_index = data[3]
        self.user_index2user_name = data[4]
        self.item_index2item_name = data[5]

        self.n2i = {}
        for key in self.user_name2user_index:
            self.n2i[key] = self.user_name2user_index[key]
        for key in self.item_name2item_index:
            self.n2i[key] = self.item_name2item_index[key]

        self.i2n = {}
        for key in self.user_index2user_name:
            self.i2n[key] = self.user_index2user_name[key]
        for key in self.item_index2item_name:
            self.i2n[key] = self.item_index2item_name[key]

    def id_by_name(self, q):
        return self.requester.id_by_track(q[0], q[1])

    def name_by_id(self, i):
        return self.requester.track_by_id(i)

    def index_by_id(self, i):
        return self.n2i[i]

    def id_by_index(self, u):
        return self.i2n[u]

    def rating_by_name(self, q1, q2):
        return self.rating_by_id(self.id_by_name(q1), self.id_by_name(q2))

    def rating_by_id(self, i1, i2):
        return self.rating_by_index(self.index_by_id(i1), self.index_by_id(i2))

    def rating_by_index(self, u1, u2):
        return self.V[u2].dot(self.U[u1])

    def ranking_by_name(self, q):
        return self.ranking_by_id(self.id_by_name(q))

    def ranking_by_id(self, i):
        return self.ranking_by_index(self.index_by_id(i))

    def ranking_by_index(self, u):
        return self.V.dot(self.U[u])

    def top_k_ranking_by_name(self, q, k):
        r = {}
        rs = self.ranking_by_name(q)
        for i, v in enumerate(rs):
            r[self.id_by_index(i)] = v
        t = []
        ks = find_k_largest(k, r)
        for i, v in enumerate(ks):
            t.append(v[0])
        return t

    def top_k_matching_by_name(self, q1, q2, k):
        s1 = {}
        s2 = {}
        t1 = self.top_k_ranking_by_name(q1, k**3)
        t2 = self.top_k_ranking_by_name(q2, k**3)
        i1 = self.id_by_name(q1)
        i2 = self.id_by_name(q2)
        for t in t1:
            s1[t] = self.rating_by_id(t, i1)
        for t in t2:
            s2[t] = self.rating_by_id(t, i2)
        t = []
        for i, v in enumerate(find_k_largest(math.ceil(k/2), s1)):
            t.append(v[0])
        for i, v in enumerate(find_k_largest(math.floor(k/2), s2)):
            t.append(v[0])
        for i in t:
            print(i, self.name_by_id(i))


file = '../results/LightGCN@2021-10-12 19-01-40-model.npz'
predictor = Predictor(file)

song1 = ('Smells Like Teen Spirit', 'Nirvana')
song2 = ('Toxic', 'Britney Spears')

print('Generate playlist for blend between', song1, 'and', song2)
predictor.top_k_matching_by_name(song1, song2, 15)
