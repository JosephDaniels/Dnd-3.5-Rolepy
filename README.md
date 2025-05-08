# Dnd-3.5-Rolepy

Dnd 3.5 Rolepy Module

Commands

*** Starred commands haven't been implemented. ***

*** Three stars is just in the imagination stage.
** Two stars means the backend has been completed.

* One star means that there's still some implementations needed.

!Hello - Says hello back to you.

!coinflip
!rolld3
!rolld4
!rolld6
!rolld8
!rolld10
!rolld12
!rolld20
!rolld100
!rolld1000

!login [username]    - Logs you in to the game as a character. *
!logout - Logs you out. *

!whois [username]    - Views a target profile ***

!availablecharacters - Shows you a list of the characters you are able to login. ***
!editprofile - Edits your profile once logged in. ***
!whereami - DMs you a description of the current room. ***
!help - Sends you a list of current commands.
!me - Shows the currently logged in profile. ***

[secret commands]
!fliptable

# Single‑Player User Commands: Test Plan

This document outlines step‑by‑step test scenarios to verify robustness of all single‑player user commands (`spawn`, `login`, `logout`, `status`, `whoami`).

Each scenario assumes a clean environment where `data/logged_in.json` and `characters/` files may or may not exist. Replace `@UserID@` with the test Discord user’s ID.

---

## 1. Spawn Command (`!spawn`)

| Scenario                    | Input            | Expected Behavior                                                                |
| --------------------------- | ---------------- | -------------------------------------------------------------------------------- |
| A. First spawn, no params   | `!spawn`         | Character created with default name = Discord username; JSON saved; confirms HP. |
| B. First spawn, custom name | `!spawn Rynn`    | Character created as “Rynn”; confirms HP; file `rynn.json` exists.               |
| C. Duplicate spawn          | `!spawn` (again) | Responds “You already have a character.”; no file overwritten.                   |

---

## 2. Login Command (`!login`)

Prerequisite: A character JSON exists (e.g. `characters/rynn.json`).

| Scenario                  | Input            | Expected Behavior                                                                              |
| ------------------------- | ---------------- | ---------------------------------------------------------------------------------------------- |
| A. Exact name match       | `!login rynn`    | Logs in Rynn; confirms “Logged in as Rynn (HP/MaxHP).”                                         |
| B. Case‑insensitive match | `!login RYNN`    | Same as A.                                                                                     |
| C. Prefix match           | `!login ry`      | If only `rynn.json`, logs in; if ambiguous (e.g. `ryan.json` also exists), prompts to specify. |
| D. No such character      | `!login unknown` | Responds “Character not found.”                                                                |

---

## 3. Status Command (`!status`)

Prerequisite: User is logged in or spawned.

| Scenario        | Input                                | Expected Behavior                                                         |
| --------------- | ------------------------------------ | ------------------------------------------------------------------------- |
| A. No character | `!status`                            | Responds “No active character.”                                           |
| B. Fresh spawn  | `!status`                            | Shows Name, Level=0, HP=Max/Max, Hunger=0/100, Thirst=0/100, Mood=Neutral |
| C. After edits  | (Use `!set` commands) then `!status` | Reflects real `current_health`, hunger, thirst, and mental mood values.   |

---

## 4. WhoAmI Command (`!whoami`)

| Scenario        | Input     | Expected Behavior                       |
| --------------- | --------- | --------------------------------------- |
| A. No character | `!whoami` | Responds “No active character.”         |
| B. Logged in    | `!whoami` | Responds “You are **<CharacterName>**.” |

---

## 5. Logout Command (`!logout`)

| Scenario     | Input     | Expected Behavior                                                    |
| ------------ | --------- | -------------------------------------------------------------------- |
| A. Logged in | `!logout` | Clears active char, updates `logged_in.json`, confirms “Logged out.” |
| B. No login  | `!logout` | Responds “No active character.”                                      |

---

## 6. Full Lifecycle

1. Ensure no prior data (delete `data/logged_in.json` and `characters/rynn.json`).
2. `!status` → “No active character.”
3. `!spawn Rynn` → Confirmation.
4. `!status` → Shows correct stats.
5. `!whoami` → “You are **Rynn**.”
6. Exit and restart bot (simulate restart).
7. `!status` → Should still find Rynn with same stats.
8. `!logout` → Confirmation.
9. `!status` → “No active character.”

---

> **Tip:** After each test, inspect `data/logged_in.json` and `characters/` folder to confirm persistence. Adjust file permissions and error handling if tests reveal failures.
> Run through tests on both Windows and Unix environments to ensure path handling is robust.
