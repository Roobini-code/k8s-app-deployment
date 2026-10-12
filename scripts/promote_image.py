import argparse
import re
from pathlib import Path


SLOTS = ("blue", "green")


def _replace_image(path: Path, slot: str, image: str) -> str:
    text = path.read_text(encoding="utf-8")
    if not re.search(r"(?m)^kind: Deployment\s*$", text) or not re.search(
        rf"(?m)^  name: deploylab-{slot}\s*$", text
    ):
        raise ValueError(f"Unexpected Deployment manifest: {path}")

    updated, count = re.subn(
        r"(?m)^([ \t]+image:[ \t]*)\S+[ \t]*$",
        lambda match: f"{match.group(1)}{image}",
        text,
    )
    if count != 1:
        raise ValueError(f"Expected one container image in {path}, found {count}")
    path.write_text(updated, encoding="utf-8")
    return text


def promote(base_dir: Path, image: str) -> str:
    deployment_paths = {
        slot: base_dir / f"deployment-{slot}.yaml" for slot in SLOTS
    }
    deployment_texts = {
        slot: path.read_text(encoding="utf-8")
        for slot, path in deployment_paths.items()
    }
    service_path = base_dir / "service.yaml"
    service_text = service_path.read_text(encoding="utf-8")
    if not re.search(r"(?m)^kind: Service\s*$", service_text) or not re.search(
        r"(?m)^  name: deploylab\s*$", service_text
    ):
        raise ValueError(f"Unexpected Service manifest: {service_path}")

    selector_match = re.search(
        r"(?ms)^  selector:\n(?P<selector>(?:^    .*\n)+)", service_text
    )
    if not selector_match or not re.search(
        r"(?m)^    app\.kubernetes\.io/name:\s*deploylab\s*$",
        selector_match["selector"],
    ):
        raise ValueError(f"Expected deploylab selector in {service_path}")

    active_match = re.search(
        r"(?m)^    app\.kubernetes\.io/slot:[ \t]*(blue|green)[ \t]*$",
        selector_match["selector"],
    )
    if not active_match:
        raise ValueError(f"Expected blue or green active slot in {service_path}")
    active = active_match.group(1)
    initial_release = any("replace-me" in text for text in deployment_texts.values())
    slots_to_update = SLOTS if initial_release else (
        "green" if active == "blue" else "blue",
    )

    for slot in slots_to_update:
        _replace_image(deployment_paths[slot], slot, image)

    if initial_release:
        return "Initialized both slots; blue remains active"

    inactive = slots_to_update[0]
    selector = selector_match["selector"]
    updated_selector, count = re.subn(
        r"(?m)^([ \t]+app\.kubernetes\.io/slot:[ \t]*)(?:blue|green)[ \t]*$",
        lambda match: f"{match.group(1)}{inactive}",
        selector,
    )
    if count != 1:
        raise ValueError(f"Expected one slot selector in {service_path}, found {count}")
    service_path.write_text(
        service_text[:selector_match.start("selector")]
        + updated_selector
        + service_text[selector_match.end("selector"):],
        encoding="utf-8",
    )
    return f"Updated {inactive}; Service will switch from {active} after it is healthy"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument(
        "--base-dir", type=Path, default=Path("k8s/base")
    )
    args = parser.parse_args()
    print(promote(args.base_dir, args.image))


if __name__ == "__main__":
    main()
