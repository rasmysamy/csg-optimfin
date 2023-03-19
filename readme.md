To run to the script, simply run the command :
`python3 main.py`
Fields (such as username, password, and api_endpoint) can be modified at the beginning of the main() function.
Inputs (such as tickers, dateStart, dateEnd and amount) can also be modified at beginning of the main() function.

The optimalValueAlgorithm calculates the best strategy for stock buying in O(n*k) where n is the number of days and k
is the number of companies + 1 (6 in our case)
