import logging
import os
from typing import List, Optional

import gitman
from gitman.models.source import Source

from .api import BaseAddonsResult, GitManAddonsConfig

_logger = logging.getLogger(__name__)


class GitManAddons(BaseAddonsResult):
    def __init__(self, gitman_config: GitManAddonsConfig, location_path: str, source: gitman.models.source.Source):
        super(GitManAddons, self).__init__(gitman_config, source.name, os.path.join(location_path, source.name))

    def install_cmd(self) -> List[List[str]]:
        return []

    def arg_cmd(self) -> List[str]:
        return []


def _get_sources_filter(self, names: List[str], sources: List[Source], skip_default_group: bool) -> List[str]:
    """Get a filtered subset of sources."""
    names_list = list(names)
    if not names_list and not skip_default_group:
        names_list.append(self.default_group)

    # Add sources from groups
    groups_filter = [group for group in self.groups if group.name in names_list]
    sources_filter = [member for group in groups_filter for member in group.members]

    # Add independent sources
    sources_filter.extend([source.name for source in sources if source.name in names_list])

    # Fall back to all sources if allowed
    if not sources_filter:
        if names and names_list != ["all"]:
            print(f"No dependencies match: {' '.join(names)}")
        else:
            sources_filter = [source.name for source in sources if source.name]

    return list(dict.fromkeys(sources_filter).keys())


def find_nested_configs(root: str, depth: Optional[int], skip_paths: List[str]) -> List[gitman.models.config.Config]:
    """Find all other projects in the same directory."""
    configs: List[gitman.models.config.Config] = []
    if depth is not None and depth <= 1:
        return configs

    _logger.debug(f"Searching for nested project in: {root}")
    for name in os.listdir(root):
        if name.startswith("."):
            continue
        path = os.path.join(root, name)
        if os.path.isdir(path) and path not in skip_paths and not os.path.islink(path):
            config = gitman.models.config.load_config(path, search=False)
            if config:
                configs.append(config)

            if os.path.islink(path):
                continue

            if depth is not None:
                configs.extend(find_nested_configs(path, depth - 1, skip_paths))
            else:
                configs.extend(find_nested_configs(path, depth, skip_paths))

    return configs


def find_addons(config: GitManAddonsConfig) -> List[BaseAddonsResult]:
    gm_config = gitman.models.config.load_config(config.path)
    if not gm_config:
        return []
    result: List[GitManAddons] = []
    for gm_config in [gm_config] + find_nested_configs(config.path, 5, []):
        gm_sources = gm_config._get_sources(use_locked=None)
        sources_filters = _get_sources_filter(
            self=gm_config, names=config.name_filter, sources=gm_config.sources, skip_default_group=False
        )
        if not sources_filters:
            # Calling again but without the toplevel source filter
            sources_filters = _get_sources_filter(self=gm_config, sources=gm_config.sources, skip_default_group=False)

        src_by_name = {src.name: src for src in gm_sources}
        for source_filter in sources_filters:
            source = src_by_name.get(source_filter)
            if not source:
                _logger.info("Skipped dependency: %s", source_filter)
                continue
            result.append(GitManAddons(config, gm_config.location_path, source))
    return result
