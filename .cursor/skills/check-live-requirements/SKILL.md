---
name: check-live-requirements
description: >-
  Check a live demo in the browser against the user's requirements and report
  each one as MET, NOT MET, or UNVERIFIED. Use this skill when the user asks
  to check a live demo against their requirements.
---

# Check live requirements

Report what you find, then stop. Do not fix anything. Do not edit the project, open a pull request, or change the live site.

## Inputs

You need both of these before testing:

1. A live link to the running demo.
2. The requirements, either pasted in the chat or in a `SPEC.md` the user points you to.

If the link is missing, ask for it and stop. If the requirements are missing, ask for them and stop. Do not guess a URL, invent requirements, or search the repo for a spec the user did not give you.

When they paste requirements, use that list. When they point you to `SPEC.md`, read that file and use it. Test every requirement in the list.

## Test each requirement in the browser

For each requirement, decide what a person would have to do on the site to tell whether it is true, then do those steps in the Cursor IDE browser.

1. Open the live link.
2. Perform the actions: click, type, and submit.
3. Read the page after the action. Look at results, messages, navigation, and errors.

Seeing a control is not enough. A README, comment, label, or placeholder that claims the feature works is not enough. Mark a requirement MET only when you saw the required behavior happen.

Visual requirements, such as orientation, layout, or appearance, need a direct view of the thing itself. A screenshot counts only when the subject is visible and clear enough to judge. Internal state, such as a position, rotation, or score, can support a finding, but it does not prove how something looks. If the subject is missing, covered, or unclear, retry the action and capture it again. If you still cannot see it clearly, mark it UNVERIFIED.

A requirement that names several directions or cases must have each one tested. Mark the whole requirement MET only when every required case is verified and passed. If a verified case fails, mark it NOT MET. If no case fails but one is missing or unclear, mark it UNVERIFIED.

Example: "search should return songs" means type a query, submit the search, and check the results. A search box on the page does not make that requirement MET.

Example: "the character faces the way it moved, left and right" means jump left and see the face, then jump right and see the face. A rotation value, with no visible character, does not verify either case.

If one requirement is blocked, mark that one UNVERIFIED and keep testing the rest.

## Status

Use one status per requirement:

- **MET** — every required case was tested, and you saw each one pass.
- **NOT MET** — you saw at least one required case fail.
- **UNVERIFIED** — a required case was not run, or you ran it and still could not tell. Say what stopped you (login, missing data, the page never loaded, the subject was not visible, the result was ambiguous, a tool error).

## Report

Reply with one table. Put every NOT MET row first, then UNVERIFIED, then MET. Within a status, keep the original requirement order.

| Requirement | Status | What you did | What should have happened | What actually happened | Evidence |
| --- | --- | --- | --- | --- | --- |
| Search returns songs | NOT MET | Opened https://example.com. Typed `blue` into the search box. Clicked Search. Error: "No results". | Submitting a search returns songs. | The page showed "No results" and no songs. | On-screen text: "No results". |

- **What you did** — the URL you opened, what you clicked, what you typed, and any error text, so the user can repeat the test. Quote errors exactly. For a multi-case requirement, list each case.
- **What should have happened** — the behavior the requirement asks for.
- **What actually happened** — what you saw. For UNVERIFIED, say what stopped you from checking it.
- **Evidence** — for each case, name the screenshot or the on-screen text you judged. Internal state may be cited only as support. If a screenshot does not show the subject, say that.

Then stop.
