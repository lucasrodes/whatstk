"""Synthetic chat generation, used to build the test fixtures.

This lives under ``tests/`` rather than in the package: it exists to produce the chats that
``make generate-test-data`` writes, and shipping it meant every user installed a lorem-ipsum
generator and carried a ``[generate]`` extra that pulled in scipy. See issue #177.

Run it with ``python -m tests.chatgen --help``.
"""

from tests.chatgen.generator import ChatGenerator, generate_chats_hformats

__all__ = ["ChatGenerator", "generate_chats_hformats"]
