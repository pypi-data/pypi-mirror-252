# ------------------------------------------------------------------------------
#  Copyright 2022 Upstream Data Inc                                            -
#                                                                              -
#  Licensed under the Apache License, Version 2.0 (the "License");             -
#  you may not use this file except in compliance with the License.            -
#  You may obtain a copy of the License at                                     -
#                                                                              -
#      http://www.apache.org/licenses/LICENSE-2.0                              -
#                                                                              -
#  Unless required by applicable law or agreed to in writing, software         -
#  distributed under the License is distributed on an "AS IS" BASIS,           -
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    -
#  See the License for the specific language governing permissions and         -
#  limitations under the License.                                              -
# ------------------------------------------------------------------------------
from typing import List, Optional

from pyasic.config import MinerConfig
from pyasic.data import Fan, HashBoard
from pyasic.errors import APIError
from pyasic.miners.base import (
    BaseMiner,
    DataFunction,
    DataLocations,
    DataOptions,
    RPCAPICommand,
)
from pyasic.rpc.luxminer import LUXMinerRPCAPI

LUXMINER_DATA_LOC = DataLocations(
    **{
        str(DataOptions.MAC): DataFunction(
            "_get_mac",
            [RPCAPICommand("api_config", "config")],
        ),
        str(DataOptions.HASHRATE): DataFunction(
            "_get_hashrate",
            [RPCAPICommand("api_summary", "summary")],
        ),
        str(DataOptions.EXPECTED_HASHRATE): DataFunction(
            "_get_expected_hashrate",
            [RPCAPICommand("api_stats", "stats")],
        ),
        str(DataOptions.HASHBOARDS): DataFunction(
            "_get_hashboards",
            [RPCAPICommand("api_stats", "stats")],
        ),
        str(DataOptions.WATTAGE): DataFunction(
            "_get_wattage",
            [RPCAPICommand("api_power", "power")],
        ),
        str(DataOptions.FANS): DataFunction(
            "_get_fans",
            [RPCAPICommand("api_fans", "fans")],
        ),
        str(DataOptions.UPTIME): DataFunction(
            "_get_uptime", [RPCAPICommand("api_stats", "stats")]
        ),
    }
)


class LUXMiner(BaseMiner):
    """Handler for LuxOS miners"""

    _api_cls = LUXMinerRPCAPI
    api: LUXMinerRPCAPI

    firmware = "LuxOS"

    data_locations = LUXMINER_DATA_LOC

    async def _get_session(self) -> Optional[str]:
        try:
            data = await self.api.session()
            if not data["SESSION"][0]["SessionID"] == "":
                return data["SESSION"][0]["SessionID"]
        except APIError:
            pass

        try:
            data = await self.api.logon()
            return data["SESSION"][0]["SessionID"]
        except (LookupError, APIError):
            return

    async def fault_light_on(self) -> bool:
        try:
            session_id = await self._get_session()
            if session_id:
                await self.api.ledset(session_id, "red", "blink")
            return True
        except (APIError, LookupError):
            pass
        return False

    async def fault_light_off(self) -> bool:
        try:
            session_id = await self._get_session()
            if session_id:
                await self.api.ledset(session_id, "red", "off")
            return True
        except (APIError, LookupError):
            pass
        return False

    async def restart_backend(self) -> bool:
        return await self.restart_luxminer()

    async def restart_luxminer(self) -> bool:
        try:
            session_id = await self._get_session()
            if session_id:
                await self.api.resetminer(session_id)
            return True
        except (APIError, LookupError):
            pass
        return False

    async def stop_mining(self) -> bool:
        try:
            session_id = await self._get_session()
            if session_id:
                await self.api.curtail(session_id)
            return True
        except (APIError, LookupError):
            pass
        return False

    async def resume_mining(self) -> bool:
        try:
            session_id = await self._get_session()
            if session_id:
                await self.api.wakeup(session_id)
            return True
        except (APIError, LookupError):
            pass

    async def reboot(self) -> bool:
        try:
            session_id = await self._get_session()
            if session_id:
                await self.api.rebootdevice(session_id)
            return True
        except (APIError, LookupError):
            pass
        return False

    async def get_config(self) -> MinerConfig:
        return self.config

    ##################################################
    ### DATA GATHERING FUNCTIONS (get_{some_data}) ###
    ##################################################

    async def _get_mac(self, api_config: dict = None) -> Optional[str]:
        mac = None
        if api_config is None:
            try:
                api_config = await self.api.config()
            except APIError:
                return None

        if api_config is not None:
            try:
                mac = api_config["CONFIG"][0]["MACAddr"]
            except KeyError:
                return None

        return mac

    async def _get_hashrate(self, api_summary: dict = None) -> Optional[float]:
        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary is not None:
            try:
                return round(float(api_summary["SUMMARY"][0]["GHS 5s"] / 1000), 2)
            except (LookupError, ValueError, TypeError):
                pass

    async def _get_hashboards(self, api_stats: dict = None) -> List[HashBoard]:
        hashboards = []

        if api_stats is None:
            try:
                api_stats = await self.api.stats()
            except APIError:
                pass

        if api_stats is not None:
            try:
                board_offset = -1
                boards = api_stats["STATS"]
                if len(boards) > 1:
                    for board_num in range(1, 16, 5):
                        for _b_num in range(5):
                            b = boards[1].get(f"chain_acn{board_num + _b_num}")

                            if b and not b == 0 and board_offset == -1:
                                board_offset = board_num
                    if board_offset == -1:
                        board_offset = 1

                    for i in range(
                        board_offset, board_offset + self.expected_hashboards
                    ):
                        hashboard = HashBoard(
                            slot=i - board_offset, expected_chips=self.expected_chips
                        )

                        chip_temp = boards[1].get(f"temp{i}")
                        if chip_temp:
                            hashboard.chip_temp = round(chip_temp)

                        temp = boards[1].get(f"temp2_{i}")
                        if temp:
                            hashboard.temp = round(temp)

                        hashrate = boards[1].get(f"chain_rate{i}")
                        if hashrate:
                            hashboard.hashrate = round(float(hashrate) / 1000, 2)

                        chips = boards[1].get(f"chain_acn{i}")
                        if chips:
                            hashboard.chips = chips
                            hashboard.missing = False
                        if (not chips) or (not chips > 0):
                            hashboard.missing = True
                        hashboards.append(hashboard)
            except (LookupError, ValueError, TypeError):
                pass

        return hashboards

    async def _get_wattage(self, api_power: dict = None) -> Optional[int]:
        if api_power is None:
            try:
                api_power = await self.api.power()
            except APIError:
                pass

        if api_power is not None:
            try:
                return api_power["POWER"][0]["Watts"]
            except (LookupError, ValueError, TypeError):
                pass

    async def _get_fans(self, api_fans: dict = None) -> List[Fan]:
        if api_fans is None:
            try:
                api_fans = await self.api.fans()
            except APIError:
                pass

        fans = []

        if api_fans is not None:
            for fan in range(self.expected_fans):
                try:
                    fans.append(Fan(api_fans["FANS"][fan]["RPM"]))
                except (LookupError, ValueError, TypeError):
                    fans.append(Fan())
        return fans

    async def _get_expected_hashrate(self, api_stats: dict = None) -> Optional[float]:
        if api_stats is None:
            try:
                api_stats = await self.api.stats()
            except APIError:
                pass

        if api_stats is not None:
            try:
                expected_rate = api_stats["STATS"][1]["total_rateideal"]
                try:
                    rate_unit = api_stats["STATS"][1]["rate_unit"]
                except KeyError:
                    rate_unit = "GH"
                if rate_unit == "GH":
                    return round(expected_rate / 1000, 2)
                if rate_unit == "MH":
                    return round(expected_rate / 1000000, 2)
                else:
                    return round(expected_rate, 2)
            except LookupError:
                pass

    async def _get_uptime(self, api_stats: dict = None) -> Optional[int]:
        if api_stats is None:
            try:
                api_stats = await self.api.stats()
            except APIError:
                pass

        if api_stats is not None:
            try:
                return int(api_stats["STATS"][1]["Elapsed"])
            except LookupError:
                pass
