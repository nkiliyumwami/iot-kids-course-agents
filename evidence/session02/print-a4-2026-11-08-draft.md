# Session 2 A4 print check, draft (2026-11-08)

- **Who:** kids-iot-academy (KUNAA-9). **Lesson files rendered at:** `02e4688` (branch `kids-iot-academy/session02-draft`). **Final render:** 2026-11-08T01:56:18Z, Azure VM (kundakode-office-vm).
- **Engine:** the Session 1 renderer, unchanged: `evidence/session01/print-a4-render-playwright.py` (A4, 12 mm margins, 10.5 pt DejaVu Sans, 15 pt worksheet rows; calibrated against Chrome in `evidence/session01/print-a4-2026-11-08.md`). Pages counted with `pypdf`.
- **Command:**
  ```
  D=/home/paperclip/work/.tools/chromium-libs
  FONTCONFIG_FILE=$D/fonts.conf LD_LIBRARY_PATH=$D/root/usr/lib/x86_64-linux-gnu PLAYWRIGHT_BROWSERS_PATH=/home/paperclip/work/.tools/ms-playwright \
    /home/paperclip/work/.tools/print-venv/bin/python evidence/session01/print-a4-render-playwright.py lessons/02-patterns evidence/session02 2026-11-08-draft
  ```
- **Output:**
  ```
  engine: Playwright Chromium 156.0.8078.4
  worksheet.md -> evidence/session02/print-a4-2026-11-08-draft-worksheet.pdf: 1 page(s), 594.96 x 841.92 pts
  teacher-guide.md -> evidence/session02/print-a4-2026-11-08-draft-teacher-guide.pdf: 4 page(s), 594.96 x 841.92 pts
  ```

## Results

| File | Pages | Page size | Limit | PDF |
|---|---|---|---|---|
| `worksheet.md`, first attempt (with a separate "Decode set_lights" table) | 2 | A4 | 1 | not kept |
| `worksheet.md` @ `02e4688` | **1** | 594.96 × 841.92 pt (A4) | 1 | `print-a4-2026-11-08-draft-worksheet.pdf` |
| `teacher-guide.md` @ `02e4688` | **4** | 594.96 × 841.92 pt (A4) | at most 4 | `print-a4-2026-11-08-draft-teacher-guide.pdf` |

What made the worksheet fit: the Decode table became two rows in "1. Predict". At a 704 px column (A4 minus margins) the
worksheet content is 894 px tall (Session 1's one-page sheet is 1015 px), so there is some spare room.
