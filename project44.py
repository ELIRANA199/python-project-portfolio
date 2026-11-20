
import hashlib
from pathlib import Path
from collections import defaultdict


def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    try:
        with file_path.open("rb") as file:
            while True:
                chunk = file.read(1024 * 1024)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    except OSError as error:
        print(f"Cannot read {file_path}: {error}")
        return None


def find_duplicates(folder_path):
    """Find files with identical content."""
    hash_groups = defaultdict(list)

    for file_path in folder_path.rglob("*"):
        if not file_path.is_file():
            continue

        file_hash = calculate_hash(file_path)

        if file_hash:
            hash_groups[file_hash].append(file_path)

    duplicates = {
        file_hash: paths
        for file_hash, paths in hash_groups.items()
        if len(paths) > 1
    }

    return duplicates


def format_size(size):
    """Convert bytes into a readable format."""
    units = ["B", "KB", "MB", "GB"]

    for unit in units:
        if size < 1024 or unit == "GB":
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} GB"


def create_report(duplicates, output_path):
    """Create a text report."""
    lines = ["===== DUPLICATE FILE REPORT =====", ""]

    if not duplicates:
        lines.append("No duplicate files found.")

    else:
        total_duplicates = 0

        for group_number, paths in enumerate(
            duplicates.values(), start=1
        ):
            lines.append(f"Group {group_number}:")

            for path in paths:
                try:
                    size = path.stat().st_size
                    lines.append(
                        f"  {path} ({format_size(size)})"
                    )
                except OSError:
                    lines.append(f"  {path} (size unavailable)")

            total_duplicates += len(paths) - 1
            lines.append("")

        lines.append(
            f"Duplicate copies found: {total_duplicates}"
        )

    try:
        output_path.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )
        print("\n".join(lines))
        print(f"\nReport saved to: {output_path}")

    except OSError as error:
        print(f"Could not save report: {error}")


def main():
    print("===== DUPLICATE FILE FINDER =====")

    folder_input = input(
        "Enter folder path to scan: "
    ).strip().strip('"')

    if not folder_input:
        print("Folder path cannot be empty.")
        return

    folder_path = Path(folder_input).expanduser()

    if not folder_path.exists() or not folder_path.is_dir():
        print("Invalid folder path.")
        return

    print("\nScanning files...")

    duplicates = find_duplicates(folder_path)

    output_path = Path.cwd() / "duplicate_report.txt"

    create_report(duplicates, output_path)


if __name__ == "__main__":
    main()
