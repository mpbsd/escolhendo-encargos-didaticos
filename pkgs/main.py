#!/usr/bin/env python3

import csv
import re
import tomllib
from itertools import combinations

PAYLOAD6 = re.compile(r"^[0-9]{3}[MTN][0-9]{2}$")
PAYLOAD4 = re.compile(r"^[0-9]{2}[MTN][0-9]{2}$")


def SCORE1ST(PARTIALITY, CURRICULUM):
    score = 0
    score += PARTIALITY["CAMPUS"][CURRICULUM[0]]
    score += PARTIALITY["CURSO"][CURRICULUM[1]]
    score += PARTIALITY["DISCIPLINA"][CURRICULUM[2]]
    score += PARTIALITY["HORARIO"][CURRICULUM[3]]
    return score


def SCORE2ND(AUSPICIOUS, PROFILE):
    F = {}
    if PROFILE in [8, 10, 12, 14, 16]:
        if PROFILE == 12:
            for n in [4, 6]:
                N = PROFILE // n
                F[n] = list(combinations(AUSPICIOUS[n], N))
    return F


def main():
    TERM = "202502"

    CURRICULUM = []
    PARTIALITY = {}
    AUSPICIOUS = []

    with open(f"data/csv/{TERM}.csv", "r") as csvfile:
        CSV = csv.reader(csvfile, delimiter=";")
        for row in CSV:
            CURRICULUM.append(row)

    with open(f"data/toml/{TERM}.toml", "rb") as tomlfile:
        TOML = tomllib.load(tomlfile)
        for k, v in TOML.items():
            PARTIALITY[k] = v

    for curriculum in CURRICULUM:
        score = SCORE1ST(PARTIALITY, curriculum)
        if score > 0:
            # curriculum.append(score)
            AUSPICIOUS.append(curriculum)

    E = {
        4: [x for x in AUSPICIOUS if PAYLOAD4.match(x[3])],
        6: [x for x in AUSPICIOUS if PAYLOAD6.match(x[3])],
    }

    F = SCORE2ND(E, 12)

    print(F[6])

    # E = sorted(AUSPICIOUS, key=lambda x: x[4], reverse=True)
    #
    # for e in E:
    #     print(e)


if __name__ == "__main__":
    main()
