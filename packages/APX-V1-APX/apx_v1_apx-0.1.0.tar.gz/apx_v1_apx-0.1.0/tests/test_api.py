import apx


def test_apx_launch(enable_all_clouds):
    task = apx.Task()
    job_id, handle = apx.launch(task, dryrun=True)
    assert job_id is None and handle is None
