# Talkcard generator 35C3 
from pack.jparse import Cards
from pack.pdfer import Pdfer
import argparse, json

cards = Cards()

parser = argparse.ArgumentParser(description='Prints or lists 35c3 Talkcards')
parser.add_argument('-l', '--list', action='store_true', help='list found json data instead of pdf-generate')
parser.add_argument('-f', '--file', type=str, default="nA", help='output found json data as file.')
parser.add_argument('-a', '--all', action='store_true', help='selects all talks')
parser.add_argument('-r', '--room', type=str, default="nA", help='can be one of [A,B,C,D,E,CW]')
parser.add_argument('-d', '--day', type=str, default="nA", help='can be 1-4')
args = parser.parse_args()

if args.all:
    cards.output(args, cards.get_data())

if (args.room != "nA") and (args.day != "nA"):
    data = cards.search_data(["room", "day"], [args.room, args.day])
    out(args, data)
else:
    if args.room != "nA":
        data = cards.search_data("room", args.room)
        out(args, data)    
    elif args.day != "nA":
        data = cards.search_data("day", args.day)
        out(args, data)
    else:
        print("error")
        parser.print_help()

def out(args, data):
    if args.list:
        print(json.dumps(data, indent=2))
    if args.file != "nA":
        with open(args.file, "w") as text_file:
            print(json.dumps(data, indent=2), file=text_file)
