#!/usr/bin/env python3
# scripts/logging.py
# Lightweight logging utility for workflow-as-list
# NOTE: Extracted from check-headers.py for modularity (2026-03-13)

from datetime import datetime


class Log:
    """LogLight-style logging with timestamp."""

    @staticmethod
    def _timestamp():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def sect(msg):
        print(f"\n{Log._timestamp()}  {msg}")

    @staticmethod
    def step(msg):
        print(f"\n{Log._timestamp()}  → {msg}")

    @staticmethod
    def work(msg):
        print(f"{Log._timestamp()}    • {msg}")

    @staticmethod
    def find(msg):
        print(f"{Log._timestamp()}    ✓ {msg}")

    @staticmethod
    def fail(msg):
        print(f"{Log._timestamp()}    ✗ {msg}")

    @staticmethod
    def warn(msg):
        print(f"{Log._timestamp()}    ⚠ {msg}")

    @staticmethod
    def end(msg):
        print(f"\n{Log._timestamp()}  {msg}\n")
