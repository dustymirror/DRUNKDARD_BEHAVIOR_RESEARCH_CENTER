# ============================================================
# DRUNKARD
# #908 v1.3
# ============================================================

from europi import *
from time import ticks_ms, sleep_ms
import random
import math
import machine


# ============================================================
# CONFIG
# ============================================================

WIDTH = 127
HEIGHT = 31

STEP_MIN = 80
STEP_MAX = 700

FRAME_INTERVAL = 25

EVENT_COOLDOWN = 400

UI_TIMEOUT = 15000

COMBO_HOLD = 500
SINGLE_DELAY = 180


# ============================================================
# MODES
# ============================================================

MODE_WANDER = 0
MODE_PORTAL = 1
MODE_COUNTERPOINT = 2


# ============================================================
# QUANTIZER NAMES
# ============================================================

QNAMES = [
    "0",
    "12",
    "7",
    "5",
    "M1",
    "M2",
    "M3",
    "M4",
    "M5",
    "M6",
    "M7"
]


# ============================================================
# TRIGGERS
# ============================================================

def pulse(cv):
    cv.value(1)
    sleep_ms(12)
    cv.value(0)


alice_trig = cv3
ben_trig = cv6


# ============================================================
# EVENT GATE
# ============================================================

class EventGate:

    def __init__(self):

        self.last_collision = 0
        self.last_wall_a = 0
        self.last_wall_b = 0

    def allow_collision(self, now):

        if now - self.last_collision > EVENT_COOLDOWN:

            self.last_collision = now

            return True

        return False

    def allow_wall(self, name, now):

        if name == "A":

            if now - self.last_wall_a > EVENT_COOLDOWN:

                self.last_wall_a = now

                return True

        else:

            if now - self.last_wall_b > EVENT_COOLDOWN:

                self.last_wall_b = now

                return True

        return False


gate = EventGate()


# ============================================================
# DRUNKARD
# ============================================================

class Drunkard:

    # --------------------------------------------------------
    # REACTION
    # --------------------------------------------------------

    def react_to(self, other):

        if self.copy_timer > 0:

            self.copy_timer -= 1

            # 模仿行为
            self.tx += other.vx * 3 * self.link
            self.ty += other.vy * 3 * self.link

            return

        dx = other.x - self.x
        dy = other.y - self.y

        d = math.sqrt(dx * dx + dy * dy)

        if d < 20:

            if random.random() < 0.03:

                self.copy_timer = random.randint(20, 60)


    # --------------------------------------------------------
    # INIT
    # --------------------------------------------------------

    def __init__(self, name, xr, yr):

        self.name = name

        self.xr = float(xr)
        self.yr = float(yr)

        # position
        self.x = WIDTH / 2
        self.y = HEIGHT / 2

        # velocity
        self.vx = 0.0
        self.vy = 0.0

        # target
        self.tx = self.x
        self.ty = self.y

        # slow bias
        self.bias_x = random.uniform(-0.01, 0.01)
        self.bias_y = random.uniform(-0.01, 0.01)

        # relationship field
        self.field_x = 0.0
        self.field_y = 0.0

        # event impulse
        self.event_x = 0.0
        self.event_y = 0.0

        self.decay = 0.985

        # individual sluggishness
        self.sluggish = random.uniform(1.0, 2.2)

        # noise
        self.noise = 0
        self.noise_next = random.randint(30, 140)

        # impulse
        self.impulse = 0
        self.impulse_x = 0.0
        self.impulse_y = 0.0

        # pause
        self.pause = 0

        # copying
        self.copy_timer = 0

        # mood
        self.mood = random.random()

        # ----------------------------------------------------
        # USER PARAMETERS
        # ----------------------------------------------------

        self.link = 0.004

        self.mode = MODE_WANDER

        self.rise = 0.15
        self.fall = 0.15

        self.quant = 0

        # Counterpoint mirror position
        self.cp_x = WIDTH / 2
        self.cp_y = HEIGHT / 2


    # ========================================================
    # MACRO STEP
    # ========================================================

    def macro_step(self):

        # --------------------------------------------
        # pause
        # --------------------------------------------

        if self.pause > 0:

            self.pause -= 1

            return


        # --------------------------------------------
        # 发呆
        # --------------------------------------------

        if random.random() < 0.08:

            self.pause = random.randint(1, 6)

            return


        # --------------------------------------------
        # 犹豫
        # --------------------------------------------

        if random.random() < 0.25:

            return


        # --------------------------------------------
        # 冲动
        # --------------------------------------------

        if self.impulse <= 0:

            if random.random() < 0.04:

                self.impulse = random.randint(2, 5)

                self.impulse_x = random.uniform(
                    -self.xr,
                    self.xr
                ) * 3

                self.impulse_y = random.uniform(
                    -self.yr,
                    self.yr
                ) * 3


        if self.impulse > 0:

            self.tx += self.impulse_x
            self.ty += self.impulse_y

            self.impulse -= 1

        else:

            sx = random.uniform(
                -self.xr,
                self.xr
            )

            sy = random.uniform(
                -self.yr,
                self.yr
            )


            # ----------------------------------------
            # 失衡
            # ----------------------------------------

            if random.random() < 0.10:

                if random.random() < 0.5:

                    sx *= 4
                    sy *= 0.25

                else:

                    sy *= 4
                    sx *= 0.25


            self.tx += sx
            self.ty += sy


        # --------------------------------------------
        # TARGET BOUNDARY
        # --------------------------------------------

        if self.mode == MODE_WANDER:

            self.tx = max(
                0,
                min(WIDTH, self.tx)
            )

            self.ty = max(
                0,
                min(HEIGHT, self.ty)
            )

        else:

            while self.tx < 0:
                self.tx += WIDTH

            while self.tx > WIDTH:
                self.tx -= WIDTH

            while self.ty < 0:
                self.ty += HEIGHT

            while self.ty > HEIGHT:
                self.ty -= HEIGHT


    # ========================================================
    # RELATION FIELD
    # ========================================================

    def apply_field(self, others):

        fx = 0.0
        fy = 0.0

        for o in others:

            if o is self:
                continue

            dx = o.x - self.x
            dy = o.y - self.y

            d = math.sqrt(
                dx * dx +
                dy * dy
            ) + 0.5

            fx += dx / (d * d)
            fy += dy / (d * d)


        self.field_x = fx * self.link
        self.field_y = fy * self.link


        # --------------------------------------------
        # safety clamp
        # --------------------------------------------

        if self.field_x > 0.2:
            self.field_x = 0.2

        if self.field_x < -0.2:
            self.field_x = -0.2

        if self.field_y > 0.2:
            self.field_y = 0.2

        if self.field_y < -0.2:
            self.field_y = -0.2


    # ========================================================
    # EVENTS
    # ========================================================

    def event_collision(self):

        self.event_x += random.uniform(
            -0.05,
            0.05
        )

        self.event_y += random.uniform(
            -0.04,
            0.04
        )

        self.trigger()


    def event_wall(self):

        self.event_x += random.uniform(
            -0.08,
            0.08
        )

        self.event_y += random.uniform(
            -0.06,
            0.06
        )

        self.trigger()


    def trigger(self):

        if self.name == "A":

            pulse(alice_trig)

        else:

            pulse(ben_trig)


    # ========================================================
    # NOISE
    # ========================================================

    def update_noise(self):

        self.noise_next -= 1

        if self.noise_next <= 0:

            self.noise = random.randint(1, 3)

            self.noise_next = random.randint(
                40,
                160
            )

        else:

            self.noise = 0


    # ========================================================
    # UPDATE
    # ========================================================

    def update(self):

        # --------------------------------------------
        # bias drift
        # --------------------------------------------

        self.bias_x += random.uniform(
            -0.001,
            0.001
        )

        self.bias_y += random.uniform(
            -0.001,
            0.001
        )

        self.bias_x *= 0.997
        self.bias_y *= 0.997


        # --------------------------------------------
        # target difference
        # --------------------------------------------

        dx = self.tx - self.x
        dy = self.ty - self.y


        # --------------------------------------------
        # Portal shortest path
        # --------------------------------------------

        if self.mode == MODE_PORTAL:

            if dx > WIDTH / 2:
                dx -= WIDTH

            elif dx < -WIDTH / 2:
                dx += WIDTH


            if dy > HEIGHT / 2:
                dy -= HEIGHT

            elif dy < -HEIGHT / 2:
                dy += HEIGHT


        # --------------------------------------------
        # Counterpoint
        # --------------------------------------------

        if self.mode == MODE_COUNTERPOINT:

            cp_strength = 0.01 + self.link * 0.08

            self.tx += (
                self.cp_x -
                self.tx
            ) * cp_strength

            self.ty += (
                self.cp_y -
                self.ty
            ) * cp_strength


            dx = self.tx - self.x
            dy = self.ty - self.y


        # --------------------------------------------
        # target attraction
        # --------------------------------------------

        self.vx += (
            dx *
            0.015 /
            self.sluggish
        )

        self.vy += (
            dy *
            0.015 /
            self.sluggish
        )


        # --------------------------------------------
        # bias
        # --------------------------------------------

        self.vx += self.bias_x
        self.vy += self.bias_y


        # --------------------------------------------
        # relation field
        # --------------------------------------------

        self.vx += self.field_x
        self.vy += self.field_y


        # --------------------------------------------
        # behavioural noise
        # --------------------------------------------

        if self.noise:

            self.vx += random.uniform(
                -0.1,
                0.1
            )

            self.vy += random.uniform(
                -0.08,
                0.08
            )


        # --------------------------------------------
        # events
        # --------------------------------------------

        self.vx += self.event_x
        self.vy += self.event_y

        self.event_x *= self.decay
        self.event_y *= self.decay


        # --------------------------------------------
        # damping
        # --------------------------------------------

        self.vx *= 0.86
        self.vy *= 0.86


        # --------------------------------------------
        # velocity safety
        # --------------------------------------------

        if self.vx < -50:
            self.vx = -50

        if self.vx > 50:
            self.vx = 50

        if self.vy < -50:
            self.vy = -50

        if self.vy > 50:
            self.vy = 50


        # --------------------------------------------
        # position
        # --------------------------------------------

        self.x += self.vx
        self.y += self.vy


        # ====================================================
        # PORTAL
        # ====================================================

        if self.mode == MODE_PORTAL:

            while self.x < 0:
                self.x += WIDTH

            while self.x > WIDTH:
                self.x -= WIDTH

            while self.y < 0:
                self.y += HEIGHT

            while self.y > HEIGHT:
                self.y -= HEIGHT

            return None


        # ====================================================
        # EMERGENCY RESET
        # ====================================================

        if self.x < -1000:
            self.x = WIDTH / 2

        if self.x > 1000:
            self.x = WIDTH / 2

        if self.y < -1000:
            self.y = HEIGHT / 2

        if self.y > 1000:
            self.y = HEIGHT / 2


        # ====================================================
        # WALL
        # ====================================================

        if self.x <= 0:

            if self.mode == MODE_WANDER:

                self.x = -self.x
                self.vx *= -0.5

            else:

                self.x = 0

            return "wall"


        if self.x >= WIDTH:

            if self.mode == MODE_WANDER:

                self.x = WIDTH - (
                    self.x - WIDTH
                )

                self.vx *= -0.5

            else:

                self.x = WIDTH

            return "wall"


        if self.y <= 0:

            if self.mode == MODE_WANDER:

                self.y = -self.y
                self.vy *= -0.5

            else:

                self.y = 0

            return "wall"


        if self.y >= HEIGHT:

            if self.mode == MODE_WANDER:

                self.y = HEIGHT - (
                    self.y - HEIGHT
                )

                self.vy *= -0.5

            else:

                self.y = HEIGHT

            return "wall"


        return None


# ============================================================
# INIT
# ============================================================

alice = Drunkard(
    "A",
    1.4,
    0.9
)

ben = Drunkard(
    "B",
    1.0,
    0.7
)

drunks = [
    alice,
    ben
]

selected = 0

page = 0

PAGE_COUNT = 5

pickup1 = False
pickup2 = False


# ============================================================
# X RANGE
# ============================================================

xrange = 5


# ============================================================
# CV STATE
# ============================================================

a_cvx = 0.0
a_cvy = 0.0

b_cvx = 0.0
b_cvy = 0.0


a_cvx_initialized = False
a_cvy_initialized = False

b_cvx_initialized = False
b_cvy_initialized = False


# ============================================================
# UI STATE
# ============================================================

last_ui_activity = ticks_ms()

ui_visible = True

last_k1v = k1.percent()
last_k2v = k2.percent()


# ============================================================
# BUTTON POLLING STATE
# ============================================================

last_b1 = 0
last_b2 = 0

b1_pending = False
b2_pending = False

b1_pending_time = 0
b2_pending_time = 0

combo_active = False
combo_fired = False
combo_start = 0


# ============================================================
# BUTTON ACTIONS
# ============================================================

def next_drunk():

    global selected
    global pickup1
    global pickup2
    global last_ui_activity

    selected = (
        selected + 1
    ) % len(drunks)

    pickup1 = False
    pickup2 = False

    last_ui_activity = ticks_ms()


def next_page():

    global page
    global pickup1
    global pickup2
    global last_ui_activity

    page = (
        page + 1
    ) % PAGE_COUNT

    pickup1 = False
    pickup2 = False

    last_ui_activity = ticks_ms()


# ============================================================
# EXIT
# ============================================================

def exit_to_menu():

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # The polling test itself is confirmed to work.
    # Here we intentionally reset the board after clearing
    # the script state.
    #
    # Bootloader should then return to its menu.
    # --------------------------------------------------------

    oled.fill(0)

    oled.text(
        "exiting...",
        30,
        16
    )

    oled.show()

    sleep_ms(500)

    try:

        reset_state()

    except:

        pass

    machine.reset()


# ============================================================
# COMBO PROCESS
# ============================================================

def process_buttons(now):

    global last_b1
    global last_b2

    global b1_pending
    global b2_pending

    global b1_pending_time
    global b2_pending_time

    global combo_active
    global combo_fired
    global combo_start

    b1_now = b1.value()
    b2_now = b2.value()


    # ========================================================
    # BOTH PRESSED
    # ========================================================

    if b1_now and b2_now:

        if not combo_active:

            combo_active = True
            combo_fired = False
            combo_start = now

        if (
            not combo_fired
            and
            now - combo_start >= COMBO_HOLD
        ):

            combo_fired = True

            b1_pending = False
            b2_pending = False

            exit_to_menu()

        return


    # ========================================================
    # BOTH RELEASED
    # ========================================================

    if not b1_now and not b2_now:

        combo_active = False
        combo_fired = False


    # ========================================================
    # NEW B1 PRESS
    # ========================================================

    if b1_now and not last_b1:

        b1_pending = True
        b1_pending_time = now


    # ========================================================
    # NEW B2 PRESS
    # ========================================================

    if b2_now and not last_b2:

        b2_pending = True
        b2_pending_time = now


    # ========================================================
    # B1 PENDING
    # ========================================================

    if b1_pending:

        # another button appeared
        if b2_now:

            b1_pending = False

        elif (
            now - b1_pending_time
            >= SINGLE_DELAY
        ):

            next_drunk()

            b1_pending = False


    # ========================================================
    # B2 PENDING
    # ========================================================

    if b2_pending:

        if b1_now:

            b2_pending = False

        elif (
            now - b2_pending_time
            >= SINGLE_DELAY
        ):

            next_page()

            b2_pending = False


    last_b1 = b1_now
    last_b2 = b2_now


# ============================================================
# QUANTIZER
# ============================================================

def quantize_cv(voltage, mode):

    if mode == 0:

        return voltage


    # --------------------------------------------------------
    # 12 equal divisions
    # --------------------------------------------------------

    if mode == 1:

        step = 1.0 / 12.0

        return round(
            voltage / step
        ) * step


    # --------------------------------------------------------
    # C major
    # --------------------------------------------------------

    if mode == 2:

        scale = [
            0, 2, 4, 5,
            7, 9, 11
        ]

        return quantize_scale(
            voltage,
            scale
        )


    # --------------------------------------------------------
    # C pentatonic
    # --------------------------------------------------------

    if mode == 3:

        scale = [
            0, 2, 4, 7, 9
        ]

        return quantize_scale(
            voltage,
            scale
        )


    # --------------------------------------------------------
    # Messiaen Mode 1
    # --------------------------------------------------------

    if mode == 4:

        scale = [
            0, 2, 4,
            6, 8, 10
        ]

        return quantize_scale(
            voltage,
            scale
        )


    # --------------------------------------------------------
    # Messiaen Mode 2
    # --------------------------------------------------------

    if mode == 5:

        scale = [
            0, 1, 3, 4,
            6, 7, 9, 10
        ]

        return quantize_scale(
            voltage,
            scale
        )


    # --------------------------------------------------------
    # Messiaen Mode 3
    # --------------------------------------------------------

    if mode == 6:

        scale = [
            0, 2, 3, 4,
            6, 7, 8,
            10, 11
        ]

        return quantize_scale(
            voltage,
            scale
        )


    # --------------------------------------------------------
    # Messiaen Mode 4
    # --------------------------------------------------------

    if mode == 7:

        scale = [
            0, 1, 2, 5,
            6, 7, 8, 11
        ]

        return quantize_scale(
            voltage,
            scale
        )


    # --------------------------------------------------------
    # Messiaen Mode 5
    # --------------------------------------------------------

    if mode == 8:

        scale = [
            0, 1, 5,
            6, 7, 11
        ]

        return quantize_scale(
            voltage,
            scale
        )


    # --------------------------------------------------------
    # Messiaen Mode 6
    # --------------------------------------------------------

    if mode == 9:

        scale = [
            0, 2, 4, 5,
            6, 8, 10, 11
        ]

        return quantize_scale(
            voltage,
            scale
        )


    # --------------------------------------------------------
    # Messiaen Mode 7
    # --------------------------------------------------------

    if mode == 10:

        scale = [
            0, 1, 2, 3,
            5, 6, 7, 8,
            9, 11
        ]

        return quantize_scale(
            voltage,
            scale
        )


    return voltage


# ============================================================
# SCALE QUANTIZER
# ============================================================

def quantize_scale(voltage, scale):

    # 1 octave = 1V
    octave = int(
        math.floor(voltage)
    )

    frac = voltage - octave

    semitone = frac * 12.0

    best = scale[0]
    best_dist = abs(
        semitone - best
    )

    for note in scale:

        dist = abs(
            semitone - note
        )

        if dist < best_dist:

            best = note
            best_dist = dist

    result = (
        octave +
        best / 12.0
    )

    return result


# ============================================================
# SLEW
# ============================================================

def slew_value(
    current,
    target,
    rise,
    fall
):

    if target > current:

        current += (
            target - current
        ) * rise

    else:

        current += (
            target - current
        ) * fall

    return current


# ============================================================
# SPLASH
# ============================================================

oled.fill(0)

oled.text(
    "DRUNKARD",
    30,
    4
)

oled.text(
    "BEHAVIOR",
    30,
    12
)

oled.text(
    "RESEARCH CENTER",
    6,
    20
)

oled.show()

sleep_ms(3200)

oled.fill(0)

oled.text(
    "Dusty Mirror",
    25,
    12
)

oled.text(
    "2026",
    55,
    22
)

oled.show()

sleep_ms(1000)


# ============================================================
# LOOP TIMERS
# ============================================================

next_step = (
    ticks_ms() +
    random.randint(
        STEP_MIN,
        STEP_MAX
    )
)

last_frame = ticks_ms()


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    now = ticks_ms()

    current = drunks[selected]


    # ========================================================
    # BUTTONS
    # ========================================================

    process_buttons(now)


    # ========================================================
    # CONTROL
    # ========================================================

    k1v = k1.percent()
    k2v = k2.percent()


    # --------------------------------------------------------
    # UI activity
    # --------------------------------------------------------

    if (
        abs(k1v - last_k1v) > 0.005
        or
        abs(k2v - last_k2v) > 0.005
    ):

        last_ui_activity = now
        ui_visible = True


    last_k1v = k1v
    last_k2v = k2v


    # --------------------------------------------------------
    # page parameters
    # --------------------------------------------------------

    if page == 0:

        p1 = current.xr / 9.9
        p2 = current.yr / 9.9


    elif page == 1:

        p1 = current.link

        p2 = current.mode / 2.0


    elif page == 2:

        p1 = (
            current.rise - 0.02
        ) / 0.48

        p2 = (
            current.fall - 0.02
        ) / 0.48


    elif page == 3:

        p1 = current.quant / 10.0

        p2 = 0


    else:

        p1 = (
            xrange - 1
        ) / 4.0

        p2 = 0


    # ========================================================
    # PICKUP
    # ========================================================

    if not pickup1:

        if abs(k1v - p1) < 0.03:

            pickup1 = True


    if not pickup2:

        if abs(k2v - p2) < 0.03:

            pickup2 = True


    # ========================================================
    # PARAMETERS
    # ========================================================

    if page == 0:

        if pickup1:

            current.xr = (
                k1v * 9.9
            )

        if pickup2:

            current.yr = (
                k2v * 9.9
            )


    elif page == 1:

        if pickup1:

            current.link = k1v


        if pickup2:

            current.mode = int(
                k2v * 2.99
            )


    elif page == 2:

        if pickup1:

            current.rise = (
                0.02 +
                k1v * 0.48
            )

        if pickup2:

            current.fall = (
                0.02 +
                k2v * 0.48
            )


    elif page == 3:

        if pickup1:

            current.quant = int(
                k1v * 10.99
            )


    elif page == 4:

        if pickup1:

            xrange = (
                1 +
                int(k1v * 4.99)
            )


    # ========================================================
    # STEP
    # ========================================================

    if now >= next_step:

        next_step = (
            now +
            random.randint(
                STEP_MIN,
                STEP_MAX
            )
        )

        alice.macro_step()
        ben.macro_step()


    # ========================================================
    # COUNTERPOINT
    # ========================================================

    if alice.mode == MODE_COUNTERPOINT:

        alice.cp_x = (
            WIDTH -
            ben.x
        )

        alice.cp_y = (
            HEIGHT -
            ben.y
        )

    else:

        alice.cp_x = alice.x
        alice.cp_y = alice.y


    if ben.mode == MODE_COUNTERPOINT:

        ben.cp_x = (
            WIDTH -
            alice.x
        )

        ben.cp_y = (
            HEIGHT -
            alice.y
        )

    else:

        ben.cp_x = ben.x
        ben.cp_y = ben.y


    # ========================================================
    # COLLISION
    # ========================================================

    dx = alice.x - ben.x
    dy = alice.y - ben.y

    dist = math.sqrt(
        dx * dx +
        dy * dy
    )


    if dist < 10:

        if gate.allow_collision(now):

            alice.event_collision()
            ben.event_collision()


    # ========================================================
    # UPDATE
    # ========================================================

    alice.react_to(ben)
    ben.react_to(alice)


    for d in drunks:

        d.apply_field(drunks)

        d.update_noise()

        wall = d.update()


        if wall == "wall":

            if gate.allow_wall(
                d.name,
                now
            ):

                d.event_wall()


    # ========================================================
    # CV TARGETS
    # ========================================================

    a_target_x = (
        alice.x /
        WIDTH
    ) * xrange


    a_target_y = (
        alice.y /
        HEIGHT
    ) * 2.5


    b_target_x = (
        ben.x /
        WIDTH
    ) * xrange


    b_target_y = (
        ben.y /
        HEIGHT
    ) * 2.5


    # ========================================================
    # QUANTIZE
    # ========================================================

    a_qx = quantize_cv(
        a_target_x,
        alice.quant
    )

    a_qy = quantize_cv(
        a_target_y,
        alice.quant
    )

    b_qx = quantize_cv(
        b_target_x,
        ben.quant
    )

    b_qy = quantize_cv(
        b_target_y,
        ben.quant
    )


    # ========================================================
    # INITIALIZE CV
    # ========================================================

    if not a_cvx_initialized:

        a_cvx = a_qx

        a_cvx_initialized = True


    if not a_cvy_initialized:

        a_cvy = a_qy

        a_cvy_initialized = True


    if not b_cvx_initialized:

        b_cvx = b_qx

        b_cvx_initialized = True


    if not b_cvy_initialized:

        b_cvy = b_qy

        b_cvy_initialized = True


    # ========================================================
    # SLEW
    # ========================================================

    a_cvx = slew_value(
        a_cvx,
        a_qx,
        alice.rise,
        alice.fall
    )


    a_cvy = slew_value(
        a_cvy,
        a_qy,
        alice.rise,
        alice.fall
    )


    b_cvx = slew_value(
        b_cvx,
        b_qx,
        ben.rise,
        ben.fall
    )


    b_cvy = slew_value(
        b_cvy,
        b_qy,
        ben.rise,
        ben.fall
    )


    # ========================================================
    # CLAMP
    # ========================================================

    if a_cvx < 0:
        a_cvx = 0

    if a_cvx > xrange:
        a_cvx = xrange


    if b_cvx < 0:
        b_cvx = 0

    if b_cvx > xrange:
        b_cvx = xrange


    if a_cvy < 0:
        a_cvy = 0

    if a_cvy > 2.5:
        a_cvy = 2.5


    if b_cvy < 0:
        b_cvy = 0

    if b_cvy > 2.5:
        b_cvy = 2.5


    # ========================================================
    # OUTPUT
    # ========================================================

    cv1.voltage(a_cvx)
    cv2.voltage(a_cvy)

    cv4.voltage(b_cvx)
    cv5.voltage(b_cvy)


    # ========================================================
    # UI AUTO HIDE
    # ========================================================

    if now - last_ui_activity > UI_TIMEOUT:

        ui_visible = False


    # ========================================================
    # OLED
    # ========================================================

    if now - last_frame >= FRAME_INTERVAL:

        last_frame = now

        oled.fill(0)


        # ----------------------------------------------------
        # parameter UI
        # ----------------------------------------------------

        if ui_visible:

            oled.text(
                "A" if selected == 0 else " ",
                0,
                0
            )

            oled.text(
                "B" if selected == 1 else " ",
                8,
                0
            )

            oled.text(
                "P%d" % (page + 1),
                20,
                0
            )


            # --------------------------------------------
            # PAGE 1
            # --------------------------------------------

            if page == 0:

                oled.text(
                    "XR%s %.1f" %
                    (
                        "*" if not pickup1 else "",
                        current.xr
                    ),
                    0,
                    10
                )

                oled.text(
                    "YR%s %.1f" %
                    (
                        "*" if not pickup2 else "",
                        current.yr
                    ),
                    0,
                    20
                )


            # --------------------------------------------
            # PAGE 2
            # --------------------------------------------

            elif page == 1:

                oled.text(
                    "LK%s %.3f" %
                    (
                        "*" if not pickup1 else "",
                        current.link
                    ),
                    0,
                    10
                )


                mode_name = [
                    "W",
                    "P",
                    "C"
                ][current.mode]


                oled.text(
                    "MD%s %s" %
                    (
                        "*" if not pickup2 else "",
                        mode_name
                    ),
                    0,
                    20
                )


            # --------------------------------------------
            # PAGE 3
            # --------------------------------------------

            elif page == 2:

                oled.text(
                    "RI%s %.2f" %
                    (
                        "*" if not pickup1 else "",
                        current.rise
                    ),
                    0,
                    10
                )

                oled.text(
                    "FA%s %.2f" %
                    (
                        "*" if not pickup2 else "",
                        current.fall
                    ),
                    0,
                    20
                )


            # --------------------------------------------
            # PAGE 4
            # --------------------------------------------

            elif page == 3:

                oled.text(
                    "QT%s %s" %
                    (
                        "*" if not pickup1 else "",
                        QNAMES[current.quant]
                    ),
                    0,
                    10
                )


            # --------------------------------------------
            # PAGE 5
            # --------------------------------------------

            elif page == 4:

                oled.text(
                    "XO%s %d-OCT" %
                    (
                        "*" if not pickup1 else "",
                        xrange
                    ),
                    0,
                    10
                )


                oled.text(
                    "A&B",
                    0,
                    20
                )


        # ====================================================
        # XY DISPLAY
        # ====================================================

        try:

            ax = int(alice.x)
            ay = int(alice.y)

        except:

            ax = WIDTH // 2
            ay = HEIGHT // 2


        try:

            bx = int(ben.x)
            by = int(ben.y)

        except:

            bx = WIDTH // 2
            by = HEIGHT // 2


        # ----------------------------------------------------
        # A
        # ----------------------------------------------------

        if (
            -4 < ax < WIDTH
            and
            -8 < ay < HEIGHT
        ):

            oled.text(
                "A",
                ax,
                ay
            )


        if (
            ax > WIDTH - 4
            and
            -8 < ay < HEIGHT
        ):

            oled.text(
                "A",
                ax - WIDTH,
                ay
            )


        if (
            ax < 4
            and
            -8 < ay < HEIGHT
        ):

            oled.text(
                "A",
                ax + WIDTH,
                ay
            )


        # ----------------------------------------------------
        # B
        # ----------------------------------------------------

        if (
            -4 < bx < WIDTH
            and
            -8 < by < HEIGHT
        ):

            oled.text(
                "B",
                bx,
                by
            )


        if (
            bx > WIDTH - 4
            and
            -8 < by < HEIGHT
        ):

            oled.text(
                "B",
                bx - WIDTH,
                by
            )


        if (
            bx < 4
            and
            -8 < by < HEIGHT
        ):

            oled.text(
                "B",
                bx + WIDTH,
                by
            )


        oled.show()