# Code Review Protocol

How QA reviews recently-added code. Use this whether it's a formal PR or an
in-flight audit of `app_build/`.

---

## 1. Goals of Review

A review succeeds when the reviewer can answer YES to all four:

1. **Correct**: does it do what the spec says?
2. **Safe**: does it fail safely? No crashes, leaks, injections?
3. **Maintainable**: will the next person understand it in 6 months?
4. **Tested**: are the important cases covered?

---

## 2. Pre-Review Context

Before diving in:

- Read the spec / acceptance criteria for the change
- Scan the diff size -- huge diffs deserve pushback toward smaller chunks
- Note the author's stated intent (commit message / PR description)
- Note what's NOT in the diff -- missing tests, missing error handling

---

## 3. The Review Pass (in order)

### Pass 1: Orientation (5 min)

- What's changing? Why?
- Is there an ADR or spec backing it?
- Is the scope of the change aligned with the commit message?

### Pass 2: Structure (10 min)

- Is the code in the right layer? (Controller/Service/Repository discipline)
- Are new files in the right folders?
- Are public APIs introduced or changed documented?
- Any unexpected dependencies added?

### Pass 3: Logic (bulk of the time)

- Walk each changed function -- happy path + error path
- Check input validation at boundaries
- Check edge cases: null, empty, negative, max, unicode, concurrency
- Check that assumptions are explicit (guard clauses, asserts)
- Check that errors propagate correctly (no silent catches)

### Pass 4: Tests

- Is the change tested?
- Do tests cover the failure modes, not just the happy path?
- Are the tests deterministic (no sleep, no real clock, no external network)?
- Do the test names describe behavior in business language?

### Pass 5: Security & Privacy

- New external input? Validated + sanitized?
- New secrets? Via env var, not code?
- New logging? No PII, no secrets, no tokens?
- New SQL? Parameterized, not concatenated?
- New auth code? Explicit allow-list approach?

### Pass 6: Documentation

- README updated if commands changed?
- API reference updated if endpoints changed?
- Changelog entry under Unreleased?
- ADR if a significant decision was made?

---

## 4. Smells Checklist

Quick scan for common problems:

### Function-level

- [ ] Functions > 50 lines
- [ ] > 3 parameters (consider an object)
- [ ] Nested > 3 levels
- [ ] Early return missing (arrow of doom)
- [ ] Multiple responsibilities in one function

### Naming

- [ ] Generic names: `data`, `info`, `handle`, `process`, `util`, `helper`
- [ ] Single-letter variables outside loops
- [ ] Negated booleans: `isNotEmpty`, `notReady`
- [ ] Verb for data / noun for action

### Duplication

- [ ] Copy-paste across > 2 places
- [ ] Parallel data structures that must stay in sync
- [ ] Config in code that changes per env (should be env var)

### Dead Code

- [ ] `// TODO` older than 30 days
- [ ] Commented-out blocks
- [ ] Unused imports
- [ ] Unused parameters
- [ ] Unreachable branches

### Magic

- [ ] Magic numbers (`* 86400`, `< 7`) without named constants
- [ ] Magic strings (`'admin'`, `'pending'`) without enums/const
- [ ] Regex without comment or `x` flag

### Concurrency & Async

- [ ] `async` without `await`
- [ ] Missing `await` on a promise
- [ ] Race condition on shared mutable state
- [ ] Rejection not handled at top level

### Error Handling

- [ ] `catch (e) {}` that swallows
- [ ] Throwing strings instead of Error classes
- [ ] Error messages that leak internals
- [ ] No distinction between expected and unexpected errors

### Resource Leaks

- [ ] Database connections not released
- [ ] File handles not closed
- [ ] Timers not cleared on unmount
- [ ] Event listeners not removed

---

## 5. Feedback Style

### Categorize every comment

- **[blocker]**: must fix before merge (bug, security, spec mismatch)
- **[major]**: strong recommendation, fix soon
- **[minor]**: worth fixing but not blocking
- **[nit]**: style/taste, author's call
- **[question]**: asking, not telling
- **[praise]**: call out good work

This removes ambiguity and lets the author triage fast.

### Comment on code, not people

Instead of: "You should have tested this."
Write: "Missing test for the empty-cart case -- want me to add one?"

### Suggest, don't dictate (when possible)

Instead of: "Rewrite this."
Write: "Consider extracting lines 45-78 into a helper -- it'll be easier to test and the intent becomes clearer."

---

## 6. When to Approve vs Request Changes

### Approve when

- No blockers
- Minor/nit comments acknowledged by the author
- Tests green, coverage maintained
- CI passing

### Request changes when

- Any blocker
- Spec not met
- Security or data-integrity risk
- Missing tests for new behavior

### Comment-only when

- You want time to think more
- You have questions that aren't blockers but need answers
- You're a drive-by reviewer without full context

---

## 7. Author's Side (Preparing Code for Review)

- Write a PR description: what, why, how to test, what's NOT in scope
- Self-review the diff before asking
- Keep PRs small: < 400 lines of real change where possible
- Screenshots / GIFs for UI
- Link to the spec / ticket
- Mark draft if still working on it

---

## 8. The Review Budget

- < 200 lines: 30 min target
- 200-500 lines: 60-90 min
- > 500 lines: push back, ask for split

Sustained review quality beats heroic reviews. Two short reviews > one sprawling one.

---

## 9. Review Done Checklist

- [ ] Read PR description and linked spec
- [ ] Verified change matches description
- [ ] Walked through happy + error paths
- [ ] Checked tests exist for new behavior
- [ ] Checked security posture
- [ ] Checked docs updated
- [ ] Every concern categorized (blocker/major/minor/nit)
- [ ] Approval / request changes / comment submitted
