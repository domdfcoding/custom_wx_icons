#!/bin/bash

# fix these
declare errors="E301,E303,E304,E305,E306,E502,W291,W293,W391,E226,E225,E241,E231,"

# Be belligerent for these
declare belligerent="W292,E265,"

# Only warn for these
declare warnings="E101,E111,E112,E113,E121,E122,E124,E125,E127,E128,E129,E131,E133,E201,E202,E203,E211,E222,E223,E224,E225,E227,E228,E242,E251,E261,E262,E271,E272,E402,E703,E711,E712,E713,E714,E721,W504,E302,"


if [ -z "$(git status --porcelain --untracked-files=no)" ] || [ "$1" == "-f" ]; then
  # Working directory clean

  echo "Running autopep8"

  autopep8 --in-place --select "$errors" -a --recursive custom_wx_icons/
  autopep8 --in-place --select "$belligerent" -a -a -a -a -a --recursive custom_wx_icons/


  echo "Running flake8"

    >&2 flake8 custom_wx_icons/

    >&2 flake8 tests/

  exit 0

else
  # Uncommitted changes
  >&2 echo "git working directory is not clean"
  exit 1

fi
