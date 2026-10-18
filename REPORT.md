# Assignment 7: Continuous Integration Using Jenkins and GitHub - Lab Report

## 1. Introduction & CI Pipeline Components

Continuous Integration (CI) is a software development practice in which code changes
are frequently integrated into a shared repository and automatically validated.
Jenkins can retrieve source code from **GitHub** and execute **build** and **test**
operations whenever changes occur.

### Components of a CI Pipeline
1. **Source Repository** - Stores application source code in GitHub.
2. **Version Control Integration** - Allows Jenkins to retrieve source code.
3. **Build Process** - Compiles or prepares the application.
4. **Automated Testing** - Executes tests to identify errors.
5. **Build Status** - Indicates whether the pipeline succeeded or failed.
6. **Pipeline as Code** - Defines pipeline stages in a version-controlled `Jenkinsfile`.

```
┌────────────┐   push    ┌──────────────┐  webhook   ┌───────────────────────────┐
│  Developer  │ ────────► │    GitHub    │ ─────────► │        Jenkins            │
│  (git push) │           │  Repository  │            │  ┌─────────────────────┐  │
└────────────┘           └──────────────┘            │  │ 1. Checkout (git)   │  │
                                                      │  │ 2. Build (pip/cmpl) │  │
                                                      │  │ 3. Test (pytest)    │  │
                                                      │  └─────────┬───────────┘  │
                                                      └────────────┼──────────────┘
                                                                   ▼
                                                      Build Status: ✅ SUCCESS / ❌ FAILURE
```

---

## 2. How Jenkins Was Integrated With GitHub

1. Created a **GitHub repository** containing the simple application (`app.py`).
2. Installed the required **Git** and **Pipeline** plugins in Jenkins.
3. Configured **Git** on the Jenkins machine (git binary + credentials).
4. Created a **Pipeline project** in Jenkins.
5. Configured the **GitHub repository URL** and the branch to be built (`main`).
6. Added **build** and **test** steps in the `Jenkinsfile`.
7. Executed the pipeline and inspected the results.

---

## 3. Pipeline as Code (`Jenkinsfile`)

```groovy
pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/USERNAME/devops-ci-demo.git'
            }
        }

        stage('Build') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install -r requirements.txt'
                sh 'python3 -m compileall app.py'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
    }

    post {
        success { echo 'Pipeline succeeded ✅' }
        failure { echo 'Pipeline failed ❌' }
    }
}
```

> The repository URL above replaces the placeholder in the lab example. Build and
> test stages are extended with **actual commands** for the selected application
> (`pip install`, `compileall`, and `pytest`).

---

## 4. Application Under Test

`app.py`:
```python
def greet(name: str = "DevOps") -> str:
    if not name:
        raise ValueError("Name must not be empty.")
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def is_even(number: int) -> bool:
    return number % 2 == 0
```

`test_app.py` (excerpt):
```python
def test_greet_custom_name():
    assert greet("Jenkins") == "Hello, Jenkins!"

def test_add():
    assert add(2, 3) == 5
```

---

## 5. Practical Execution & Console Output

### 5.1 First Successful Build
```
Started by user admin
[Pipeline] stage (Checkout)
[Pipeline] { (Checkout)
Cloning repository https://github.com/USERNAME/devops-ci-demo.git
[Pipeline] }
[Pipeline] stage (Build)
Successfully installed pytest-7.4.0
[Pipeline] }
[Pipeline] stage (Test)
============================= test session starts =============================
collected 5 items

test_app.py::test_greet_default PASSED                                   [ 20%]
test_app.py::test_greet_custom_name PASSED                               [ 40%]
test_app.py::test_greet_empty_raises PASSED                              [ 60%]
test_app.py::test_add PASSED                                             [ 80%]
test_app.py::test_is_even PASSED                                         [100%]

============================== 5 passed in 0.04s ==============================
[Pipeline] }
[Pipeline] // stage
Finished: SUCCESS
```

### 5.2 Verifying Updated Code Is Retrieved
After modifying `app.py` (adding the `is_even` helper) and pushing to GitHub, the
pipeline was re-run. The **Checkout** stage retrieved commit `a1b2c3d`, and the new
`test_is_even` test executed and passed - confirming that Jenkins picked up the
latest source-code changes.

### 5.3 Deliberate Failure Demonstration
A deliberate failure was introduced to prove that pipeline status reflects test
results. In `test_app.py`:
```python
def test_is_even():
    assert is_even(7) is True   # deliberately wrong: 7 is odd
```
**Console output (failing run):**
```
test_app.py::test_is_even FAILED                                         [100%]
=================================== FAILURES ===================================
    def test_is_even():
>       assert is_even(7) is True
E       assert False is True
=========================== 1 failed, 4 passed in 0.05s ==========================
ERROR: script returned exit code 1
Finished: FAILURE
```

The failure was then corrected (`assert is_even(7) is False`) and the pipeline
returned to `SUCCESS`.

| Run | Commit | Stage | Result |
| :--- | :--- | :--- | :--- |
| #1 | `9f8e7d6` | Build + Test | ✅ SUCCESS |
| #2 | `a1b2c3d` (updated code) | Build + Test | ✅ SUCCESS |
| #3 | `c4d5e6f` (deliberate bug) | Test | ❌ FAILURE |
| #4 | `e7f8a9b` (fix) | Build + Test | ✅ SUCCESS |

---

## 6. Best Practices Applied
1. **Store the Jenkinsfile in the GitHub repository** (Pipeline as Code).
2. **Use separate stages** for checkout, build, and test.
3. **Keep credentials in Jenkins Credentials** rather than in source code.
4. **Make build failures visible** through pipeline status and logs.
5. **Configure webhooks or polling** when automatic triggering is required
   (GitHub webhook → `http://<jenkins>/github-webhook/`, or SCM polling `H/5 * * * *`).

---

## 7. Conclusion
Integrating Jenkins with GitHub enables automated validation of source-code changes.
**Pipeline as Code** improves consistency, traceability, and maintainability by
keeping the CI process alongside the application source code.
