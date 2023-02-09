import pytest
from brownie import config
from brownie import Contract


@pytest.fixture
def deployer(accounts):
    yield accounts[0]


@pytest.fixture
def user(accounts):
    yield accounts[1]

@pytest.fixture(scope="session")
def RELATIVE_APPROX():
    yield 1e-10

@pytest.fixture
def steth():
    steth_address = Contract("0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")
    yield steth_address

@pytest.fixture
def wsteth():
    wsteth_address = Contract("0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0")
    yield wsteth_address

@pytest.fixture
def transfer_eth(accounts, user):
    amount = 100 * 1e18 # 100 ether
    whale_address = accounts.at("0xbF3aEB96e164ae67E763D9e050FF124e7c3Fdd28", force=True)
    whale_address.transfer(user, "100 ether")
    yield whale_address


@pytest.fixture
def steth_pool_gauge():
    steth_pool_gauge_address = Contract("0x182b723a58739a9c974cfdb385ceadb237453c28")
    yield steth_pool_gauge_address

@pytest.fixture
def steth_pool():
    steth_pool_address = Contract("0xDC24316b9AE028F1497c275EB9192a3Ea0f67022")
    yield steth_pool_address

@pytest.fixture
def steth_pool_lp_token():
    steth_pool_lp_token_address = Contract("0x06325440d014e39736583c165c2963ba99faf14e")
    yield steth_pool_lp_token_address


## steth 
@pytest.fixture
def steth_oracle_reporter():
    steth_oracle_reporter_address = Contract("0x442af784A788A5bd6F42A01Ebe9F287a871243fb")
    yield steth_oracle_reporter_address

## steth 
@pytest.fixture
def oracle_1(accounts):
    oracle_1_address = accounts.at("0x140Bd8FbDc884f48dA7cb1c09bE8A2fAdfea776E", force=True)
    yield oracle_1_address

@pytest.fixture
def oracle_2(accounts):
    oracle_2_address = accounts.at("0x1d0813bf088BE3047d827D98524fBf779Bc25F00", force=True)
    yield oracle_2_address

@pytest.fixture
def oracle_3(accounts):
    oracle_3_address = accounts.at("0x404335BcE530400a5814375E7Ec1FB55fAff3eA2", force=True)
    yield oracle_3_address

@pytest.fixture
def oracle_4(accounts):
    oracle_4_address = accounts.at("0x946D3b081ed19173dC83Cd974fC69e1e760B7d78", force=True)
    yield oracle_4_address

@pytest.fixture
def oracle_5(accounts):
    oracle_5_address = accounts.at("0x007DE4a5F7bc37E2F26c0cb2E8A95006EE9B89b5", force=True)
    yield oracle_5_address
