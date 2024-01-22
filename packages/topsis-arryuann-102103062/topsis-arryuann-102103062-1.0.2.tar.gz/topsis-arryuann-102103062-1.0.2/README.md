## topsis-Arryuann-102103062
for: Assignment01-Topsis (UCS633) submitted by: Arryuann Khanna Roll no: 102103062 Group: 3COE3
This Python library helps with Multiple Criteria Decision Making(MCDM) problems by using Technique for Order of Preference by Similarity to Ideal Solution(TOPSIS).

## Installation
```pip install topsis-Arryuann-102103062```

## How to use it?
Open terminal and enter a valid csv filename followed by .csv extentsion, then enter the weights vector with vector values separated by commas, then impacts vector with comma separated signs (+,-) and finally the output file name in csv format.

```topsis 102103062-data.csv "1,1,1,1" "+,-,+,+" 102103062-result-1.csv```

## Example

If you have this content inside the 102103062-data.csv-

| Fund Name  | P1    |    P2 |    P3 |    P4 |    P5 | 
|------------|-------|-------|-------|-------|-------|
| M1         | 0.88  | 0.77  | 3.0   | 57.7  | 15.59 |
| M2         | 0.87  | 0.76  | 4.9   | 39.4  | 11.48 |
| M3         | 0.91  | 0.83  | 5.5   | 59.4  | 16.66 |
| M4         | 0.61  | 0.37  | 3.2   | 39.6  | 10.95 |
| M5         | 0.60  | 0.36  | 5.6   | 62.3  | 17.22 |
| M6         | 0.77  | 0.59  | 6.1   | 51.5  | 14.74 |
| M7         | 0.61  | 0.37  | 4.7   | 43.3  | 12.25 |
| M7         | 0.71  | 0.50  | 6.1   | 42.6  | 12.48 |

and you ran the command-

`topsis 102103062-data.csv "1,1,1,1,1" "+,-,+,-,+" 102103062-result-1.csv`

you get this as output-
```
 Fund Name    P1    P2   P3    P4     P5  Topsis Score  Rank
0        M1  0.88  0.77  3.0  57.7  15.59      0.626255     1
1        M2  0.87  0.76  4.9  39.4  11.48      0.535066     3
2        M3  0.91  0.83  5.5  59.4  16.66      0.460473     4
3        M4  0.61  0.37  3.2  39.6  10.95      0.559417     2
4        M5  0.60  0.36  5.6  62.3  17.22      0.363836     7
5        M6  0.77  0.59  6.1  51.5  14.74      0.353200     8
6        M7  0.61  0.37  4.7  43.3  12.25      0.455437     5
7        M8  0.71  0.50  6.1  42.6  12.48      0.378622     6
```

and also saved in 102103062-result-1.csv in current working directory

## License

© 2024 Arryuann Khanna

This repository is licensed under the MIT license. See LICENSE for details.
