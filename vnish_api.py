import json

import aiohttp
from pydantic import BaseModel, Field
from typing import List, Optional


API_KEY = "jberberhuioerhi348934ubi34334g93"


# ----------- Pydantic Models -----------

class OverclockGlobals(BaseModel):
    volt: int
    freq: int


class Chain(BaseModel):
    freq: int
    chips: List[int]
    disabled: bool


class PresetSwitcher(BaseModel):
    enabled: bool
    top_preset: str
    decrease_temp: int
    rise_temp: int
    check_time: int
    autochange_top_preset: bool
    ignore_fan_speed: bool
    min_preset: str


class Overclock(BaseModel):
    modded_psu: bool
    preset: str
    globals: OverclockGlobals
    chains: List[Chain]
    preset_switcher: PresetSwitcher


class CoolingMode(BaseModel):
    name: str
    param: int


class Cooling(BaseModel):
    mode: CoolingMode
    fan_min_count: int
    fan_min_duty: int
    fan_max_duty: int


class Misc(BaseModel):
    asic_boost: bool
    restart_hashrate: int
    restart_temp: int
    disable_restart_unbalanced: bool
    disable_chain_break_protection: bool
    max_restart_attempts: int
    bitmain_disable_volt_comp: bool
    quick_start: bool
    higher_volt_offset: int
    tuner_bad_chip_hr_threshold: int
    remain_stopped_on_reboot: bool
    ignore_broken_sensors: bool
    disable_volt_checks: bool
    quiet_mode: bool
    downscale_preset_on_failure: bool
    auto_chip_throttling: bool
    disable_ignore_broken_chains: bool
    max_startup_delay_time: int
    ignore_chip_sensors: bool
    min_operational_chains: int


class Pool(BaseModel):
    url: str
    user: str
    pass_field: str = Field(alias="pass")



class Miner(BaseModel):
    cooling: Cooling
    misc: Misc
    overclock: Overclock
    pools: List[Pool]


class UI(BaseModel):
    theme: str
    dark_side_pane: bool
    disable_animation: bool
    locale: str
    timezone: str


class Regional(BaseModel):
    timezone: dict


class Network(BaseModel):
    hostname: str
    dhcp: bool
    ipaddress: str
    netmask: str
    gateway: str
    dnsservers: List[str]


class Settings(BaseModel):
    miner: Miner
    ui: UI
    regional: Regional
    network: Network
    password: Optional[str] = None
    layout: Optional[str] = None

    def __str__(self):
        return json.dumps(self.model_dump(by_alias=True), indent=2, ensure_ascii=False)


# ----------- API Wrapper Class -----------

class MinerAPI:
    def __init__(self, ip: str, api_key: str = API_KEY):
        self.ip = ip
        self.api_key = api_key
        self.settings: Optional[Settings] = None

    async def fetch_settings(self) -> Settings:
        url = f"http://{self.ip}/api/v1/settings"

        headers = {
            "x-api-key": self.api_key,
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=5) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    self.settings = Settings.parse_obj(json_data)
                    return self.settings
        except aiohttp.ClientError as e:
            raise ConnectionError(f"Failed to fetch settings: {str(e)}")

    async def send_settings(self, settings: Settings) -> Optional[bool]:
        """
        Отправка настроек обратно на майнер.
        Возвращает:
            True — настройки отправлены
            False — ошибка
            None — настройки уже совпадают, отправка не требуется
        """
        if self.settings is not None:
            current_dump = self.settings.model_dump(by_alias=True)
            new_dump = settings.model_dump(by_alias=True)

            if current_dump == new_dump:
                # Настройки идентичны — пропускаем
                return None

        url = f"http://{self.ip}/api/v1/settings"
        headers = {
            "x-api-key": self.api_key,
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=settings.model_dump(by_alias=True)) as response:
                    response.raise_for_status()
                    return True
        except aiohttp.ClientError as e:
            print(f"❌ Ошибка отправки настроек: {e}")
            return False

    def __repr__(self):
        return f"<MinerAPI ip={self.ip}>"
