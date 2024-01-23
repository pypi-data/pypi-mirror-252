# TOPSIS-Python

Submitted By: **Arshiya Sethi** <br>
Roll Number: **102103150** <br>

## Installation
```pip install Topsis-ArshiyaSethi-102103150```

## What is TOPSIS

Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) originated in the 1980s as a multi-criteria decision making method. TOPSIS chooses the alternative of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.More details at [wikipedia](https://en.wikipedia.org/wiki/TOPSIS).

<br>

## How to use this package:

Topsis-ArshiyaSethi-102103150  can be run as:



### In Command Prompt
```
>> topsis data.csv "1,1,1,1" "+,+,-,+" result.csv
```
<br>



## Sample dataset

Consider this sample.csv file  

| Model  | P1 | P2 | P3 | P4 | P5 |
| :----: |:--:|:--:|:--:|:--:|:--:|
| M1 |0.85|0.72|4.6|41.5|11.92|
| M2 |0.66|0.44|6.6|49.4|14.28|
| M3 |0.9 |0.81|6.7|66.5|18.73|
| M4 |0.8 |0.64|6.9|69.7|19.51|
| M5 |0.84|0.71|4.7|36.5|10.69|
| M6 |0.91|0.83|3.6|42.3|11.91|
| M7 |0.65|0.42|6.9|38.1|11.52|
| M8 |0.71|0.5 |3.5|60.9|16.4 |

weights vector = [ 1,2,1,2,1 ]

impacts vector = [ +,-,+,+,- ]

### input:

```python
topsis sample.csv "1,2,1,2,1" "+,-,+,+,-" output.csv
```

### output:

output.csv file will contain following data :

| Model | P1 | P2 | P3 | P4 | P5 | Topsis score | Rank |
| :---: |:--:|:--:|:--:|:--:|:--:| :----------: | :--: |
| M1 |0.85|0.72|4.6|41.5|11.92| 0.3267076760116426 | 6 |
| M2 |0.66|0.44|6.6|49.4|14.28| 0.6230956090525585 | 2 |
| M3 |0.9 |0.81|6.7|66.5|18.73| 0.5006083702087599 | 5 |
| M4 |0.8 |0.64|6.9|69.7|19.51| 0.6275096427934269 | 1 |
| M5 |0.84|0.71|4.7|36.5|10.69| 0.3249142875298663 | 7 |
| M6 |0.91|0.83|3.6|42.3|11.91| 0.2715902624653612 | 8 |
| M7 |0.65|0.42|6.9|38.1|11.52| 0.5439263412940541 | 4 |
| M8 |0.71|0.5 |3.5|60.9|16.4 | 0.6166791918077927 | 3 |

<br>

## License
Copyright 2024 Arshiya Sethi
<br>
This repository is licensed under the MIT license.
<br>
See LICENSE for details.
[MIT](https://choosealicense.com/licenses/mit/)