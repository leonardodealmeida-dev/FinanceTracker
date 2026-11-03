import os
import sys
from contextlib import contextmanager

from app import config


@contextmanager
def env(**values):
    """Temporarily set (or clear, when None) environment variables."""
    old = {k: os.environ.get(k) for k in values}
    try:
        for k, v in values.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def test_env_vars_are_used():
    with env(SUPABASE_URL="https://x.supabase.co", SUPABASE_KEY="sb_publishable_abc"):
        assert config.get_supabase_settings() == ("https://x.supabase.co", "sb_publishable_abc")


def test_missing_settings_raise_config_error():
    from app import bundled_config
    old = (bundled_config.SUPABASE_URL, bundled_config.SUPABASE_KEY)
    bundled_config.SUPABASE_URL = bundled_config.SUPABASE_KEY = ""
    try:
        with env(SUPABASE_URL=None, SUPABASE_KEY=None):
            # Not frozen, so a developer .env could be read; point cwd away.
            cwd = os.getcwd()
            os.chdir("/")
            try:
                try:
                    config.get_supabase_settings()
                    raised = False
                except config.ConfigError:
                    raised = True
            finally:
                os.chdir(cwd)
        assert raised
    finally:
        bundled_config.SUPABASE_URL, bundled_config.SUPABASE_KEY = old


def test_bundled_values_used_when_env_empty():
    from app import bundled_config
    old = (bundled_config.SUPABASE_URL, bundled_config.SUPABASE_KEY)
    bundled_config.SUPABASE_URL = "https://bundled.supabase.co"
    bundled_config.SUPABASE_KEY = "sb_publishable_bundled"
    try:
        with env(SUPABASE_URL=None, SUPABASE_KEY=None):
            cwd = os.getcwd()
            os.chdir("/")
            try:
                got = config.get_supabase_settings()
            finally:
                os.chdir(cwd)
        assert got == ("https://bundled.supabase.co", "sb_publishable_bundled")
    finally:
        bundled_config.SUPABASE_URL, bundled_config.SUPABASE_KEY = old


def test_resource_path_points_to_assets():
    assert os.path.exists(config.resource_path("assets/icon.png"))


def test_bundler_refuses_secret_keys():
    import subprocess
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script = os.path.join(root, "tools", "write_bundled_config.py")
    for bad in ("sb_secret_123", "eyJ...service_role...x"):
        result = subprocess.run(
            [sys.executable, script],
            env={**os.environ, "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_KEY": bad},
            capture_output=True, text=True,
        )
        assert result.returncode != 0 and "secret" in result.stderr.lower()
    result = subprocess.run(
        [sys.executable, script],
        env={k: v for k, v in os.environ.items() if not k.startswith("SUPABASE_")},
        capture_output=True, text=True,
    )
    assert result.returncode != 0
