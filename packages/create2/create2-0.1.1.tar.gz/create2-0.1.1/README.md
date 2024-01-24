# README for create2

## Overview

This Python library is used to implement the create2 function of smart contracts through Python code, thereby achieving
the goal of predicting smart contract addresses and deploying smart contracts.

## Features

- **Address Prediction**: Predicts contract addresses based on chain ID, salt, and initialization code.
- **Deployment**: Simplifies the process of deploying contracts to Ethereum-based blockchains.

## Principle

- The implementation principle is to deploy factory contracts on various EVM public chains in advance, to achieve the
  native create2 function of Python. A factory contract only needs to be deployed once on each public chain. After
  deployment, it is only necessary to update the corresponding chain ID and factory contract address in the
  factory_mapping
  dictionary of this library.
- If you want to add support for a public chain not in the factory_mapping, please deploy the factory
  contract source code from the contracts in the library to the public chain you need, and then use it by submitting a
  PR
  or through monkey patching.

## Requirements

- web3

## Installation

Install the package using pip:

```bash
pip install create2
```

## Usage

### Predicting an Address

```python
from create2 import predict_address

predict_address(chain_id, salt, init_code)
```

- `chain_id`: The chain ID.
- `salt`: A hexadecimal string used as a salt.
- `init_code`: Hexadecimal string representing the contract's initialization code.

### Getting Transaction Params

If you want to deploy the contract by hand, you can get the transaction params first.

```python
from create2 import get_deploy_tx_params

get_deploy_tx_params(chain_id, salt, init_code, private_key, nonce, endpoint_uri)
```

- `chain_id`: The chain ID.
- `salt`: A hexadecimal string used as a salt.
- `init_code`: Hexadecimal string representing the contract's initialization code.
- `private_key`: Private key for signing the transaction.
- `nonce`: Transaction nonce.
- `endpoint_uri`: Endpoint URI of the blockchain node.

### Deploying a Contract

```python
from create2 import deploy

deploy(chain_id, salt, init_code, private_key, nonce, endpoint_uri)
```

- `chain_id`: The chain ID.
- `salt`: A hexadecimal string used as a salt.
- `init_code`: Hexadecimal string representing the contract's initialization code.
- `private_key`: Private key for signing the transaction.
- `nonce`: Transaction nonce.
- `endpoint_uri`: Endpoint URI of the blockchain node.

## Supported Chains

- Ethereum (ETH)
- Binance Smart Chain (BSC)
- Polygon
- BSC Testnet
- Ethereum Testnet (Sepolia)
- And more coming...

## Example

```python
from create2 import deploy

# Deploy a contract
tx_hash = deploy(
    chain_id=1,
    salt="0x123...",
    init_code="0x456...",
    private_key="0xABC...",
    nonce=0,
    endpoint_uri="https://mainnet.infura.io/v3/YOUR_PROJECT_ID"
)
print(f"Transaction Hash: {tx_hash}")
```

## Contact

For additional support or to request new features, please contact the community.

## License

[MIT License](LICENSE)

---