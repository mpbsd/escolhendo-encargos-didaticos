# Escolhendo Encargos Didáticos

Scripts para auxiliar-me na escolha de meus encargos didáticos para o semestre
vindouro.

## Regras do jogo

1. Apresentar ao menos oito configurações distintas;

1. Cada quádrupla ordenada (campus, curso, disciplina, horário) deve aparecer em
   apenas uma das configurações apresentadas;

1. Ao menos uma das configurações apresentadas deve conter disciplinas no
   período noturno;

1. As configurações apresentadas devem abranger ao menos dois turnos distintos;

1. Ao menos uma das configurações apresentadas deve conter uma ou mais
   disciplinas no Campus da FCT (Faculdade de Ciências e Tecnologia).

## Sobre os arquivos csv

Eles funcionam como bancos de dados para as disciplinas nos semestres indicados
pelo nome do arquivo, e os campos neles contidos têm o seguinte significado:

```csv
CAMPUS, CURSO, DISCIPLINA, HORARIO
```

## Sobre os arquivos Toml

Eles funcionam como arquivos de configuração em que você especifica suas
preferências pessoais quanto a:

1. **Campus**,
1. **Curso**,
1. **Disciplinas**, e
1. **Horários**.

Deste modo, cada arquivo `toml` deve conter estes 4 grupos: `CAMPUS`, `CURSO`,
`DISCIPLINA` e `HORARIO` (sem ascento).
