import csv
import QSTK
import sys
import re


def parse_orders(filename):
	parser = csv.reader(open(filename, 'rU'), delimiter = ",")
	orders = {"year":[],"month":[],"date":[],"symbol":[],"buy_or_sell":[],
			"quantity":[]}
	for row in parser:
		orders["year"].append(row[0])
		orders["month"].append(row[1])
		orders["date"].append(row[2])
		orders["symbol"].append(row[3])
		orders["buy_or_sell"].append(row[4])
		orders["quantity"].append(row[5])
	return orders
if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Not sufficient arguments."
		print "Arguments should be: [Starting Cash] [Order File] [Output File]"
	elif re.match("$[0-9]*^",sys.argv[1]):
		print "First argument must be an integer representing investable cash."
	else:
		startingcash = sys.argv[1]
		orderbook = parse_orders(sys.argv[2])
		outputfile = sys.argv[2]
		print orderbook
