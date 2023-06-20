#!/bin/sh
set -e

export REVIEWDOG_GITHUB_API_TOKEN="${INPUT_GITHUB_TOKEN}"

/convert.py "${INPUT_FILE}" \
| xargs -n1 reviewdog -f="rdjson" \
    -name="${INPUT_TOOL_NAME:-SARIF}" \
    -reporter="${INPUT_REPORTER:-github-pr-review}" \
    -filter-mode="${INPUT_FILTER_MODE}" \
    -fail-on-error="${INPUT_FAIL_ON_ERROR}" \
    -level="${INPUT_LEVEL}" \
    ${INPUT_REVIEWDOG_FLAGS}
