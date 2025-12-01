#!/usr/bin/env python3

import csv
import tomllib


def SCORE(PREFERENCES, DISCIPLINE):
    score = 0
    score += PREFERENCES["CAMPUS"][DISCIPLINE[0]]
    score += PREFERENCES["CURSO"][DISCIPLINE[1]]
    score += PREFERENCES["DISCIPLINA"][DISCIPLINE[2]]
    score += PREFERENCES["HORARIO"][DISCIPLINE[3]]
    return score


def main():

    CURRICULUM = []
    PARTIALITY = {}

    GOLDEN = []

    with open("data/csv/202502.csv", "r") as csvfile:
        CSV = csv.reader(csvfile, delimiter=";")
        for row in CSV:
            CURRICULUM.append(row)

    with open("data/toml/202502.toml", "rb") as tomlfile:
        TOML = tomllib.load(tomlfile)
        for k, v in TOML.items():
            PARTIALITY[k] = v

    for dscpln in CURRICULUM:
        score = SCORE(PARTIALITY, dscpln)
        if score > 0:
            dscpln.append(score)
            GOLDEN.append(dscpln)

    E = sorted(GOLDEN, key=lambda x: x[4], reverse=True)

    for e in E:
        print(e)


if __name__ == "__main__":
    main()
