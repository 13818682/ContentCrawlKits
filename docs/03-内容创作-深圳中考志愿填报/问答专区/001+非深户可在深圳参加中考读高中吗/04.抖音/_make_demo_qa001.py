# -*- coding: utf-8 -*-
"""QA-001 抖音 60s 示意样片合成（ffmpeg，1080×1920 9:16，30fps）
9 张分镜按口播脚本节奏分配时长，逐张缓慢推/拉镜头（Ken Burns），拼接为无声+静音轨的示意片。
时长对齐口播：首图(0-3s 兑现钩子) → 钩子 → 资格 → 竞争 → 出路 → 中职3+4 → 三件事 → 共情 → CTA。
正式成片请在剪映按 01-QA-001-...md 制作说明完成配音与字幕。"""
import subprocess
import os

FPS = 30
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "01-QA-001-非深户能在深圳读高中吗-抖音-三件事-示意样片-60s.mp4")

# (镜头文件关键词, 时长秒) —— 时长总计 60s
shots = [
    ("镜头01-首图", 3),
    ("镜头02-钩子", 5),
    ("镜头03-资格", 10),
    ("镜头04-竞争", 9),
    ("镜头05-出路", 11),
    ("镜头06-中职", 7),
    ("镜头07-三件事", 7),
    ("镜头08-你不是一个人", 4),
    ("镜头09-CTA", 4),
]
assert sum(s[1] for s in shots) == 60, "时长总和应为60s"

inputs = []
filters = []
labels = []
for i, (kw, dur) in enumerate(shots):
    fn = [f for f in os.listdir(BASE) if kw in f and f.endswith(".png")][0]
    inputs += ["-i", os.path.join(BASE, fn)]
    frames = int(dur * FPS)
    # 交替推拉：偶=推近(zoom in)，奇=拉远(zoom out)
    expr = f"1.0+0.10*on/{frames}" if i % 2 == 0 else f"1.10-0.10*on/{frames}"
    lab = f"v{i}"
    filters.append(
        f"[{i}:v]zoompan=z='{expr}':d={frames}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={FPS}[{lab}]"
    )
    labels.append(lab)

filters.append("".join(f"[{l}]" for l in labels) + f"concat=n={len(labels)}:v=1:a=0[outv]")

cmd = [
    "ffmpeg", "-y",
    *inputs,
    "-f", "lavfi", "-t", "60", "-i", "anullsrc=r=44100:cl=stereo",
    "-filter_complex", ";".join(filters),
    "-map", "[outv]", "-map", "9:a",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
    "-c:a", "aac", "-b:a", "128k", "-shortest",
    OUT,
]
print("RUN:", " ".join(cmd)[:200], "...")
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("FFMPEG FAIL:\n", r.stderr[-1500:])
else:
    print("OK:", OUT)
    print(r.stderr.strip().splitlines()[-4:])
