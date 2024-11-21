from binance.client import Client


class CryptoClientApi:
    def __init__(self) -> None:
        self.client = Client()

    def get_coins_price(self, coin: str, property: str = "lastPrice") -> float | None:
        """
        Expected coins format: BTCUSDC, BTC/USDC
        """
        if "USDC" in coin.upper() or "USDT" in coin.upper():
            coin_price = self.client.get_ticker(symbol=coin.replace("/", ""))[property]
            print(f"{coin}: {coin_price}")
            return coin_price
        return None
