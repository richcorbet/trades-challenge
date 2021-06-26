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


def build_graph(price_data=[]):

    # create Directed Graph
    graph = nx.DiGraph()

    data_length = len(price_data)

    if data_length < 31:
        # cannot make any trades if there is no opportunit
        return graph

    final_batch = data_length - 60

    end_idx = data_length - 30

    offset = 30

    for idx, price_record in enumerate(price_data[:end_idx]):

        if idx % 100 == 0:
            print(idx)

        # iterable range of time increments - possible trade close time points
        time_range = range(30)

        if idx >= final_batch:
            time_range = range(30 - (idx - final_batch))

        for x in time_range:

            buy_node = price_record[0]

            # a sell node is different than a buy node as you cannot buy at the same timepoint as as sell
            sell_node = price_data[idx + offset + x][0] + ":sell"
            trade_value = price_data[idx + offset + x][1] - price_record[1]

            if trade_value > 0:

                # good trades are profitable - only include if trade_value > 0
                # trade_edges.append((buy_node, sell_node, trade_value, attr=edge_attrs))

                graph.add_edge(
                    buy_node,
                    sell_node,
                    weight=trade_value,
                    buy_value=price_record[1],
                    sell_value=price_data[idx + offset + x][1],
                )

                try:
                    # add wait node after sell node to move to the next time point
                    # condition 2

                    wait_node = price_data[idx + offset + x + 1][0]
                    # trade_edges.append((sell_node, wait_node, 0))
                    graph.add_edge(sell_node, wait_node, weight=0)

                except IndexError:
                    print("wait node is beyond the end of the data set, ignoring")

        # wait for a good trade is zero cost or benefit
        # add one edge from current minute to next with zero weight
        # following the entire wait path should cost zero

        next_node = price_data[idx + 1]
        graph.add_edge(price_record[0], next_node[0], weight=0)
        # graph.add_weighted_edges_from(wait_edge)
        # graph.add_weighted_edges_from(trade_edges)

    return graph


def longest_path(G):
    path = nx.dag_longest_path(G)

    print(path)

    for p in path:
        print(p)

    return path


def print_trades(path, graph):
    total_profit = 0
    trade_idx = 0
    path_len = len(path)
    for idx, current_node in enumerate(path):
        if idx > path_len - 2:
            # no more possible trades
            break

        if ":sell" in path[idx + 1]:
            # next node is a sell node - current node is a buy node

            edge = graph.get_edge_data(current_node, path[idx + 1])
            print(
                f'Trade: {trade_idx} - Buy: {edge["buy_value"]} -> Sell: {edge["sell_value"]} = Profit: {edge["weight"]:.4}   ---- start: {current_node} min, end: {path[idx + 1].split(":")[0]} min'
            )

            total_profit += edge["weight"]
            trade_idx += 1

    print("total profit: %s" % ("{:.4}".format(total_profit)))


def write_trades(path, graph):

    with open("trades.txt", "w") as trades_file:

        total_profit = 0
        trade_idx = 0
        path_len = len(path)

        # only consider path nodes that can be possible buy points
        for idx, current_node in enumerate(path[: path_len - 2]):
            if ":sell" in path[idx + 1]:
                # next node is a sell node - current node is a buy node

                edge = graph.get_edge_data(current_node, path[idx + 1])
                trades_file.write(
                    f'Trade: {trade_idx} - Buy: {edge["buy_value"]} -> Sell: {edge["sell_value"]} = Profit: {edge["weight"]:.4}   ---- start: {current_node} min, end: {path[idx + 1].split(":")[0]} min'
                )

                total_profit += edge["weight"]
                trade_idx += 1

        trades_file.write("total profit: %s\n" % ("{:.4}".format(total_profit)))


# with open("./data_all.csv") as data_file:


def read_data(file_path=None):

    with open(file_path) as data_file:
        next(data_file)

        data = []

        for row in data_file:

            row_values = row.split(",")

            data.append((row_values[0], float(row_values[1])))

        return data


def main():
    # get file path from commandline
    file_path = sys.argv[1]

    print(file_path)

    data = read_data(file_path)

    # print(data)

    # G = build_graph(data[:240])

    G = build_graph(data)

    print("edges\n\n\n")
    print(G.edges)

    path = longest_path(G)

    print_trades(path, G)
    # write_trades(path, data)


if __name__ == "__main__":
    main()
