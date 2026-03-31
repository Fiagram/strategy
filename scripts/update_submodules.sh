#! /bin/sh
# This script updates all git submodules to their latest commit on the tracked branch. 
# It should be run from the root of the repository.
git submodule foreach git pull origin main
git submodule status
