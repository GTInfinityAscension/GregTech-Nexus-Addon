# Contributing code

The organisation-wide guide is the [CONTRIBUTING](https://github.com/GTInfinityAscension/.github/blob/main/CONTRIBUTING.md) of GTInfinityAscension. The short version for GTNA:

1. For anything larger than a bug fix, open an issue first. Balance and progression changes need the author's approval.
2. Fork, branch from `main`, one topic per pull request.
3. Every new machine, item or recipe ships with names in **en_us, pt_br and zh_cn**.
4. Add or update GameTests. A new multiblock needs a test that it forms and a negative test (it must not form or run when it should not).
5. Run `./gradlew spotlessCheck compileJava runUnitTests runGameTestServer runData` and say in the pull request how you tested in game.
6. Commit messages and changelog entries are in English.
7. Ports keep their source credit: add the machine to `GTNASources` and follow the licence notes in `THIRD_PARTY_NOTICES.md`.
