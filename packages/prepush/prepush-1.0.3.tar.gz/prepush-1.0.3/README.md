## pre-push

check what CI workflows are gonna be triggered after your push

### How it works

basically we are taking every modified file path, and check if it matches to any of the path-strings in the current git repository workflows

### workflows location

yaml files in `.github/workflows/` directory

### changed files

changed files are the one, which are added to the latest commit from the previous commit

### usage

run the `prepush` command, from anywhere in the git repository
