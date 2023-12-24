from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
from dataclasses import dataclass, field
from collections import defaultdict, deque
from math import lcm
from copy import deepcopy


@dataclass
class Message:
    sender: str
    user: str
    signal: int


@dataclass
class Module:
    name: str
    links: list[str] = field(default_factory=list)

    def receive(self, sender, signal, q):
        ...

    def send(self, signal, q):
        for link in self.links:
            q.append(Message(self.name, link, signal))


@dataclass
class FlipFlop(Module):
    value: int = 0

    def receive(self, sender, signal, q):
        if signal == 0:
            self.value = 1 - self.value
            self.send(self.value, q)


class Conjunction(Module):
    def set_pre(self, pre):
        self.pre = {p: 0 for p in pre}

    def receive(self, sender, signal, q):
        self.pre[sender] = signal
        self.send(0 if all(self.pre.values()) else 1, q)


class Broadcaster(Module):
    def send(self, signal, q):
        for link in self.links:
            q.append(Message(self.name, link, signal))


class Output(Module):
    def send(self, signal, q):
        ...


def get_module(config):
    name, links = config.split(" -> ")
    links = list(links.split(", "))
    if name == "broadcaster":
        return Broadcaster(name, links)
    if name[0] == "%":
        return FlipFlop(name[1:], links)
    if name[0] == "&":
        return Conjunction(name[1:], links)


def get_input(file):
    raw = aoc.read_input(2023, 20, file)
    modules = {}
    for line in aoc_parse.as_lines(raw):
        module = get_module(line)
        modules[module.name] = module
    # compute predecessors of conjuctions
    pre = defaultdict(list)
    for name, module in modules.items():
        for link in module.links:
            pre[link].append(name)
    for name, module in modules.items():
        if isinstance(module, Conjunction):
            module.set_pre(pre[name])
    # add output nodes
    for module in list(modules.values()):
        for link in module.links:
            if link not in modules:
                modules[link] = Output(link)
    return modules


@aoc.pretty_solution(1)
def part1(modules):
    # !
    modules = deepcopy(modules)
    low_pulse, high_pulse = 0, 0
    for _ in range(1000):
        # manually handle the queue of messages
        q = deque()
        # start button sends low to broadcast
        low_pulse += 1
        modules["broadcaster"].send(0, q)
        while q:
            msg = q.popleft()
            low_pulse += msg.signal == 0
            high_pulse += msg.signal == 1
            # process this message
            # the module that receives it will update the q
            modules[msg.user].receive(msg.sender, msg.signal, q)
    return low_pulse * high_pulse


@aoc.pretty_solution(2)
def part2(modules):
    # find predecessor of 'rx'
    for module in modules.values():
        if "rx" in module.links:
            pre_rx = module.name
    # find predecessors of pre_rx:
    pre_dg = []
    for module in modules.values():
        if pre_rx in module.links:
            pre_dg.append(module.name)
    # by inspecting the input, we find that
    # 'rx' is an output node and is triggered only by one conjunction 'dg'
    # 'dg', in turn, is triggered by only 4 conjuctions.
    # we assume that these 4 conjuctions will be independently triggered
    # with a period. we take the lcm of those periods to find when
    # all 4 will be triggered, which will trigger 'dg', which will
    # send a low signal to 'rx'
    cycles = {}
    for t in range(1, 10_000):
        q = deque()
        # do the simulation
        modules["broadcaster"].send(0, q)
        while q:
            msg = q.popleft()
            # inspect message:
            # check if it's one of the relevant triggers
            # and save it's time
            if msg.user == pre_rx and msg.signal == 1:
                if msg.sender in cycles:
                    continue
                cycles[msg.sender] = t
                # all cycles length computed.
                # return the lcm, i.e. when all
                # will be triggered at the same time
                if len(cycles) == len(pre_dg):
                    return lcm(*cycles.values())
            modules[msg.user].receive(msg.sender, msg.signal, q)
    raise "Not enough time"


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 866435264
    assert part2(data) == 229215609826339
    print("Test OK")


if __name__ == "__main__":
    test()
