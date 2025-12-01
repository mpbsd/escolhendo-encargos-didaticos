#!/usr/bin/env python3

import csv
import tomllib


def PRIMARY_SCORE(PARTIALITY, CURRICULUM):
    score = 0
    score += PARTIALITY["CAMPUS"][CURRICULUM[0]]
    score += PARTIALITY["CURSO"][CURRICULUM[1]]
    score += PARTIALITY["DISCIPLINA"][CURRICULUM[2]]
    score += PARTIALITY["HORARIO"][CURRICULUM[3]]
    return score


def main():

    CURRICULUM = []
    PARTIALITY = {}
    AUSPICIOUS = []

    with open("data/csv/202502.csv", "r") as csvfile:
        CSV = csv.reader(csvfile, delimiter=";")
        for row in CSV:
            CURRICULUM.append(row)

    with open("data/toml/202502.toml", "rb") as tomlfile:
        TOML = tomllib.load(tomlfile)
        for k, v in TOML.items():
            PARTIALITY[k] = v

    for curriculum in CURRICULUM:
        score = PRIMARY_SCORE(PARTIALITY, curriculum)
        if score > 0:
            curriculum.append(score)
            AUSPICIOUS.append(curriculum)

    E = sorted(AUSPICIOUS, key=lambda x: x[4], reverse=True)

    for e in E:
        print(e)


if __name__ == "__main__":
    main()
