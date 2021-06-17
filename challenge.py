# challenge - trading algorithm

# given historical data, attempts to determine the best trades that could have been made to maximise profits.

# 1. A trade must be open for a minimum of 30 mins and closed before reaching 60mins.
# 2. You may only have 1 trade active at a time (eg, if you close at time 1:36 you can then open at 1:37).
# 3. You can only buy into the market, that is you can only make a profit from buying low and selling high.

# a trade is like a weighted path between two points in time
# with the limit of one open trade, a single path can be followed
# the trader can wait for an optimal time for a trade at zero cost/gain (path weight of 0)
# the overall timeseries data can be transformed into a directed acyclic graph
# the optimal strategy should be the "heaviest" path through the DAG 

import sys
import networkx as nx


def build_graph(data):

    # create Directed Graph 
    graph = nx.DiGraph()

    data_length = len(data)

    final_batch = data_length - 60

    end_idx = data_length - 30

    offset = 30 

    for idx, val in enumerate(data):

        if idx%100 == 0:
            print(idx)

        if idx >= end_idx:
            break
            
        # iterable range of time increments - possible trade close time points
        time_range = range(30)
        
        if idx >= final_batch:
            time_range = range(30 - (idx-final_batch))
        
        # good trades are profitable - only include if trade val > 0
        trade_edges = [(idx, idx+offset+x, (data[idx+offset+x]-val)) for x in time_range if data[idx+offset+x]-val > 0 ]

        # wait for a good trade is zero cost or benefit
        # add one edge from current minute to next with zero weight
        # following the entire wait path should cost zero 

        wait_edges = [(idx, idx+1, 0)]

        graph.add_weighted_edges_from(wait_edges)
        graph.add_weighted_edges_from(trade_edges)
    
    return graph


def longest_path(G):
    path = nx.dag_longest_path(G)

    print(path)

    for p in path:
        print(p)
    
    return path


def print_trades(path, data):
    total_profit = 0
    trade_idx = 0
    path_len = len(path)
    for idx, i in enumerate(path):
        if idx > path_len-2:
            break

        if path[idx+1] >= i+30:
            if data[path[idx+1]] - data[i] > 0:

                print("Trade: %d - Buy: %s -> Sell: %s = Profit: %s   ---- start: %s min, end: %s min" % (trade_idx, data[i], data[path[idx+1]], "{:.4}".format(data[path[idx+1]] - data[i]), i, path[idx+1]))
                total_profit += data[path[idx+1]] - data[i]
                trade_idx += 1
    
    print("total profit: %s" % ("{:.4}".format(total_profit)))


def write_trades(path, data):

    with open("trades.txt", 'w') as trades_file:

        total_profit = 0
        trade_idx = 0
        path_len = len(path)
        for idx, i in enumerate(path):
            if idx > path_len-2:
                break

            # ignore wait steps - next step is greater than 30 min
            if path[idx+1] >= i+30:
                    trades_file.write("Trade: %d - Buy: %s -> Sell: %s = Profit: %s   ---- start: %s min, end: %s min\n" % (trade_idx, data[i], data[path[idx+1]], "{:.4}".format(data[path[idx+1]] - data[i]), i, path[idx+1]))
                    total_profit += data[path[idx+1]] - data[i]
                    trade_idx += 1
        
        trades_file.write("total profit: %s\n" % ("{:.4}".format(total_profit)))    


# with open("./data_all.csv") as data_file:



def main():
    # get file path from commandline
    file_path = sys.argv[1]

    print(file_path)

    with open(file_path) as data_file:
        next(data_file)
        data = [float(x.split(",")[1]) for x in data_file ]

        # G = build_graph(data[:240])

        G = build_graph(data)

        path = longest_path(G)

        write_trades(path, data)



if __name__ == "__main__":
    main()