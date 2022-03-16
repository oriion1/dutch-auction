from brownie import DummyDummy, DutchAuction, accounts, config, network, exceptions
import time
import datetime
from datetime import timezone
import pytest

def test_auction():
    account = accounts[0]
    balanceAcc0 = account.balance() 
    # Mint the Dummy ERC20 Token to be sold
    dumDumToken = DummyDummy.deploy({"from": account})
    # Dates in epoch time
    startDate = int(time.time())
    endDate = int(datetime.datetime(2022, 3, 15, 14, 55, 0).replace(
        tzinfo=timezone.utc).timestamp())
    # 18 decimals
    startPrice = 0.0001 * 10**18
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
    balanceAcc1 = bidder.balance() 
    # Buyer bids at the current price
    txBid = auction.bid({"from": bidder, "value": auction.get_price()})
    state = auction.get_auction_state()
    
    assert state == 0
    assert txBid.events["AuctionEnded"]["winner"] == bidder
    assert bidder.balance() == balanceAcc1 - txBid.events["AuctionEnded"]["bidAmount"]
    assert account.balance() == balanceAcc0 + txBid.events["AuctionEnded"]["bidAmount"]