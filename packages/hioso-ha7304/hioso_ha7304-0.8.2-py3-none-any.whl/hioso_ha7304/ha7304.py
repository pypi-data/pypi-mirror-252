import attr
from cachetools import Cache, TTLCache, cachedmethod
from operator import attrgetter
from requests import Session
from requests.auth import HTTPBasicAuth
from typing import List, Literal, Optional

from . import Mac, Onu


OnuOperation = Literal["rebootOp", "activeOp", "noactiveOp", "restoreOp", "cleanLoopOp"]


@attr.dataclass(slots=True)
class Ha7304:
    url: str
    username: str
    password: str
    session: Session = attr.ib(factory=Session)
    cached_onu_time: int = 30
    onu_cache: Optional[Cache] = None
    timeout: int = 3

    def __attrs_post_init__(self) -> None:
        if self.url.endswith("/"):
            self.url = self.url.rstrip("/")
        self.session.auth = HTTPBasicAuth(self.username, self.password)
        if not self.onu_cache:
            self.onu_cache = TTLCache(1, self.cached_onu_time)

    def all_pon(self, ponno: str) -> List[Onu]:
        results: List[Onu] = list()
        for dpon in self._all_pon(ponno):
            try:
                results.append(Onu.from_all_onu_data(dpon))
            except:
                pass
        return results

    def _all_pon(self, ponno: str) -> List[str]:
        params = {"oltponno": ponno}
        res = self.session.get(
            self.url + "/onuOverview.asp",
            params=params,
            timeout=self.timeout,
        )
        datas = res.text.split('\n);\nvar displayfunc ="displayAll";')[0]
        datas = datas.split("var onutable=new Array(\n")[1]
        return datas.splitlines()

    @cachedmethod(attrgetter("onu_cache"))
    def all_pon_onu(self, retry: int = 3):
        while retry > 0:
            try:
                datas = self._all_pon_onu()
                break
            except IndexError:
                pass
            retry -= 1
        results: List[Onu] = list()
        for data in datas.splitlines():
            try:
                results.append(Onu.from_all_onu_data(data))
            except IndexError:
                continue
        return results

    def mac_list(self, retry: int = 3):
        while retry > 0:
            try:
                datas = self._all_mac_list()
                break
            except IndexError:
                pass
            retry -= 1
        results: List[Mac] = list()
        for data in datas.splitlines():
            try:
                results.append(Mac.from_all_mac_data(data))
            except IndexError:
                continue
        return results

    def _all_pon_onu(self) -> str:
        res = self.session.get(self.url + "/onuAllPonOnuList.asp", timeout=self.timeout)
        data = res.text
        try:
            data = data.split("'\n);\nfunction Reload()")[0]
            data = data.split("Array(\n'")[1]
        except IndexError:
            pass
        return data

    def _all_mac_list(self) -> str:
        res = self.session.get(self.url + "/oltMacFdb.asp", timeout=self.timeout)
        data = res.text
        try:
            data = data.split("'\n);\nfunction Reload()")[0]
            data = data.split("Array(\n'")[1]
        except IndexError:
            pass
        return data

    def getOnu(self, onu: Onu) -> Onu:
        oltpon, _ = onu.id.split(":")
        params = {"onuno": onu.id, "oltponno": oltpon}
        res = self.session.get(
            self.url + "/onuConfig.asp",
            params=params,
            timeout=self.timeout,
        )
        data: str = res.text
        lines = data.splitlines()
        for i, line in enumerate(lines):
            try:
                if "Array" in line:
                    onud = lines[i + 1].split(",")
                    onu.name = onud[1].lstrip("'").rstrip("'")
                    onu.status = onud[3].lstrip("'").rstrip("'")
                    break
            except IndexError:
                pass
        return onu

    def setOnu(self, onu_id: str, onu_name: str, operation: OnuOperation):
        data = {"onuId": onu_id, "onuName": onu_name, "onuOperation": operation}
        self.session.post(
            self.url + "/goform/setOnu",
            data,
            allow_redirects=False,
            timeout=self.timeout,
        )

    def reboot(self, onu: Onu):
        return self.setOnu(onu.id, onu.name, "rebootOp")

    def activate(self, onu: Onu):
        return self.setOnu(onu.id, onu.name, "activeOp")

    def deactivate(self, onu: Onu):
        return self.setOnu(onu.id, onu.name, "noactiveOp")

    def factory(self, onu: Onu):
        return self.setOnu(onu.id, onu.name, "restoreOp")

    def clean_loop_flag(self, onu: Onu):
        return self.setOnu(onu.id, onu.name, "cleanLoopOp")

    def set_onu_port_vlan(
        self,
        port_id: str,
        vlan_mode: str,
        vlan_id: str,
        port_name: str = None,
    ):
        data = {
            "onuPortName": port_id,
            "onuPortVlanMode": vlan_mode,
            "onuPortVlanPvid": vlan_id,
            "onuPortId": port_name if port_name else port_id,
        }
        self.session.post(
            self.url + "/goform/setOnuPortVlan",
            data,
            allow_redirects=False,
            timeout=self.timeout,
        )

    def search(self, mac: str) -> List[Onu]:
        results: List[Onu] = list()
        params = {"mac0": mac, "searching_onu": mac.replace(":", "_")}
        res = self.session.get(
            self.url + "/goform/setOnuSearchEntry", params=params, timeout=self.timeout
        )
        try:
            data = res.text.split("var searchResult=new Array( ")[1]
            data = data.split(");")[0]
        except IndexError:
            pass
        for line in data.splitlines():
            try:
                results.append(Onu.from_all_onu_data(line))
            except IndexError:
                continue
        return results
