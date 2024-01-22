## Topsis-Vansh-102103072
Topsis-Vansh-102103072 is a library for Multiple Criteria Decision making using TOPSIS using command line
Assignment1
By: Vansh Batra 
Roll No: 102103072
Group: 3CO3

## Installation
Use pip to install it
```sh
pip install Topsis-Vansh-102103072
```
##General Instruction
For running it you would provide input csv file, weights ,impacts and output csv file in command line and the result would be stored in output csv file as well as displayed on command line.

## Steps to use it
In command line use the format :
topsis inputcsvfile weights impact output file
1) the first argument should be a csv file containing input data
2) The second argument should be weights 
3) The third should be impacts
4) The fourth should be the output csv file

```sh
 topsis input.csv "1,2,1,1" "+,-,+,-" output.csv
```
## Example
| Fund Name |   P1   |   P2   |  P3  |   P4   |   P5   |
|-----------|--------|--------|------|--------|--------|
|    M1     |  0.88  |  0.77  | 3.1  |  42.5  | 11.81  |
|    M2     |  0.74  |  0.55  | 3.6  |  67.6  | 18.12  |
|    M3     |  0.73  |  0.53  | 3.3  |  39.3  | 10.97  |
|    M4     |  0.75  |  0.56  |  5   |  30.8  |  9.28  |
|    M5     |   0.7  |  0.49  |  5   |  34.2  |  10.1  |
|    M6     |   0.6  |  0.36  | 6.4  |  49.1  | 14.12  |
|    M7     |  0.84  |  0.71  | 5.6  |  69.3  | 19.11  |
|    M8     |   0.9  |  0.81  | 6.4  |  61.6  | 17.43  |

Weights "1,1,1,2,2"
Impacts "+,-,+,+,+"
## OUTPUT
Output file: output.csv is written succesfully
 | Fund Name | P1   | P2   | P3   | P4   | P5   | Topsis Score | Rank |
|-----------|------|------|------|------|------|--------------|------|
| M1        | 0.88 | 0.77 | 3.1  | 42.5 | 11.81| 0.282550     | 5    |
| M2        | 0.74 | 0.55 | 3.6  | 67.6 | 18.12| 0.737680     | 2    |
| M3        | 0.73 | 0.53 | 3.3  | 39.3 | 10.97| 0.262740     | 7    |
| M4        | 0.75 | 0.56 | 5.0  | 30.8 | 9.28 | 0.220834     | 8    |
| M5        | 0.70 | 0.49 | 5.0  | 34.2 | 10.10| 0.263293     | 6    |
| M6        | 0.60 | 0.36 | 6.4  | 49.1 | 14.12| 0.554459     | 4    |
| M7        | 0.84 | 0.71 | 5.6  | 69.3 | 19.11| 0.780545     | 1    |
| M8        | 0.90 | 0.81 | 6.4  | 61.6 | 17.43| 0.688456     | 3    |
The result is also stored in output.csv file
## License

MIT


 
