from brownie import DummyDummy, DutchAuction, network, config, accounts
import time
import datetime
from datetime import timezone


def get_account(index=None, id=None):
    if(network.show_active() == "development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_auction():
    account = get_account()

    # Mint the Dummy ERC20 Token to be sold
    dumDumToken = DummyDummy.deploy({"from": account})

    # Defines the parameters of the constructor of the auction contract
    # Dates in Unix Time
    startDate = int(time.time())
    endDate = int(datetime.datetime(2022, 3, 15, 14, 55, 0).replace(
        tzinfo=timezone.utc).timestamp())
    startPrice = 0.0001 * 10**18
    # Deploy the contract
    auction = DutchAuction.deploy(
        startDate,
        endDate,
        startPrice,
        dumDumToken,
        {"from": account}
    )
    # Approve the auction contract to spend the token under auction
    dumDumToken.approve(auction, 10E18, {"from": account})
    # Assign an account to the buyer
    bidder = accounts[1]
    # Buyer bids at the current price
    txBid = auction.bid({"from": bidder, "value": auction.get_price()})
    print(txBid.events)
    
    print(auction.get_auction_state())
    return auction


def main():
    deploy_auction()
