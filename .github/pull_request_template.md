## Motivation (WHY)

Please provide the background and context for this PR. Explain the problem it solves or the feature it adds.

- Why is this change necessary?
- What problem does it solve?
- What functionality or bug has been addressed?

If this PR is addressing multiple issues, please mention them to automatically close these issues when the PR is merged.

Closes #123
Closes #456

## Summary of Changes (WHAT)

Provide a concise overview of the changes introduced in this PR. Describe the specific modifications made to the codebase.

- Are there any breaking changes?
- What changes have you made?

## Type of change

Please delete options that are not relevant and **add the corresponding tag to the PR title** using the Conventional Commits format. For example: `docs: correct typo in README`, `feat: add user authentication feature`. Use the most important or significant commit type (usually feat, fix, or breaking if applicable).

- **BREAKING CHANGE** (appends a ! after the type), introduces a breaking INTERFACE (API, CLI, ...) change. A BREAKING CHANGE can be part of commits of any type. In a library, any change to the signature or name of a function, would be a breaking change.
- **fix**: Bug fix (non-breaking change which fixes an issue)
- **feat**: New feature (non-breaking change which adds functionality)
- **docs**: Documentation update
- **refactor**: Refactor (non-breaking change that improves the structure or style of the code)
- **perf**: Performance improvement
- **chore**: Routine tasks and maintenance changes (e.g., updating dependencies, formatting code) that don't affect functionality
- **test**: Adding or updating tests without affecting production code
- **ci**: Changes to the continuous integration pipeline or related scripts

## Checklist

Please ensure the following are completed **before marking your PR ready for review**:

- [ ] I have assigned myself to the _Assignees_ of the PR in GitHub
- [ ] I have filled the _Labels_ of the PR in GitHub
- [ ] I have performed a self-review of my own code.
- [ ] I have commented my code, particularly in hard-to-understand areas.
- [ ] I have added type annotations to any new arguments, methods, or functions.
- [ ] Any new dependencies have been added to the appropriate dependency management files (e.g., `requirements*.in`, `pyproject.toml`). Also, they have been compiled into their respective `requirements*.txt` or `uv.lock` file.
- [ ] I have updated documentation where applicable (e.g., README, inline docstrings).
- [ ] I have followed [Komorebi's code style guidelines](https://github.com/Komorebi-AI/docs/blob/main/python_dev.md).
- [ ] I have added "Closes #xxxx" in the Motivation
- [ ] Tests added and passed if fixing a bug or adding a new feature.
- [ ] All new and existing tests pass locally.
- [ ] I have add the most relevant tag to the PR title, and it is clear and descriptive.

## (OPTIONAL) Additional Context, Comments, Benchmarks, Experiments

Add any other context or information about the PR that might be useful for the reviewer.

For example, if you have perform any benchmark or experiments. You can include screenshots.
