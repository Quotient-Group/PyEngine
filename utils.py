
import pygame
import inspect
import math

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
OLIVE = (128, 128, 0)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
MAROON = (128, 0, 0)
GOLD = (255, 215, 0)
CORAL = (255, 127, 80)
INDIGO = (75, 0, 130)
VIOLET = (238, 130, 238)
HOT_PINK = (255, 105, 180)
CRIMSON = (220, 20, 60)
CHOCOLATE = (210, 105, 30)
TURQUOISE = (64, 224, 208)
LAVENDER = (230, 230, 250)
PLUM = (221, 160, 221)
KHAKI = (240, 230, 140)
SALMON = (250, 128, 114)
TOMATO = (255, 99, 71)
ORANGE_RED = (255, 69, 0)
DARK_GOLDENROD = (184, 134, 11)
LIME_GREEN = (50, 205, 50)
FOREST_GREEN = (34, 139, 34)
SKY_BLUE = (135, 206, 235)


# Useful functions

# Returns a surface with alpha regulation
def AlphaSurface(size: tuple[int,int] = (32,32), alpha: int = 50) -> pygame.Surface:
    alpha_surface = pygame.Surface(size)
    alpha_surface.set_alpha(alpha)
    return alpha_surface

# Checks if a function accepts a certain parameter as kwarg
def accepts_kwarg(func, kwarg_name):
    func = inspect.unwrap(func)
    sig = inspect.signature(func)
    for param in sig.parameters.values():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True
        if param.name == kwarg_name:
            # Ensure it's not positional-only
            if param.kind != inspect.Parameter.POSITIONAL_ONLY:
                return True
    return False


def get_nearest_res(target: tuple[int,int], res: tuple[int,int]):
    GCD = math.gcd(res[0], res[1])
    candidates = [(res[0]/d, res[1]/d) for d in range(1, GCD+1)]
    def score(candidate: tuple[int,int]):
        return abs(math.hypot(*candidate) - math.hypot(*target))
    favorite = candidates[0]
    for candidate in candidates:
        if candidate[0]==int(candidate[0]) and candidate[1]==int(candidate[1]):
            if score(candidate) < score(favorite):
                favorite = candidate
    return (int(favorite[0]), int(favorite[1]))


def get_largest_rect_size_inside(host: tuple[int,int]):
    ...


# Easing functions

# ----------------------------------------------------------------------
# Utility
# ----------------------------------------------------------------------
def clamp(t, low=0.0, high=1.0):
    """Clamp t to the range [low, high]."""
    return max(low, min(high, t))

# ----------------------------------------------------------------------
# 1. Linear
# ----------------------------------------------------------------------
def linear(t):
    return t

# ----------------------------------------------------------------------
# 2. Quadratic
# ----------------------------------------------------------------------
def ease_in_quad(t):
    return t * t

def ease_out_quad(t):
    return t * (2 - t)

def ease_in_out_quad(t):
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t

# ----------------------------------------------------------------------
# 3. Cubic
# ----------------------------------------------------------------------
def ease_in_cubic(t):
    return t * t * t

def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def ease_in_out_cubic(t):
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2

# ----------------------------------------------------------------------
# 4. Quartic
# ----------------------------------------------------------------------
def ease_in_quart(t):
    return t ** 4

def ease_out_quart(t):
    return 1 - (1 - t) ** 4

def ease_in_out_quart(t):
    if t < 0.5:
        return 8 * t ** 4
    else:
        return 1 - (-2 * t + 2) ** 4 / 2

# ----------------------------------------------------------------------
# 5. Quintic
# ----------------------------------------------------------------------
def ease_in_quint(t):
    return t ** 5

def ease_out_quint(t):
    return 1 - (1 - t) ** 5

def ease_in_out_quint(t):
    if t < 0.5:
        return 16 * t ** 5
    else:
        return 1 - (-2 * t + 2) ** 5 / 2

# ----------------------------------------------------------------------
# 6. Sine
# ----------------------------------------------------------------------
def ease_in_sine(t):
    return 1 - math.cos(t * math.pi / 2)

def ease_out_sine(t):
    return math.sin(t * math.pi / 2)

def ease_in_out_sine(t):
    return -(math.cos(math.pi * t) - 1) / 2

# ----------------------------------------------------------------------
# 7. Exponential
# ----------------------------------------------------------------------
def ease_in_expo(t):
    return 0.0 if t == 0 else 2 ** (10 * (t - 1))

def ease_out_expo(t):
    return 1.0 if t == 1 else 1 - 2 ** (-10 * t)

def ease_in_out_expo(t):
    if t == 0 or t == 1:
        return t
    if t < 0.5:
        return 2 ** (20 * t - 10) / 2
    else:
        return (2 - 2 ** (-20 * t + 10)) / 2

# ----------------------------------------------------------------------
# 8. Circular
# ----------------------------------------------------------------------
def ease_in_circ(t):
    return 1 - math.sqrt(1 - t * t)

def ease_out_circ(t):
    return math.sqrt(1 - (t - 1) ** 2)

def ease_in_out_circ(t):
    if t < 0.5:
        return (1 - math.sqrt(1 - (2 * t) ** 2)) / 2
    else:
        return (math.sqrt(1 - (-2 * t + 2) ** 2) + 1) / 2

# ----------------------------------------------------------------------
# 9. Back (with overshoot)
# ----------------------------------------------------------------------
def ease_in_back(t, overshoot=1.70158):
    return t * t * ((overshoot + 1) * t - overshoot)

def ease_out_back(t, overshoot=1.70158):
    return 1 - (1 - t) * (1 - t) * ((overshoot + 1) * (1 - t) - overshoot)

def ease_in_out_back(t, overshoot=1.70158):
    c = overshoot * 1.525
    if t < 0.5:
        return (2 * t) ** 2 * ((c + 1) * 2 * t - c) / 2
    else:
        return ( (2 * t - 2) ** 2 * ((c + 1) * (t * 2 - 2) + c) + 2 ) / 2

# ----------------------------------------------------------------------
# 10. Elastic (with optional amplitude and period)
# ----------------------------------------------------------------------
def ease_in_elastic(t, amplitude=1.0, period=0.3):
    if t == 0 or t == 1:
        return t
    s = period / (2 * math.pi) * math.asin(1 / amplitude) if amplitude < 1 else period / 4
    return -(amplitude * 2 ** (10 * (t - 1)) * math.sin((t - 1 - s) * (2 * math.pi) / period))

def ease_out_elastic(t, amplitude=1.0, period=0.3):
    if t == 0 or t == 1:
        return t
    s = period / (2 * math.pi) * math.asin(1 / amplitude) if amplitude < 1 else period / 4
    return amplitude * 2 ** (-10 * t) * math.sin((t - s) * (2 * math.pi) / period) + 1

def ease_in_out_elastic(t, amplitude=1.0, period=0.3):
    if t == 0 or t == 1:
        return t
    s = period / (2 * math.pi) * math.asin(1 / amplitude) if amplitude < 1 else period / 4
    if t < 0.5:
        return -0.5 * (amplitude * 2 ** (20 * t - 10) * math.sin((20 * t - 10 - s) * (2 * math.pi) / period))
    else:
        return amplitude * 2 ** (-20 * t + 10) * math.sin((20 * t - 10 - s) * (2 * math.pi) / period) * 0.5 + 1

# ----------------------------------------------------------------------
# 11. Bounce
# ----------------------------------------------------------------------
def ease_out_bounce(t):
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375

def ease_in_bounce(t):
    return 1 - ease_out_bounce(1 - t)

def ease_in_out_bounce(t):
    if t < 0.5:
        return (1 - ease_out_bounce(1 - 2 * t)) / 2
    else:
        return (1 + ease_out_bounce(2 * t - 1)) / 2
