# Topsis

**TOPSIS** (Technique for Order of Preference by Similarity to Ideal Solution) is a decision-making method based on the concept that the best solution is the one closest to the positive-ideal solution and farthest from the negative-ideal one. The alternatives are ranked using an overall index calculated from the distances to the ideal solutions.

## Function Parameters

The `topsis` function takes four arguments:

1. **Data.csv file**: The input CSV file containing the data for decision-making.
2. **Weights**: A string representing the weights for each criterion, separated by commas. For example, "1,1,1,1,1".
3. **Impacts**: A string representing the impacts for each criterion, specified as either '+' or '-'. For example, "+,-,+,-,+".
4. **Result file**: The name of the output file that will contain Topsis Score and Rank information.

## How to Use

To use the Topsis package, follow these steps:

1. Open your terminal.
2. Type the following command to install the Topsis package:

   ```bash
   pip install Topsis-Vanshika-102103484
   ```

3. To get started quickly, use the following Python code:

   ```python
   from topis_pckg.topsis import topsis
   topsis('inputfilename','Weights','Impacts','Outputfilename')
   ```

   Make sure to replace `'inputfilename'`, `'Weights'`, `'Impacts'`, and `'Outputfilename'` with your actual file names and values. Ensure that the weights and impacts are specified in double quotes, as shown in the example.

By following these steps, you can efficiently use the Topsis package to calculate scores and ranks based on your decision-making criteria.
