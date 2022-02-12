# Deploy the lottery contract.

from scripts.helpfull_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, config, network  # type: ignore
import time


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify", False
        ),  # if there is no verify key, set to false
    )
    print("Deployed Lottery!")
    return lottery


# Start the lottery.
def start_lottery():
    account = get_account()  # Has to be the owner!
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery has started!")


# Enter the lottery.
def enter_lottery():
    account = get_account()  # Anyone can enter...
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000  # Why add?
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")


# End the lottery.
def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # Fund the contract with LINK
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(60)  # Wait for the winner to be chosen!
    # If we're testing locally, there will be no Chainlink node to answer the request!
    # So the winner will be 0x00000000000..., since the recent winner variable wasn't changed!
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
