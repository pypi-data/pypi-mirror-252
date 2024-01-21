from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from py_git_auto_version.git import Git
from py_git_auto_version.git_ref import GitRef
from py_git_auto_version.settings.auto_version import PyGitAutoVersionSettings
from py_git_auto_version.settings.github import GitHubActionEnvVars
import regex


class VersionGenerator(ABC):
    @staticmethod
    def _helper_method(
            get_version_from: GitRef,
            get_branch_from: GitRef,
            auto_version_: PyGitAutoVersionSettings,
            github_: GitHubActionEnvVars
    ):
        branch_name = get_branch_from.full_remote_branch_name.name
        describe_long_output = Git.Describe.long(get_version_from.object_git_hash)
        compiled_pattern = regex.compile(
                r"^(?P<tag_name>.+)[-](?P<commit_count>[0-9]+)[-](?P<short_hash>[0-9a-z]+)$",
                flags=regex.V1
        )
        m = compiled_pattern.match(describe_long_output)
        if not m:
            raise ValueError(
                f"could not parse output from git describe --long: {describe_long_output}"
                )
        cd = m.capturesdict()
        extracted_tag = cd["tag_name"][0]
        commit_count = cd["commit_count"][0]
        tag_m = auto_version_.TAG_TO_VERSION_PATTERN.match(extracted_tag)
        if not tag_m:
            raise ValueError(f"Unable to use configured pattern to parse tag: {tag_m}")
        captures_dict = tag_m.capturesdict()
        major_v = captures_dict['major'][0]
        minor_v = captures_dict['minor'][0]
        patch_v = captures_dict['patch'][0]
        version_text = f"{major_v}.{minor_v}.{patch_v}"
        if auto_version_.APPEND_BRANCH_AS_LOCAL_VERSION_IDENTIFIER:
            if branch_name == 'main':
                if commit_count == '0':
                    extra_version_text = ""
                else:
                    extra_version_text = f".post{commit_count}"
            else:
                cleaned_branch_name = regex.sub(
                        pattern="[^0-9a-zA-Z.-]",
                        repl="",
                        string=branch_name
                ).replace('-', '.').strip(".")
                extra_version_text = f".dev{commit_count}+branch.{cleaned_branch_name}"
            return f"{version_text}{extra_version_text}"
        else:
            return version_text

    @classmethod
    @abstractmethod
    def generate_version_string(
            cls,
            auto_version_: PyGitAutoVersionSettings,
            github_: GitHubActionEnvVars
    ) -> str:
        ...


class GitHubActionVersionGenerator(VersionGenerator):
    @classmethod
    @abstractmethod
    def generate_version_string(
            cls,
            auto_version_: PyGitAutoVersionSettings,
            github_: GitHubActionEnvVars
    ) -> str: ...


class LocalVersionGenerator(VersionGenerator):
    @classmethod
    @abstractmethod
    def generate_version_string(
            cls,
            auto_version_: PyGitAutoVersionSettings,
            github_: GitHubActionEnvVars
    ) -> str: ...


class PublishActionVersionGenerator(GitHubActionVersionGenerator):
    @classmethod
    def generate_version_string(
            cls,
            auto_version_: PyGitAutoVersionSettings,
            github_: GitHubActionEnvVars
    ):
        ref_name = github_.REF_NAME
        ref_type = github_.REF_TYPE
        # print((ref_name, ref_type))
        build_tag = GitRef(
                (
                        (ref_name, ref_type)
                ),
                tag_to_version_pattern=auto_version_.TAG_TO_VERSION_PATTERN
        )
        if build_tag.object_ref_type != 'tag':
            raise ValueError("build tag must be provided as a GitRef object of type 'tag'")
        # print(build_tag)
        return cls._helper_method(
                get_version_from=build_tag,
                get_branch_from=build_tag,
                auto_version_=auto_version_,
                github_=github_
        )


class PullRequestActionVersionGenerator(GitHubActionVersionGenerator):
    @classmethod
    def generate_version_string(
            cls,
            auto_version_: PyGitAutoVersionSettings,
            github_: GitHubActionEnvVars
    ):
        base_ref_string = github_.BASE_REF
        head_ref_string = github_.HEAD_REF
        # print("base ref: ", base_ref_string)
        # print("head ref: ", head_ref_string)
        base_branch = GitRef(
                (
                        base_ref_string,
                        'remote'
                ),
                tag_to_version_pattern=auto_version_.TAG_TO_VERSION_PATTERN
        )
        merge_branch = GitRef(
                (
                        head_ref_string,
                        'remote'
                ),
                tag_to_version_pattern=auto_version_.TAG_TO_VERSION_PATTERN
        )
        # print(base_branch)
        # print(merge_branch)
        return cls._helper_method(
                get_version_from=merge_branch,
                get_branch_from=base_branch,
                auto_version_=auto_version_,
                github_=github_
        )


class LocalBuildVersionGenerator(LocalVersionGenerator):
    @classmethod
    def generate_version_string(
            cls,
            auto_version_: PyGitAutoVersionSettings,
            github_: GitHubActionEnvVars
    ):
        current_branch_name = Git.Branch.show_current()
        git_ref = GitRef(
                (current_branch_name, 'branch'),
                tag_to_version_pattern=auto_version_.TAG_TO_VERSION_PATTERN
        )
        # print(git_ref)
        return cls._helper_method(
                get_version_from=git_ref,
                get_branch_from=git_ref,
                auto_version_=auto_version_,
                github_=github_
        )


def generate_version_string_for_scenario(
        auto_version_settings: Optional[PyGitAutoVersionSettings] = None,
        github_action_env_vars: Optional[GitHubActionEnvVars] = None
) -> str:
    def neither_none_nor_empty(val: Optional[str]) -> bool:
        return not((val is None) or (len(val) == 0))
    
    if auto_version_settings is None:
        auto_version_ = PyGitAutoVersionSettings()
    else:
        auto_version_ = auto_version_settings
    if github_action_env_vars is None:
        github_ = GitHubActionEnvVars()
    else:
        github_ = github_action_env_vars
    if (
        neither_none_nor_empty(github_.HEAD_REF)
        and
        neither_none_nor_empty(github_.BASE_REF)
    ):
        return PullRequestActionVersionGenerator.generate_version_string(
                auto_version_=auto_version_,
                github_=github_
        )
    elif neither_none_nor_empty(github_.REF_NAME):
        return PublishActionVersionGenerator.generate_version_string(
                auto_version_=auto_version_,
                github_=github_
        )
    else:
        return LocalBuildVersionGenerator.generate_version_string(
                auto_version_=auto_version_,
                github_=github_
        )


__all__ = [
        'generate_version_string_for_scenario'
]


if __name__ == "__main__":
    from py_git_auto_version.get_version import for_toml
    print(for_toml())
