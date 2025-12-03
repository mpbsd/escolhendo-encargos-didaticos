#!/usr/bin/env python3

import csv
import re
import tomllib
from itertools import combinations

PAYLOAD = {
    0: re.compile(r"^([0-9]{1,3})([MTN])([0-9]{1,3})$"),
    6: re.compile(r"^([0-9]{3})([MTN])([0-9]{2})$"),
    4: re.compile(r"^([0-9]{2})([MTN])([0-9]{2})$"),
}


def SCORE1ST(PARTIALITY, CURRICULUM):
    score = 0
    score += PARTIALITY["CAMPUS"][CURRICULUM[0]]
    score += PARTIALITY["CURSO"][CURRICULUM[1]]
    score += PARTIALITY["DISCIPLINA"][CURRICULUM[2]]
    score += PARTIALITY["HORARIO"][CURRICULUM[3]]
    return score


def HARMONIOUS(list_of_schedules):
    V = True
    D = re.compile(r"[0-9]")
    L = list(
        map(
            lambda x: PAYLOAD[0].match(x).groups(),
            list_of_schedules,
        )
    )
    for x in combinations(L, 2):
        A, B, C = x[0]
        a, b, c = x[1]
        C0 = len([d for d in D.findall(A) if d in D.findall(a)]) > 0
        C1 = B == b
        C2 = len([d for d in D.findall(C) if d in D.findall(c)]) > 0
        if C0 and C1 and C2:
            V = False
    return V


def PAIRINGS(AUSPICIOUS, PROFILE):
    F = {}
    if PROFILE == 12:
        for n in [4, 6]:
            N = PROFILE // n
            F[n] = [
                X
                for X in combinations(AUSPICIOUS[n], N)
                if HARMONIOUS([x[3] for x in X])
            ]
    return F


def SCORE2ND(PAIRINGS, payload):
    F = {}
    if payload in PAIRINGS.keys():
        k = 0
        for pairing in PAIRINGS[payload]:
            F[k] = {"P": pairing, "S": 0}

            if len(set([x[0] for x in F[k]["P"]])) == 1:
                F[k]["S"] += 1
            else:
                F[k]["S"] -= 1

            if len(set([x[2] for x in F[k]["P"]])) == 1:
                F[k]["S"] += 1
            else:
                F[k]["S"] -= 1

            D = len(set([PAYLOAD[payload].match(x[3])[1] for x in F[k]["P"]]))
            P = len(set([PAYLOAD[payload].match(x[3])[2] for x in F[k]["P"]]))

            if (D == 1) and (P == 1):
                N = sorted([PAYLOAD[payload].match(x[3])[3] for x in F[k]["P"]])
                n = len(N) - 1
                B = True
                while (B == True) and (n > 1):
                    if int(N[n][0]) - int(N[n - 1][-1]) > 1:
                        B = False
                    else:
                        n -= 1
                if B is True:
                    F[k]["S"] += 1
                else:
                    F[k]["S"] -= 1
            else:
                F[k]["S"] -= 1

            k += 1

        I = sorted(F.keys(), key=lambda k: F[k]["S"], reverse=True)

        return [F[k]["P"] for k in I]
    else:
        return F


def PRINTOUT(AUSPICIOUS, PROFILE):
    E = {
        4: [x for x in AUSPICIOUS if PAYLOAD[4].match(x[3])],
        6: [x for x in AUSPICIOUS if PAYLOAD[6].match(x[3])],
    }

    F = SCORE2ND(PAIRINGS(E, 12), PROFILE)
    M = len(F)

    if M <= 8:
        G = F
    else:
        G = []
        X = []
        i = 0
        while (len(G) < 8) and (i < M):
            B = True
            N = len(F[i])
            j = 0
            while (B == True) and (j < N):
                if F[i][j] in X:
                    B = False
                else:
                    j += 1
            if B == True:
                G.append(F[i])
                for j in range(N):
                    X.append(F[i][j])
            i += 1

    with open(f"brew/DRAFT{PROFILE}.txt", "w") as tfile:
        print(G, file=tfile)


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
            AUSPICIOUS.append(curriculum)

    PRINTOUT(AUSPICIOUS, 4)
    PRINTOUT(AUSPICIOUS, 6)


if __name__ == "__main__":
    main()
