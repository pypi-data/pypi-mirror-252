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

import logging
from typing import List, Optional

from pyasic.config import MinerConfig, MiningModeConfig
from pyasic.data import Fan, HashBoard
from pyasic.data.error_codes import MinerErrorData, WhatsminerError
from pyasic.errors import APIError
from pyasic.miners.base import (
    BaseMiner,
    DataFunction,
    DataLocations,
    DataOptions,
    RPCAPICommand,
)
from pyasic.rpc.btminer import BTMinerRPCAPI

BTMINER_DATA_LOC = DataLocations(
    **{
        str(DataOptions.MAC): DataFunction(
            "_get_mac",
            [
                RPCAPICommand("api_summary", "summary"),
                RPCAPICommand("api_get_miner_info", "get_miner_info"),
            ],
        ),
        str(DataOptions.API_VERSION): DataFunction(
            "_get_api_ver",
            [RPCAPICommand("api_get_version", "get_version")],
        ),
        str(DataOptions.FW_VERSION): DataFunction(
            "_get_fw_ver",
            [
                RPCAPICommand("api_get_version", "get_version"),
                RPCAPICommand("api_summary", "summary"),
            ],
        ),
        str(DataOptions.HOSTNAME): DataFunction(
            "_get_hostname",
            [RPCAPICommand("api_get_miner_info", "get_miner_info")],
        ),
        str(DataOptions.HASHRATE): DataFunction(
            "_get_hashrate",
            [RPCAPICommand("api_summary", "summary")],
        ),
        str(DataOptions.EXPECTED_HASHRATE): DataFunction(
            "_get_expected_hashrate",
            [RPCAPICommand("api_summary", "summary")],
        ),
        str(DataOptions.HASHBOARDS): DataFunction(
            "_get_hashboards",
            [RPCAPICommand("api_devs", "devs")],
        ),
        str(DataOptions.ENVIRONMENT_TEMP): DataFunction(
            "_get_env_temp",
            [RPCAPICommand("api_summary", "summary")],
        ),
        str(DataOptions.WATTAGE): DataFunction(
            "_get_wattage",
            [RPCAPICommand("api_summary", "summary")],
        ),
        str(DataOptions.WATTAGE_LIMIT): DataFunction(
            "_get_wattage_limit",
            [RPCAPICommand("api_summary", "summary")],
        ),
        str(DataOptions.FANS): DataFunction(
            "_get_fans",
            [
                RPCAPICommand("api_summary", "summary"),
                RPCAPICommand("api_get_psu", "get_psu"),
            ],
        ),
        str(DataOptions.FAN_PSU): DataFunction(
            "_get_fan_psu",
            [
                RPCAPICommand("api_summary", "summary"),
                RPCAPICommand("api_get_psu", "get_psu"),
            ],
        ),
        str(DataOptions.ERRORS): DataFunction(
            "_get_errors",
            [
                RPCAPICommand("api_get_error_code", "get_error_code"),
                RPCAPICommand("api_summary", "summary"),
            ],
        ),
        str(DataOptions.FAULT_LIGHT): DataFunction(
            "_get_fault_light",
            [RPCAPICommand("api_get_miner_info", "get_miner_info")],
        ),
        str(DataOptions.IS_MINING): DataFunction(
            "_is_mining",
            [RPCAPICommand("api_status", "status")],
        ),
        str(DataOptions.UPTIME): DataFunction(
            "_get_uptime",
            [RPCAPICommand("api_summary", "summary")],
        ),
    }
)


class BTMiner(BaseMiner):
    """Base handler for BTMiner based miners."""

    _api_cls = BTMinerRPCAPI
    api: BTMinerRPCAPI

    data_locations = BTMINER_DATA_LOC

    supports_shutdown = True

    async def _reset_api_pwd_to_admin(self, pwd: str):
        try:
            data = await self.api.update_pwd(pwd, "admin")
        except APIError:
            return False
        if data:
            if "Code" in data.keys():
                if data["Code"] == 131:
                    return True
        return False

    async def fault_light_off(self) -> bool:
        try:
            data = await self.api.set_led(auto=True)
        except APIError:
            return False
        if data:
            if "Code" in data.keys():
                if data["Code"] == 131:
                    self.light = False
                    return True
        return False

    async def fault_light_on(self) -> bool:
        try:
            data = await self.api.set_led(auto=False)
            await self.api.set_led(
                auto=False, color="green", start=0, period=1, duration=0
            )
        except APIError:
            return False
        if data:
            if "Code" in data.keys():
                if data["Code"] == 131:
                    self.light = True
                    return True
        return False

    async def reboot(self) -> bool:
        try:
            data = await self.api.reboot()
        except APIError:
            return False
        if data.get("Msg"):
            if data["Msg"] == "API command OK":
                return True
        return False

    async def restart_backend(self) -> bool:
        try:
            data = await self.api.restart()
        except APIError:
            return False
        if data.get("Msg"):
            if data["Msg"] == "API command OK":
                return True
        return False

    async def stop_mining(self) -> bool:
        try:
            data = await self.api.power_off(respbefore=True)
        except APIError:
            return False
        if data.get("Msg"):
            if data["Msg"] == "API command OK":
                return True
        return False

    async def resume_mining(self) -> bool:
        try:
            data = await self.api.power_on()
        except APIError:
            return False
        if data.get("Msg"):
            if data["Msg"] == "API command OK":
                return True
        return False

    async def send_config(self, config: MinerConfig, user_suffix: str = None) -> None:
        self.config = config

        conf = config.as_wm(user_suffix=user_suffix)
        pools_conf = conf["pools"]

        try:
            await self.api.update_pools(**pools_conf)

            if conf["mode"] == "normal":
                await self.api.set_normal_power()
            elif conf["mode"] == "high":
                await self.api.set_high_power()
            elif conf["mode"] == "low":
                await self.api.set_low_power()
            elif conf["mode"] == "power_tuning":
                await self.api.adjust_power_limit(conf["power_tuning"]["wattage"])
        except APIError:
            # cannot update, no API access usually
            pass

    async def get_config(self) -> MinerConfig:
        pools = None
        summary = None
        status = None
        try:
            data = await self.api.multicommand("pools", "summary", "status")
            pools = data["pools"][0]
            summary = data["summary"][0]
            status = data["status"][0]
        except APIError as e:
            logging.warning(e)
        except LookupError:
            pass

        if pools is not None:
            cfg = MinerConfig.from_api(pools)
        else:
            cfg = MinerConfig()

        is_mining = await self._is_mining(status)
        if not is_mining:
            cfg.mining_mode = MiningModeConfig.sleep()
            return cfg

        if summary is not None:
            mining_mode = None
            try:
                mining_mode = summary["SUMMARY"][0]["Power Mode"]
            except LookupError:
                pass

            if mining_mode == "High":
                cfg.mining_mode = MiningModeConfig.high()
                return cfg
            elif mining_mode == "Low":
                cfg.mining_mode = MiningModeConfig.low()
                return cfg
            try:
                power_lim = summary["SUMMARY"][0]["Power Limit"]
            except LookupError:
                power_lim = None

            if power_lim is None:
                cfg.mining_mode = MiningModeConfig.normal()
                return cfg

            cfg.mining_mode = MiningModeConfig.power_tuning(power_lim)
            self.config = cfg
            return self.config

    async def set_power_limit(self, wattage: int) -> bool:
        try:
            await self.api.adjust_power_limit(wattage)
        except Exception as e:
            logging.warning(f"{self} set_power_limit: {e}")
            return False
        else:
            return True

    ##################################################
    ### DATA GATHERING FUNCTIONS (get_{some_data}) ###
    ##################################################

    async def _get_mac(
        self, api_summary: dict = None, api_get_miner_info: dict = None
    ) -> Optional[str]:
        if api_get_miner_info is None:
            try:
                api_get_miner_info = await self.api.get_miner_info()
            except APIError:
                pass

        if api_get_miner_info is not None:
            try:
                mac = api_get_miner_info["Msg"]["mac"]
                return str(mac).upper()
            except KeyError:
                pass

        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary is not None:
            try:
                mac = api_summary["SUMMARY"][0]["MAC"]
                return str(mac).upper()
            except LookupError:
                pass

    async def _get_api_ver(self, api_get_version: dict = None) -> Optional[str]:
        if api_get_version is None:
            try:
                api_get_version = await self.api.get_version()
            except APIError:
                pass

        if api_get_version is not None:
            if "Code" in api_get_version.keys():
                if api_get_version["Code"] == 131:
                    try:
                        api_ver = api_get_version["Msg"]
                        if not isinstance(api_ver, str):
                            api_ver = api_ver["api_ver"]
                        self.api_ver = api_ver.replace("whatsminer v", "")
                    except (KeyError, TypeError):
                        pass
                    else:
                        self.api.api_ver = self.api_ver
                        return self.api_ver

        return self.api_ver

    async def _get_fw_ver(
        self, api_get_version: dict = None, api_summary: dict = None
    ) -> Optional[str]:
        if api_get_version is None:
            try:
                api_get_version = await self.api.get_version()
            except APIError:
                pass

        if api_get_version is not None:
            if "Code" in api_get_version.keys():
                if api_get_version["Code"] == 131:
                    try:
                        self.fw_ver = api_get_version["Msg"]["fw_ver"]
                    except (KeyError, TypeError):
                        pass
                    else:
                        return self.fw_ver

        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary:
            try:
                self.fw_ver = api_summary["SUMMARY"][0]["Firmware Version"].replace(
                    "'", ""
                )
            except LookupError:
                pass

        return self.fw_ver

    async def _get_hostname(self, api_get_miner_info: dict = None) -> Optional[str]:
        hostname = None
        if api_get_miner_info is None:
            try:
                api_get_miner_info = await self.api.get_miner_info()
            except APIError:
                return None  # only one way to get this

        if api_get_miner_info is not None:
            try:
                hostname = api_get_miner_info["Msg"]["hostname"]
            except KeyError:
                return None

        return hostname

    async def _get_hashrate(self, api_summary: dict = None) -> Optional[float]:
        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary is not None:
            try:
                return round(float(api_summary["SUMMARY"][0]["MHS 1m"] / 1000000), 2)
            except LookupError:
                pass

    async def _get_hashboards(self, api_devs: dict = None) -> List[HashBoard]:
        hashboards = [
            HashBoard(slot=i, expected_chips=self.expected_chips)
            for i in range(self.expected_hashboards)
        ]

        if api_devs is None:
            try:
                api_devs = await self.api.devs()
            except APIError:
                pass

        if api_devs is not None:
            try:
                for board in api_devs["DEVS"]:
                    if len(hashboards) < board["ASC"] + 1:
                        hashboards.append(
                            HashBoard(
                                slot=board["ASC"], expected_chips=self.expected_chips
                            )
                        )
                        self.expected_hashboards += 1
                    hashboards[board["ASC"]].chip_temp = round(board["Chip Temp Avg"])
                    hashboards[board["ASC"]].temp = round(board["Temperature"])
                    hashboards[board["ASC"]].hashrate = round(
                        float(board["MHS 1m"] / 1000000), 2
                    )
                    hashboards[board["ASC"]].chips = board["Effective Chips"]
                    hashboards[board["ASC"]].serial_number = board["PCB SN"]
                    hashboards[board["ASC"]].missing = False
            except LookupError:
                pass

        return hashboards

    async def _get_env_temp(self, api_summary: dict = None) -> Optional[float]:
        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary is not None:
            try:
                return api_summary["SUMMARY"][0]["Env Temp"]
            except LookupError:
                pass

    async def _get_wattage(self, api_summary: dict = None) -> Optional[int]:
        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary is not None:
            try:
                wattage = api_summary["SUMMARY"][0]["Power"]
                return wattage if not wattage == -1 else None
            except LookupError:
                pass

    async def _get_wattage_limit(self, api_summary: dict = None) -> Optional[int]:
        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary is not None:
            try:
                return api_summary["SUMMARY"][0]["Power Limit"]
            except LookupError:
                pass

    async def _get_fans(
        self, api_summary: dict = None, api_get_psu: dict = None
    ) -> List[Fan]:
        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        fans = [Fan() for _ in range(self.expected_fans)]
        if api_summary is not None:
            try:
                if self.expected_fans > 0:
                    fans = [
                        Fan(api_summary["SUMMARY"][0].get("Fan Speed In", 0)),
                        Fan(api_summary["SUMMARY"][0].get("Fan Speed Out", 0)),
                    ]
            except LookupError:
                pass

        return fans

    async def _get_fan_psu(
        self, api_summary: dict = None, api_get_psu: dict = None
    ) -> Optional[int]:
        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary is not None:
            try:
                return int(api_summary["SUMMARY"][0]["Power Fanspeed"])
            except LookupError:
                pass

        if api_get_psu is None:
            try:
                api_get_psu = await self.api.get_psu()
            except APIError:
                pass

        if api_get_psu is not None:
            try:
                return int(api_get_psu["Msg"]["fan_speed"])
            except (KeyError, TypeError):
                pass

    async def _get_errors(
        self, api_summary: dict = None, api_get_error_code: dict = None
    ) -> List[MinerErrorData]:
        errors = []
        if api_get_error_code is None and api_summary is None:
            try:
                api_get_error_code = await self.api.get_error_code()
            except APIError:
                pass

        if api_get_error_code is not None:
            try:
                for err in api_get_error_code["Msg"]["error_code"]:
                    if isinstance(err, dict):
                        for code in err:
                            errors.append(WhatsminerError(error_code=int(code)))
                    else:
                        errors.append(WhatsminerError(error_code=int(err)))
            except KeyError:
                pass

        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary is not None:
            try:
                for i in range(api_summary["SUMMARY"][0]["Error Code Count"]):
                    err = api_summary["SUMMARY"][0].get(f"Error Code {i}")
                    if err:
                        errors.append(WhatsminerError(error_code=err))
            except (LookupError, ValueError, TypeError):
                pass
        return errors

    async def _get_expected_hashrate(self, api_summary: dict = None) -> Optional[float]:
        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary is not None:
            try:
                expected_hashrate = api_summary["SUMMARY"][0]["Factory GHS"]
                if expected_hashrate:
                    return round(expected_hashrate / 1000, 2)
            except LookupError:
                pass

    async def _get_fault_light(self, api_get_miner_info: dict = None) -> Optional[bool]:
        if api_get_miner_info is None:
            try:
                api_get_miner_info = await self.api.get_miner_info()
            except APIError:
                if not self.light:
                    self.light = False

        if api_get_miner_info is not None:
            try:
                self.light = not (api_get_miner_info["Msg"]["ledstat"] == "auto")
            except KeyError:
                pass

        return self.light if self.light else False

    async def set_static_ip(
        self,
        ip: str,
        dns: str,
        gateway: str,
        subnet_mask: str = "255.255.255.0",
        hostname: str = None,
    ):
        if not hostname:
            hostname = await self.get_hostname()
        await self.api.net_config(
            ip=ip, mask=subnet_mask, dns=dns, gate=gateway, host=hostname, dhcp=False
        )

    async def set_dhcp(self, hostname: str = None):
        if hostname:
            await self.set_hostname(hostname)
        await self.api.net_config()

    async def set_hostname(self, hostname: str):
        await self.api.set_hostname(hostname)

    async def _is_mining(self, api_status: dict = None) -> Optional[bool]:
        if api_status is None:
            try:
                api_status = await self.api.status()
            except APIError:
                pass

        if api_status is not None:
            try:
                if api_status["Msg"].get("btmineroff"):
                    try:
                        await self.api.devdetails()
                    except APIError:
                        return False
                    return True
                return True if api_status["Msg"]["mineroff"] == "false" else False
            except LookupError:
                pass

    async def _get_uptime(self, api_summary: dict = None) -> Optional[int]:
        if api_summary is None:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary is not None:
            try:
                return int(api_summary["SUMMARY"][0]["Elapsed"])
            except LookupError:
                pass
