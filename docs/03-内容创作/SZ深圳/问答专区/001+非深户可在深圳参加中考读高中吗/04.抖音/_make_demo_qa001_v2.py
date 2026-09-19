# -*- coding: utf-8 -*-
"""QA-001 抖音「配音+字幕」示意样片合成（ffmpeg，1080×1920 9:16，30fps）
流程：逐镜头 edge-tts 配音(微软神经语音女声 zh-CN-XiaoxiaoNeural) → 按配音时长对齐镜头
      → zoompan 推拉镜头 + drawtext 烧录底部字幕 → 拼接视频/音频 → 输出 mp4。
配音分段 mp3 也保留在 配音/ 子目录，可在剪映里单独使用。
正式成片请在剪映按 01-QA-001-...md 制作说明完成（字幕上移1行、数据核对、剪映自有配音更优）。"""
import subprocess
import asyncio
import edge_tts
import os

FPS = 30
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "+8%"
BASE = os.path.dirname(os.path.abspath(__file__))
VOICE_DIR = os.path.join(BASE, "配音")
os.makedirs(VOICE_DIR, exist_ok=True)
OUT = os.path.join(BASE, "01-QA-001-非深户能在深圳读高中吗-抖音-三件事-示意样片-配音字幕.mp4")
FD = "C:/Windows/Fonts/msyhbd.ttc"

# 9 镜头：配音全文(精简，控时长) + 字幕(可含\n两行) + 镜头文件名关键词
shots = [
    ("非深户能读高中！5项条件，3条路。",
     "非深户能读高中！\n5项条件，3条路", "镜头01-首图"),
    ("答案先给你：能！非深户孩子在深圳，能参加中考，能读高中。",
     "答案先给你：能！\n非深户孩子在深圳，能参加中考、能读高中", "镜头02-钩子"),
    ("第一件事，资格。5项条件：职业、住所、居住证，社保满3年，孩子3年学籍。",
     "第一件事·资格：5项条件\n职业、住所、居住证、社保3年、学籍3年", "镜头03-资格"),
    ("第二件事，竞争。非深户占54%，公办指标只有23%。但四大AC线和D线只差0-5分，分数越高，差距越小。",
     "第二件事·竞争：54%考生，抢23%公办指标\n分数越高，户籍差距越小", "镜头04-竞争"),
    ("第三件事，出路。公办靠D线指标生，低20分；民办49所同分录取，当保底。",
     "第三件事·出路：公办指标生、民办保底\n全市普高录取率超73%", "镜头05-出路"),
    ("还有中职3+4贯通，中职3年加本科4年，拿全日制本科文凭。",
     "还有中职3+4贯通\n中职3年+本科4年，拿全日制本科", "镜头06-中职"),
    ("现在就能做：核对5项材料，别等3月报名才发现。",
     "现在就能做：核对5项材料\n社保断没断、居住证过没过期、学籍连不连贯", "镜头07-三件事"),
    ("你不是一个人在焦虑。",
     "你不是一个人在焦虑", "镜头08-你不是一个人"),
    ("你是深户还是非深户？评论区聊聊。关注我，深圳中考系列连载。",
     "关注我·深圳中考系列连载\n评论区聊聊，下一篇按你最关心的写", "镜头09-CTA"),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("CMD FAIL: " + " ".join(cmd)[:200] + "\n" + r.stderr[-800:])
    return r


def probe_dur(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", path])
    return float(r.stdout.strip())


async def synth(text, path):
    c = edge_tts.Communicate(text, VOICE, rate=RATE)
    await c.save(path)


# ---------- 1) 逐镜头生成配音 + 测时长 ----------
import shutil
shutil.rmtree(VOICE_DIR, ignore_errors=True)       # 文本有变，每次全新生成
os.makedirs(VOICE_DIR, exist_ok=True)
durs = []
for i, (narr, sub, kw) in enumerate(shots, 1):
    vpath = os.path.join(VOICE_DIR, f"配音-镜头{i:02d}.mp3")
    asyncio.run(synth(narr, vpath))
    d = probe_dur(vpath) + 0.5                       # 每镜加 0.5s 停顿
    durs.append(d)
    print(f"镜头{i:02d} 配音 {probe_dur(vpath):.2f}s → 镜头时长 {d:.2f}s")

# ---------- 2) 组 ffmpeg 命令（图片 0-8，音频 9-17，分开排列） ----------
img_paths = []
audio_paths = []
for i, (narr, sub, kw) in enumerate(shots):
    fn = [f for f in os.listdir(BASE) if kw in f and f.endswith(".png")][0]
    img_paths.append(os.path.join(BASE, fn))
    subpath = os.path.join(BASE, f"_sub_{i}.txt")
    with open(subpath, "w", encoding="utf-8") as fh:
        fh.write(sub)
    audio_paths.append(os.path.join(VOICE_DIR, f"配音-镜头{i+1:02d}.mp3"))
inputs = []
for p in img_paths:
    inputs += ["-i", p]
for p in audio_paths:
    inputs += ["-i", p]

filters = []
vin = []
ain = []
for i, d in enumerate(durs):
    frames = int(round(d * FPS))
    expr = f"1.0+0.10*on/{frames}" if i % 2 == 0 else f"1.10-0.10*on/{frames}"
    vi = f"z{i}"
    si = f"s{i}"
    filters.append(
        f"[{i}:v]zoompan=z='{expr}':d={frames}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={FPS}[{vi}]"
    )
    FD_esc = FD.replace(":", "\\:")                       # C:/Windows/... 正斜杠，仅转义冒号
    sub_esc = subpath.replace("\\", "/").replace(":", "\\:")   # 路径转正斜杠，避免反斜杠被解析吞掉
    filters.append(
        f"[{vi}]drawtext=fontfile='{FD_esc}':"
        f"textfile='{sub_esc}':fontsize=44:fontcolor=white:"
        f"borderw=3:bordercolor=black@0.6:box=1:boxcolor=black@0.35:boxborderw=18:"
        f"line_spacing=10:x=(w-text_w)/2:y=h-text_h-280[{si}]"
    )
    vin.append(f"[{si}]")
    ai = f"a{i}"
    filters.append(
        f"[{9+i}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[{ai}]"
    )
    ain.append(f"[{ai}]")

filters.append("".join(vin) + f"concat=n={len(shots)}:v=1:a=0[vout]")
filters.append("".join(ain) + f"concat=n={len(shots)}:v=0:a=1[aout]")

cmd = ["ffmpeg", "-y", *inputs,
       "-filter_complex", ";".join(filters),
       "-map", "[vout]", "-map", "[aout]",
       "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "128k", OUT]
print("总时长≈", round(sum(durs), 1), "s")
run(cmd)
print("OK:", OUT)

# ---------- 3) 生成 srt 字幕（供剪映复用） ----------
srt = []
t = 0.0
for i, (narr, sub, kw) in enumerate(shots):
    d = durs[i]
    start, end = t, t + d
    def ts(x):
        hh = int(x // 3600); mm = int(x % 3600 // 60); ss = int(x % 60); ms = int(round(x % 1 * 1000))
        return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"
    srt.append(f"{i+1}\n{ts(start)} --> {ts(end)}\n{sub.replace(chr(10), chr(10))}\n")
    t = end
with open(os.path.join(BASE, "01-QA-001-非深户能在深圳读高中吗-抖音-三件事-示意样片-字幕.srt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(srt))
print("srt 已生成")
