from pathlib import Path

BASE_DIR = Path(__file__).absolute().parent.parent
LIB_DIR = BASE_DIR / "whatstk"
CHATS_DIR = BASE_DIR / "chats"
TEST_DIR = BASE_DIR / "tests"
TEST_CHATS_DIR = TEST_DIR / "chats"
TEST_CHATS_HFORMATS_DIR = TEST_CHATS_DIR / "hformats"
TEST_CHATS_MERGE_DIR = TEST_CHATS_DIR / "merge"
