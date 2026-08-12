import sys
from sources import SOURCES

def main():
    success = 0
    fail = 0
    total = 0

    for src in SOURCES:
        total += 1
        name = type(src).__name__
        try:
            count = src.generate()
            print(f"Success  {name:20s} →   {src.output_file} ({count} entries)")
            success += 1
        except Exception as e:
            print(f"Failed   {name:20s} →   {e}")
            fail += 1

    print(f"\nDone: {total} Total, {success} Success, {fail} Failures")
    if fail > 0:
        return 1
    else:
        return 0

if __name__ == "__main__":
    sys.exit(main())