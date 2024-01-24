import eth_abi
from eth_typing.evm import HexAddress
from web3 import Web3
from web3.exceptions import ExtraDataLengthError
from web3.middleware import geth_poa_middleware
from web3.types import HexStr, TxParams
from web3.utils.address import get_create2_address

from .exceptions import InvalidChainIDException

mapping = {
    1: HexStr("0x54F5A04417E29FF5D7141a6d33cb286F50d5d50e"),  # ETH
    56: HexStr("0x54F5A04417E29FF5D7141a6d33cb286F50d5d50e"),  # BSC
    137: HexStr("0x54F5A04417E29FF5D7141a6d33cb286F50d5d50e"),  # Polygon
    97: HexStr("0x9Dd64C6cC93dDb9719d43815fE8017174f29475d"),  # BSC Testnet
    11155111: HexStr("0x9Dd64C6cC93dDb9719d43815fE8017174f29475d"),  # ETH Testnet(Sepolia)
}


def is_poa(w3: Web3) -> bool:
    try:
        w3.eth.get_block("latest")
        return False

    except ExtraDataLengthError:
        return True


def is_chain_valid(chain_id: int) -> bool:
    return chain_id in mapping


def predict_address(chain_id: int, salt: HexStr, init_code: HexStr):
    if not is_chain_valid(chain_id):
        raise InvalidChainIDException("当前 Chain 暂不支持，如有需要请联系社区.")

    return get_create2_address(HexAddress(mapping[chain_id]), salt, init_code)


def get_deploy_tx_params(
    chain_id: int,
    salt: HexStr,
    init_code: HexStr,
    private_key: HexStr,
    nonce: int,
    endpoint_uri: str,
) -> TxParams:
    if not is_chain_valid(chain_id):
        raise InvalidChainIDException("当前 chain_id 暂不支持，如有需要请联系社区.")

    w3 = Web3(Web3.HTTPProvider(endpoint_uri))
    if is_poa(w3):
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    if w3.eth.chain_id != chain_id:
        raise InvalidChainIDException("chain_id 与 endpoint_uri 不匹配.")

    encoded_params = eth_abi.encode(
        ["bytes", "uint256"],
        [
            bytes.fromhex(init_code),
            int.from_bytes(bytes.fromhex(salt), byteorder="big"),
        ],
    )
    transaction: TxParams = {
        "chainId": chain_id,
        "nonce": nonce,
        "from": w3.eth.account.from_key(private_key).address,
        "to": mapping[chain_id],
        "value": 0,
        "gas": 320_000,
        "gasPrice": w3.eth.gas_price,
        "data": "0x9c4ae2d0" + encoded_params.hex(),
    }

    return transaction


def deploy(
    chain_id: int,
    salt: HexStr,
    init_code: HexStr,
    private_key: HexStr,
    nonce: int,
    endpoint_uri: str,
):
    tx_params = get_deploy_tx_params(
        chain_id=chain_id,
        salt=salt,
        init_code=init_code,
        private_key=private_key,
        nonce=nonce,
        endpoint_uri=endpoint_uri,
    )

    w3 = Web3(Web3.HTTPProvider(endpoint_uri))
    signed_transaction = w3.eth.account.sign_transaction(tx_params, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    return tx_hash
