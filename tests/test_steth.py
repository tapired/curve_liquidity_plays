import brownie
import pytest
from utils import convert_to_string

def test_steth_single_sided_liquidity(RELATIVE_APPROX, steth, wsteth, user, steth_pool_lp_token, steth_pool):
    add_liquidity_single_sided(RELATIVE_APPROX, steth, user, steth_pool_lp_token, steth_pool)

    withdrawn_steth = steth_pool.remove_liquidity_one_coin(steth_pool_lp_token.balanceOf(user), 1, 0, {'from':user})
    print("User steth amount after removen single sided to steth", withdrawn_steth.return_value)


def test_steth_single_sided_liquidity_steth_grow(RELATIVE_APPROX, steth, wsteth, user, steth_pool_lp_token, steth_pool, steth_oracle_reporter, oracle_1, oracle_2, oracle_3, oracle_4, oracle_5):
    steth_added_lp = add_liquidity_single_sided(RELATIVE_APPROX, steth, user, steth_pool_lp_token, steth_pool)
    
    report_rewards = 5069123824661090
    epoch_id = steth_oracle_reporter.getExpectedEpochId()
    validators = 151444
    
    user_steth_idle_bal = steth.balanceOf(user)
    print("User idle steth bal before", user_steth_idle_bal)

    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_1})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_2})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_3})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_4})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_5})

    user_steth_idle_bal_after = steth.balanceOf(user)
    print("User idle steth bal after oracle report", user_steth_idle_bal_after)
    
    withdrawn_steth = steth_pool.remove_liquidity_one_coin(steth_pool_lp_token.balanceOf(user), 1, 0, {'from':user})

    predicted_steth_withdrawable_from_lp = (steth_added_lp * user_steth_idle_bal_after) / user_steth_idle_bal

    print("After removing liquidity single sided to steth balance", withdrawn_steth.return_value)
    print("Predicted withdrawable steth after steth growing in pool", convert_to_string(predicted_steth_withdrawable_from_lp))


def test_steth_balanced_liquidity(RELATIVE_APPROX, steth, wsteth, user, steth_pool_lp_token, steth_pool):
    received_lp, x = add_liquidity_balanced_amounts(RELATIVE_APPROX, steth, user, steth_pool_lp_token, steth_pool, 10*1e18)

    withdrawn_amounts = steth_pool.remove_liquidity(received_lp, [0,0], {'from':user})

    print("After removing liquidity balanced eth and steth withdrawn", withdrawn_amounts.return_value)
    #assert pytest.approx(eth_amount, rel=RELATIVE_APPROX) == withdrawn_amounts.return_value[0]
    #assert pytest.approx(steth_amount, rel=RELATIVE_APPROX) == withdrawn_amounts.return_value[1]

def test_steth_balanced_liquidity_steth_grow(RELATIVE_APPROX, steth, wsteth, user, steth_pool_lp_token, steth_pool, steth_oracle_reporter, oracle_1, oracle_2, oracle_3, oracle_4, oracle_5):
    received_lp, steth_added_lp = add_liquidity_balanced_amounts(RELATIVE_APPROX, steth, user, steth_pool_lp_token, steth_pool, 10*1e18)

    report_rewards = 5069123824661090
    epoch_id = steth_oracle_reporter.getExpectedEpochId()
    validators = 151444
    
    user_steth_idle_bal = steth.balanceOf(user)
    print("User idle steth bal before", user_steth_idle_bal)

    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_1})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_2})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_3})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_4})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_5})

    user_steth_idle_bal_after = steth.balanceOf(user)
    print("User idle steth bal after oracle report", user_steth_idle_bal_after)
    
    withdrawn_amounts = steth_pool.remove_liquidity(received_lp, [0,0], {'from':user})

    predicted_steth_withdrawable_from_lp = (steth_added_lp * user_steth_idle_bal_after) / user_steth_idle_bal

    print("After removing liquidity balanced eth and steth withdrawn", withdrawn_amounts.return_value)
    print("Predicted withdrawable steth after steth growing in pool", convert_to_string(predicted_steth_withdrawable_from_lp))





## HELPERS ##

def add_liquidity_balanced_amounts(RELATIVE_APPROX, steth, user, steth_pool_lp_token, steth_pool, position_size_in_eth):
    steth.approve(steth_pool, 2**256 - 1, {'from':user})
    steth_pool_lp_token.approve(steth_pool, 2**256 - 1, {'from':user})

    steth.submit(brownie.ZERO_ADDRESS, {"from" :user, "value":"20 ether"})
    steth_bal_user = steth.balanceOf(user)
    assert steth_bal_user > 0
    
    bal_0 = steth_pool.balances(0)
    bal_1 = steth_pool.balances(1)
    total_bal = bal_0 + bal_1

    eth_amount = (position_size_in_eth * bal_0) / total_bal
    steth_amount = (position_size_in_eth * bal_1) / total_bal

    eth_amount = convert_to_string(eth_amount)
    steth_amount_string = convert_to_string(steth_amount)

    print(f"Adding liquidity in these amounts: ETH amount {eth_amount} Steth amount {steth_amount_string}")
    tx = steth_pool.add_liquidity([eth_amount, steth_amount_string], 0, {'from':user, 'value':eth_amount})
    user_lp_bal = steth_pool_lp_token.balanceOf(user)
    assert user_lp_bal > 0
    print("Received LP", user_lp_bal)
    print("Events of add liquidity", tx.events["AddLiquidity"]["fees"])

    return user_lp_bal, steth_amount


def add_liquidity_single_sided(RELATIVE_APPROX, steth, user, steth_pool_lp_token, steth_pool):
    steth.approve(steth_pool, 2**256 - 1, {'from':user})
    steth_pool_lp_token.approve(steth_pool, 2**256 - 1, {'from':user})
    
    steth.submit(brownie.ZERO_ADDRESS, {"from" :user, "value":"20 ether"})
    steth_bal_user = steth.balanceOf(user)
    assert steth_bal_user > 0

    steth_amount = steth_bal_user / 2

    tx = steth_pool.add_liquidity([0, steth_amount], 0, {'from':user})
    print("Fees paid for single sided liquidity added with only steth", tx.events["AddLiquidity"]["fees"])
    
    return steth_amount

