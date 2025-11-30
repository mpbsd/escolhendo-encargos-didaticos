#!/usr/bin/env python3

from .core import DSCPLN


def main():

    for Y in ["2022", "2023", "2024", "2025"]:
        for S in [1, 2]:
            if (Y == "2022" and S == 1) or (Y == "2023" and S == 2):
                continue
            else:
                with open(f"brew/{Y}{S:02d}.csv", "w") as cfile:
                    SBJCT = DSCPLN(Y, S)
                    print(SBJCT, file=cfile)


if __name__ == "__main__":
    main()
