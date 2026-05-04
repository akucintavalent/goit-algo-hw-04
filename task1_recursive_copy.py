import sys
from pathlib import Path

if len(sys.argv) != 3 and len(sys.argv) != 2:
    print("Usage: python task1_recursive_copy.py <src> [<dst>]")
    sys.exit(1)

if len(sys.argv) == 3:
    [src, dst] = sys.argv[1:]
    try:
        src_path = Path(src).expanduser().resolve()
        dst_path = Path(dst).expanduser().resolve()
    except Exception as e:
        print(f"Failed to resolve paths: {e}")
        sys.exit(1)
else:
    [src] = sys.argv[1:]
    try:
        src_path = Path(src).expanduser().resolve()
        dst_path = src_path.parent / "dist"
    except Exception as e:
        print(f"Failed to resolve paths: {e}")
        sys.exit(1)

print(f"Source: '{src_path}'")
print(f"Destination: '{dst_path}'")

if not src_path.exists() or not src_path.is_dir():
    print(f"Source path '{src_path}' does not exist or is not a directory.")
    sys.exit(1)


def recursive_copy(src_path: Path):
    try:
        if not dst_path.exists():
            dst_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Failed to create destination directory '{dst_path}': {e}")
        return

    try:
        src_path_is_dir = src_path.is_dir()
    except Exception as e:
        print(f"Failed to determine if '{src_path}' is a directory or a file: {e}")
        return

    if src_path_is_dir:
        try:
            src_path_iter = src_path.iterdir()
        except Exception as e:
            print(f"Failed to iterate over directory '{src_path}': {e}")
            return

        for item in src_path_iter:
            recursive_copy(item)

        return

    try:
        extension = "no_extension"
        if src_path.suffix:
            extension = src_path.suffix[1:]

        if not (dst_path / extension).exists():
            (dst_path / extension).mkdir(parents=True, exist_ok=True)

        sub_dst = dst_path / extension / src_path.name

        print(f"Copying '{src_path}' to '{sub_dst}'...")

        sub_dst.write_bytes(src_path.read_bytes())
    except Exception as e:
        print(f"Failed to copy '{src_path}' to '{dst_path / extension}': {e}")


if __name__ == "__main__":
    recursive_copy(src_path)
    print(f"Copied '{src_path}' to '{dst_path}' successfully.")
