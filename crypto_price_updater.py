from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
import os

from constants import SpreadsheetScope
from crypto_client import CryptoClientApi
from google_client import GoogleSpreadsheetClient


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
SAMPLE_RANGE_NAME = "coins-budget-tracker!{}"


def main(
    crypto_client: CryptoClientApi,
    spreadsheet_client: GoogleSpreadsheetClient,
    once: bool = True,
):
    coins = spreadsheet_client.read_spreadsheet(range=SAMPLE_RANGE_NAME.format("A2:A"))

    while True:
        coins_prices = []
        for coin in coins:
            coin_price = crypto_client.get_coins_price(coin[0])
            if coin_price:  # skip the coins where no USDT/USDC identifiers
                coins_prices.append([str(coin_price)])

        spreadsheet_client.update_spreadsheet(
            range=SAMPLE_RANGE_NAME.format("E2:E"), values=coins_prices
        )

        if once:
            break

        time.sleep(2)

    spreadsheet_client.read_spreadsheet(
        range=SAMPLE_RANGE_NAME.format(f"G2:G"), print_result=True
    )


if __name__ == "__main__":
    spreadsheet_client = GoogleSpreadsheetClient(
        SAMPLE_SPREADSHEET_ID, SpreadsheetScope.read_write
    )
    crypto_client = CryptoClientApi()

    main(crypto_client, spreadsheet_client)
