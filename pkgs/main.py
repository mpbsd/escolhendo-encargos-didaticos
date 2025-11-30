#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path

from .core import DSCPLN

T = datetime.now()
Y = T.strftime("%Y")
M = T.strftime("%m")
S = 1 if int(M) <= 6 else 2


def DEFAULT_PDF_FILE(year=Y, semester=S):
    PDF = None
    if Path(f"data/{year}_{semester}.pdf").is_file():
        PDF = f"data/{year}_{semester}.pdf"
    return PDF


def main():

    print(DEFAULT_PDF_FILE())

    SBJCT = DSCPLN("2025_1")
    print(SBJCT)


if __name__ == "__main__":
    main()
