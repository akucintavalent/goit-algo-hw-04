import shutil
import sys
from pathlib import Path

if len(sys.argv) not in (2, 3):
    print("Usage: python task1_recursive_copy.py <src> [<dst>]")
    sys.exit(1)

try:
    src_path = Path(sys.argv[1]).expanduser().resolve()
    if len(sys.argv) == 3:
        dst_path = Path(sys.argv[2]).expanduser().resolve()
    else:
        dst_path = (Path.cwd() / "dist").resolve()
except Exception as e:
    print(f"Failed to resolve paths: {e}")
    sys.exit(1)

print(f"Source: '{src_path}'")
print(f"Destination: '{dst_path}'")

if not src_path.exists() or not src_path.is_dir():
    print(f"Source path '{src_path}' does not exist or is not a directory.")
    sys.exit(1)

try:
    dst_path_resolved = dst_path.resolve()
except Exception as e:
    print(f"Failed to resolve destination path '{dst_path}': {e}")
    sys.exit(1)

try:
    dst_path.mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(f"Failed to create destination directory '{dst_path}': {e}")
    sys.exit(1)


def recursive_copy(src_path: Path):
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
            try:
                item_resolved = item.resolve()
            except Exception:
                item_resolved = None

            if item_resolved is not None and (
                item_resolved == dst_path_resolved
                or dst_path_resolved in item_resolved.parents
            ):
                continue
            recursive_copy(item)

        return

    try:
        extension = src_path.suffix[1:].lower() if src_path.suffix else "no_extension"
        target_dir = dst_path / extension
        target_dir.mkdir(parents=True, exist_ok=True)
        sub_dst = target_dir / src_path.name

        print(f"Copying '{src_path}' to '{sub_dst}'...")
        shutil.copy2(src_path, sub_dst)
    except Exception as e:
        print(f"Failed to copy '{src_path}': {e}")


if __name__ == "__main__":
    recursive_copy(src_path)
    print(f"Copied '{src_path}' to '{dst_path}' successfully.")
