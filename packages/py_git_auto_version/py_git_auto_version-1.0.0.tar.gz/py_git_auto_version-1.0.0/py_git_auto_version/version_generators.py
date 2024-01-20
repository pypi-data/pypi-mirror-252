from abc import ABC, abstractmethod
import os

from py_git_auto_version.git import Git
from py_git_auto_version.git_ref import GitRef
import regex


def check_envvar_exists_is_not_none_or_empty(envvar):
    if envvar not in os.environ:
        return False
    if os.environ[envvar] is None:
        return False
    if len(os.environ[envvar].strip()) == 0:
        return False
    return True


class VersionGenerator(ABC):
    @staticmethod
    def _helper_method(get_version_from: GitRef, get_branch_from: GitRef):
        branch_name = get_branch_from.full_remote_branch_name.name
        # tag = get_version_from.tag_name.name[1:]
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
        extracted_tag = cd["tag_name"][0][1:]
        commit_count = cd["commit_count"][0]
        # print(branch_name)
        # print(tag)
        # print(extracted_tag)
        # print(commit_count)
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
        return f"{extracted_tag}{extra_version_text}"

    @staticmethod
    @abstractmethod
    def generate_version_string(self) -> str:
        ...


class GitHubActionVersionGenerator(VersionGenerator):
    @staticmethod
    @abstractmethod
    def generate_version_string(self) -> str: ...


class LocalVersionGenerator(VersionGenerator):
    @staticmethod
    @abstractmethod
    def generate_version_string(self) -> str: ...


class PublishActionVersionGenerator(GitHubActionVersionGenerator):
    @classmethod
    def generate_version_string(cls):
        ref_name = os.environ['GITHUB_REF_NAME']
        ref_type = os.environ['GITHUB_REF_TYPE']
        print((ref_name, ref_type))
        build_tag = GitRef(
                (
                        (ref_name, ref_type)
                )
        )
        if build_tag.object_ref_type != 'tag':
            raise ValueError("build tag must be provided as a GitRef object of type 'tag'")
        print(build_tag)
        return cls._helper_method(build_tag, build_tag)


class PullRequestActionVersionGenerator(GitHubActionVersionGenerator):
    @classmethod
    def generate_version_string(cls):
        base_ref_string = os.environ['GITHUB_BASE_REF']
        head_ref_string = os.environ['GITHUB_HEAD_REF']
        print("base ref: ", base_ref_string)
        print("head ref: ", head_ref_string)
        base_branch = GitRef(
                (
                        base_ref_string,
                        'remote'
                )
        )
        merge_branch = GitRef(
                (
                        head_ref_string,
                        'remote'
                )
        )
        print(base_branch)
        print(merge_branch)
        return cls._helper_method(get_version_from=merge_branch, get_branch_from=base_branch)


class LocalBranchBuildVersionGenerator(LocalVersionGenerator):
    @classmethod
    def generate_version_string(cls):
        current_branch_name = Git.Branch.show_current()
        git_ref = GitRef((current_branch_name, 'branch'))
        print(git_ref)
        return cls._helper_method(git_ref, git_ref)


def generate_version_string_for_scenario() -> str:
    if (
            check_envvar_exists_is_not_none_or_empty('GITHUB_BASE_REF')
            and
            check_envvar_exists_is_not_none_or_empty('GITHUB_HEAD_REF')
    ):
        return PullRequestActionVersionGenerator.generate_version_string()
    elif check_envvar_exists_is_not_none_or_empty('GITHUB_REF_NAME'):
        return PublishActionVersionGenerator.generate_version_string()
    else:
        return LocalBranchBuildVersionGenerator.generate_version_string()


if __name__ == "__main__":
    print(generate_version_string_for_scenario())
