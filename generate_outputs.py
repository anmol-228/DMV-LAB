from __future__ import annotations

import builtins
import io
import os
import runpy
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = REPO_ROOT / "outputs"

SCRIPTS = [
    "ani_circle.py",
    "ani_line.py",
    "dyn_ani_circle.py",
    "dyn_barc.py",
    "dyn_pie.py",
    "dyn_scatter.py",
    "dynamic_hist.py",
    "dynamic_lc.py",
    "handling_dataset.py",
    "missingvar.py",
    "static_barc.py",
    "static_hist.py",
    "static_lc.py",
    "static_pie.py",
    "static_sp.py",
    "subplot.py",
    "ver_graph.py",
]

SAMPLE_INPUTS = {
    "dyn_ani_circle.py": ["0.05", "200"],
    "dyn_barc.py": ["A B C D", "12 18 9 14"],
    "dyn_pie.py": ["Python Java C SQL", "35 30 20 15"],
    "dyn_scatter.py": ["1 2 3 4 5", "2 5 3 7 6"],
    "dynamic_hist.py": ["12 14 15 18 19 21 23 24 26 30", "5"],
    "dynamic_lc.py": ["1 2 3 4 5", "3 5 4 7 9"],
    "ver_graph.py": ["6"],
}


def run_script(script_name: str) -> None:
    script_path = REPO_ROOT / script_name
    script_output_dir = OUTPUT_DIR / script_path.stem
    script_output_dir.mkdir(parents=True, exist_ok=True)

    figure_index = 0
    inputs = iter(SAMPLE_INPUTS.get(script_name, []))
    captured_stdout = io.StringIO()

    original_input = builtins.input
    original_show = plt.show
    original_cwd = os.getcwd()

    def fake_input(prompt: str = "") -> str:
        try:
            value = next(inputs)
        except StopIteration as exc:
            raise RuntimeError(f"No sample input configured for {script_name}") from exc
        print(f"{prompt}{value}")
        return value

    def fake_show(*args, **kwargs) -> None:
        nonlocal figure_index
        for fig_num in plt.get_fignums():
            figure = plt.figure(fig_num)
            figure.canvas.draw()
            figure_index += 1
            figure.savefig(
                script_output_dir / f"figure_{figure_index:02d}.png",
                dpi=160,
                bbox_inches="tight",
            )
        plt.close("all")

    builtins.input = fake_input
    plt.show = fake_show
    os.chdir(REPO_ROOT)

    try:
        with redirect_stdout(captured_stdout):
            runpy.run_path(str(script_path), run_name="__main__")
    finally:
        builtins.input = original_input
        plt.show = original_show
        plt.close("all")
        os.chdir(original_cwd)

    stdout_text = captured_stdout.getvalue().strip()
    if not stdout_text:
        stdout_text = "No console output."
    (script_output_dir / "stdout.txt").write_text(stdout_text + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for script_name in SCRIPTS:
        print(f"Generating outputs for {script_name}...")
        run_script(script_name)


if __name__ == "__main__":
    main()
