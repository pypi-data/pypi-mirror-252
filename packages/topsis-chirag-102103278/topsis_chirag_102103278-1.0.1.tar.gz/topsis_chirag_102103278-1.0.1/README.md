# Topsis
TOPSIS( Technique for order for preference by similarity to Ideal solution ) for MCDM (Multiple criteria decision making) in Python compiled by Chirag Gupta, 102103278, TIET, Patiala. 

## Installation
Use the package manager pip to install.
```pip install topsis_chirag_102103278```

## Usage
Enter csv filename followed by .csv extentsion, then enter the weights vector with vector values separated by commas, followed by the impacts vector with comma separated signs (+,-) and enter the output file name followed by .csv extension.

```python [InputDataFile as .csv] [Weights as a string] [Impacts as a string] [ResultFileName as .csv]```

### Example
```python sample.csv "1,1,1,1" "-,+,+,+" output.csv```

## Please Note That"

The first column and first row are removed by the library before processing, in attempt to remove indices and headers. So the csv MUST follow the format as shown in sample.csv shown in the Example section.
The input data file MUST contain three or more columns.
The second to last columns of the data file MUST contain NUMERIC values.
The number of weights, impacts and columns (second to last) MUST be SAME.
Impacts MUST either be '+' or '-'.
Impacts and Weights MUST be separated by , (comma).

## License

© 2024 Chirag Gupta

This reopsitory is licensed under MIT License. See LICENSE for details.