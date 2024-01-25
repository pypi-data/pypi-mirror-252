# The MIT License (MIT)
# Copyright © 2024 Nimble Labs Ltd

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import json
import argparse
import nimble
from tqdm import tqdm
from rich.table import Table
from rich.prompt import Prompt
from .utils import check_netuid_set, get_delegates_details, DelegatesDetails
from . import defaults

console = nimble.__console__

import os
import nimble
from typing import List, Tuple, Optional, Dict


def _get_coldkey_wallets_for_path(path: str) -> List["nimble.wallet"]:
    try:
        wallet_names = next(os.walk(os.path.expanduser(path)))[1]
        return [nimble.wallet(path=path, name=name) for name in wallet_names]
    except StopIteration:
        # No wallet files found.
        wallets = []
    return wallets


def _get_hotkey_wallets_for_wallet(wallet) -> List["nimble.wallet"]:
    hotkey_wallets = []
    hotkeys_path = wallet.path + "/" + wallet.name + "/hotkeys"
    try:
        hotkey_files = next(os.walk(os.path.expanduser(hotkeys_path)))[2]
    except StopIteration:
        hotkey_files = []
    for hotkey_file_name in hotkey_files:
        try:
            hotkey_for_name = nimble.wallet(
                path=wallet.path, name=wallet.name, hotkey=hotkey_file_name
            )
            if (
                hotkey_for_name.hotkey_file.exists_on_device()
                and not hotkey_for_name.hotkey_file.is_encrypted()
            ):
                hotkey_wallets.append(hotkey_for_name)
        except Exception:
            pass
    return hotkey_wallets


class InspectCommand:
    """
    Executes the 'inspect' command, which compiles and displays a detailed report of a user's
    wallet pairs (coldkey, hotkey) on the nimble network. This report includes balance and
    staking information for both the coldkey and hotkey associated with the wallet.

    Optional arguments:
    -all: If set to True, the command will inspect all wallets located within the specified
    path. If set to False, the command will inspect only the wallet specified by the user.

    The command gathers data on:
    - Coldkey balance and delegated stakes.
    - Hotkey stake and emissions per neuron on the network.
    - Delegate names and details fetched from the network.

    The resulting table includes columns for:
    - Coldkey: The coldkey associated with the user's wallet.
    - Balance: The balance of the coldkey.
    - Delegate: The name of the delegate to which the coldkey has staked funds.
    - Stake: The amount of stake held by both the coldkey and hotkey.
    - Emission: The emission or rewards earned from staking.
    - Netuid: The network unique identifier of the subnet where the hotkey is active.
    - Hotkey: The hotkey associated with the neuron on the network.

    Usage:
    This command can be used to inspect a single wallet or all wallets located within a
    specified path. It is useful for a comprehensive overview of a user's participation
    and performance in the nimble network.

    Example usage:
    >>> nbcli inspect
    >>> nbcli inspect --all

    Note:
    The 'inspect' command is for displaying information only and does not perform any
    transactions or state changes on the nimble network. It is intended to be used as
    part of the nimble CLI and not as a standalone function within user code.
    """

    @staticmethod
    def run(cli):
        r"""Inspect a cold, hot pair."""
        if cli.config.get("all", d=False) == True:
            wallets = _get_coldkey_wallets_for_path(cli.config.wallet.path)
        else:
            wallets = [nimble.wallet(config=cli.config)]
        nbnetwork = nimble.nbnetwork(config=cli.config, log_verbose=False)

        netuids = nbnetwork.get_all_subnet_netuids()

        registered_delegate_info: Optional[
            Dict[str, DelegatesDetails]
        ] = get_delegates_details(url=nimble.__delegates_details_url__)
        if registered_delegate_info is None:
            nimble.__console__.print(
                ":warning:[yellow]Could not get delegate info from chain.[/yellow]"
            )
            registered_delegate_info = {}

        neuron_state_dict = {}
        for netuid in tqdm(netuids):
            neurons = nbnetwork.neurons_lite(netuid)
            neuron_state_dict[netuid] = neurons if neurons != None else []

        table = Table(show_footer=True, pad_edge=False, box=None, expand=True)
        table.add_column(
            "[overline white]Coldkey",
            footer_style="overline white",
            style="bold white",
        )
        table.add_column(
            "[overline white]Balance",
            footer_style="overline white",
            style="green",
        )
        table.add_column(
            "[overline white]Delegate",
            footer_style="overline white",
            style="blue",
        )
        table.add_column(
            "[overline white]Stake",
            footer_style="overline white",
            style="green",
        )
        table.add_column(
            "[overline white]Emission",
            footer_style="overline white",
            style="green",
        )
        table.add_column(
            "[overline white]Netuid",
            footer_style="overline white",
            style="bold white",
        )
        table.add_column(
            "[overline white]Hotkey",
            footer_style="overline white",
            style="yellow",
        )
        table.add_column(
            "[overline white]Stake",
            footer_style="overline white",
            style="green",
        )
        table.add_column(
            "[overline white]Emission",
            footer_style="overline white",
            style="green",
        )
        for wallet in tqdm(wallets):
            delegates: List[
                Tuple(nimble.DelegateInfo, nimble.Balance)
            ] = nbnetwork.get_delegated(
                coldkey_ss58=wallet.coldkeypub.ss58_address
            )
            if not wallet.coldkeypub_file.exists_on_device():
                continue
            cold_balance = nbnetwork.get_balance(wallet.coldkeypub.ss58_address)
            table.add_row(
                wallet.name, str(cold_balance), "", "", "", "", "", "", ""
            )
            for dele, staked in delegates:
                if dele.hotkey_ss58 in registered_delegate_info:
                    delegate_name = registered_delegate_info[
                        dele.hotkey_ss58
                    ].name
                else:
                    delegate_name = dele.hotkey_ss58
                table.add_row(
                    "",
                    "",
                    str(delegate_name),
                    str(staked),
                    str(
                        dele.total_daily_return.nim
                        * (staked.nim / dele.total_stake.nim)
                    ),
                    "",
                    "",
                    "",
                    "",
                )

            hotkeys = _get_hotkey_wallets_for_wallet(wallet)
            for netuid in netuids:
                for neuron in neuron_state_dict[netuid]:
                    if neuron.coldkey == wallet.coldkeypub.ss58_address:
                        hotkey_name: str = ""

                        hotkey_names: List[str] = [
                            wallet.hotkey_str
                            for wallet in filter(
                                lambda hotkey: hotkey.hotkey.ss58_address
                                == neuron.hotkey,
                                hotkeys,
                            )
                        ]
                        if len(hotkey_names) > 0:
                            hotkey_name = f"{hotkey_names[0]}-"

                        table.add_row(
                            "",
                            "",
                            "",
                            "",
                            "",
                            str(netuid),
                            f"{hotkey_name}{neuron.hotkey}",
                            str(neuron.stake),
                            str(nimble.Balance.from_nim(neuron.emission)),
                        )

        nimble.__console__.print(table)

    @staticmethod
    def check_config(config: "nimble.config"):
        if (
            not config.get("all", d=None)
            and not config.is_set("wallet.name")
            and not config.no_prompt
        ):
            wallet_name = Prompt.ask(
                "Enter wallet name", default=defaults.wallet.name
            )
            config.wallet.name = str(wallet_name)

    @staticmethod
    def add_args(parser: argparse.ArgumentParser):
        inspect_parser = parser.add_parser(
            "inspect", help="""Inspect a wallet (cold, hot) pair"""
        )
        inspect_parser.add_argument(
            "--all",
            action="store_true",
            help="""Check all coldkey wallets.""",
            default=False,
        )

        nimble.wallet.add_args(inspect_parser)
        nimble.nbnetwork.add_args(inspect_parser)
