"""
-- Day 14: Reindeer Olympics ---
This year is the Reindeer Olympics! Reindeer can fly at high speeds, but must rest occasionally to recover their energy. Santa would like to know which of his reindeer is fastest, and so he has them race.

Reindeer can only either be flying (always at their top speed) or resting (not moving at all), and always spend whole seconds in either state.

For example, suppose you have the following Reindeer:

Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
After one second, Comet has gone 14 km, while Dancer has gone 16 km. After ten seconds, Comet has gone 140 km, while Dancer has gone 160 km. On the eleventh second, Comet begins resting (staying at 140 km), and Dancer continues on for a total distance of 176 km. On the 12th second, both reindeer are resting. They continue to rest until the 138th second, when Comet flies for another ten seconds. On the 174th second, Dancer flies for another 11 seconds.

In this example, after the 1000th second, both reindeer are resting, and Comet is in the lead at 1120 km (poor Dancer has only gotten 1056 km by that point). So, in this situation, Comet would win (if the race ended at 1000 seconds).

Given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds, what distance has the winning reindeer traveled?
"""

import re
from dataclasses import dataclass
from collections import defaultdict

SAMPLE_INPUT = [
    "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
    "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."]

with open("input/day14.txt") as input_file:
    inp = input_file.readlines()

# part 1: some data structuring and input parsing first

pattern = r"(\w+) can fly ([0-9]+) km/s for ([0-9]+) seconds, but then must rest for ([0-9]+) seconds."
reindeer = []

@dataclass
class Reindeer:
    name: str
    speed: int
    travel_time: int
    rest_time: int

    # time of one cycle of travelling + resting
    def interval_time(self):
        return self.travel_time + self.rest_time

    def total_distance(self, seconds):
        # There's a naive solution here; just check every reindeer every second until the total time is reached.
        # However it's much cleaner to combine the input times as cycles and calculate the total distance all at once
        # I'll do two quick calculations to do so; the amount of full cycles the reindeer travelled, and the length of the final partial cycle

        one_cycle_time = self.interval_time()
        # use modulus to find length of unfinished cycle
        cycles, remainder = divmod(seconds, one_cycle_time)
        
        # base distance for all completed cycles
        distance = cycles * self.travel_time * self.speed

        if remainder != 0:
            # if they spent less or equal than the max travel time, add all of it
            if remainder <= self.travel_time:
                distance += remainder * self.speed
            # if they spent more time, then add just the travel time
            else:
                distance += self.travel_time * self.speed

        return distance

    

def parse_input(lines):
    for line in lines:
        match = re.match(pattern, line)
        # print(match.groups())
        name, speed, travel_time, rest_time = match.groups()
        reindeer.append(Reindeer(name, int(speed), int(travel_time), int(rest_time)))



# part 1 solution
# parse_input(inp)
# for r in reindeer:
#     print(r)
#     print(r.total_distance(2503))


"""
--- Part Two ---
Seeing how reindeer move in bursts, Santa decides he's not pleased with the old scoring system.

Instead, at the end of each second, he awards one point to the reindeer currently in the lead. (If there are multiple reindeer tied for the lead, they each get one point.) He keeps the traditional 2503 second time limit, of course, as doing otherwise would be entirely ridiculous.

Given the example reindeer from above, after the first second, Dancer is in the lead and gets one point. He stays in the lead until several seconds into Comet's second burst: after the 140th second, Comet pulls into the lead and gets his first point. Of course, since Dancer had been in the lead for the 139 seconds before that, he has accumulated 139 points by the 140th second.

After the 1000th second, Dancer has accumulated 689 points, while poor Comet, our old champion, only has 312. So, with the new scoring system, Dancer would win (if the race ended at 1000 seconds).

Again given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds, how many points does the winning reindeer have?
"""

# We now basically are forced to do the distance calculation every second, or come with an entirely different distance algorithm.
# Fortunately the current total_distance algorithm is efficient enough that we can just do it for every second

parse_input(inp)
points_dict = defaultdict(int)


for s in range(1, 2504):
    dist_dict = {}
    for r in reindeer:
        dist_dict[r.name] = r.total_distance(s)
    max_dist = max(dist_dict.values())
    leading_deer = [k for k, v in dist_dict.items() if v == max_dist]
    # every leading deer gets a point, even when there are multiple
    for l in leading_deer:
        points_dict[l] += 1
print(points_dict, max(points_dict.values()))
