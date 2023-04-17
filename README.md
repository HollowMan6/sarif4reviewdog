# SARIF for Reviewdog
[![Test](https://github.com/HollowMan6/sarif4reviewdog/workflows/Test/badge.svg)](https://github.com/HollowMan6/sarif4reviewdog/actions?query=workflow%3ATest)
[![reviewdog](https://github.com/HollowMan6/sarif4reviewdog/workflows/reviewdog/badge.svg)](https://github.com/HollowMan6/sarif4reviewdog/actions?query=workflow%3Areviewdog)
[![depup](https://github.com/HollowMan6/sarif4reviewdog/workflows/depup/badge.svg)](https://github.com/HollowMan6/sarif4reviewdog/actions?query=workflow%3Adepup)
[![release](https://github.com/HollowMan6/sarif4reviewdog/workflows/release/badge.svg)](https://github.com/HollowMan6/sarif4reviewdog/actions?query=workflow%3Arelease)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/HollowMan6/sarif4reviewdog?logo=github&sort=semver)](https://github.com/HollowMan6/sarif4reviewdog/releases)
[![action-bumpr supported](https://img.shields.io/badge/bumpr-supported-ff69b4?logo=github&link=https://github.com/haya14busa/action-bumpr)](https://github.com/haya14busa/action-bumpr)
## Input

```yaml
inputs:
  github_token:
    description: 'GITHUB_TOKEN'
    default: '${{ github.token }}'
  ### Flags for reviewdog ###
  tool_name:
    description: 'Tool name to use for reviewdog reporter'
    default: 'SARIF'
  level:
    description: 'Report level for reviewdog [info,warning,error]'
    default: 'error'
  reporter:
    description: 'Reporter of reviewdog command [github-pr-check,github-pr-review].'
    default: 'github-pr-review'
  filter_mode:
    description: |
      Filtering mode for the reviewdog command [added,diff_context,file,nofilter].
      Default is added.
    default: 'added'
  fail_on_error:
    description: |
      Exit code for reviewdog when errors are found [true,false]
      Default is `false`.
    default: 'false'
  reviewdog_flags:
    description: 'Additional reviewdog flags'
    default: ''
  ### Flags for linter ###
  file:
    description: 'SARIF file path'
    default: ''
    required: true
```

## Usage
```yaml
name: sarif4reviewdog
on: [pull_request]
jobs:
  # TODO: change `linter_name`.
  sarif_reviewdog:
    name: sarif reviewdog
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v2
      - uses: HollowMan6/sarif4reviewdog@v1
        with:
          file: 'results.sarif'
          # Remember to allow GitHub Actions to create and approve pull requests
          # https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#preventing-github-actions-from-creating-or-approving-pull-requests
          github_token: ${{ secrets.github_token }}
          # Change reviewdog reporter if you need [github-pr-check,github-check,github-pr-review].
          reporter: github-pr-review
          # Change reporter level if you need.
          # GitHub Status Check won't become failure with warning.
          level: warning
```

## Development

### Release

#### [haya14busa/action-bumpr](https://github.com/haya14busa/action-bumpr)
You can bump version on merging Pull Requests with specific labels (bump:major,bump:minor,bump:patch).
Pushing tag manually by yourself also work.

#### [haya14busa/action-update-semver](https://github.com/haya14busa/action-update-semver)

This action updates major/minor release tags on a tag push. e.g. Update v1 and v1.2 tag when released v1.2.3.
ref: https://help.github.com/en/articles/about-actions#versioning-your-action

### Lint - reviewdog integration

This reviewdog action template itself is integrated with reviewdog to run lints
which is useful for Docker container based actions.

![reviewdog integration](https://user-images.githubusercontent.com/3797062/72735107-7fbb9600-3bde-11ea-8087-12af76e7ee6f.png)

Supported linters:

- [reviewdog/action-shellcheck](https://github.com/reviewdog/action-shellcheck)
- [reviewdog/action-hadolint](https://github.com/reviewdog/action-hadolint)
- [reviewdog/action-misspell](https://github.com/reviewdog/action-misspell)

### Dependencies Update Automation
This repository uses [reviewdog/action-depup](https://github.com/reviewdog/action-depup) to update
reviewdog version.
