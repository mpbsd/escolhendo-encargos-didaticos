# Escolhendo Encargos Didáticos

Scripts para auxiliar-me na escolha de meus encargos didáticos para o semestre
vindouro.

## Regras do jogo

1. Apresentar ao menos oito configurações distintas;

1. Cada terna ordenada (curso, disciplina, horário) deve aparecer em apenas uma
   das configurações apresentadas;

1. Ao menos uma das configurações apresentadas deve conter disciplinas do
   noturno;

1. As configurações apresentadas devem abranger ao menos dois turnos distintos;

1. Ao menos uma das configurações apresentadas deve conter uma ou mais
   disciplinas no Campus FCT (Faculdade de Ciências e Tecnologia).

## Sobre o arquivo csv

Ele funciona como um banco de dados para as disciplinas para o próximo semestre
e suas colunas devem ter o seguinte significado:

```csv
CAMPUS; CURSO; DISCIPLINA; HORARIO
```

Sim, o separador utilizado é o `;`

Sinta-se à vontade para alterá-lo ;)

## Sobre o arquivo toml

Ele funciona como um arquivo de configuração em que você especifica suas
preferências pessoais quanto a:

1. **Campus**,
1. **Curso**,
1. **Disciplinas**, e
1. **Horários**.

Deste modo, ele deve conter os 4 grupos seguintes: `CAMPUS`, `CURSO`,
`DISCIPLINA` e `HORARIO` (sem ascento).

## Afazeres

- Adicionar CLI (Command Line Interface);
