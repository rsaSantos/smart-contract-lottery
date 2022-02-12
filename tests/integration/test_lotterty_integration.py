# This test will run on Kovan testnet

from brownie import network  # type: ignore
import pytest
from scripts.helpfull_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
)
from scripts.deploy_lottery import deploy_lottery
import time


def test_can_pick_winner():
    # Skip if we're not in local development network, skip test.
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account(id="solidity-learn")
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(60)  # wait for chainlink response
    assert lottery.recentWinner() == account  # we were the only ones participating...
    assert lottery.balance() == 0
