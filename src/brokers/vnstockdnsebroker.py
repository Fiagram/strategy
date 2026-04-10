import 

class VnStocksDnseBroker:
    def __init__(self, config):
        self.config = config
        self.name = "vnstockdnse"

    def crawlVn30Stocks(self) -> None:
    Vn30StockSymbolList = [
        "ACB", "BID", "CTG", "DGC", "FPT", "GAS", 
        "GVR", "HDB", "HPG", "LPB", "MBB", "MSN", 
        "MWG", "PLX", "SAB", "SHB", "SSB", "SSI", 
        "STB", "TCB", "TPB", "VCB", "VHM", "VIB", 
        "VIC", "VJC", "VNM", "VPB", "VPL", "VRE"
        ]
