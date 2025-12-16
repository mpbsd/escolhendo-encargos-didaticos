#!/usr/bin/env python3

import csv
import re
import sys
import tomllib
from datetime import datetime
from itertools import combinations, product

PAYLOAD = {  # {{{
    0: re.compile(r"^([0-9]{1,3})([MTN])([0-9]{1,3})$"),
    2: re.compile(r"^([0-9]{1})([MTN])([0-9]{2})$"),
    4: re.compile(r"^([0-9]{2})([MTN])([0-9]{2})$"),
    6: re.compile(r"^([0-9]{3})([MTN])([0-9]{2})$"),
}  # }}}


def SCORE1ST(PARTIALITY, DISCIPLINE):  # {{{
    score = 0
    score += PARTIALITY["CAMPUS"][DISCIPLINE[0]]
    score += PARTIALITY["CURSO"][DISCIPLINE[1]]
    score += PARTIALITY["DISCIPLINA"][DISCIPLINE[2]]
    score += PARTIALITY["HORARIO"][DISCIPLINE[3]]
    return score  # }}}


def HARMONIOUS(SCHEDULE):  # {{{
    V = True
    D = re.compile(r"[0-9]")
    L = [PAYLOAD[0].match(x).groups() for x in SCHEDULE]
    for x in combinations(L, 2):
        A, B, C = x[0]
        a, b, c = x[1]
        C0 = len([d for d in D.findall(A) if d in D.findall(a)]) > 0
        C1 = B == b
        C2 = len([d for d in D.findall(C) if d in D.findall(c)]) > 0
        if C0 and C1 and C2:
            V = False
    return V  # }}}


def PAIRINGS(AUSPICIOUS, LUMP):  # {{{
    P = []
    if LUMP == 8:
        C = combinations(AUSPICIOUS[4], 2)
        for X in C:
            if HARMONIOUS([x[3] for x in X]):
                P.append(X)
    elif LUMP == 10:
        C = product(AUSPICIOUS[4], AUSPICIOUS[6])
        for X in C:
            if HARMONIOUS([x[3] for x in X]):
                P.append(X)
    elif LUMP == 12:
        for n in [4, 6]:
            C = combinations(AUSPICIOUS[n], LUMP // n)
            for X in C:
                if HARMONIOUS([x[3] for x in X]):
                    P.append(X)
    elif LUMP == 14:
        C = [
            (x[0][0], x[0][1], x[1])
            for x in product(combinations(AUSPICIOUS[4], 2), AUSPICIOUS[6])
        ]
        for X in C:
            if HARMONIOUS([x[3] for x in X]):
                P.append(X)
    elif LUMP == 16:
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
    return P  # }}}


def SCORE2ND(PARTIALITY, PAIRINGS):  # {{{
    F = {}
    k = 0
    for pairing in PAIRINGS:
        score = sum([SCORE1ST(PARTIALITY, dscpln) for dscpln in pairing])

        F[k] = {"P": pairing, "S": score}

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

        if len(F[k]["P"]) == sorted([len(x) for x in PAIRINGS])[0]:
            F[k]["S"] += 1
        else:
            F[k]["S"] -= 1

        k += 1

    I = sorted(F.keys(), key=lambda t: F[t]["S"], reverse=True)

    return [F[k]["P"] for k in I]  # }}}


def PRINTOUT(PARTIALITY, AUSPICIOUS, LUMP):  # {{{
    F = SCORE2ND(PARTIALITY, PAIRINGS(AUSPICIOUS, LUMP))
    M = len(F)
    Q = 8

    if M <= Q:
        G = F
    else:
        G = []
        X = []
        i = 0
        while (len(G) < Q) and (i < M):
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

    with open(f"brew/DRAFT{LUMP}.txt", "w") as tfile:
        print(G, file=tfile)  # }}}


def OPENSESAME(TERM):  # {{{
    PARTIALITY = {}
    AUSPICIOUS = {4: [], 6: []}

    with open(f"data/toml/{TERM}.toml", "rb") as tomlfile:
        TOML = tomllib.load(tomlfile)
        for k, v in TOML.items():
            PARTIALITY[k] = v

    with open(f"data/csv/{TERM}.csv", "r") as csvfile:
        DISCIPLINE = csv.reader(csvfile, delimiter=",")
        for discipline in DISCIPLINE:
            if SCORE1ST(PARTIALITY, discipline) > 0:
                if PAYLOAD[4].match(discipline[3]):
                    AUSPICIOUS[4].append(discipline)
                elif PAYLOAD[6].match(discipline[3]):
                    AUSPICIOUS[6].append(discipline)

    return PARTIALITY, AUSPICIOUS  # }}}


def HELP():  # {{{
    help = """
    Convenção:

    Representamos semestres letivos como strings no formato 'YYYYSS' em que
    'YYYY' representa o ano (quatro dígitos) e 'SS' representa o semestre (dois
    dígitos). Assim, por exemplo, os primeiro e segundo semestres letivos de
    2026 são representados, respectivamente, como '202601' e '202602'.

    Uso:

    Seja N a carga horária semanal do docente, em que N é um dentre os naturais:
    8, 10, 12, 14 ou 16. Neste caso, deve-se digitar o seguinte:

        python3 -m pkgs.core (-l|--lump) N (-t|--term) YYYYSS

    É possível digitar apenas a carga horária semanal do docente, como a seguir:

        python3 -m pkgs.core (-l|--lump) N

    Neste caso, os scripts assumem que o semestre letivo é o semestre atual
    (datas do sistema).

    Dependências:

    Para o correto funcionamento dos scripts os seguintes arquivos se fazem
    necessários:

        - data/csv/YYYYSS.csv

            Contém as disciplinas ofertadas pelo IME/UFG em YYYYSS. Por exemplo,
            veja data/csv/202501.csv e data/csv/202502.csv.

        - data/toml/YYYYSS.toml

            Contém as preferências pessoais do docente quanto a CAMPUS, CURSO,
            DISCIPLINA e HORÁRIOS. Por exemplo, veja data/toml/202501.toml e
            data/toml/202502.toml.

    Dúvidas:

    Envie um e-mail para bezerra@ufg.br. Responderei assim que possível.
    """
    print(help)  # }}}


def core():

    FLAG = {  # {{{
        "HELP": ["-h", "--help"],
        "LUMP": ["-l", "--lump"],
        "TERM": ["-t", "--term"],
    }  # }}}

    OPTS = {  # {{{
        "LUMP": ["8", "10", "12", "14", "16"],
        "TERM": re.compile(r"^20(?:2[5-9]|[3-9][0-9])0[12]$"),
    }  # }}}

    # handle flags/options
    if len(sys.argv) == 2:
        _, F1 = sys.argv
        if F1 in FLAG["HELP"]:
            HELP()
        else:
            print("Unrecognized flag. Please, type -h for help.")
    elif len(sys.argv) == 3:
        _, F1, O1 = sys.argv
        if (F1 in FLAG["LUMP"]) and (O1 in OPTS["LUMP"]):
            T0 = datetime.now()
            Y0 = T0.strftime("%Y")
            M0 = 1 if int(T0.strftime("%m")) <= 6 else 2
            LUMP = int(O1)
            TERM = f"{Y0}{M0:02d}"
            PARTIALITY, AUSPICIOUS = OPENSESAME(TERM)
            PRINTOUT(PARTIALITY, AUSPICIOUS, LUMP)
        else:
            print("Unrecognized flags/options. Please, type -h for help.")
    elif len(sys.argv) == 5:
        _, F1, O1, F2, O2 = sys.argv
        C0 = (F1 in FLAG["LUMP"]) and (O1 in OPTS["LUMP"])
        C1 = (F2 in FLAG["TERM"]) and (OPTS["TERM"].match(O2))
        C2 = (F1 in FLAG["TERM"]) and (OPTS["TERM"].match(O1))
        C3 = (F2 in FLAG["LUMP"]) and (O2 in OPTS["LUMP"])
        if C0 and C1:
            LUMP = int(O1)
            TERM = O2
            PARTIALITY, AUSPICIOUS = OPENSESAME(TERM)
            PRINTOUT(PARTIALITY, AUSPICIOUS, LUMP)
        elif C2 and C3:
            LUMP = int(O2)
            TERM = O1
            PARTIALITY, AUSPICIOUS = OPENSESAME(TERM)
            PRINTOUT(PARTIALITY, AUSPICIOUS, LUMP)
        else:
            print("Unrecognized flags/options. Please, type -h for help.")
    else:
        print("Wrong number of flags/options. Please, type -h for help.")


if __name__ == "__main__":
    core()
