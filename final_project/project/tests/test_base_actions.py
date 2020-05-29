import pytest


@pytest.mark.runapp
def test_run_app(run_app):
    run_app()


@pytest.mark.shutdownapp
def test_shutdown_app(shutdown_app):
    shutdown_app()
