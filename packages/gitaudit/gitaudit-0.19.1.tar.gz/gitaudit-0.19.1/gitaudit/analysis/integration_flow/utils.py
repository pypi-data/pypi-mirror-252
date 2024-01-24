"""Utils for Integration Flow Analysis."""

from typing import List, Tuple, Set
from .int_flow import IntflowPullRequest


def _find_last_stage_in_names(
    names_arr: List[List[str]],
) -> Tuple[Set[str], List[List[str]]]:
    # get the last name of all arrays
    last_names = list(map(lambda x: x[-1], names_arr))

    # get the most used name
    most_used_name = max(set(last_names), key=last_names.count)

    stage_names = set()
    new_found_names = set([most_used_name])

    index_of_names_arr = list(map(len, names_arr))

    while new_found_names:
        current_name = new_found_names.pop()
        stage_names.add(current_name)

        index_of_names_arr = list(
            map(
                lambda names, index, c_name=current_name: min(
                    index,
                    names.index(c_name) if c_name in names else len(names),
                ),
                names_arr,
                index_of_names_arr,
            )
        )

        for names, index in zip(names_arr, index_of_names_arr):
            add_names = names[index:]

            for a_name in add_names:
                if a_name not in stage_names:
                    new_found_names.add(a_name)

    new_names_arr = list(
        map(
            lambda names, index: names[:index],
            names_arr,
            index_of_names_arr,
        )
    )

    new_names_arr = list(filter(None, new_names_arr))

    return stage_names, new_names_arr


def _extract_integration_stages_by_names(names_arr: List[List[str]]) -> List[Set[str]]:
    stage_names = []

    while names_arr:
        new_stage_names, names_arr = _find_last_stage_in_names(names_arr)
        stage_names.append(new_stage_names)

    return list(reversed(stage_names))


def extract_integration_stages(intflow_prs: List[IntflowPullRequest]) -> List[Set[str]]:
    """
    Extracts the integration stages from a list of IntflowPullRequest objects.

    Args:
        intflow_prs: A list of IntflowPullRequest objects.

    Returns:
        A list of sets of integration stages.
    """
    sorted_status_check_names = []

    for int_pr in intflow_prs:
        pr_sorted_status_checks = sorted(
            int_pr.required_status_checks, key=lambda x: x.triggered_at
        )
        names = list(map(lambda x: x.name, pr_sorted_status_checks))

        sorted_status_check_names.append(names)

    return _extract_integration_stages_by_names(sorted_status_check_names)
