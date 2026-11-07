"""Tests for tools/verify_lesson.py. Run: python3 -m unittest discover -s tools/tests -v

Each test builds a small throwaway git repo with a copy of lesson 1's real page, then breaks
one thing on purpose and checks that the right gate (and only that gate) fails.
Needs node, git and mpy-cross, like the tool itself. No board, no network.
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import verify_lesson as v  # noqa: E402

SLUG = "01-traffic-light"
REAL_PAGE = ROOT / "lessons" / SLUG / "index.html"


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=test", "-c", "user.email=test@example.com",
                    "-c", "commit.gpgsign=false"] + list(args), check=True, capture_output=True)


def results(lines):
    """{'a': 'PASS', 'b': 'FAIL', ...} from the tool's output lines."""
    out = {}
    for line in lines:
        if line.startswith("[PASS] ") or line.startswith("[FAIL] "):
            out[line[7]] = line[1:5]
    return out


class LessonRepo(unittest.TestCase):
    """A temp repo: main has lesson 1's page, lesson 2's page, AGENT.md; HEAD is a work branch."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="verify-lesson-"))
        self.repo = self.tmp / "repo"
        self.lesson = self.repo / "lessons" / SLUG
        self.lesson.mkdir(parents=True)
        shutil.copy(REAL_PAGE, self.lesson / "index.html")
        (self.repo / "lessons" / "02-patterns").mkdir()
        (self.repo / "lessons" / "02-patterns" / "index.html").write_text("<p>lesson 2</p>\n")
        (self.repo / "AGENT.md").write_text("# brief\n")
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "main")
        git(self.repo, "checkout", "-q", "-b", "phase0/test")
        self.good_program, _ = v.extract_program(self.lesson / "index.html")
        self.write_main(self.good_program)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_main(self, text):
        (self.lesson / "main.py").write_text(text)

    def edit_page(self, old, new):
        page = self.lesson / "index.html"
        html = page.read_text()
        self.assertIn(old, html)
        page.write_text(html.replace(old, new, 1))

    def verify(self):
        lines = []
        rc = v.run(self.lesson, base="main", out=lines.append)
        self.output = "\n".join(lines)
        return rc, results(lines)

    def assertOnlyFails(self, *checks):
        rc, res = self.verify()
        self.assertEqual(rc, 1, self.output)
        failed = sorted(k for k, s in res.items() if s == "FAIL")
        self.assertEqual(failed, sorted(checks), self.output)


class GoodVersion(LessonRepo):
    def test_good_lesson_passes_every_gate(self):
        rc, res = self.verify()
        self.assertEqual(res, {"a": "PASS", "b": "PASS", "c": "PASS", "d": "PASS", "e": "PASS"}, self.output)
        self.assertEqual(rc, 0, self.output)

    def test_page_default_green_time_is_used(self):
        self.assertNotIn("GREEN_S", self.good_program)
        self.assertEqual(self.good_program.count("time.sleep(5)"), 2)

    def test_extra_comment_lines_in_main_are_allowed(self):
        lines = self.good_program.split("\n")
        i = lines.index("    time.sleep(5)", lines.index("    green.value(1)"))
        lines.insert(i, "    # 5 s is the page's default green time")
        self.write_main("\n".join(lines))
        rc, res = self.verify()
        self.assertEqual(rc, 0, self.output)

    def test_committed_main_still_passes(self):
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "main.py")
        rc, _ = self.verify()
        self.assertEqual(rc, 0, self.output)


class BrokenCopies(LessonRepo):
    # ---- syntax errors (gate b)
    def test_syntax_error_on_page_and_main(self):
        self.edit_page("['while True:', ''],", "['while True', ''],")
        self.write_main(self.good_program.replace("while True:", "while True"))
        self.assertOnlyFails("b", "d")  # d fails too: a program that does not parse cannot be pin-checked

    def test_syntax_error_only_in_main(self):
        self.write_main(self.good_program.replace("red.value(1)", "red.value(1"))
        self.assertOnlyFails("b", "c", "d")

    def test_python_valid_but_wrong_indent_in_main(self):
        self.write_main(self.good_program.replace("    red.value(1)", "      red.value(1)"))
        self.assertOnlyFails("b", "c", "d")

    # ---- page and main.py disagree (gate c)
    def test_mismatch_changed_number(self):
        self.write_main(self.good_program.replace("time.sleep(2)", "time.sleep(3)"))
        self.assertOnlyFails("c")

    def test_mismatch_missing_line(self):
        self.write_main(self.good_program.replace("    yellow.value(0)\n", "", 1))
        self.assertOnlyFails("c")

    def test_mismatch_extra_code_line(self):
        self.write_main(self.good_program + "print('done')\n")
        self.assertOnlyFails("c")

    def test_mismatch_main_uses_other_green_time(self):
        lines = self.good_program.split("\n")
        i = lines.index("    time.sleep(5)", lines.index("    green.value(1)"))
        lines[i] = "    time.sleep(7)"
        self.write_main("\n".join(lines))
        self.assertOnlyFails("c")

    def test_missing_main(self):
        (self.lesson / "main.py").unlink()
        self.assertOnlyFails("c")

    # ---- pins (gate d)
    def break_pin(self, old, new):
        self.edit_page(old, new)
        self.write_main(self.good_program.replace(old, new))

    def test_output_on_input_only_pin(self):
        self.break_pin("Pin(25, Pin.OUT)", "Pin(34, Pin.OUT)")
        self.assertOnlyFails("d")

    def test_lights_swapped(self):
        self.break_pin("red = Pin(25, Pin.OUT)", "red = Pin(26, Pin.OUT)")
        self.assertOnlyFails("d")

    def test_start_up_pin_for_a_part(self):
        self.break_pin("green = Pin(27, Pin.OUT)", "green = Pin(12, Pin.OUT)")
        self.assertOnlyFails("d")

    def test_pin_that_does_not_exist(self):
        self.break_pin("Pin(26, Pin.OUT)", "Pin(24, Pin.OUT)")
        self.assertOnlyFails("d")

    def test_wrong_pin_only_in_main(self):
        self.write_main(self.good_program.replace("Pin(27, Pin.OUT)", "Pin(35, Pin.OUT)"))
        self.assertOnlyFails("c", "d")

    # ---- changed files (gate e)
    def test_protected_file_changed(self):
        (self.repo / "AGENT.md").write_text("# brief, edited\n")
        self.assertOnlyFails("e")

    def test_other_lesson_changed_and_committed(self):
        (self.repo / "lessons" / "02-patterns" / "index.html").write_text("<p>edited</p>\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "oops")
        self.assertOnlyFails("e")

    def test_untracked_file_outside_allowlist(self):
        (self.repo / "notes.txt").write_text("scratch\n")
        self.assertOnlyFails("e")

    def test_github_folder_is_protected(self):
        (self.repo / ".github").mkdir()
        (self.repo / ".github" / "x.yml").write_text("on: push\n")
        self.assertOnlyFails("e")

    # ---- extraction (gate a)
    def test_page_without_program(self):
        self.edit_page("window.__lessonProgram = () =>", "window.__notTheProgram = () =>")
        rc, res = self.verify()
        self.assertEqual(rc, 1)
        self.assertEqual(res["a"], "FAIL", self.output)


class PinRules(unittest.TestCase):
    def problems(self, code, slug="x"):
        return v.check_pins(code, slug)[0]

    def test_pwm_on_input_only_pin(self):
        self.assertTrue(self.problems("from machine import Pin, PWM\nb = PWM(Pin(35))\n"))

    def test_adc2_pin_for_analog(self):
        self.assertTrue(self.problems("from machine import Pin, ADC\nl = ADC(Pin(14))\n"))

    def test_adc1_pin_ok(self):
        self.assertFalse(self.problems("from machine import Pin, ADC\nl = ADC(Pin(34))\n"))

    def test_input_on_input_only_pin_ok(self):
        self.assertFalse(self.problems("from machine import Pin\nb = Pin(34, Pin.IN)\n"))

    def test_serial_pins(self):
        self.assertTrue(self.problems("from machine import Pin\nb = Pin(1, Pin.OUT)\n"))
        self.assertTrue(self.problems("from machine import Pin\nb = Pin(3, Pin.IN)\n"))

    def test_named_constant_is_followed(self):
        self.assertTrue(self.problems("from machine import Pin\nP = 34\nb = Pin(P, Pin.OUT)\n"))

    def test_unknown_pin_number_fails(self):
        self.assertTrue(self.problems("from machine import Pin\nb = Pin(int('25'), Pin.OUT)\n"))

    def test_onboard_led_only_exempt_in_lesson_0(self):
        code = "from machine import Pin\nled = Pin(2, Pin.OUT)\n"
        self.assertFalse(self.problems(code, "00-meet-esp32"))
        self.assertTrue(self.problems(code, "03-pedestrian-button"))


class RealLessons(unittest.TestCase):
    """Read-only: every real lesson page gives a program that compiles and follows the pin rules."""

    def test_lessons_00_to_10(self):
        lessons = sorted(p for p in (ROOT / "lessons").iterdir() if p.name[:2].isdigit())
        self.assertEqual(len(lessons), 11)
        for lesson in lessons:
            with self.subTest(lesson=lesson.name):
                program, _ = v.extract_program(lesson / "index.html")
                ok, msg = v.compile_mpy(program, "main.py")
                self.assertTrue(ok, msg)
                self.assertEqual(v.check_pins(program, lesson.name)[0], [])

    def test_codelines_uses_default_cfg(self):
        program, _ = v.extract_program(ROOT / "lessons" / "04-fair-crossing" / "index.html")
        self.assertIn("    while count < 80:  # 80 x 0.05 s = 4 s", program)  # DEFAULT_CFG.green = 4
        self.assertIn("        time.sleep(5)", program)  # DEFAULT_CFG.cross = 5


if __name__ == "__main__":
    unittest.main()
