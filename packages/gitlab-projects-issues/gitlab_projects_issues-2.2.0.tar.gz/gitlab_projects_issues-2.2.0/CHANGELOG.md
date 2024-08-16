# Changelog

<a name="2.2.0"></a>
## [2.2.0](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/compare/2.1.0...2.2.0) (2024-08-15)

### 🐛 Bug Fixes

- **setup:** refactor 'python_requires' versions syntax ([7ee6dc2](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/7ee6dc29778b35bd9be265e1b3c6a27be001d709))
- **setup:** resolve project package and name usage ([0afa3a7](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/0afa3a74dc678dae87610df39e30818816473438))
- **updates:** ensure 'DEBUG_UPDATES_DISABLE' has non-empty value ([18d921b](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/18d921b8aca5b67cba7ea60acefef5d34bcd5da1))
- **updates:** fix offline mode and SemVer versions comparisons ([a67c8b7](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/a67c8b7dd08d459a50984ac90e37f82614f34915))

### 📚 Documentation

- **cliff:** use '|' to separate breaking changes in 'CHANGELOG' ([af857b2](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/af857b2ad2ee59dce9bb2ebb2c8ccf0919ed97a9))
- **license:** update copyright details for 2024 ([3eca176](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/3eca1763ffa476971267abca451e84152d38e226))
- **readme:** add 'Commitizen friendly' badge ([b96b30a](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/b96b30a223da97639ab33616e3504cf6084aed64))

### 🎨 Styling

- **cli:** improve Python arguments codestyle syntax ([ce9cac6](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/ce9cac6fb0dac3e74d3a3a5cf0ea4c79c14cc545))
- **commitizen, pre-commit:** implement 'commitizen' custom configurations ([9488db6](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/9488db65c415d14545e9843a30e5fb87b95d87e4))
- **pre-commit:** implement 'pre-commit' configurations ([34534f1](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/34534f1622138fc70716de8a9b04b58096e8aff4))

### ⚙️ Cleanups

- **cli, package:** minor Python codestyle improvements ([02ea0ae](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/02ea0aeea6c12a465d36855fab865994961627e2))
- **pre-commit:** disable 'check-xml' unused hook ([4e7e544](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/4e7e544c6c476ec1bd9d0840cd96e1f58aef5703))
- **pre-commit:** fix 'commitizen-branch' for same commits ranges ([ca6817f](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/ca6817f4411f45abb7aab6361ccadde731f73480))
- **setup:** refactor with more project configurations ([f07ae78](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/f07ae7819a5598b063dc9c94f325e6dc6bb0f705))
- **updates:** ignore coverage of online updates message ([c408cdd](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/c408cdd8de88210b75fcb82604a0237e0b8ec6d8))
- **vscode:** remove illegal comments in 'extensions.json' ([7a37d41](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/7a37d414a37add5effa5cbd5bda4e49d533ae204))

### 🚀 CI

- **gitlab-ci:** watch for 'codestyle', 'lint' and 'typings' jobs success ([b0504e5](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/b0504e537c5e2b53933553511d41943042f9e0d2))
- **gitlab-ci:** create 'commits' job to validate with 'commitizen' ([51d41d5](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/51d41d583a2f4a3ea7894f33e447f88446a41475))
- **gitlab-ci:** fix 'commits' job for non-default branches pipelines ([b60089f](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/b60089fccce504f631ae909941c5d38fe8eed1c4))

### 📦 Build

- **hooks:** create './.hooks/manage' hooks manager for developers ([237612c](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/237612cdd2db2edb67dec6b31c6aa2f1269d76df))
- **hooks:** implement 'prepare-commit-msg' template generator ([dc436aa](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/dc436aaac1109c40ff7ac3c3b193f3f0e34e0673))
- **pre-commit:** enable 'check-hooks-apply' and 'check-useless-excludes' ([4b361d5](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/4b361d50608b6e01f6d2891d689abc4d176e9333))


<a name="2.1.0"></a>
## [2.1.0](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/compare/2.0.2...2.1.0) (2024-08-11)

### ✨ Features

- **cli:** implement '--no-color' to disable colors ([e3c3376](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/e3c3376ed07b726da6757ed9755949f399571461))

### 🐛 Bug Fixes

- **package:** check empty 'environ' values before usage ([a9b8937](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/a9b89378672f392fe22a04c3044214487bd747ae))
- **updates:** remove unused 'recommended' feature ([7b3a4c4](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/7b3a4c43ee480a2daec05556a4d09ab4fe11feea))

### 📚 Documentation

- **readme:** migrate from 'gitlabci-local' to 'gcil' package ([326712f](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/326712f003cd1667f2e1f12f13ce8579667154db))

### ⚙️ Cleanups

- **colors:** resolve 'pragma: no cover' detection ([6559e13](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/6559e138fda507cb710179af213c352e0a1608a3))
- **platform:** disable coverage of 'SUDO' without write access ([09c2042](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/09c2042032399fd563821d1c17da9a265aa3d55c))
- **setup:** remove faulty '# pragma: exclude file' flag ([f6a4310](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/f6a431038603fd4e084c89eb07aaed3934b1718a))


<a name="2.0.2"></a>
## [2.0.2](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/compare/2.0.1...2.0.2) (2024-08-10)

### ✨ Features

- **setup:** add support for Python 3.12 ([ad3d5f6](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/ad3d5f67c6f30e97a8cdb9b599a53dbfbf9b54a5))

### 🧪 Test

- **setup:** disable sources coverage of the build script ([4653fa4](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/4653fa49fb6e99a0023f5b3421486b2e828e6af2))

### 🚀 CI

- **gitlab-ci:** raise latest Python test images from 3.11 to 3.12 ([60f3c29](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/60f3c29edba83d2d26106c9b11725f2f775342f9))
- **gitlab-ci:** deprecate outdated and unsafe 'unify' tool ([e820b67](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/e820b6777aa967e267a4d7cf61cf74b3893e87db))


<a name="2.0.1"></a>
## [2.0.1](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/compare/2.0.0...2.0.1) (2024-08-10)

### ✨ Features

- **gitlab-projects-issues:** migrate under 'RadianDevCore/tools' group ([55516fa](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/55516fa8bc3f091269809a87ebcbe38ac718b92a))

### 🐛 Bug Fixes

- **settings:** ensure 'Settings' class initializes settings file ([b8afd5b](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/b8afd5b3b3286c5e22a3a0a3bb7479800893bd02))
- **src:** use relative module paths in '__init__' and '__main__' ([965c996](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/965c9962298f114285b88425c6b9142947817acd))


<a name="2.0.0"></a>
## [2.0.0](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/compare/1.0.5...2.0.0) (2024-08-08)

### 🛡️ Security

- **🚨 BREAKING CHANGE 🚨 |** **cli:** acquire tokens only from environment variables ([ca80cfe](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/ca80cfe398875e043f6b266af7c812a718bfd7d3))

### ✨ Features

- **🚨 BREAKING CHANGE 🚨 |** **cli:** refactor CLI into simpler GitLab URL bound parameters ([f589c8d](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/f589c8d8948d73770c0ccb12276a18fe78af568f))
- **cli:** add tool identifier header with name and version ([ffb86e6](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/ffb86e6bafb5066c599fb99f6e4f7656b55bccb6))
- **cli:** implement '.python-gitlab.cfg' GitLab configurations files ([e87a3c7](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/e87a3c714a62cb8118cfaa6fc80991ed13a6fdc0))
- **cli, argparse:** implement environment variables helpers ([74acb0e](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/74acb0e85713aff9e51b1733fc3b5016ea6c1750))
- **cli, gitlab:** implement CI job token and public authentications ([57b7253](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/57b7253e275c86e6a3e6d26a1eb5b234d5b034f9))
- **main:** document '--default-estimate' metavar as 'ESTIMATE' ([d5a46d8](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/d5a46d861bd183a15465efa3416f4210b9a45761))

### 🐛 Bug Fixes

- **environments:** add missing ':' to the README help description ([7e05429](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/7e05429536b559ee26219e5893bde94ce5550054))

### 📚 Documentation

- **cliff:** document 'security(...)' first in changelog ([e0e2b46](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/e0e2b4690aa005e3116b8e92119c193e9c28a6e4))
- **readme:** document '~/.python-gitlab.cfg' configuration file ([d9b5954](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/d9b59541ab07de337e16d0ceed249a1f8a91b201))

### ⚙️ Cleanups

- **cli/main:** minor codestyle improvement of 'import argparse' ([33e608b](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/33e608b23e4365e88a086bb74931f251a0493a0f))
- **types:** cleanup inconsistent '()' over base classes ([a0eaa89](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/a0eaa898e8d8a8830223213c619d6ba4a168a0a0))

### 🚀 CI

- **gitlab-ci:** migrate from 'git-chglog' to 'git-cliff' ([79b29f0](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/79b29f070d81d5fafcdefe8478e8c331e7a76b08))
- **gitlab-ci:** bind '.docker/config.json' for local test builds ([5ac41d5](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/5ac41d57fff03095b4a63650e9b039d6605759f1))


<a name="1.0.5"></a>
## [1.0.5](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/compare/1.0.4...1.0.5) (2024-07-14)

### 🐛 Bug Fixes

- **entrypoint:** initialize for issues without assignee and milestone ([f3692b8](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/f3692b8a8cad3d84c52eedbf572d6d11f04730b5))


<a name="1.0.4"></a>
## [1.0.4](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/compare/1.0.3...1.0.4) (2024-07-14)

### 🐛 Bug Fixes

- **entrypoint:** avoid failures upon issues without milestones ([57c8dc6](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/57c8dc614371486c5dcb40a79ca7f6f24f5b42ed))


<a name="1.0.3"></a>
## [1.0.3](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/compare/1.0.2...1.0.3) (2024-06-10)

### 📚 Documentation

- **readme:** improve milestones statistics outputs example ([decf7f4](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/decf7f42d9cdc534d41fec89ee098327d36f6c43))

### 🚀 CI

- **gitlab-ci:** install 'coreutils' in the deployed container image ([4946bdb](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/4946bdb226d33806634c6438461b92e7395770ca))
- **gitlab-ci:** use 'buildah' instead of 'docker' to pull images ([0b969b9](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/0b969b9f742a9a450f11aa45d7807ceee41dd723))


<a name="1.0.2"></a>
## [1.0.2](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/compare/1.0.1...1.0.2) (2024-06-01)

### 🚀 CI

- **gitlab-ci:** set '/bin/sh' as 'CMD' rather than 'ENTRYPOINT' ([5e742d8](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/5e742d8d9b1cae59891d5048b422ad50db04131d))


<a name="1.0.1"></a>
## [1.0.1](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/compare/1.0.0...1.0.1) (2024-06-01)

### 📚 Documentation

- **chglog:** add 'ci' as 'CI' configuration for 'CHANGELOG.md' ([29f0b43](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/29f0b43b95d49ee2f53ea07129ef675e8cbb57ed))
- **readme:** update 'README.md' for 'gitlab-projects-issues' ([4fb7d02](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/4fb7d024b45ae68112eac54e5b864f4099d9649a))

### 🚀 CI

- **gitlab-ci:** change commit messages to tag name ([8f8016f](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/8f8016f2c9f03d72afadc62a25109c42d2222dd3))


<a name="1.0.0"></a>
## [1.0.0](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commits/1.0.0) (2024-06-01)

### ✨ Features

- **gitlab-projects-issues:** initial sources implementation ([f1cc034](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/f1cc03421e051da80b4d2d1b9227fe03f05a66a7))

### 🚀 CI

- **gitlab-ci:** use 'CI_DEFAULT_BRANCH' to access 'develop' branch ([bae1c08](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/bae1c0826a97aca9805df868f11d08b480901bf2))
- **gitlab-ci:** rehost 'docker:latest' image in 'images' job ([c4cfc9a](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/c4cfc9aa78e408586247741944cd00c85cb3f20a))
- **gitlab-ci:** rehost 'quay.io/buildah/stable:latest' image ([100c069](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/100c069e5f4220f4ebfe9d12dcbb7d863665489e))
- **gitlab-ci:** implement 'deploy:container' release container image ([d3eae88](https://gitlab.com/RadianDevCore/tools/gitlab-projects-issues/commit/d3eae8870274a333768078e5fbd7f192fa717bd6))


