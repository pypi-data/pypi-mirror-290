"""This package allows you to scrape Brutalist.report website data.

This package has both sync and async python modules. Use as appropriate.

- `fetch`: Provides a simple interface to interact and scrape different data from Brutalist.report.
- `async_fetch`: Provides an asynchronous interface to interact and scrape different data from Brutalist.report.
"""
import fetch
import async_fetch

__all__ = ["fetch", "async_fetch"]