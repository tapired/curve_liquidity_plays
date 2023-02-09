import brownie
import pytest
from utils import convert_to_string

#def test_steth_thingies(steth, wsteth, user, steth_pool_lp_token, steth_pool, transfer_eth, steth_oracle_reporter, oracle_1, oracle_2, oracle_3, oracle_4, oracle_5):
    # assert user.balance() == 200 * 1e18 # 200 eth, starts with 100 eth and 100 eth from whale!
    # steth.approve(steth_pool, 2**256 - 1, {'from':user})
    # steth_pool_lp_token.approve(steth_pool, 2**256 - 1, {'from':user})

    # #user.transfer(wsteth, "100 ether") ## send 100 ether to wsteth 
    # steth.submit(brownie.ZERO_ADDRESS, {"from" :user, "value":"10 ether"})
    # steth_bal_user = steth.balanceOf(user)
    # print("User steth balance before", steth_bal_user)
    
    # report_rewards = 5034300466842392
    # epoch_id = steth_oracle_reporter.getExpectedEpochId()
    # validators = 151282

    # steth_pool.add_liquidity([0, steth_bal_user / 10], 0, {'from':user})
    # print("User steth balance after adding 10 to LP", steth.balanceOf(user))
    # user_lp_bal = steth_pool_lp_token.balanceOf(user)

    # estimated_steth_withdrawal = steth_pool.calc_withdraw_one_coin(user_lp_bal, 1)

    # print("User estimated steth balance after immediate withdraw", estimated_steth_withdrawal)

    # steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_1})
    # steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_2})
    # steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_3})
    # steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_4})
    # steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_5})

    # print("User steth balance after oracle reports (it was 90 before)", steth.balanceOf(user))

    # estimated_steth_withdrawal = steth_pool.calc_withdraw_one_coin(user_lp_bal, 1)
    # tx = steth_pool.remove_liquidity_one_coin(user_lp_bal, 1, 0, {'from':user})
    # assert steth_pool_lp_token.balanceOf(user) == 0 # all burned

    # print("User estimated steth balance after oracle thingies", estimated_steth_withdrawal)
    # print("User steth balance", steth.balanceOf(user))
    # print("Withdrawn steth", tx.return_value)  

def test_steth_balanced_liquidity(RELATIVE_APPROX, steth, wsteth, user, steth_pool_lp_token, steth_pool, steth_oracle_reporter, oracle_1, oracle_2, oracle_3, oracle_4, oracle_5):
    received_lp = add_liquidity_balanced_amounts(RELATIVE_APPROX, steth, user, steth_pool_lp_token, steth_pool, 10*1e18)

    withdrawn_amounts = steth_pool.remove_liquidity(received_lp, [0,0], {'from':user})

    print("After removing liquidity balanced eth and steth withdrawn", withdrawn_amounts.return_value)
    #assert pytest.approx(eth_amount, rel=RELATIVE_APPROX) == withdrawn_amounts.return_value[0]
    #assert pytest.approx(steth_amount, rel=RELATIVE_APPROX) == withdrawn_amounts.return_value[1]

def test_steth_balanced_liquidity_steth_grow(RELATIVE_APPROX, steth, wsteth, user, steth_pool_lp_token, steth_pool, steth_oracle_reporter, oracle_1, oracle_2, oracle_3, oracle_4, oracle_5):
    received_lp = add_liquidity_balanced_amounts(RELATIVE_APPROX, steth, user, steth_pool_lp_token, steth_pool, 10*1e18)

    report_rewards = 5034300466842392
    epoch_id = steth_oracle_reporter.getExpectedEpochId()
    validators = 151282
    
    user_steth_idle_bal = steth.balanceOf(user)
    print("User idle steth bal before", user_steth_idle_bal)
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_1})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_2})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_3})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_4})
    steth_oracle_reporter.reportBeacon(epoch_id, report_rewards, validators, {"from": oracle_5})
    print("User idle steth bal after oracle report", steth.balanceOf(user))

    withdrawn_amounts = steth_pool.remove_liquidity(received_lp, [0,0], {'from':user})

    print("After removing liquidity balanced eth and steth withdrawn", withdrawn_amounts.return_value)






## HELPERS ##

def add_liquidity_balanced_amounts(RELATIVE_APPROX, steth, user, steth_pool_lp_token, steth_pool, position_size_in_eth):
    steth.approve(steth_pool, 2**256 - 1, {'from':user})
    steth_pool_lp_token.approve(steth_pool, 2**256 - 1, {'from':user})

    steth.submit(brownie.ZERO_ADDRESS, {"from" :user, "value":"20 ether"})
    steth_bal_user = steth.balanceOf(user)
    assert steth_bal_user > 0
    print("User steth balance before", steth_bal_user)
    
    bal_0 = steth_pool.balances(0)
    bal_1 = steth_pool.balances(1)
    total_bal = bal_0 + bal_1

    eth_amount = (position_size_in_eth * bal_0) / total_bal
    steth_amount = (position_size_in_eth * bal_1) / total_bal

    eth_amount = convert_to_string(eth_amount)
    steth_amount = convert_to_string(steth_amount)

    print(f"Adding liquidity in these amounts: ETH amount {eth_amount} Steth amount {steth_amount}")
    steth_pool.add_liquidity([eth_amount, steth_amount], 0, {'from':user, 'value':eth_amount})
    user_lp_bal = steth_pool_lp_token.balanceOf(user)
    assert user_lp_bal > 0
    print("Received LP", user_lp_bal)

    return user_lp_bal


