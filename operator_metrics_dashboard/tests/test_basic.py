import json
import os
import subprocess
import sys

def test_applications_json_valid():
    """Ensure that the applications.json file exists and contains valid records."""
    root = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(root, "applications.json")
    assert os.path.isfile(path), f"{path} does not exist"
    with open(path, "r") as f:
        data = json.load(f)
    assert isinstance(data, list), "applications.json should contain a list"
    for record in data:
        assert "company" in record
        assert "position" in record
        assert "status" in record
        assert "hours_saved_by_automation" in record

def test_update_data_runs():
    """Run the update_data script and assert it exits successfully."""
    root = os.path.dirname(os.path.dirname(__file__))
    script = os.path.join(root, "update_data.py")
    # Use sys.executable to ensure the same interpreter is used
    result = subprocess.run([sys.executable, script], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, f"update_data.py failed: {result.stderr}"