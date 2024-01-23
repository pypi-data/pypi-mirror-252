import os
import unittest
from typing import TypeVar

from src.addons_installer import cli
from src.addons_installer.git_credential import (
    AddonsCredentialGit,
    GitCredentialManager,
)
from tests import PROFILE_PATH

T = TypeVar("T")


class TestGitCredentialProfile(unittest.TestCase):
    def test_gitlab_com_profile(self):
        result = cli.setup_git_from_env(
            cli.ArgsCli(profiles=str(PROFILE_PATH.joinpath("gitlab-ndp-cred.env")), install="GITLAB", cmd_only=True)
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0],
            [
                "git",
                "config",
                "--global",
                "url.https://my-login-http-for-gitlab.ndp:my-token-for-gitlab.ndp@gitlab.ndp-systemes.fr/.insteadOf",
                "git@gitlab.ndp-systemes.fr:",
            ],
        )

    def test_gitlab_both_profile_order1(self):
        result = cli.setup_git_from_env(
            cli.ArgsCli(
                profiles=",".join(
                    [
                        str(PROFILE_PATH.joinpath("gitlab-ndp-cred.env")),
                        str(PROFILE_PATH.joinpath("gitlab-com-cred.env")),
                    ]
                ),
                install="GITLAB_COM,GITLAB",
                cmd_only=True,
            )
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(
            result[0],
            [
                "git",
                "config",
                "--global",
                "url.https://my-login-http-for-gitlab.ndp:my-token-for-gitlab.ndp@gitlab.ndp-systemes.fr/.insteadOf",
                "git@gitlab.ndp-systemes.fr:",
            ],
        )
        self.assertEqual(
            result[1],
            [
                "git",
                "config",
                "--global",
                "url.https://my-login-http-for-gitlab.com:my-token-for-gitlab.com@gitlab.com/.insteadOf",
                "git@gitlab.com:",
            ],
        )

    @unittest.skipIf(os.getenv("CI"), "Never run in a CI env")
    def test_all_profiles(self):
        result = cli.setup_git_from_env(
            cli.ArgsCli(
                profiles=",".join(
                    [
                        str(PROFILE_PATH.joinpath("gitlab-ndp-cred.env")),
                        str(PROFILE_PATH.joinpath("gitlab-com-cred.env")),
                    ]
                ),
                all=True,
                cmd_only=True,
            )
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(
            result[0],
            [
                "git",
                "config",
                "--global",
                "url.https://my-login-http-for-gitlab.ndp:my-token-for-gitlab.ndp@gitlab.ndp-systemes.fr/.insteadOf",
                "git@gitlab.ndp-systemes.fr:",
            ],
        )
        self.assertEqual(
            result[1],
            [
                "git",
                "config",
                "--global",
                "url.https://my-login-http-for-gitlab.com:my-token-for-gitlab.com@gitlab.com/.insteadOf",
                "git@gitlab.com:",
            ],
        )

    @unittest.skipUnless(os.getenv("CI"), "Only run in a CI env")
    def test_all_profiles_ci_context(self):
        result = cli.setup_git_from_env(
            cli.ArgsCli(
                profiles=",".join(
                    [
                        str(PROFILE_PATH.joinpath("gitlab-ndp-cred.env")),
                        str(PROFILE_PATH.joinpath("gitlab-com-cred.env")),
                    ]
                ),
                all=True,
                cmd_only=True,
            )
        )
        self.assertEqual(len(result), 3)
        self.assertEqual(
            result[0],
            [
                "git",
                "config",
                "--global",
                "url.https://my-login-http-for-gitlab.ndp:my-token-for-gitlab.ndp@gitlab.ndp-systemes.fr/.insteadOf",
                "git@gitlab.ndp-systemes.fr:",
            ],
        )
        self.assertEqual(
            result[1],
            [
                "git",
                "config",
                "--global",
                "url.https://my-login-http-for-gitlab.com:my-token-for-gitlab.com@gitlab.com/.insteadOf",
                "git@gitlab.com:",
            ],
        )
        self.assertEqual(
            result[2],
            [
                "git",
                "config",
                "--global",
                f'url.https://gitlab-ci-token:{os.getenv("CI_JOB_TOKEN")}@gitlab.ndp-systemes.fr/.insteadOf',
                "git@gitlab.ndp-systemes.fr:",
            ],
        )

    @unittest.skipUnless(os.getenv("CI"), "Only run in a CI env")
    def test_gitlab_ci_profiles(self):
        result = cli.setup_git_from_env(
            cli.ArgsCli(
                profiles=",".join(
                    [
                        str(PROFILE_PATH.joinpath("gitlab-ndp-cred.env")),
                        str(PROFILE_PATH.joinpath("gitlab-com-cred.env")),
                    ]
                ),
                install="GITLAB_CI",
                cmd_only=True,
            )
        )
        self.assertEqual(
            result[0],
            [
                "git",
                "config",
                "--global",
                f'url.https://gitlab-ci-token:{os.getenv("CI_JOB_TOKEN")}@gitlab.ndp-systemes.fr/.insteadOf',
                "git@gitlab.ndp-systemes.fr:",
            ],
        )

    @unittest.skipUnless(os.getenv("CI"), "Only run in a CI env")
    def test_ci_auto_define(self):
        addon_def = AddonsCredentialGit.extract_ci_credential(dict(os.environ))
        self.assertTrue(addon_def, "A Gitlab ci credential is created with the job token")
        self.assertEqual(addon_def.name, "GITLAB_CI")
        self.assertEqual(addon_def.username, "gitlab-ci-token")
        self.assertEqual(addon_def.password, os.getenv("CI_JOB_TOKEN"))
        self.assertEqual(addon_def.host, os.getenv("CI_SERVER_HOST"))

    def test_gitlab_both_profile_order2(self):
        result = cli.setup_git_from_env(
            cli.ArgsCli(
                profiles=",".join(
                    [
                        str(PROFILE_PATH.joinpath("gitlab-ndp-cred.env")),
                        str(PROFILE_PATH.joinpath("gitlab-com-cred.env")),
                    ]
                ),
                install="GITLAB,GITLAB_COM",
                cmd_only=True,
            )
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(
            result[0],
            [
                "git",
                "config",
                "--global",
                "url.https://my-login-http-for-gitlab.ndp:my-token-for-gitlab.ndp@gitlab.ndp-systemes.fr/.insteadOf",
                "git@gitlab.ndp-systemes.fr:",
            ],
        )
        self.assertEqual(
            result[1],
            [
                "git",
                "config",
                "--global",
                "url.https://my-login-http-for-gitlab.com:my-token-for-gitlab.com@gitlab.com/.insteadOf",
                "git@gitlab.com:",
            ],
        )


class TestGitCredentialInstall(unittest.TestCase):
    def test_1(self):
        manager = GitCredentialManager(
            {
                "CREDENTIAL_GIT_MY_PROJECT": "gitlab.my-company.fr",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_LOGIN": "gitlab_login",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_PASSWORD": "gitlab_password",
            }
        )
        extractors = manager.create_extractors()
        self.assertEqual(1, len(extractors))
        commands = manager.get_cmd(manager.extract(extractors[0])[0])
        self.assertEqual(
            [
                "git",
                "config",
                "--global",
                "url.https://gitlab_login:gitlab_password@gitlab.my-company.fr/.insteadOf",
                "git@gitlab.my-company.fr:",
            ],
            commands,
        )

    def test_2(self):
        manager = GitCredentialManager(
            {
                "CREDENTIAL_GIT_MY_PROJECT": "gitlab.my-company.fr/group/project.git",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_LOGIN": "gitlab_login",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_PASSWORD": "gitlab_password",
            }
        )
        extractors = manager.create_extractors()
        self.assertEqual(1, len(extractors))
        commands = manager.get_cmd(manager.extract(extractors[0])[0])
        self.assertEqual(
            [
                "git",
                "config",
                "--global",
                "url.https://gitlab_login:gitlab_password@gitlab.my-company.fr/group/project.git.insteadOf",
                "git@gitlab.my-company.fr:group/project.git",
            ],
            commands,
        )


class TestGitCredentialEtract(unittest.TestCase):
    def setUp(self):
        self.ad_suffix = AddonsCredentialGit("MY_PROJECT")

    def test_no_path(self):
        res = self.ad_suffix.extract(
            {
                "CREDENTIAL_GIT_MY_PROJECT": "gitlab.my-company.fr",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_LOGIN": "gitlab_login",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_PASSWORD": "gitlab_password",
            }
        )

        self.assertEqual("MY_PROJECT", res.name)
        self.assertEqual("gitlab_login", res.username)
        self.assertEqual("gitlab_password", res.password)
        self.assertEqual("", res.path)

        self.assertEqual("https://gitlab_login:gitlab_password@gitlab.my-company.fr/", res.git_uri("https"))
        self.assertEqual("git@gitlab.my-company.fr:", res.git_uri("ssh"))
        self.assertEqual("https://gitlab.my-company.fr/", res.git_uri("public"))

    def test_partial_path(self):
        res = self.ad_suffix.extract(
            {
                "CREDENTIAL_GIT_MY_PROJECT": "gitlab.my-company.fr/group",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_LOGIN": "gitlab_login",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_PASSWORD": "gitlab_password",
            }
        )
        self.assertEqual("MY_PROJECT", res.name)
        self.assertEqual("gitlab_login", res.username)
        self.assertEqual("gitlab_password", res.password)
        self.assertEqual("group", res.path)

        self.assertEqual("https://gitlab_login:gitlab_password@gitlab.my-company.fr/group", res.git_uri("https"))
        self.assertEqual("git@gitlab.my-company.fr:group", res.git_uri("ssh"))
        self.assertEqual("https://gitlab.my-company.fr/group", res.git_uri("public"))

    def test_full_path(self):
        res = self.ad_suffix.extract(
            {
                "CREDENTIAL_GIT_MY_PROJECT": "gitlab.my-company.fr/group/sub/project.git",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_LOGIN": "gitlab_login",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_PASSWORD": "gitlab_password",
            }
        )

        self.assertEqual("MY_PROJECT", res.name)
        self.assertEqual("gitlab_login", res.username)
        self.assertEqual("gitlab_password", res.password)
        self.assertEqual("group/sub/project.git", res.path)
        self.assertEqual(
            "https://gitlab_login:gitlab_password@gitlab.my-company.fr/group/sub/project.git", res.git_uri("https")
        )
        self.assertEqual("git@gitlab.my-company.fr:group/sub/project.git", res.git_uri("ssh"))
        self.assertEqual("https://gitlab.my-company.fr/group/sub/project.git", res.git_uri("public"))
