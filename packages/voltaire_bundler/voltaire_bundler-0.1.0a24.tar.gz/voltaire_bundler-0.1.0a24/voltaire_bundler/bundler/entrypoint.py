from voltaire_bundler.bundler.entrypoints.mempool import Mempool


class Entrypoint:
    version: str
    address: str
    mempools:list[Mempool]