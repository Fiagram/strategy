from producer import TorchProducer
from queue import Queue

def main():
    signal_queue: Queue = Queue()
    torchProducer = TorchProducer(
        signal_queue=signal_queue,
        bootstrap_servers="localhost:9092",
        topic="torch",
    )
    torchProducer.start()
    signal = {"symbol": "VIC", "signal": "SELL", "price": 50.0}
    signal_queue.put(signal)
    signal_queue.join()
    torchProducer.stop()
    

if __name__ == "__main__":
    main()