import threading

from .models import Symbol, Timeframe, Ohlcv


class Warehouse:
    def __init__(self):
        self._mutex = threading.RLock()
        self._VnStockList: dict[Symbol, dict[Timeframe, list[Ohlcv]]] = {}

    def clear_vn_stock_list(self) -> None:
        with self._mutex:
            self._VnStockList.clear()

    def delete_stock(
        self,
        symbol: Symbol,
        timeframe: Timeframe | None = None,
    ) -> None:
        with self._mutex:
            if symbol not in self._VnStockList:
                return

            if timeframe is None:
                del self._VnStockList[symbol]
                return

            timeframe_map = self._VnStockList[symbol]
            timeframe_map.pop(timeframe, None)

            if not timeframe_map:
                del self._VnStockList[symbol]

    def get_stock(
        self,
        symbol: Symbol,
        timeframe: Timeframe | None = None,
    ) -> dict[Timeframe, list[Ohlcv]] | list[Ohlcv] | None:
        with self._mutex:
            if timeframe is None:
                timeframe_map = self._VnStockList.get(symbol)
                if timeframe_map is None:
                    return None

                return {
                    current_timeframe: list(current_ohlcv_list)
                    for current_timeframe, current_ohlcv_list in timeframe_map.items()
                }

            ohlcv_list = self._VnStockList.get(symbol, {}).get(timeframe)
            return list(ohlcv_list) if ohlcv_list is not None else None

    def set_stock(self, symbol: Symbol, timeframe: Timeframe, data: list[Ohlcv]) -> None:
        with self._mutex:
            self._VnStockList.setdefault(symbol, {})[timeframe] = data

