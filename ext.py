class Page:
    def __init__(self, page_size=2) -> None:
        self.page_size = page_size
        self.map = []
        self.local_depth = 0

    def full(self) -> bool:
        return len(self.map) >= self.page_size

    def put(self, k, v) -> None:
        for i, (key, value) in enumerate(self.map):
            if key == k:
                del self.map[i]
                break
        self.map.append((k, v))

    def get(self, k):
        for key, value in self.map:
            if key == k:
                return value

    def get_local_high_bit(self):
        return 1 << self.local_depth

    def __repr__(self) -> str:
        return f"local_depth: {self.local_depth}\t {self.map}"


class ExtendibleHashing:
    def __init__(self, page_size=2) -> None:
        self.global_depth = 0
        self.directory = [Page(page_size)]

    def get_page(self, k):
        h = hash(k)
        return self.directory[h & ((1 << self.global_depth) - 1)]

    def put(self, k, v) -> None:
        p = self.get_page(k)
        full = p.full()
        p.put(k, v)
        if full:
            if p.local_depth == self.global_depth:
                self.directory *= 2
                self.global_depth += 1

            p0 = Page()
            p1 = Page()
            p0.local_depth = p1.local_depth = p.local_depth + 1
            high_bit = p.get_local_high_bit()
            for k2, v2 in p.map:
                h = hash(k2)
                new_p = p1 if h & high_bit else p0
                new_p.put(k2, v2)

            for i in range(hash(k) & (high_bit - 1), len(self.directory), high_bit):
                self.directory[i] = p1 if i & high_bit else p0

    def get(self, k):
        return self.get_page(k).get(k)

    def __repr__(self):
        s = f"global depth: {self.global_depth}\n"
        for i, page in enumerate(self.directory):
            s += f"\tid: {i} {page}\n"
        return s

        

