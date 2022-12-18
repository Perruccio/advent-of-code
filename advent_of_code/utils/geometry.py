def get_neighbours(pos, ends, exclude_diag=False):
    """return the position of the neighbours of pos in a 2d matrix"""
    shifts = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if not exclude_diag:
        shifts += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for di, dj in shifts:
        i2, j2 = pos[0] + di, pos[1] + dj
        if 0 <= i2 < ends[0] and 0 <= j2 < ends[1]:
            yield i2, j2


def merge_intervals(v: list[int]):
    """
    Return sorted list of lists where overlapping intervals are merged.
    Example expand1d([(0, 1), (5, 7), (10, 12)], (6, 11)) -> [[0, 1], [5, 12]]
    """
    # sort alphabetically
    v.sort()

    merged = []
    for lo, hi in v:
        # nothing to merge
        if not merged:
            merged.append([lo, hi])
            continue

        last_lo, last_hi = merged[-1]

        # intervals not intersecting (and not touching). merge touching integer intervals like
        # (1, 2), (2, 3) -> [1, 3] even if not intersecting
        if lo > last_hi + 1:
            merged.append([lo, hi])
            continue

        # intervals are intersecting, just compute upper bound
        merged[-1][1] = max(hi, last_hi)
    return merged


def manhattan_distance(a, b):
    return sum(abs(ca - cb) for ca, cb in zip(a, b))


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
    pass
