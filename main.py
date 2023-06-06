import asyncio
import numpy as np
from pybit.unified_trading import WebSocket
from series_corr import SeriesRegression


p_value, available_r = 0.05, 0.5

corr = SeriesRegression(
    p_value,
    available_r
)

ws = WebSocket(
    testnet=True,
    channel_type="linear",
)


class CoinExtract:
    influence = 'BTCUSDT'
    influenced = 'ETHUSDT'

    influence_price = float()

    def get_coin_info(self, name, price):
        if name == self.influence:
            self.influence_price = price

        if name == self.influenced:
            corr.add_influenced(price)
            corr.add_influence(self.influence_price)


coin_extract = CoinExtract()


def handle_ticker(message):
    ticker_data = message['data']
    coin_symbol = ticker_data['symbol']
    prev_1h_price = float(ticker_data['prevPrice1h'])
    mark_price = float(ticker_data['markPrice'])

    coin_extract.get_coin_info(coin_symbol, mark_price)

    if abs(mark_price - prev_1h_price) >= 0.01 * prev_1h_price:
        print(coin_symbol, '-', mark_price)


ws.ticker_stream(
    symbol='BTCUSDT',
    callback=handle_ticker)

ws.ticker_stream(
    symbol='ETHUSDT',
    callback=handle_ticker)


async def main():
    while True:
        await asyncio.sleep(0.5)
        result = corr.corr()
        if result:
            print(result.is_valid, result.intercept, result.slope)
            if result.is_valid:
                print('True ETHUSDT', result.intercept)


if __name__ == '__main__':
    asyncio.run(main())
