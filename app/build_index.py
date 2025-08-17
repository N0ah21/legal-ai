"""Utility script to build the local vector index."""

from .rag import LocalRAG


def build():
    LocalRAG()


if __name__ == "__main__":
    build()
