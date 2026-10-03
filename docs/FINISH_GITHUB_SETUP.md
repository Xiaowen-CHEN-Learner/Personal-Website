# Finish GitHub account setup

The connected editing session published repository-content improvements, but did not change account settings or create the username-matching repository. This script completes the supported account-side steps using **your own authenticated GitHub CLI**, without sharing credentials in chat.

## What the script applies

- Creates the public `Xiaowen-CHEN-Learner/Xiaowen-CHEN-Learner` repository when absent and copies in `docs/PROFILE_README.md` from this repository.
- Updates the display name, bio, affiliation, location, and LinkedIn website field.
- Updates descriptions and adds relevant topics to the eight reviewed project repositories, preserving existing topics.
- Reads back changes and reports verification. Saves public-field/README backups under `~/.xavier-github-setup/` outside the repository before writing.

It does not rename, delete, archive, change existing visibility, publish email, choose a photo, or modify pins. It does not handle or print access tokens. A private profile repository or an unexpected signed-in account stops the process. Existing custom profile README content is not overwritten unless `--replace-profile-readme` is explicitly supplied.

## Run on your computer

Requirements: Python 3.10+ and [GitHub CLI](https://cli.github.com/). The script and safety tests were run locally with Python 3.13.5.

Authenticate through GitHub's browser flow:

```bash
gh auth login --hostname github.com --web --scopes write:user
```

Use `Xiaowen-CHEN-Learner`. The authenticated account must have permissions to create a public repository, write its contents, update repository metadata/topics, and update its profile. When already signed in, `gh auth refresh --hostname github.com --scopes write:user` can request the additional profile-writing scope. Do not paste tokens into issues or chat.

From a local clone of this repository:

```bash
python tools/finish_github_setup.py
python tools/finish_github_setup.py --apply
```

On Windows with the Python launcher, replace `python` with `py`. The first command is a local-only preview. The second command makes and verifies the public changes. The script can also be run as a standalone downloaded Python file: it reads the profile README from GitHub rather than requiring local template files.

If a permission, network, or verification error occurs, it exits with a nonzero status. Earlier successful operations may remain; inspect the printed verification messages and local backup before retrying. It never tries to bypass permission restrictions.

## Two interface-only finishing touches

On your GitHub profile, choose **Customize your pins** and feature: Learn Finance Through Games; Quantamental Investing; Equity Research; Precious-Metals Portfolio; Market Price and Catalyst Visualizations; AI Research Workflows. Reorder them in that sequence and save. This is a suggested starting selection, not a claim that the pins were already changed.

Review your profile photo through **Settings → Public profile**. Use a genuine professional portrait that you choose; this session did not replace or generate one.

Keep current repository names while their links and GitHub Pages sites remain in use. A later rename should be a coordinated migration, not a cosmetic change made without checking dependent links.

## Validation and boundaries

Eleven local safety tests passed on 2026-10-03:

```bash
python -m unittest discover -s tests -v
```

Tests cover correct/wrong-account handling, additive topics, duplicates, limits, invalid topics, bio length, no email/photo publication, preview without network calls, 404-vs-403 behavior, and missing-CLI handling. The authenticated apply path has **not been executed in this editing session**. Local unit tests do not establish that your eventual token has the required permissions.

## Official references

- [GitHub CLI authentication](https://cli.github.com/manual/gh_auth_login)
- [GitHub CLI API requests](https://cli.github.com/manual/gh_api)
- [Updating a public profile](https://docs.github.com/en/rest/users/users#update-the-authenticated-user)
- [Repository creation](https://docs.github.com/en/rest/repos/repos#create-a-repository-for-the-authenticated-user)
- [Repository topics](https://docs.github.com/en/rest/repos/repos#replace-all-repository-topics)
- [Profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- [Pinning items](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/pinning-items-to-your-profile)
