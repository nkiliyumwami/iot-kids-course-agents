# KundaKode agent team: house rules

Every agent on the team follows these rules. The Academy Director owns this file. Ask the Director to change it; don't edit it yourself.

## Where we work

- Repo: `nkiliyumwami/iot-kids-course-agents`. The shared clone on the Acer is `/home/paperclip/work/iot-kids-course-agents`; its `main` belongs to the Director.
- **Never touch the live `iot-kids-course` repo or site.** The Board copies approved work into it.
- Work in your own git worktree on your own branch, never in the shared clone and never on `main`:
  ```
  cd /home/paperclip/work/iot-kids-course-agents
  git worktree add /home/paperclip/work/wt/<your-agent-name> -b <your-agent-name>/<topic> main
  ```
  Commit there, then hand the branch to the Director in your task comment. The Director merges it into `main`.
  Commit identity: `git -c user.name=<your-agent-name> -c user.email=<your-agent-name>@kundakode.local commit ...`
- Session N is `lessons/NN-*` (Session 1 = `lessons/01-traffic-light`). Lesson 00 and the labs come before the course.

## Rules you can't skip

1. `AGENT.md` in the repo sets the teaching style and wiring rules.
2. Pin rules:
   - no outputs on D34/D35/VP/VN;
   - no new parts on D2/D5/D12/D15/TX0/RX0;
   - D25/D26/D27 red/yellow/green wiring stays.
3. The five gates must PASS before you hand over any lesson change:
   ```
   MPY_CROSS=/home/paperclip/work/.tools/py/mpy_cross/mpy-cross python3 tools/verify_lesson.py lessons/<NN-slug> [--allow 'evidence/*']
   ```
   Save the output as an evidence file.
4. **No evidence, not done.** Every result is a file in the repo under `evidence/session<NN>/` (a gate output, a test log, a PASS/FAIL file or a render). Each file says what was run, when, and on which commit.
5. Only **hardware-tester** writes hardware results. Nobody else may say "tested on the board" or "works on the ESP32".
6. Only the **Board** writes READY. Never call a session "ready", "done for class" or "tested" without an evidence file behind the claim.
7. No spending, no ordering, no messages to parents, partners or the public, and no new outside accounts. Ask the Director, who asks the Board.
8. Hand work to other agents through Paperclip tasks, never by editing their files.
9. If you're blocked, write the blocker in STATUS.md and in your task, then move on. Don't wait and don't loop.
10. At the end of every run, update **your own section** of `STATUS.md`: what changed, what is blocked, what you assumed. Commit it on your branch.
11. Keep runs short. Tokens are money.

## Session status ladder

DRAFT → GATES PASS → HARDWARE PASS → SCENE PASS → AWAITING BOARD → READY (Board only).
