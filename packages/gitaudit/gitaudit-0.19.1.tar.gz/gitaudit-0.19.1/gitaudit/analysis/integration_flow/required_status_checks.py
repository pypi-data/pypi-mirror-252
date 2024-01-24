"""Gets required status checks for a pull request"""

from typing import Dict, List, Tuple
from datetime import datetime, timedelta

from gitaudit.root import GitauditRootModel
from gitaudit.github.instance import Github
from gitaudit.github.graphql_objects import PullRequest, PullRequestState, CheckRun


class RequiredNameResult(GitauditRootModel):
    """Result of a required name query"""

    names: List[str]
    last_updated: datetime


class GithubPullRequestRequired:
    """Gets required status checks for a pull request"""

    def __init__(
        self, github: Github, refresh_time_delta: timedelta = timedelta(minutes=30)
    ) -> None:
        self.github = github
        self.refresh_time_delta = refresh_time_delta

        self.repo_branch_map: Dict[Tuple[str, str, str], RequiredNameResult] = {}

    def _query_get_required_check_run_names(
        self,
        owner: str,
        repo: str,
        number: int,
        head_ref_oid: str,
    ) -> List[str]:
        commit = self.github.get_commit_for_expression(
            owner,
            repo,
            head_ref_oid,
            f"""
            statusCheckRollup {{
                contexts (last:100) {{
                    nodes {{
                        ... on CheckRun {{
                            name
                            isRequired (pullRequestNumber: {number})
                        }}
                        ... on StatusContext {{
                            context
                            isRequired (pullRequestNumber: {number})
                        }}
                    }}
                }}
            }}
            """,
        )

        if not commit.status_check_rollup:
            return []

        return list(
            map(
                lambda y: y.name if isinstance(y, CheckRun) else y.context,
                filter(lambda x: x.is_required, commit.status_check_rollup.contexts),
            )
        )

    def get_required_status_checks_for_branch(
        self, owner: str, repo: str, branch: str
    ) -> List[str]:
        """
        Gets required check run names for a branch

        Args:
            owner: Owner of the repository
            repo: Repository name
            branch: Branch name

        Returns:
            list[str]: List of required check run names
        """

        repo_branch_key = (
            owner,
            repo,
            branch,
        )

        if repo_branch_key in self.repo_branch_map:
            res = self.repo_branch_map[repo_branch_key]
            if datetime.utcnow() - res.last_updated < self.refresh_time_delta:
                return res.names
            else:
                self.repo_branch_map.pop(repo_branch_key)

        pull_requests = self.github.search_pull_requests(
            search_query=f"repo:{owner}/{repo} base:{branch} is:pr is:open",
            querydata="headRefOid number repository { nameWithOwner } baseRefName state",
            count=1,
        )

        if not len(pull_requests) == 1:
            return []

        pull_request = pull_requests[0]

        return self.get_required_status_checks_for_pull_request(pull_request)

    def get_required_status_checks_for_pull_request(
        self, pull_request: PullRequest
    ) -> List[str]:
        """
        Gets required check run names for a pull request

        Args:
            pull_request: Pull request to get required check run names for

        Returns:
            list[str]: List of required check run names"""

        if pull_request.state != PullRequestState.OPEN:
            # In case of a merged PR the result all checks are no longer required. So only
            # in case of an open PR querying the information is actually required.
            return []

        owner, repo = pull_request.repository.name_with_owner.split("/")

        repo_branch_key = (
            owner,
            repo,
            pull_request.base_ref_name,
        )

        if repo_branch_key in self.repo_branch_map:
            res = self.repo_branch_map[repo_branch_key]
            if datetime.utcnow() - res.last_updated < self.refresh_time_delta:
                return res.names
            else:
                self.repo_branch_map.pop(repo_branch_key)

        names = self._query_get_required_check_run_names(
            owner,
            repo,
            pull_request.number,
            pull_request.head_ref_oid,
        )
        self.repo_branch_map[repo_branch_key] = RequiredNameResult(
            names=names,
            last_updated=datetime.utcnow(),
        )
        return names
