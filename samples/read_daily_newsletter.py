import b3
import collections
import itertools
import sys

def main():
    if len(sys.argv) < 2:
        print('usage: read_daily_newsletter.py <file>')
        return 1

    quotes_by_ticker = collections.defaultdict(list)

    with open(sys.argv[1]) as file:
        reader = b3.parsing.daily_newsletter.reader(file)

        for daily_news in itertools.islice(reader, 10000):
            if daily_news.type == b3.datatypes.DailyNewsletterType.ROUND_LOT:
                quotes_by_ticker[daily_news.ticker].append((daily_news.exchange_date, daily_news.quotes))

    for ticker, dated_quotes in quotes_by_ticker.items():
        print(ticker, ':', sep='')

        for (exchange_date, quotes) in dated_quotes:
            s = f' - {exchange_date} / O: {quotes.open} / L: {quotes.low} / H: {quotes.high} / C: {quotes.close}'

            print(s)
        
        print()

    return 0

if __name__ == '__main__':
    sys.exit(main())