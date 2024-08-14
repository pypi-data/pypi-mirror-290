import os

from loguru import logger
from sqlmodel import Session, create_engine, select

from concave.internal.codebase.search.symbol.db import SymbolInfo, Occurrences
from concave.internal.codebase.search.symbol.index import create_index_db


class SymbolsResponse:

    def __init__(self, symbols, occurrences):
        self.symbols = symbols
        self.occurrences = occurrences

    def print(self):
        print("=" * 30)
        print("| SYMBOLS SEARCH RESULTS")
        print(f"| Found {len(self.symbols)} symbols and {len(self.occurrences)} occurrences")
        print("=" * 30)
        print("Symbols:")
        for symbol in self.symbols:
            print(f"{symbol.symbol}")
            print("-" * 30)
            print(f"{symbol.documentation}")
            print()
        print("Occurrences:")
        for occurrence in self.occurrences:
            print(
                f"  {occurrence.role} in {occurrence.relative_path} at {occurrence.start_line}:{occurrence.start_char}-{occurrence.end_line}:{occurrence.end_char}")


class SymbolSearcher:

    def __init__(self, index_path: str):
        index_file = os.path.abspath(os.path.join(index_path, "scip.sqlite"))
        if not os.path.exists(index_file):
            scip_file = os.path.abspath(os.path.join(index_path, "index.scip"))
            if not os.path.exists(scip_file):
                raise FileNotFoundError(f"Index file {index_file} does not exist")
            logger.info(f"Creating index database from {scip_file}, to {index_file}")
            create_index_db(scip_file, index_file)

        self.engine = create_engine(f"sqlite:///{index_file}")

    def test(self):
        if self.search() or self.search() or self.search():
            return 0

    def search(self, query: str):
        with Session(self.engine) as session:
            symbol_query = select(SymbolInfo).where(SymbolInfo.symbol.like(f"%{query}%"))
            symbols_exec = session.exec(symbol_query)
            symbols = symbols_exec.all()

            occurrences_query = select(Occurrences).where(Occurrences.symbol.like(f"%{query}%"))
            occurrences_exec = session.exec(occurrences_query)
            occurrences = occurrences_exec.all()

            return SymbolsResponse(symbols, occurrences)
