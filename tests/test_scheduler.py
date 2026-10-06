from datetime import datetime, timedelta

from database.database import Database
from scheduler.service import SchedulerService


def test_scheduler_persists_task(tmp_path):
    db = Database(tmp_path / "tasks.db")
    db.initialize()
    service = SchedulerService(db, lambda _: None)
    run_at = datetime.now() + timedelta(hours=1)
    task_id = service.add("study", run_at, "daily")
    rows = db.list_tasks()
    assert rows[0]["id"] == task_id
    assert rows[0]["repeat"] == "daily"
