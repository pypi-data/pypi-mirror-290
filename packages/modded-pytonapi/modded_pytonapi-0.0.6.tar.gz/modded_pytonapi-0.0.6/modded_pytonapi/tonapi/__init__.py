from modded_pytonapi.tonapi.client import TonapiClient
from modded_pytonapi.tonapi.methods.accounts import AccountMethod
from modded_pytonapi.tonapi.methods.blockchain import BlockchainMethod
from modded_pytonapi.tonapi.methods.dns import DnsMethod
from modded_pytonapi.tonapi.methods.events import EventMethod
from modded_pytonapi.tonapi.methods.jettons import JettonMethod
from modded_pytonapi.tonapi.methods.nft import NftMethod
from modded_pytonapi.tonapi.methods.rates import RateMethod
from modded_pytonapi.tonapi.methods.staking import StakingMethod
from modded_pytonapi.tonapi.methods.storage import StorageMethod
from modded_pytonapi.tonapi.methods.traces import TraceMethod


class Tonapi(TonapiClient):

    def __init__(self, api_key: str, testnet: bool = False, max_retries: int = 3):
        """
        :param api_key: You can get an API key here https://tonconsole.com/
        :param testnet: Use true, if you want to switch to testnet
        :param max_retries: Maximum number of retries per request if rate limit is reached
        """
        super().__init__(api_key, testnet, max_retries)

    @property
    def blockchain(self) -> BlockchainMethod:
        return BlockchainMethod(self._api_key, self._testnet, self._max_retries)

    @property
    def accounts(self) -> AccountMethod:
        return AccountMethod(self._api_key, self._testnet, self._max_retries)

    @property
    def jettons(self) -> JettonMethod:
        return JettonMethod(self._api_key, self._testnet, self._max_retries)

    @property
    def dns(self) -> DnsMethod:
        return DnsMethod(self._api_key, self._testnet, self._max_retries)

    @property
    def events(self) -> EventMethod:
        return EventMethod(self._api_key, self._testnet, self._max_retries)

    @property
    def nft(self) -> NftMethod:
        return NftMethod(self._api_key, self._testnet, self._max_retries)

    @property
    def rates(self) -> RateMethod:
        return RateMethod(self._api_key, self._testnet, self._max_retries)

    @property
    def staking(self) -> StakingMethod:
        return StakingMethod(self._api_key, self._testnet, self._max_retries)

    @property
    def storage(self) -> StorageMethod:
        return StorageMethod(self._api_key, self._testnet, self._max_retries)

    @property
    def traces(self) -> TraceMethod:
        return TraceMethod(self._api_key, self._testnet, self._max_retries)
