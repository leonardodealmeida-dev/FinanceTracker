import tempfile
from pathlib import Path
from types import SimpleNamespace

from app import tutorial_state as ts


def user(uid="u1", metadata=None):
    return SimpleNamespace(id=uid, user_metadata=metadata)


class FakeClient:
    def __init__(self, fail=False):
        self.calls, self.fail = [], fail
        self.auth = self

    def update_user(self, payload):
        if self.fail:
            raise RuntimeError("offline")
        self.calls.append(payload)


def tmp_path():
    return Path(tempfile.mkdtemp()) / "state.json"


def test_new_user_sees_tutorial_then_not_again():
    path = tmp_path()
    u = user()
    assert ts.should_show(u, path)
    client = FakeClient()
    ts.mark_seen(u, client, path)
    assert not ts.should_show(u, path)
    assert client.calls == [{"data": {"tutorial_seen": True}}]


def test_other_user_on_same_computer_still_sees_it():
    path = tmp_path()
    ts.mark_seen(user("a"), None, path)
    assert ts.should_show(user("b"), path)


def test_account_flag_follows_user_to_new_computer():
    assert not ts.should_show(user("x", {"tutorial_seen": True}), tmp_path())


def test_offline_failure_still_remembers_locally():
    path = tmp_path()
    u = user()
    ts.mark_seen(u, FakeClient(fail=True), path)
    assert not ts.should_show(u, path)


def test_corrupt_state_file_is_ignored():
    path = tmp_path()
    path.write_text("{not json")
    assert ts.should_show(user(), path)
    ts.mark_seen(user(), None, path)
    assert not ts.should_show(user(), path)
