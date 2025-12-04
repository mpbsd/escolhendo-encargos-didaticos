#!/usr/bin/env python3

import csv
import re
import tomllib
from itertools import combinations, product

PAYLOAD = {
    0: re.compile(r"^([0-9]{1,3})([MTN])([0-9]{1,3})$"),
    2: re.compile(r"^([0-9]{1})([MTN])([0-9]{2})$"),
    4: re.compile(r"^([0-9]{2})([MTN])([0-9]{2})$"),
    6: re.compile(r"^([0-9]{3})([MTN])([0-9]{2})$"),
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
    L = [PAYLOAD[0].match(x).groups() for x in list_of_schedules]
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
    P = []
    if PROFILE == 8:
        C = combinations(AUSPICIOUS[4], 2)
        for X in C:
            if HARMONIOUS([x[3] for x in X]):
                P.append(X)
    elif PROFILE == 10:
        C = product(AUSPICIOUS[4], AUSPICIOUS[6])
        for X in C:
            if HARMONIOUS([x[3] for x in X]):
                P.append(X)
    elif PROFILE == 12:
        for n in [4, 6]:
            C = combinations(AUSPICIOUS[n], PROFILE // n)
            for X in C:
                if HARMONIOUS([x[3] for x in X]):
                    P.append(X)
    elif PROFILE == 14:
        C = [
            (x[0][0], x[0][1], x[1])
            for x in product(combinations(AUSPICIOUS[4], 2), AUSPICIOUS[6])
        ]
        for X in C:
            if HARMONIOUS([x[3] for x in X]):
                P.append(X)
    elif PROFILE == 16:
        C = [x for x in combinations(AUSPICIOUS[4], 4)]
        D = [
            (x[0][0], x[0][1], x[1])
            for x in product(combinations(AUSPICIOUS[6], 2), AUSPICIOUS[4])
        ]
        for d in D:
            C.append(d)
        for X in C:
            if HARMONIOUS([x[3] for x in X]):
                P.append(X)
    return P


def SCORE2ND(PAIRINGS):
    F = {}
    k = 0
    for pairing in PAIRINGS:
        F[k] = {"P": pairing, "S": 0}

        if len(set([x[0] for x in F[k]["P"]])) == 1:
            F[k]["S"] += 1
        else:
            F[k]["S"] -= 1

        if len(set([x[2] for x in F[k]["P"]])) == 1:
            F[k]["S"] += 1
        else:
            F[k]["S"] -= 1

        D = len(set([PAYLOAD[0].match(x[3])[1] for x in F[k]["P"]]))
        P = len(set([PAYLOAD[0].match(x[3])[2] for x in F[k]["P"]]))

        if (D == 1) and (P == 1):
            N = sorted([PAYLOAD[0].match(x[3])[3] for x in F[k]["P"]])
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

        if len(F[k]["P"]) <= 2:
            F[k]["S"] += 1
        else:
            F[k]["S"] -= 1

        k += 1

    I = sorted(F.keys(), key=lambda t: F[t]["S"], reverse=True)

    return [F[k]["P"] for k in I]


def PRINTOUT(AUSPICIOUS, PROFILE):
    F = SCORE2ND(PAIRINGS(AUSPICIOUS, PROFILE))
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
    PROFILE = 16
    TERM = "202502"

    PARTIALITY = {}
    AUSPICIOUS = {4: [], 6: []}

    with open(f"data/toml/{TERM}.toml", "rb") as tomlfile:
        TOML = tomllib.load(tomlfile)
        for k, v in TOML.items():
            PARTIALITY[k] = v

    with open(f"data/csv/{TERM}.csv", "r") as csvfile:
        CURRICULUM = csv.reader(csvfile, delimiter=";")
        for curriculum in CURRICULUM:
            if SCORE1ST(PARTIALITY, curriculum) > 0:
                if PAYLOAD[4].match(curriculum[3]):
                    AUSPICIOUS[4].append(curriculum)
                elif PAYLOAD[6].match(curriculum[3]):
                    AUSPICIOUS[6].append(curriculum)

    PRINTOUT(AUSPICIOUS, PROFILE)


if __name__ == "__main__":
    main()
