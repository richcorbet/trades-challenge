## Biarri Techical Challenge
####Trading Algorithm

Given historical data, attempt to determine the best trades that could have been made to maximise profits.

1. A trade must be open for a minimum of 30 mins and closed before reaching 60mins.
2. You may only have 1 trade active at a time (eg, if you close at time 1:36 you can then open at 1:37).
3. You can only buy into the market, that is you can only make a profit from buying low and selling high.



### Language Choice - PYTHON

### Dependencies
python3
networkx


### How to run
Assuming Python3 is already installed

``` git clone https://github.com/richcorbet/trades-challenge.git ```

```cd trades-challenge```


##### Install Dependencies 
```pip3 install networkx```

or
```pip install networkx```


##### Run Code 
```./python3 challenge.py data_3600.csv```

or 
```./python challenge.py data_3600.csv```

##### Review Results
The code outputs the trade results to the file ```trades.txt```
