<p align="center">
  <img src="https://raw.githubusercontent.com/dustymirror/DRUNKDARD_BEHAVIOR_RESEARCH_CENTER/refs/heads/main/ba.jpg" alt="DRUNKDARD Research Center" width="400">
</p>



[跳转到中文说明](#chinese)



# Drunkard Behavior Research Center

> **A small behavioral system that happens to make voltage ；）**

### An experimental CV instrument for EuroPi

**Drunkard Behavior Research Center** is an experimental generative CV instrument for **EuroPi**.

Instead of generating random voltages directly, the program creates two virtual agents — **Alice** and **Ben** — and lets them move through a shared two-dimensional space.

Their movement is influenced by inertia, random impulses, noise, hesitation, boundaries, and interaction with each other.

The resulting CV is therefore not simply random. It emerges from the changing state and relationship of the two agents.

> **Not a random generator.  
> Not an LFO.  
> Not a sequencer.  
> A small behavioral system that happens to make voltage.**

---

# 1. Introduction & Concept

The basic idea is to create **behavior rather than randomness**.

Each drunkard maintains its own internal state:

- position
- velocity
- target
- behavioral noise
- bias
- impulses
- interaction
- current CV state

The next movement is therefore influenced by previous movements.

Alice and Ben share the same space, but they do not share the same trajectory. Depending on the selected mode and Link setting, they may move independently, interact, imitate, avoid each other, or develop loosely related trajectories.

The system is intentionally designed to produce:

- irregular movement
- hesitation
- micro-changes
- discontinuity
- imperfect repetition
- weak interaction
- emergent patterns

The OLED shows the underlying behavioral space, while the CV outputs provide a musical interpretation of that behavior.

---

# 2. Interface

The module uses:

- **B1** — select Alice / Ben
- **B2** — switch parameter pages
- **K1** — parameter A
- **K2** — parameter B
- **128 × 32 OLED** — behavioral visualization

The display normally shows the current parameter page. After a period of inactivity, the interface can automatically disappear so that the OLED becomes primarily a visualization of the two agents.

## Parameter Pages

| Page | K1 | K2 |
|---|---|---|
| 0 | XR | YR |
| 1 | Link | Mode |
| 2 | Rise | Fall |
| 3 | Quant | — |
| 4 | X Range | — |

The currently selected drunkard is indicated by the interface.

---

# 3. Controls

## B1 — Select Agent

Press **B1** to switch between:

```text
A — Alice
B — Ben
```

Parameters that belong to an individual agent are edited for the selected agent.

---

## B2 — Parameter Page

（Parameter page will automatically hide after 15 seconds if no knobs or buttons are operated; turn any knob to bring the page back.）

Press **B2** to cycle through the parameter pages.

```text
PAGE 0    XR / YR
PAGE 1    Link / Mode
PAGE 2    Rise / Fall
PAGE 3    Quant
PAGE 4    X Range
```

---

## Pickup

The parameter controls use **pickup behavior**.

When changing pages, a physical knob does not immediately jump to the stored parameter value.

If the knob position does not correspond to a Pickup parameter, the parameter will be marked with an asterisk (*). 

The knob must first cross the stored value before taking control.

This prevents unexpected parameter jumps when moving between pages.

---

# 4. Behavioral Parameters

## XR — X Range

Controls the horizontal behavioral range of the selected agent.

Higher values allow the agent to explore a larger horizontal space.

Current mapping:

```text
XR = K1 × 9.9
```

---

## YR — Y Range

Controls the vertical behavioral range.

Current mapping:

```text
YR = K2 × 9.9
```

XR and YR can therefore be used to create different spatial proportions for the two agents.

---

## Link

Controls the interaction between Alice and Ben.

A low Link value keeps their behavior relatively independent.

Higher values make their movements increasingly related. For example, collisions and interaction behaviors.

The current preferred working value is approximately:

```text
Link ≈ 0.004
```

The intention is not to force synchronization, but to create a weak behavioral relationship.

---

# 5. Behavior Modes

There are three modes:

```text
W — Wander
P — Portal
C — Counterpoint
```

## Wander

The agents move through a bounded space.

Walls become part of the behavior. When an agent reaches a boundary, it reacts to the wall rather than simply passing through it.

This is the most conventional spatial behavior of the three modes.

---

## Portal

The boundaries become portals.

Leaving one side of the space causes the agent to reappear on the opposite side.

```text
LEFT  → RIGHT
RIGHT → LEFT

TOP    → BOTTOM
BOTTOM → TOP
```

The OLED also uses edge ghosting to make these transitions easier to perceive.

---

## Counterpoint

Counterpoint mode introduces a stronger relationship between the two agents.

This mode originates from the author’s first event score piece, XTS0001 —— a piece in which two performers attempt to execute mirror-image movements in a symmetrical space, relying solely on their sense of hearing. 

The agents influence each other while maintaining independent movement.

The goal is **related behavior without synchronization**.

The two trajectories may therefore:

- approach
- separate
- follow
- imitate
- diverge
- occasionally collide

---

# 6. Events & Triggers

Behavioral events can generate trigger pulses.

```text
CV3 → Alice Trigger
CV6 → Ben Trigger
```

Events can be associated with interactions such as:

- collisions
- wall encounters

An event cooldown prevents continuous retriggering when an agent remains near an event condition.

Current value:

```text
EVENT_COOLDOWN = 400 ms
```

The triggers are therefore intended as **behavioral events**, not clock signals.

---

# 7. CV Outputs

The six EuroPi outputs are organized as two behavioral channels.

| Output | Function | Range |
|---|---|---|
| CV1 | Alice X | 0–X Range |
| CV2 | Alice Y | 0–2.5 V |
| CV3 | Alice Trigger | Pulse |
| CV4 | Ben X | 0–X Range |
| CV5 | Ben Y | 0–2.5 V |
| CV6 | Ben Trigger | Pulse |

The X output range can be selected globally from:

```text
1–5 OCT
```

---

# 8. Quantization

Global control of Alice and Ben’s position CV outputs for musical quantisation.

Quantization affects the **CV output**, not the underlying behavioral position.

Available modes:

```text
0   0  Continuous
1   12 semitone
2   7  seven-tone
3   5  pentatonic
4   M1 whole-tone
5   M2
6   M3
7   M4
8   M5
9   M6
10  M7
```

The M1–M7 options are ** Olivier Messiaen‘s 7 modes of limited transposition**.

### M1

```text
0 2 4 6 8 10
```

### M2

```text
0 1 3 4 6 7 9 10
```

### M3

```text
0 2 3 4 6 7 8 10 11
```

### M4

```text
0 1 2 5 6 7 8 11
```

### M5

```text
0 1 5 6 7 11
```

### M6

```text
0 2 4 5 6 8 10 11
```

### M7

```text
0 1 2 3 5 6 7 8 9 11
```

Quantization provides a musical interpretation of the same underlying behavioral trajectory without changing the movement shown on the OLED.

---

# 9. Rise / Fall

Rise and Fall provide independent slew for the CV outputs.

> **The default value is no slew; the smaller the value, the greater the slew.**

Current mapping:

```text
Rise = 0.02 + K1 × 0.48
Fall = 0.02 + K2 × 0.48
```

Slew is applied **after quantization**.

The signal path is therefore:

```text
Behavior
   ↓
Position
   ↓
CV Target
   ↓
Quantization
   ↓
Rise / Fall
   ↓
CV Output
```

This allows a continuous behavioral trajectory to produce anything from relatively sharp pitch changes to slow, smooth modulation.

---

# 10. OLED Visualization

The OLED represents the internal two-dimensional behavioral space.

Importantly:

> **The OLED position is not simply a display of the final CV voltage.**

The behavioral position is processed separately for the CV output.

Therefore it is possible to see:

```text
continuous movement
```

on the OLED while hearing:

```text
quantized + slewed CV
```

at the outputs.

This separation is an important part of the instrument's design.

---

# 11. Timing

Some of the main timing parameters are:

```text
STEP_INTERVAL   = 220 ms
FRAME_INTERVAL  = 25 ms
EVENT_COOLDOWN  = 400 ms
```

The behavioral update and OLED refresh operate at different rates.

The display can therefore remain visually smooth without forcing the behavioral engine to update at the same rate.

---

# 12. Installation

Drunkard Behavior Research Center is designed for the **EuroPi** MicroPython environment.

Install the script in the appropriate EuroPi script directory, for example:

```text
lib/
└── contrib/
    └── drunkard.py
```

Register the script with the EuroPi Menu if required by your installation.

The program can then be launched from the EuroPi Menu.

---

# 13. Design Philosophy

Drunkard Behavior Research Center is intentionally not optimized for stability.

The system is interested in the space between:

```text
randomness
        ↓
unpredictability
        ↓
behavior
        ↓
emergence
```

A movement that appears inefficient, hesitant, repetitive, or unstable may be more interesting than a perfectly smooth random trajectory.

The goal is not to eliminate irregularity, but to make irregularity **structurally meaningful**.

---

# 14. Project Status

**Experimental / Research Instrument**

The project is intended as an evolving system for experimentation with:

- generative CV
- behavioral algorithms
- chaotic movement
- interactive systems
- experimental music
- visual-sonic relationships
- artificial behavior

Possible future directions include additional agents, environmental fields, obstacles, memory, attraction/repulsion zones, dynamic coupling, and external CV influence.

---

# 15. Credits

**Drunkard Behavior Research Center**

Concept, design and implementation:

**Xu Cheng / 徐程**

Developed as an experimental instrument for Eurorack, generative sound and behavioral systems.

Built for the open-source **EuroPi** platform by Allen Synthesis.

---

# Drunkard Behavior Research Center

> **A small behavioral system that happens to make voltage.**

---

<a id="chinese"></a>
## 中文说明


# 醉鬼行为研究中心
> **一个恰好会产生电压的小型行为系统:P**

### 一个为 EuroPi 制作的实验性CV发生器

**Drunkard Behavior Research Center（醉鬼行为研究中心）** 是一个运行于 **EuroPi** 上的实验性生成式 CV 乐器。

它并不直接生成随机电压，而是创造两个虚拟对象——**Alice** 与 **Ben**——让它们在一个共享的二维空间中运动。

它们的运动受到惯性、随机冲动、噪声、犹豫、空间边界以及彼此关系的影响。

因此最终产生的 CV 并不是简单的随机数，而是两个对象不断变化的内部状态及其关系所产生的结果。

> **不是随机发生器。  
> 不是 LFO。  
> 不是 Sequencer。  
> 而是一个恰好会产生电压的小型行为系统。**

---

# 1. 介绍与概念

基本观念：

> **创造行为，而不是直接创造随机性。**

每一个“醉鬼”都拥有自己的内部状态：

- 位置
- 速度
- 目标位置
- 行为噪声
- 偏置
- 随机冲动
- 与另一个对象的关系
- 当前 CV 状态

因此下一次运动会受到之前运动的影响。

Alice 与 Ben 共享同一个空间，但并不共享同一条轨迹。

根据不同的模式以及 Link 参数，它们可能：

- 独立运动
- 相互影响
- 模仿
- 回避
- 接近
- 分离
- 产生松散的对应关系
- 偶尔发生碰撞

系统有意保留：

- 不规则运动
- 犹豫
- 微小变化
- 不连续性
- 不完全重复
- 弱耦合
- 涌现性的行为

OLED 显示的是底层的行为状态，而 CV 输出则是对这种行为进行音乐化解释后的结果。

---

# 2. 界面

模块使用：

- **B1** — 选择 Alice / Ben
- **B2** — 切换参数页面
- **K1** — 参数 A
- **K2** — 参数 B
- **128 × 32 OLED** — 行为可视化

经过一段时间没有操作之后，参数界面可以自动隐藏，使 OLED 主要用于显示两个对象的行为轨迹。

## 参数页面

| 页面 | K1 | K2 |
|---|---|---|
| 0 | XR | YR |
| 1 | Link | Mode |
| 2 | Rise | Fall |
| 3 | Quant | — |
| 4 | X Range | — |

界面会显示当前正在选择的对象。

---

# 3. 操控

## B1 — 选择对象

按下 **B1**，在两个对象之间切换：

```text
A — Alice
B — Ben
```

属于单个对象的参数会作用于当前选中的对象。

---

## B2 — 参数页面

（参数页面在没有旋钮和按钮控制15秒的情况下会自动隐藏，旋转任一旋钮来唤醒页面。）

按下 **B2**，依次切换：

```text
PAGE 0    XR / YR
PAGE 1    Link / Mode
PAGE 2    Rise / Fall
PAGE 3    Quant
PAGE 4    X Range
```

---

## Pickup

参数旋钮采用 **Pickup（拾取）机制**。

切换页面时，旋钮不会立即使参数跳到当前旋钮位置。

若旋钮位置没有Pickup，参数会带*号。

只有当实体旋钮经过当前储存值之后，旋钮才重新接管参数。

这样可以避免在不同页面之间切换时产生突然的参数跳变。

---

# 4. 行为参数

## XR — X Range

控制当前对象的水平行为范围。

数值越大，对象单步可能探索的水平空间越大。

当前映射：

```text
XR = K1 × 9.9
```

---

## YR — Y Range

控制垂直行为范围。

当前映射：

```text
YR = K2 × 9.9
```

XR 与 YR 可以分别调整，因此可以形成不同的空间比例。

---

## Link

控制 Alice 与 Ben 之间的相互作用强度。

较低的 Link 会让两个对象保持相对独立。

提高 Link 后，它们的行为会变得更加相关。如碰撞和互动行为。

目前比较理想的工作值约为：

```text
Link ≈ 0.004
```

它的目的并不是让两个对象同步，而是建立一种**互动的行为关系**。

---

# 5. 行为模式

目前有三种模式：

```text
W — Wander
P — Portal
C — Counterpoint
```

## Wander — 漫游

对象在一个有限空间中运动。

边界成为行为的一部分。当对象到达边缘时，会与墙壁发生反应并触发trigger信号，而不是简单穿过边界。

这是三种模式中最直观的空间行为。

---

## Portal — 穿越

在 Portal 模式中，边界不再是墙，而成为 Portal。

离开一侧之后，对象会从相对的一侧重新出现：

```text
LEFT  → RIGHT
RIGHT → LEFT

TOP    → BOTTOM
BOTTOM → TOP
```

OLED 同时使用边缘残影，使这种穿越更容易被观察。

---

## Counterpoint — 对位

Counterpoint 为两个对象建立更强的行为关系。
“对位法”模式灵感来自作者的首个文字谱作品XTS0001。这是一个由两名表演者在仅依靠听觉的情况下尝试在对称空间中进行镜像运动的作品。
它们相互影响，但仍然保持各自独立的运动。

目标是：

> **相关，但不同步，却有规则感。**

两个轨迹因此可能出现：

- 接近
- 分离
- 跟随
- 模仿
- 偏离
- 偶发碰撞

---

# 6. 事件与 Trigger

行为事件可以产生 Trigger。

```text
CV3 → Alice Trigger
CV6 → Ben Trigger
```

事件可以与以下行为有关：

- 两个对象发生碰撞
- 对象撞到空间边界

系统设置了事件冷却时间，以避免对象停留在某个事件区域时持续触发。

用户可以把它送到其他的AR类工具来外部加工这种碰撞产生的效果。

因此 Trigger 并不是一个传统意义上的 Clock，而更接近：

> **行为系统中发生的事件。**

---

# 7. CV 输出

六个 EuroPi 输出被组织为两个行为通道。

| 输出 | 功能 | 范围 |
|---|---|---|
| CV1 | Alice X | 0–X Range |
| CV2 | Alice Y | 0–2.5 V |
| CV3 | Alice Trigger | Pulse |
| CV4 | Ben X | 0–X Range |
| CV5 | Ben Y | 0–2.5 V |
| CV6 | Ben Trigger | Pulse |

X 输出的全局范围可以设置为：

```text
1–5 OCT
```

---

# 8. 量化

量化只作用于 **CV 输出**，不会改变底层的行为位置。

可选：

```text
0   0  连续电压
1   12 半音阶
2   7  七声
3   5  五声
4   M1 全音阶
5   M2
6   M3
7   M4
8   M5
9   M6
10  M7
```

M1–M7 对应 **Olivier Messiaen 的七种有限移调模式**。

### M1

```text
0 2 4 6 8 10
```

### M2

```text
0 1 3 4 6 7 9 10
```

### M3

```text
0 2 3 4 6 7 8 10 11
```

### M4

```text
0 1 2 5 6 7 8 11
```

### M5

```text
0 1 5 6 7 11
```

### M6

```text
0 2 4 5 6 8 10 11
```

### M7

```text
0 1 2 3 5 6 7 8 9 11
```

量化可以在不改变 OLED 轨迹的情况下，改变同一行为在音乐上的结果。

---

# 9. Rise / Fall

Rise / Fall 为 CV 输出提供独立的增量和降量平滑控制。

> **默认值为不平滑，数值越小越平滑**

当前映射：

```text
Rise = 0.02 + K1 × 0.48
Fall = 0.02 + K2 × 0.48
```

Slew 位于量化之后，以表现滑音：

```text
Behavior
   ↓
Position
   ↓
CV Target
   ↓
Quantization
   ↓
Rise / Fall
   ↓
CV Output
```

因此，同一个行为轨迹可以产生从相对快速的音高变化，到缓慢连续的调制电压。

---

# 10. OLED 可视化

OLED 显示的是内部二维行为空间。

需要特别注意：

> **OLED 上的位置并不等同于最终的 CV 电压。**

行为位置和 CV 输出是分开处理的。

因此可能出现：

```text
OLED：
连续运动
```

同时：

```text
CV：
量化 + Slew
```

这也是本项目设计中的重要区别。

---

# 11. 时间系统

主要时间参数包括：

```text
STEP_INTERVAL   = 220 ms
FRAME_INTERVAL  = 25 ms
EVENT_COOLDOWN  = 400 ms
```

行为更新与 OLED 刷新采用不同的时间尺度。

这样既可以保持 OLED 的视觉连续性，又不会迫使行为引擎以同样的速度运行。

---

# 12. 安装

Drunkard Behavior Research Center 面向 **EuroPi MicroPython** 环境。

将程序放入相应的 EuroPi 程序目录，例如：

```text
lib/
└── contrib/
    └── drunkard.py
```

根据你的 EuroPi 安装方式，将程序加入 EuroPi Menu。

之后即可从 EuroPi Menu 启动。

---

# 13. 设计理念

Drunkard Behavior Research Center 并不以稳定为目标。

它关注的是：

```text
随机性
   ↓
不可预测性
   ↓
行为
   ↓
涌现
```

一个看起来低效、犹豫、重复或者不稳定的运动，并不一定是错误。

相反，这些“不完美”可能正是系统最有趣的部分。

项目的目标不是消除不规则性，而是让这种不规则性具有**结构性的意义**。

---

# 14. 项目状态

**Experimental / Research Instrument**

这是一个持续实验中的行为系统，用于探索：

- 生成式 CV
- 行为算法
- 混沌运动
- 互动系统
- 实验音乐
- 视觉与声音之间的关系
- 人工行为

未来可以继续探索：

- 更多对象
- 环境场
- 障碍物
- 记忆
- 吸引 / 排斥区域
- 动态耦合
- 外部 CV 对行为的影响

---

# 15. 作者

**Drunkard Behavior Research Center**

概念、设计与程序：

**徐程 / Xu Cheng**

作为一个实验性 Eurorack 乐器，用于生成式声音、行为系统以及视觉—声音关系的研究。

本项目基于 Allen Synthesis 的开源 **EuroPi** 平台开发。

---

# Drunkard Behavior Research Center

> **一个恰好会产生电压的小型行为系统。**
