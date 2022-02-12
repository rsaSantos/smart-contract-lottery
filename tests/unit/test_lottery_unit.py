# Test the Lottery contract.

# Imports
from web3 import Web3
from brownie import accounts, config, network, Lottery, exceptions  # type: ignore
from scripts.deploy_lottery import deploy_lottery
from scripts.helpfull_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
    fund_with_link,
)
import pytest


def skip_if_not_dev_net():
    # Skip if we're not in local development network, skip test.
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()


def test_get_entrance_fee():
    # Old test..
    #
    # account = accounts[0]
    # lottery = Lottery.deploy(
    #     config["networks"][network.show_active()]["eth_usd_price_feed"],
    #     {"from": account},
    # )
    #
    # Assertion based on todays price (12/02/2022)
    # We want the minimum entrance fee to be around 10$.
    # This is not a good way to test the contract, it's just a quick fact-check.
    # assert lottery.getEntranceFee() > Web3.toWei(0.003, "ether")
    # assert lottery.getEntranceFee() > Web3.toWei(0.004, "ether")

    # Skip if we're not in local development network, skip test.
    skip_if_not_dev_net()

    # New tests - better format
    #
    # Arrange
    lottery = deploy_lottery()
    # Act
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee


# Only allow entrance if lottery started!
def test_cant_enter_unless_starter():
    # Skip if we're not in local development network, skip test.
    skip_if_not_dev_net()

    # Arrange
    lottery = deploy_lottery()
    # Act
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


# Can we enter the lottery?
def test_can_start_enter_lottery():
    # Skip if we're not in local development network, skip test.
    skip_if_not_dev_net()

    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": get_account()})
    # Act
    lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account


# Can we end the lottery?
def test_can_end_lottery():
    # Skip if we're not in local development network, skip test.
    skip_if_not_dev_net()

    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": get_account()})
    lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})
    # Act
    fund_with_link(lottery)
    lottery.endLottery({"from": get_account()})
    # Assert
    assert (
        lottery.lottery_state() == 2
    )  # In respect with the enum used in the Lottery.sol


# Do we choose and reward the winner correctly?
def test_can_pick_winner_correctly():
    # Skip if we're not in local development network, skip test.
    skip_if_not_dev_net()

    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": get_account()})
    lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    # Act
    transcation = lottery.endLottery({"from": get_account()})
    request_Id = transcation.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777  # Our "random" number! Since we're only testing locally.
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_Id, STATIC_RNG, lottery.address, {"from": get_account()}
    )
    # Assert
    starting_balanc_of_account = account.balance()
    balance_lottery = lottery.balance()
    # 777 % 3 = 0 -> Selected player is players(0)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balanc_of_account + balance_lottery


# Improve the copy pasting...
