// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract DutchAuction {
    // The Asset under auction
    IERC20 public immutable tokenAsset;

    uint256 public immutable startDate;
    uint256 public immutable endDate;
    uint256 public immutable startPrice;
    uint256 public immutable decreaseRate;
    address payable public immutable seller;
    enum AUCTION_STATE {
        CLOSED,
        OPEN
    }
    AUCTION_STATE public auction_state;

    event AuctionEnded(address winner, uint256 bidAmount);

    constructor(
        uint256 _startDate,
        uint256 _endDate,
        uint256 _startPrice,
        address _tokenAsset
    ) {
        seller = payable(msg.sender);
        startDate = _startDate;
        endDate = _endDate;
        startPrice = _startPrice;
        require(_startPrice > 0, "Your start price must be greater than zero!");
        require(
            _endDate > _startDate,
            "The auction must end after the start date!"
        );
        decreaseRate = _startPrice / (_endDate - _startDate);
        tokenAsset = IERC20(_tokenAsset);
        auction_state = AUCTION_STATE.OPEN;
    }

    /**
     @notice Get the current price of the auction based on the startPrice, decreaseRate and elapsedTime
     @dev make sure the decreaseRate is positive otherwise price will increase
    */
    function get_auction_state() public view returns (AUCTION_STATE) {
        return auction_state;
    }

    /**
     @notice Get the current price of the auction based on the startPrice, decreaseRate and elapsedTime
     @dev make sure the decreaseRate is positive otherwise price will increase
    */
    function get_price() public view returns (uint256) {
        require(auction_state == AUCTION_STATE.OPEN, "The auction is closed!");
        uint256 elapsedTime = block.timestamp - startDate;
        return startPrice - decreaseRate * elapsedTime;
    }

    function getBalanceToken() external view returns (uint256) {
        return tokenAsset.balanceOf(address(this));
    }

    /**
     @notice Allows the users to bid for the itens in auction and be refunded if they bidded too much
     @dev 
    */
    function bid() external payable {
        require(auction_state == AUCTION_STATE.OPEN, "The auction is closed!");
        // Check if the auction is still hapenning
        // Get the the current price
        uint256 currentPrice = get_price();
        // Check if the value of the msg is higher or equal to the current price
        require(
            msg.value >= currentPrice,
            "This does not match the current price!"
        );
        tokenAsset.transferFrom(
            seller,
            msg.sender,
            tokenAsset.balanceOf(seller)
        );
        // We refund the difference between the price and the value
        uint256 refund = msg.value - currentPrice;
        if (refund > 0) {
            payable(msg.sender).transfer(refund);
        }
        emit AuctionEnded(msg.sender, currentPrice);
        seller.transfer(address(this).balance);

        auction_state = AUCTION_STATE.CLOSED;
    }
}
