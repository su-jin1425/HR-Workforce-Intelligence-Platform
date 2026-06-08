from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    app_manifest = load_json(ROOT / "appPackage" / "manifest.json")
    agent_manifest = load_json(ROOT / "appPackage" / "declarativeAgent.json")
    plugin_manifest = load_json(ROOT / "appPackage" / "hr-workforce-plugin.json")

    assert "copilotAgents" in app_manifest, "M365 app manifest must reference a Copilot agent"
    assert agent_manifest["actions"], "Declarative agent must reference at least one action"
    assert plugin_manifest["runtimes"], "Plugin manifest must include an OpenAPI runtime"
    assert (ROOT / "appPackage" / "apiSpecificationFile" / "openapi.yaml").exists()
    print("Manifest structure checks passed.")


if __name__ == "__main__":
    main()
