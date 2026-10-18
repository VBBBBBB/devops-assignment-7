# Assignment 7: Continuous Integration Using Jenkins and GitHub

A Jenkins **Declarative Pipeline** that checks out a plain Python application from
GitHub and executes automated **build** and **test** stages.

## Project Structure
- `app.py`: Simple application (greeting + arithmetic helpers).
- `test_app.py`: Pytest automated tests executed by the pipeline.
- `requirements.txt`: Python dependencies.
- `Jenkinsfile`: Pipeline-as-Code definition (Checkout → Build → Test).
- `REPORT.md`: Full lab report.

## Pipeline Stages
1. **Checkout** - Clones the GitHub repository using the `git` step.
2. **Build** - Installs dependencies and byte-compiles the application.
3. **Test** - Runs `pytest` and publishes the JUnit test report.

## Usage
```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

> Replace `USERNAME/devops-ci-demo.git` inside `Jenkinsfile` with your own GitHub
> repository URL before running the pipeline.
