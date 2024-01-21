from typing import Any, AnyStr, Optional

from pydantic import BaseSettings, validator, ValidationError
import regex


class PyGitAutoVersionSettings(BaseSettings):
    TAG_TO_VERSION_PATTERN: regex.Pattern[AnyStr]
    APPEND_BRANCH_AS_LOCAL_VERSION_IDENTIFIER: bool
    
    @classmethod
    def generate_defaults(cls):
        tag_to_version_pattern = regex.compile(
                "^v?(?P<major>[0-9]+)[.](?P<minor>[0-9]+)[.](?P<patch>[0-9]+)$", flags=regex.V1)
        append_branch_as_local_version = True
        return cls(
                TAG_TO_VERSION_PATTERN=tag_to_version_pattern,
                APPEND_BRANCH_AS_LOCAL_VERSION_IDENTIFIER=append_branch_as_local_version
        )
    
    @classmethod
    def create_object_from_env(
            cls,
            _env_file: Optional[str] = None,
            _env_file_encoding: Optional[str] = None,
            fall_back_to_defaults_on_error=True
    ):
        try:
            result = cls(
                    _env_file=_env_file,
                    _env_file_encoding=_env_file_encoding
            )
            return result
        except ValueError as e:
            if not fall_back_to_defaults_on_error:
                raise e
        except TypeError as e:
            if not fall_back_to_defaults_on_error:
                raise e
        return cls.generate_defaults()
    
    @classmethod
    def generate_failover_try_env_then_dotenv_then_defaults(
            cls
    ):
        try:
            result = cls.create_object_from_env(
                    fall_back_to_defaults_on_error=False
            )
            return result
        except ValueError:
            ...
        except TypeError:
            ...
        return cls.create_object_from_env(
                _env_file=".env",
                fall_back_to_defaults_on_error=True
        )
        
    @validator("TAG_TO_VERSION_PATTERN")
    def must_capture_version_segments_by_name(
            cls,
            v: regex.Pattern[AnyStr]
    ):
        if v is None:
            raise ValueError("Pattern must not be none")
        required_captures = {'major', 'minor', 'patch'}
        named_group_keys = set(v.groupindex.keys())
        missing_groups = required_captures - named_group_keys
        if len(missing_groups) != 0:
            raise ValueError(
                    (
                        f"Pattern must provide the following named capture groups: {required_captures}."
                        f" the following are missing: {missing_groups}."
                    )
            )
        return v
    
    class Config:
        env_prefix = "PY_GIT_AUTO_VERSION_"
        case_sensitive = True
        
        @validator("")
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == 'TAG_TO_VERSION_PATTERN':
                return regex.compile(raw_val, flags=regex.V1)
            else:
                return cls.json_loads(raw_val)


__all__ = [
        PyGitAutoVersionSettings
]
