# smart-contract-lottery
This contract was deployed at Kovan testnet!
Contract address: 0xe49CfD3A5D88A504D360ea83515834F9c660dE31 (https://kovan.etherscan.io/address/0xe49cfd3a5d88a504d360ea83515834f9c660de31)

# Lesson 7: [SmartContract Lottery](https://www.youtube.com/watch?v=M576WGiDBdQ&t=22298s)
💻 Code: https://github.com/rsaSantos/smart-contract-lottery

### Introduction
- Add a `README.md`
- Defining the project
- Is it decentralized?
### `Lottery.sol`
- basic setup
- Main Functions
- address payable[]
- getEntranceFee & Setup
  - [Chainlink Price Feed](https://docs.chain.link/docs/get-the-latest-price/)
  - brownie-config
  - SPDX
- Matching Units of Measure
  - Can't just divide
- Test early and often
- Quick Math Sanity Check
- deleting networks
- [Alchemy](https://www.alchemy.com/) again
- Enum
- `startLottery`
- [Openzeppelin](https://openzeppelin.com/contracts/)... Is this the first openzeppelin reference? 
- [Openzeppelin Contracts Github](https://github.com/OpenZeppelin/openzeppelin-contracts)
- Randomness
- Pseudorandomness
- `block` keyword
  - `block.difficulty`
  - `block.timestamp`
- `keccack256`
- [True Randomness with Chainlink VRF](https://docs.chain.link/docs/get-a-random-number/)
- Chainlink VRF Remix Version
- Inheriting Constructors
- Oracle Gas & Transaction Gas
- [Why didn't we pay gas on the price feeds?](https://ethereum.stackexchange.com/questions/87473/is-chainlinks-price-reference-data-free-to-consume)
- Chainlink Node Fees
- [Request And Receive Introduction](https://docs.chain.link/docs/architecture-request-model/)
- [Kovan Faucets](https://docs.chain.link/docs/link-token-contracts/#kovan)
- Funding Chainlink Contracts
- [Request And Receive Explanation](https://docs.chain.link/docs/architecture-request-model/)
- A Clarification
- `endLottery`
- `returns (type variableName)`
- `fulfillRandomness`
- `override`
- Modulo Operation (Mod Operation %)
- Paying the lottery winner
- Resetting the lottery
### Testing Lottery.sol
- `deploy_lottery.py`
- `get_account()` refactored
- `get_contract`
  - `contract_to_mock`
  - `Contract.from_abi`
- Adding the parameters to deploying to lottery
- `vrfCoordinatorMock` and adding mocks
- `LinkToken` and Mocks
- Successful Ganache Deployment!
- Python Lottery Scripts/Functions
  - `start_lottery`
  - Brownie tip: Remember to `tx.wait(1)` your last transaction
  - `enter_lottery`
  - `end_lottery`
- Funding with LINK
- brownie interfaces
- Waiting for callback
- Integration Tests & Unit Tests
- Test all lines of code
- `test_get_entrance_fee`
- `pytest.skip` (again)
- `test_cant_enter_unless_started`
- `test_can_start_and_enter_lottery`
- `test_can_pick_winner_correctly`
- Events and Logs
- `callBackWithRandomness`
### Lottery.sol Testnet Deployment
- `topics`
- - [conftest.py](https://stackoverflow.com/questions/34466027/in-pytest-what-is-the-use-of-conftest-py-files)
