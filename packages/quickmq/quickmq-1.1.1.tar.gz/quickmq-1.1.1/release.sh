#! /usr/bin/env bash
#
# Release script that will bump the project version and commit and push
# the version file.
#
# This supports a limited, but reasonable, set of version specifiers.
#
# ASSUMES:
#   1. You are using Hatch
#   2. You have `version` in your `project.dynamic` list
#
# REQUIRES:
#   1. You are not on the main branch
#   2. You are using GitLab
#
# Created originally by Bruce Flynn at the SSEC, slightly modified for quickmq's purpose.

set -e

if [[ ! "$1" =~ ^(major|minor|patch|dev)$ ]]; then
    echo "USAGE: $0 <major|minor|patch|dev>"
    exit 1
fi

cur_branch=$(git branch --show-current)
readonly cur_branch
if [[ "$cur_branch" == "main" ]]; then
    echo "Cannot make commits from the main branch!"
    exit 1
fi

# Make sure the current branch is clean of changes,
# the version bump should be the only change.


# Bumps the version, i.e., sets the version in the version file specified in
# the hatch version file config.
hatch version "$1"

ver=$(hatch version)
readonly ver
if git tag -l | grep "${ver}" &>/dev/null; then
    echo "Whoops!! Tag for version ${ver} already exists"
    echo "You may have to manually revert the version before running this script again."
    exit 1
fi

# Get the name of the file contain the version var __version__. This may need
# to be adjusted if version handing doesn't meet assumptions.
proj_dir=$(hatch status 2>&1 | awk '/\[Location\] - / {print $3}')
verfile=$(find "$proj_dir"/src -name \*.py -print0 | xargs -0 grep -nE '^__version__ = ' | cut -d: -f1)
readonly verfile
[[ -z ${verfile} ]] && echo "Failed to find version file" && exit 1

git commit -vm "bump version" "${verfile}"
git tag -am "bump to ${ver}" "${ver}"

push_args="--follow-tags -o merge_request.create -o merge_request.target=main -o merge_request.merge_when_pipeline_succeeds -o merge_request.remove_source_branch -o merge_request.title='Bump version ${ver}'"
if [[ $(git ls-remote --heads origin /refs/heads/"$cur_branch") ]]; then
    git push "$push_args"
else
    git push -u origin "$cur_branch" "$push_args"
fi
