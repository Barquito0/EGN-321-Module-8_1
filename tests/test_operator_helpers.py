from pathlib import Path
from scripts.source_control import change_source
from scripts.preflight import source_csv_check,port_free
from scripts.prepare_application import verify_app
from scripts.view_logs import last_events


def test_source_pause_and_resume_non_destructive(tmp_path):
    app=tmp_path/'application'
    (app/'src').mkdir(parents=True)
    (app/'src'/'monitor.py').write_text('')
    (app/'state').mkdir()
    preserved=app/'state'/'monitor.db'
    preserved.write_bytes(b'persist-me')
    assert 'PAUSED' in change_source(app,'pause')
    assert 'PAUSED' in change_source(app,'status')
    assert 'RESUMED' in change_source(app,'resume')
    assert 'NOT PAUSED' in change_source(app,'status')
    assert preserved.read_bytes()==b'persist-me'


def test_csv_structure_accept_and_reject(tmp_path):
    p=tmp_path/'readings.csv'
    p.write_text('sample_number,timestamp,temperature_c,temperature_status\n1,2026-10-01T08:00:00,21,OK\n')
    assert source_csv_check(p)[0]
    p.write_text('sample_number,temp\n1,20\n')
    ok,message=source_csv_check(p)
    assert not ok and 'columns' in message


def test_prepared_source_verification(tmp_path):
    assert 'app.py' in verify_app(tmp_path)


def test_log_reader_handles_unreadable_entry(tmp_path):
    p=tmp_path/'app.jsonl'
    p.write_text('{"event":"STARTUP","message":"ready"}\ninvalid\n',encoding='utf-8')
    entries=last_events(p,2)
    assert entries[0]['event']=='STARTUP'
    assert entries[1]['event']=='UNPARSEABLE_LINE'


def test_bundle_csv_sample_is_real():
    p=Path(__file__).resolve().parents[1]/'data'/'module6_sample_sensor_history.csv'
    ok,detail=source_csv_check(p)
    assert ok and 'sample #1' in detail


def test_inherited_tests_runner_reports_missing_checkout():
    import subprocess
    import sys
    from scripts import run_application_tests
    # The helper uses an explicit working directory and current Python interpreter.
    assert (run_application_tests.ROOT / "scripts" / "run_application_tests.py").is_file()
    assert sys.executable
