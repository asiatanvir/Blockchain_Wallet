# Cryptocurrency Wallet
################################################################################

# This file contains the Ethereum transaction functions that you have created throughout this module’s lessons.
# By using import statements, you will integrate this `crypto_wallet.py` Python script
# into the KryptoJobs2Go interface program that is found in the `krypto_jobs.py` file.

################################################################################
# Imports
import os
import requests
from dotenv import load_dotenv

load_dotenv()
from bip44 import Wallet
from web3 import Account, Web3
from web3 import middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy


w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
################################################################################
# Wallet functionality


def generate_account():
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""
    # Fetch mnemonic from environment variable.
    mnemonic = os.getenv("MNEMONIC")

    # Create Wallet Object
    wallet = Wallet(mnemonic)

    # Derive Ethereum Private Key
    private, public = wallet.derive_account("eth")

    # Convert private key into an Ethereum account
    account = Account.privateKeyToAccount(private)

    return account


def get_balance(w3, address):
    """Using an Ethereum account address access the balance of Ether"""
    # Get balance of address in Wei
    wei_balance = w3.eth.get_balance(address)

    # Convert Wei value to ether
    ether = w3.fromWei(wei_balance, "ether")

    # Return the value in ether
    return ether


def send_transaction( w3, account, to, wage):
    """Send an authorized transaction to the Ganache blockchain."""
    # Set gas price strategy
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

    # Convert eth amount to Wei
    value = w3.toWei(wage, "ether")

    # Calculate gas estimate
    gasEstimate = w3.eth.estimateGas(
        {"to": to, "from": account.address, "value": value}
    )

    # Construct a raw transaction
    raw_tx = {
        "to": to,
        "from": account.address,
        "value": value,

        "gas": gasEstimate,
        "gasPrice": w3.eth.gas_price ,
        "nonce": w3.eth.getTransactionCount(account.address)
    }

    # # Sign the raw transaction with ethereum account
    signed_tx = account.signTransaction(raw_tx)

    # # Send the signed transactions
    return w3.eth.sendRawTransaction(signed_tx.rawTransaction)

#     def send_transaction(w3, account, receiver, wage):

#     # """Send an authorized transaction."""
#     # Change account to string type:
#     # acct_str = str(account.address)
#     # print(f'======= Here is the account address {acct_str } =======')
    

#     # Convert eth amount to Wei
#          wei_value = w3.toWei(wage, "ether")

# # ==============================================
#          tx_hash = w3.eth.send_transaction({
#          "from": acct_str,
#          "to": receiver,
#          "value": wei_value
#     })

#          tx = w3.eth.get_transaction(tx_hash)
#          assert tx["from"] == acct_str

#     return tx_hash

# # ===============================================
#     # # Calculate gas estimate
#     # # Set a medium gas price strategy
#     # w3.eth.set_gas_price_strategy(medium_gas_price_strategy)

#     # gas_estimate = w3.eth.estimateGas({"to": receiver, "from": account.address, "value": wei_value})

#     # # Construct a raw transaction
#     # raw_tx = {
#     #     "to": receiver,
#     #     # "maxFeePerGas": 2000000000,
#     #     # "maxPriorityFeePerGas": 1000000000,
#     #     "value": wei_value,
#     #     "gas": gas_estimate,
#     #     "nonce": w3.eth.get_transaction_count(account.address)
#     # }

#     # # Sign the raw transaction with ethereum account private key
#     # signed_tx = account.sign_transaction(raw_tx, account)

#     # # Send the signed transactions
#     # tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction) # Returns Transaction Hash
#     # print(f'Sent Tx Hash = {tx_hash}')
#     # return tx_hash

