# TOPSIS PACKAGE - Assignment 1
I have developed a command line python program to implement the TOPSIS.
TOPSIS (technique for order performance by similarity to ideal solution) is a useful technique in dealing with multi-attribute or multi-criteria decision making (MADM/MCDM) problems in the real world
## Installation
```pip install topsis-bhavya-102103345```

## Usage
Please provide the filename for the CSV, including the .csv extension. After that, enter the weights vector with values separated by commas. Following the weights vector, input the impacts vector, where each element is denoted by a plus (+) or minus (-) sign. Lastly, specify the output file name along with the .csv extension.

```py -m topsis.__main__ [input_file_name.csv] [weight as string] [impact as string] [result_file_name.csv]```

### Example
Example

sample.csv

Model Name P1 P2 P3 P4 P5

M1 0.68 0.46 4 52.7 14.46

M2 0.61 0.37 6.9 51.5 14.85

M3 0.61 0.37 4.4 53.5 14.72

M4 0.7, 0.49 6 54.5 15.42

M5 0.65 0.42 4.1 68.7 18.47

M6 0.62 0.38 3.6 36.4 10.25

M7 0.92 0.85 5.2 44.6 12.89

M8 0.81 0.66 3.7 35.9 10.27

weights vector = [ 1,1,1,2,2 ]

impacts vector = [ +,+,-,+,+ ]

input

output

result.csv

Model Name,P1,P2,P3,P4,P5,Topsis Score,Rank

M1,0.68,0.46,4.0,52.7,14.46,0.5903064989592446,4.0

M2,0.61,0.37,6.9,51.5,14.85,0.5408709514358343,5.0

M3,0.61,0.37,4.4,53.5,14.72,0.5933191124418361,3.0

M4,0.7,0.49,6.0,54.5,15.42,0.4714313335411608,7.0

M5,0.65,0.42,4.1,68.7,18.47,0.3803866453639049,8.0

M6,0.62,0.38,3.6,36.4,10.25,0.9855303249104818,1.0

M7,0.92,0.85,5.2,44.6,12.89,0.5209148114910495,6.0

M8,0.81,0.66,3.7,35.9,10.27,0.7535236734320149,2.0

Other Notes

1. The first column and first row are removed by the library before processing, in attempt to remove indices and headers. So make sure the csv follows the format as shown in sample.csv.

2. Make sure the csv does not contain categorical values

License

&copy; 2024 Bhavya Bhalla

This repository is licensed under the MIT license.

See LICENSE for details.
