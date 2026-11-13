import json
from meridian.cli import execute, main
from meridian.evaluation.benchmark import run as quality_report


def test_all_cli_experiments_work(capsys):
    for command in ("retrieval", "serving", "quantization", "agents", "temporal", "calibration"):
        result = execute(command, seed=7)
        assert isinstance(result, dict) and result


def test_cli_output_writes_reproducible_report(tmp_path, capsys):
    path = tmp_path / "report.json"
    result = main(["retrieval", "--seed", "3", "--output", str(path)])
    assert json.loads(path.read_text()) == result
    assert "retrieval" in capsys.readouterr().out


def test_quality_report_deterministic_with_seed():
    assert quality_report(seed=13, n=100) == quality_report(seed=13, n=100)


def test_all_experiments_produce_strict_json():
    import json
    for name in ("retrieval", "serving", "quantization", "agents", "temporal", "calibration"):
        data = execute(name, seed=7)
        assert json.loads(json.dumps(data, allow_nan=False)) == data
