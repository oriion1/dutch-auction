//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DummyDummy is ERC20 {
    uint256 constant _initial_supply = 10 * (10**18);

    constructor() public ERC20("DummyDummy", "DD") {
        _mint(msg.sender, _initial_supply);
    }
}
