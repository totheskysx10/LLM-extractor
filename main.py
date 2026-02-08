from config import Config
from tests.test_runner import TestRunner


def main() -> int:
    config = Config()
    runner = TestRunner(config)
    return runner.run()


if __name__ == "__main__":
    raise SystemExit(main())