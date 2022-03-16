from brownie import DummyDummy, DutchAuction, accounts, config, network, exceptions
import time
import datetime
from datetime import timezone
import pytest

def test_deploy():
    account = accounts[0]
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
    state = auction.get_auction_state()
    assert state == 1

def test_bid():
    account = accounts[0]
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

    assert txBid.events["AuctionEnded"]["winner"] == bidder

def test_bid_lower():
    account = accounts[0]
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
    with pytest.raises(exceptions.VirtualMachineError):
        txBid = auction.bid({"from": bidder, "value": auction.get_price()-10000})

def test_bid_higher():
    account = accounts[0]
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
    balanceBeforeBid = bidder.balance()
    # Bid higher than the current price and see if the refund is sucessful 
    txBid = auction.bid({"from": bidder, "value": auction.get_price() + 100000})
    assert bidder.balance() == balanceBeforeBid - txBid.events["AuctionEnded"]["bidAmount"]