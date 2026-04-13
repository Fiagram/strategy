import threading
from queue import Queue
from handlers.producer.models import ProducerSignalAbstract
from models.indicators import IndicatorAbstract
from models.alert import Symbol, Timeframe, IndicatorName
from lib.dnse.python.dnse.client import DNSEClient

class Warehouse:
    def __init__(
            self,
            signal_queue: Queue[ProducerSignalAbstract],
            DNSE_key: str,
            DNSE_secret: str,
        ):
        self._lock = threading.RLock()
        self._signal_queue = signal_queue
        self._symbols_indicators_dict : dict[Symbol, dict[Timeframe, dict[IndicatorName, IndicatorAbstract]]]= {}
        self._dnse_client = DNSEClient(
            api_key=DNSE_key,
            api_secret=DNSE_secret,
            base_url="https://openapi.dnse.com.vn",
        )

    def start(self) -> None:
        pass

    def stop (self) -> None:
        pass

    def _refresh_data(self) -> None:
        self._clear_data()
        Vn30StockSymbolList = [
        "ACB", "BID", "CTG", "DGC", "FPT", "GAS", 
        "GVR", "HDB", "HPG", "LPB", "MBB", "MSN", 
        "MWG", "PLX", "SAB", "SHB", "SSB", "SSI", 
        "STB", "TCB", "TPB", "VCB", "VHM", "VIB", 
        "VIC", "VJC", "VNM", "VPB", "VPL", "VRE"
        ]
        
    
    def _set_data(
            self,
            symbol: Symbol,
            timeframe: Timeframe,
            indicator: dict [IndicatorName, IndicatorAbstract],
        ) -> None:
        with self._lock:
            self._symbols_indicators_dict[symbol][timeframe] = indicator
        

    def _clear_data(self) -> None:
        with self._lock:
            if self._symbols_indicators_dict:
                self._symbols_indicators_dict.clear()

    def _publish_signal(self, signal: ProducerSignalAbstract) -> None:
        self._signal_queue.put(signal)
    



