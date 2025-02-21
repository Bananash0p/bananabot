import asyncio

from solana.keypair import Keypair
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey


def generate_solana_address():
    deposit_keypair = Keypair.generate()
    deposit_address = deposit_keypair.public_key
    return deposit_address, deposit_keypair.secret_key


RPC_ENDPOINT = "https://api.mainnet-beta.solana.com"

async def verify_payment(expected_amount: int, deposit_address: str, timeout: int = 500):
    """
    Monitors a unique deposit address for a payment.

    expected_amount: Minimum amount (in lamports) expected.
    deposit_address: The unique deposit address as a string.
    timeout: Maximum time in seconds to wait.

    return: Transaction signature if a valid transaction is detected, else None.
    """
    client = AsyncClient(RPC_ENDPOINT)
    address = PublicKey(deposit_address)
    start_time = asyncio.get_event_loop().time()

    while (asyncio.get_event_loop().time() - start_time) < timeout:
        sig_resp = await client.get_signatures_for_address(address)
        if sig_resp.get("result"):
            for sig_info in sig_resp["result"]:
                tx_signature = sig_info["signature"]
                tx_resp = await client.get_transaction(tx_signature, commitment="finalized")
                if not tx_resp.get("result"):
                    continue

                tx_details = tx_resp["result"]
                meta = tx_details.get("meta", {})
                pre_balances = meta.get("preBalances", [])
                post_balances = meta.get("postBalances", [])

                if pre_balances and post_balances:
                    amount_received = post_balances[0] - pre_balances[0]
                    if amount_received >= expected_amount:
                        await client.close()
                        return tx_signature
        await asyncio.sleep(5)

    await client.close()
    return None

# testing
if __name__ == "__main__":
    expected_lamports = 1000000 
    deposit_address, secret_key = generate_solana_address()
    deposit_address_str = str(deposit_address)  

    loop = asyncio.get_event_loop()
    tx_signature = loop.run_until_complete(verify_payment(expected_lamports, deposit_address_str))
    if tx_signature:
        print(f"Payment confirmed with transaction: {tx_signature}")
    else:
        print("Payment not detected within the timeout period.")

