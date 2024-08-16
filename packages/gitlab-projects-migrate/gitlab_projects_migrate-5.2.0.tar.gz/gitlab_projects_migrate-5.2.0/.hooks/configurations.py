#!/usr/bin/env python3

# Standard libraries
from typing import List, NamedTuple

# Changes regex type
ChangesRegex = str

# Changes parsers class
class ChangesParsers(NamedTuple):
    match: str
    group: int
    commit_type: str

# Changes evaluator class
class ChangesEvaluator(NamedTuple):
    changes: List[ChangesRegex]
    parsers: List[ChangesParsers]

# Changes types class
class ChangesType(NamedTuple):
    commit_type: str
    changes: List[ChangesRegex]

# Changes matcher class
class ChangesMatcher(NamedTuple):
    commit_scope: str
    types: List[ChangesType]

# Commits changes constants
COMMITS_CHANGES_PATTERN: str = r'^#\s*(new file|modified|deleted|renamed|copied):\s*(.+)$'
COMMITS_CHANGES_SECTION: str = '# Changes to be committed:'

# Commits comments constants
COMMITS_COMMENTS_PREFIX: str = '#'

# Commits default constants
COMMITS_DEFAULT_BODY: str = 'Issue: #...'
COMMITS_DEFAULT_SCOPE: str = 'scope'
COMMITS_DEFAULT_SUBJECT: str = ''
COMMITS_DEFAULT_TYPE: str = 'type'

# Commits footers constants
COMMITS_FOOTER_SIGNOFF: str = 'Signed-off-by: '

# Changes evaluators constants
CHANGES_EVALUATORS: List[ChangesEvaluator] = [
    # Sources
    ChangesEvaluator(
        changes=[
            r'^sources|^src',
        ],
        parsers=[
            ChangesParsers(
                match=r'.*/([^_]{1}[^/]*)\.[^/]*$',
                group=1,
                commit_type='fix',
            ),
        ],
    ),
    # Yocto
    ChangesEvaluator(
        changes=[
            r'conf/(distro|machine)|recipes-[^/*]',
        ],
        parsers=[
            ChangesParsers(
                match=r'conf/(distro|machine)/[^/]*.conf$',
                group=1,
                commit_type='fix',
            ),
            ChangesParsers(
                match=r'.*/([^/]*)/[^/]*\.(bb[^/.]*|inc)$',
                group=1,
                commit_type='fix',
            ),
        ],
    ),
]

# Changes matchers constant
CHANGES_MATCHERS: List[ChangesMatcher] = [
    ChangesMatcher(
        commit_scope='gitlab-ci',
        types=[
            ChangesType(
                commit_type='ci',
                changes=[
                    r'\.gitlab-ci\.yml$',
                    r'\.gitlab-ci\.d$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='githooks',
        types=[
            ChangesType(
                commit_type='chore',
                changes=[
                    r'\.githooks$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='gitignore',
        types=[
            ChangesType(
                commit_type='chore',
                changes=[
                    r'\.gitignore$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='makefile',
        types=[
            ChangesType(
                commit_type='build',
                changes=[
                    r'Makefile$',
                    r'\.make$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='commitizen',
        types=[
            ChangesType(
                commit_type='chore',
                changes=[
                    r'\.cz.*$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='coveragerc',
        types=[
            ChangesType(
                commit_type='chore',
                changes=[
                    r'.coveragerc$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='mypy',
        types=[
            ChangesType(
                commit_type='chore',
                changes=[
                    r'mypy\.ini$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='pre-commit',
        types=[
            ChangesType(
                commit_type='chore',
                changes=[
                    r'\.pre-commit.*$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='setup',
        types=[
            ChangesType(
                commit_type='chore',
                changes=[
                    r'setup\.py$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='vscode',
        types=[
            ChangesType(
                commit_type='chore',
                changes=[
                    r'\.vscode/',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='license',
        types=[
            ChangesType(
                commit_type='docs',
                changes=[
                    r'LICENSE.*$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='readme',
        types=[
            ChangesType(
                commit_type='docs',
                changes=[
                    r'docs/',
                    r'README.*$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='changelog',
        types=[
            ChangesType(
                commit_type='docs',
                changes=[
                    r'CHANGELOG.*$',
                ],
            ),
        ],
    ),
    ChangesMatcher(
        commit_scope='tests',
        types=[
            ChangesType(
                commit_type='test',
                changes=[
                    r'^test/',
                    r'^tests/',
                ],
            ),
        ],
    ),
]
