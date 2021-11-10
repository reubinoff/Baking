from nox_poetry import session, Session

# @nox.session
# def lint(session):
#     session.install("pylint")
#     session.run("pylint", "src")


@session(python="3.9")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run("safety", "check", "--full-report", f"--file={requirements}")


@session(python="3.9")
def pytest(session: Session) -> None:
    """pytest"""
    requirements = session.poetry.export_requirements()
    session.install("-r", f"{requirements}")
    session.install(".")
    session.run("pytest", "tests", "-xvv", "--cov=src/baking/routers")
