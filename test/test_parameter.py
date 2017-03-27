#!/usr/bin/python
import argparse
class EscapeNamespace():
    pass

escape = EscapeNamespace()
parser = argparse.ArgumentParser(description='Process newspaper url sources')
parser.add_argument('source',help='permits the scrapping of the url source in argument ',nargs=1)
#parser.parse_args(args=['--foo', 'BAR'], namespace=c)
argum = parser.parse_args(namespace=escape)
print(escape.source)
