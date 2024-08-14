import base64
import json

import httpx
import requests
from cashu.core.models import GetInfoResponse, MintMeltMethodSetting
from cashu.mint.ledger import Ledger
from cashu.nostr.key import PublicKey, PrivateKey
from cashu.wallet.wallet import Wallet

from nostr_dvm.utils.database_utils import get_or_add_user
from nostr_dvm.utils.zap_utils import create_bolt11_ln_bits, create_bolt11_lud16

BASE_URL = "https://mint.minibits.cash/Bitcoin"


async def test_create_p2pk_pubkey(wallet1: Wallet):
    invoice = await wallet1.request_mint(64)
    # await pay_if_regtest(invoice.bolt11)
    await wallet1.mint(64, id=invoice.id)
    pubkey = await wallet1.create_p2pk_pubkey()
    PublicKey(bytes.fromhex(pubkey), raw=True)


async def cashu_wallet():
    wallet1 = await Wallet.with_db(
        url=BASE_URL,
        db="db/Cashu",
        name="wallet_mint_api",
    )
    await wallet1.load_mint()
    return wallet1


async def test_info(ledger: Ledger):
    response = httpx.get(f"{BASE_URL}/v1/info")
    assert response.status_code == 200, f"{response.url} {response.status_code}"
    assert ledger.pubkey
    assert response.json()["pubkey"] == ledger.pubkey.serialize().hex()
    info = GetInfoResponse(**response.json())
    assert info.nuts
    assert info.nuts[4]["disabled"] is False
    setting = MintMeltMethodSetting.parse_obj(info.nuts[4]["methods"][0])
    assert setting.method == "bolt11"
    assert setting.unit == "sat"


async def get_cashu_balance(url):
    from cashu.wallet.wallet import Wallet
    from cashu.core.settings import settings

    settings.tor = False
    wallet = await Wallet.with_db(
        url=url,
        db="db/Cashu",
    )
    await wallet.load_mint()
    await wallet.load_proofs()
    print("Cashu Wallet balance " + str(wallet.available_balance) + " sats")
    mint_balances = await wallet.balance_per_minturl()
    print(mint_balances)


async def mint_cashu_test(url, amount):
    from cashu.wallet.wallet import Wallet
    from cashu.core.settings import settings

    settings.tor = False
    wallet = await Wallet.with_db(
        url=url,
        db="db/Cashu",
    )
    await wallet.load_mint()
    await wallet.load_proofs()
    print("Wallet balance " + str(wallet.available_balance) + " sats")
    mint_balances = await wallet.balance_per_minturl()
    print(mint_balances)
    # mint tokens into wallet, skip if wallet already has funds

    # if wallet.available_balance <= 10:
    #    invoice = await wallet.request_mint(amount)
    #    input(f"Pay this invoice and press any button: {invoice.bolt11}\n")
    #    await wallet.mint(amount, id=invoice.id)

    # create 10 sat token
    proofs_to_send, _ = await wallet.split_to_send(wallet.proofs, amount, set_reserved=True)
    token_str = await wallet.serialize_proofs(proofs_to_send)
    print(token_str)
    return token_str


async def receive_cashu_test(token_str):
    from cashu.wallet.wallet import Wallet
    from cashu.core.settings import settings
    from cashu.core.base import TokenV3

    token = TokenV3.deserialize(token_str)
    print(token.token[0])

    settings.tor = False
    wallet = await Wallet.with_db(
        url=token.token[0].mint,
        db="db/Cashu",
    )

    await wallet.load_mint()
    await wallet.load_proofs()

    print(f"Wallet balance: {wallet.available_balance} sats")

    try:
        await wallet.redeem(token.token[0].proofs)
        print(f"Wallet balance: {wallet.available_balance} sats")
    except Exception as e:
        print(e)


def parse_cashu(cashu_token: str):
    try:
        prefix = "cashuA"
        assert cashu_token.startswith(prefix), Exception(
            f"Token prefix not valid. Expected {prefix}."
        )
        if not cashu_token.endswith("="):
            cashu_token = str(cashu_token) + "=="
        print(cashu_token)
        token_base64 = cashu_token[len(prefix):].encode("utf-8")
        cashu = json.loads(base64.urlsafe_b64decode(token_base64))
        token = cashu["token"][0]
        proofs = token["proofs"]
        mint = token["mint"]
        total_amount = 0
        for proof in proofs:
            total_amount += proof["amount"]

        return proofs, mint, total_amount, None

    except Exception as e:
        print(e)
        return None, None, None, "Cashu Parser: " + str(e)


async def redeem_cashu(cashu, config, client, required_amount=0, update_self=False) -> (bool, str, int, int):
    proofs, mint, total_amount, message = parse_cashu(cashu)
    if message is not None:
        return False, message, 0, 0

    estimated_fees = max(int(total_amount * 0.02), 3)
    estimated_redeem_invoice_amount = total_amount - estimated_fees

    # Not sure if this the best way to go, we first create an invoice that we send to the mint, we catch the fees
    # for that invoice, and create another invoice with the amount without fees to melt.
    if config.LNBITS_INVOICE_KEY != "":
        invoice, paymenthash = create_bolt11_ln_bits(estimated_redeem_invoice_amount, config)
    else:

        user = await get_or_add_user(db=config.DB, npub=config.PUBLIC_KEY,
                                     client=client, config=config, update=update_self)
        invoice = create_bolt11_lud16(user.lud16, estimated_redeem_invoice_amount)
    print(invoice)
    if invoice is None:
        return False, "couldn't create invoice", 0, 0

    url = mint + "/checkfees"  # Melt cashu tokens at Mint
    json_object = {"pr": invoice}
    headers = {"Content-Type": "application/json; charset=utf-8"}
    request_body = json.dumps(json_object).encode('utf-8')
    request = requests.post(url, data=request_body, headers=headers)
    tree = json.loads(request.text)
    fees = tree["fee"]
    print("Fees on this mint are " + str(fees) + " Sats")
    redeem_invoice_amount = total_amount - fees
    if redeem_invoice_amount < required_amount:
        err = ("Token value (Payment: " + str(total_amount) + " Sats. Fees: " +
               str(fees) + " Sats) below required amount of  " + str(required_amount)
               + " Sats. Cashu token has not been claimed.")
        print("[" + config.NIP89.NAME + "] " + err)
        return False, err, 0, 0

    if config.LNBITS_INVOICE_KEY != "":
        invoice, paymenthash = create_bolt11_ln_bits(redeem_invoice_amount, config)
    else:

        user = await get_or_add_user(db=config.DB, npub=config.PUBLIC_KEY,
                                     client=client, config=config, update=update_self)
        invoice = create_bolt11_lud16(user.lud16, redeem_invoice_amount)
    print(invoice)

    try:
        url = mint + "/melt"  # Melt cashu tokens at Mint
        json_object = {"proofs": proofs, "pr": invoice}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        request_body = json.dumps(json_object).encode('utf-8')
        request = requests.post(url, data=request_body, headers=headers)
        tree = json.loads(request.text)
        print(request.text)
        is_paid = tree["paid"] if tree.get("paid") else False
        print(is_paid)
        if is_paid:
            print("cashu token redeemed")
            return True, "success", redeem_invoice_amount, fees
        else:
            msg = tree.get("detail").split('.')[0].strip() if tree.get("detail") else None
            print(msg)
            return False, msg, redeem_invoice_amount, fees
    except Exception as e:
        print(e)

    return False, "", redeem_invoice_amount, fees
