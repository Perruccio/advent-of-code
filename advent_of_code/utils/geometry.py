def get_neighbours(pos, ends, exclude_diag=False):
    """return the position of the neighbours of pos in a 2d matrix"""
    shifts = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if not exclude_diag:
        shifts += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for di, dj in shifts:
        i2, j2 = pos[0] + di, pos[1] + dj
        if 0 <= i2 < ends[0] and 0 <= j2 < ends[1]:
            yield i2, j2


def expand1d(v, xx):
    """
    In-place expand vector of non-intersecting sorted ranges v with
    another range xx.
    Example expand1d([(0, 1), (5, 7), (10, 12)], (6, 11)) -> [(0, 1), (5, 12)]
    """
    intersections_i = []
    for i in range(len(v)):
        if intersect1d(v[i], xx) is not None:
            intersections_i.append(i)
    if not intersections_i:
        new_i = len(v)
        for i in range(len(v)):
            if xx[0] < v[i][0]:
                new_i = i
                break
        
        v.insert(new_i, xx)
        return
    new = min(xx[0], v[intersections_i[0]][0]), max(xx[1], v[intersections_i[-1]][1])
    del v[intersections_i[0] : intersections_i[-1] + 1]
    v.insert(intersections_i[0], new)


def intersect1d(aa, bb):
    if aa is None or bb is None:
        return None
    l = max(aa[0], bb[0])
    r = min(aa[1], bb[1])
    return (l, r) if l <= r else None


class Cuboid:
    def __init__(self, xx, yy, zz):
        assert xx[0] <= xx[1] and yy[0] <= yy[1] and zz[0] <= zz[1]
        self.xx = xx
        self.yy = yy
        self.zz = zz

    def is_small(self, l=50):
        return all(-l <= tt[0] and tt[1] <= l for tt in [self.xx, self.yy, self.zz])

    def volume(self):
        return (
            (self.xx[1] - self.xx[0] + 1)
            * (self.yy[1] - self.yy[0] + 1)
            * (self.zz[1] - self.zz[0] + 1)
        )

    def intersect(self, other):
        xx = intersect1d(self.xx, other.xx)
        yy = intersect1d(self.yy, other.yy)
        zz = intersect1d(self.zz, other.zz)
        if any([t is None for t in [xx, yy, zz]]):
            return None
        return Cuboid(xx, yy, zz)


if __name__ == "__main__":
    v = [(1,2), ]
    expand1d(v, (3,5))
    print(v)
