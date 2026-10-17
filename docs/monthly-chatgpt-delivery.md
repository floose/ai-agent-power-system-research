# Monthly ChatGPT scientific delivery

## Configuration as of 2026-10-17

The existing ChatGPT task `Power Systems AI Research` is enabled for day 1 of each month at 09:00 Europe/Madrid. Its saved instructions now request source-backed scientific reading and GitHub report delivery through a feature branch and PR into main. This uses the ChatGPT task, not an OpenAI API key in GitHub Actions. Repository write access in an interactive conversation does not, by itself, establish that the scheduled execution has the same tools.

An immediate test run was requested on 2026-10-17. That acknowledgement confirms dispatch only. End-to-end success requires an actual scheduled-run report and verified PR URL; it has not been established by this configuration document.

## Operating sequence

1. Read current AGENTS.md, topic rules, seen DOI state, existing literature and open research PRs.
2. Prefer the Python candidate report when available. The GitHub Actions candidate workflow and the ChatGPT task are independent schedules, not a wired trigger chain. They currently run at the same nominal monthly time; do not assume the current Python report is ready when the ChatGPT task starts. If needed, perform a bounded web-assisted search and explicitly identify that fallback.
3. Select up to five unseen papers with explicit grid application, method and topic evidence. Preserve ambiguity rather than invent dates or fill a quota.
4. Read accessible legitimate sources, distinguishing full text, author versions and abstract-only evidence. Record quantitative support by section, page or table.
5. Create `reports/YYYY-MM-DD-insights.md` and `.json` and the corresponding reported DOI state on a `chatgpt-research/YYYY-MM-DD` branch. Check open PRs to avoid duplicate scientific reading before merge.
6. Open a PR into main. Return the verified PR/report URLs in the ChatGPT result. Never merge or auto-approve scientific findings.

## Token and execution limits

Routine Python triage uses no LLM calls. The task should reuse saved metadata and existing analyses, and reserve reading effort for the shortlist. No extra paid model API integration has been configured. Persistent source caching and direct workflow-to-ChatGPT triggering are not implemented. Web-assisted fallback may use more model work than reusing Python output.

If GitHub tools are unavailable in the scheduled run, deliver the findings in ChatGPT and identify the exact failed repository action. Do not claim automatic publication. A successful end-to-end run must be observed before relying on unattended repository delivery. Android notification receipt depends on the user's notification permissions and is not verified by this repository.
