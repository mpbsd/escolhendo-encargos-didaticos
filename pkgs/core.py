import re
from datetime import datetime
from pathlib import Path

import pdfplumber
from unidecode import unidecode

T = datetime.now()
Y = T.strftime("%Y")
M = T.strftime("%m")
S = 1 if int(M) <= 6 else 2


# REGEXES {{{
dashs_re = re.compile(r" *-{1,} *")
clean_re = re.compile(
    r"("
    r"^(?:.*?)(?=CAMPUS)"
    r"|"
    r"- (?:FCT|PRACA|MANHA|MATUTINO|TARDE|VESPERTINO|NOITE|NOTURNO)\b"
    r")"
)
white_re = re.compile(r"^\s*$")
split_re = re.compile(
    r"- ("
    r"CAMPUS (?:APARECIDA|COLEMAR|SAMAMBAIA)"
    r"|"
    r"[^-]+ - [^-]+ - [0-9]{1,3}[MTN][0-9]{1,3}"
    r")"
)
where_re = re.compile(r"^(?:- )?(CAMPUS (?:APARECIDA|COLEMAR|SAMAMBAIA))$")
# }}}


def IFIXIT(a_given_str):  # {{{1
    FIXLIST = {  # {{{2
        r"ALGEBRALINEAR": "ALGEBRA LINEAR",
        r"ANALISEREALII": "ANALISE REAL II",
        r"BIOESTATISTICA1": "BIOESTATISTICA 1",
        r"BIOESTATISTICA2": "BIOESTATISTICA 2",
        r"CALCULO1A": "CALCULO 1A",
        r"CALCULO1B": "CALCULO 1B",
        r"CALCULO1C": "CALCULO 1C",
        r"CALCULO2A": "CALCULO 2A",
        r"CALCULO2B": "CALCULO 2B",
        r"CALCULO3": "CALCULO 3",
        r"CALCULO3A": "CALCULO 3A",
        r"CALCULO3B": "CALCULO 3B",
        r"CALCULODIFERENCIAL": "CALCULO DIFERENCIAL",
        r"CALCULONUMERICO": "CALCULO NUMERICO",
        r"CAMPUSAPARECIDA": "CAMPUS APARECIDA",
        r"CAMPUSCOLEMAR": "CAMPUS COLEMAR",
        r"CAMPUSGOIAS": "CAMPUS GOIAS",
        r"CAMPUSSAMAMBAIA": "CAMPUS SAMAMBAIA",
        r"CIENCIADACOMPUTACAO": "CIENCIA DA COMPUTACAO",
        r"CIENCIASAMBIENTAIS": "CIENCIAS AMBIENTAIS",
        r"CIENCIASBIOLOGICAS": "CIENCIAS BIOLOGICAS",
        r"CIENCIASCONTABEIS": "CIENCIAS CONTABEIS",
        r"CIENCIASDACOMPUTACAO": "CIENCIA DA COMPUTACAO",
        r"CIENCIASECONOMICAS": "CIENCIAS ECONOMICAS",
        r"COMUNICACAOSOCIAL": "COMUNICACAO SOCIAL",
        r"DISCIPLINASDEEXTERNAS": "DISCIPLINAS EXTERNAS",
        r"EDUCACAOMATEMATICAINCLUSIVA": "EDUCACAO MATEMATICA INCLUSIVA",
        r"ENGENHARIAAMBIENTAL": "ENGENHARIA AMBIENTAL",
        r"ENGENHARIACIVIL": "ENGENHARIA CIVIL",
        r"ENGENHARIADAMECANICA": "ENGENHARIA MECANICA",
        r"ENGENHARIADEALIMENTOS": "ENGENHARIA DE ALIMENTOS",
        r"ENG\.? DE ALIMENTOS": "ENGENHARIA DE ALIMENTOS",
        r"ENGENHARIADECOMPUTACAO": "ENGENHARIA DE COMPUTACAO",
        r"ENGENHARIADEMATERIAIS": "ENGENHARIA DE MATERIAIS",
        r"ENGENHARIADEPRODUCAO": "ENGENHARIA DE PRODUCAO",
        r"ENGENHARIADESOFTWARE": "ENGENHARIA DE SOFTWARE",
        r"ENGENHARIADETRANSPORTE": "ENGENHARIA DE TRANSPORTE",
        r"ENGENHARIAELETRICA": "ENGENHARIA ELETRICA",
        r"ENGENHARIAFLORESTAL": "ENGENHARIA FLORESTAL",
        r"ENGENHARIAMECANICA": "ENGENHARIA MECANICA",
        r"ENGENHARIAQUIMICA": "ENGENHARIA QUIMICA",
        r"ESTATISICAI": "ESTATISICA I",
        r"ESTATISTICA1": "ESTATISTICA 1",
        r"ESTATISTICAAPLICADAAPSICOLOGIA": "ESTATISTICA APLICADA A PSICOLOGIA",
        r"ESTATISTICADESCRITIVAEPROBABILIDADE": "ESTATISTICA DESCRITIVA E PROBABILIDADE",
        r"ESTATISTICAII": "ESTATISTICA II",
        r"ESTATISTICAINFERENCIAL": "ESTATISTICA INFERENCIAL",
        r"FISICABACHARELADO": "FISICA BACHARELADO",
        r"FISICALICENCIATURA": "FISICA LICENCIATURA",
        r"GEOMETRIAANALITICA": "GEOMETRIA ANALITICA",
        r"GESTAODAINFORMACAO": "GESTAO DA INFORMACAO",
        r"GESTAODEINFORMACAO": "GESTAO DA INFORMACAO",
        r"INSTITUTODEFISICA": "INSTITUTO DE FISICA",
        r"INTELIGENCIAARTIFICIAL": "INTELIGENCIA ARTIFICIAL",
        r"INTRODUCAOAESTATISTICA": "INTRODUCAO A ESTATISTICA",
        r"INTRODUCAOAPROBABILIDADE": "INTRODUCAO A PROBABILIDADE",
        r"MATEMATICAAPLICADA": "MATEMATICA APLICADA",
        r"MATEMATICABACHARELADO": "MATEMATICA BACHARELADO",
        r"MATEMATICADISCRETA": "MATEMATICA DISCRETA",
        r"MATEMATICALICENCIATURA": "MATEMATICA LICENCIATURA",
        r"NOCOESDEATUARIA": "NOCOES DE ATUARIA",
        r"PROBABILIDADEEESTATISTICA": "PROBABILIDADE E ESTATISTICA",
        r"PROBABILIDADEEESTATISTICAA": "PROBABILIDADE E ESTATISTICA A",
        r"PROBABILIDADEEESTATISTICAB": "PROBABILIDADE E ESTATISTICA B",
        r"PROBABILIDADE E ESTATISTICA": "PROBABILIDADE E ESTATISTICA",
        r"PROBABILIDADE E ESTATISTICAA": "PROBABILIDADE E ESTATISTICA A",
        r"PROBABILIDADE E ESTATISTICAB": "PROBABILIDADE E ESTATISTICA B",
        r"QUIMICABACH\.": "QUIMICA BACHARELADO",
        r"QUIMICABACHARELADO": "QUIMICA BACHARELADO",
        r"QUIMICALICENCIATURA": "QUIMICA LICENCIATURA",
        r"RELACOESINTERNACIONAIS": "RELACOES INTERNACIONAIS",
        r"RELACOESPUBLICAS": "RELACOES PUBLICAS",
        r"SISTEMASDEINFORMACAO": "SISTEMAS DE INFORMACAO",
    }  # }}}
    for err in FIXLIST.keys():
        a_given_str = re.sub(err, FIXLIST[err], a_given_str)
    return a_given_str  # }}}


def DSCPLN(year=Y, semester=S):  # {{{
    PDF = f"data/pdf/{year}_{semester}.pdf"

    if Path(PDF).is_file():
        STR = ""

        with pdfplumber.open(PDF) as pdf:
            for page in pdf.pages:
                TBL = page.extract_table()
                for ROW in TBL:
                    for COL in ROW:
                        if COL not in ["", None]:
                            STR += r"-" + IFIXIT(unidecode(COL.upper()))

        STR = dashs_re.sub(r" - ", STR)
        STR = clean_re.sub(r"", STR)
        STR = [x.strip() for x in split_re.split(STR) if not white_re.match(x)]

        N = len(STR)
        i = 0

        while i < N:
            if where_re.match(STR[i]):
                CAMPUS = where_re.sub(r"\1", STR[i])
            else:
                STR[i] = f"{year}{semester:02d} - " + CAMPUS + r" - " + STR[i]
            i += 1

        STR = [x for x in STR if not where_re.match(x)]
    else:
        print("Could find file on disk. Aborting.")
        STR = None

    return STR  # }}}


def core():

    dscpln = DSCPLN()
    if dscpln:
        with open("brew/draft.csv", "w") as cfile:
            print(dscpln, file=cfile)


if __name__ == "__main__":
    core()
