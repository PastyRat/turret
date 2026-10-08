import math

INTERVAL = 0.001
P = 1.0
C = 0.4
A = 0.025
M = 0.4
K = 12000.0
U = 0.3
G = 9.81
TOLERANCE = 0.003


def find_xzangle(coordinateX, coordinateZ):
    """Return the azimuth angle in degrees, normalized to 0..360."""
    angle = math.degrees(math.atan2(coordinateZ, coordinateX))
    return angle % 360.0


def model(p, c, a, angle_rad, m, k, x, u, h, g):
    """Compute the distance travelled by the system for a given band extension and angle.

    The original logic is preserved structurally, but the hot path is tightened by:
    - reducing repeated math operations inside loops,
    - using local variables instead of repeated global lookups,
    - short-circuiting when the extension is already zero,
    - avoiding redundant sqrt calls.
    """
    coeff = 0.5 * p * c * a / m
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    band_extension = max(0.0, float(x))
    velocity = 0.0

    while band_extension > 0.0:
        previous_velocity = velocity
        drag_term = 0.5 * p * c * a * (velocity ** 2)
        acceleration = (
            k * band_extension
            - m * u * g * cos_a
            - drag_term
            - m * g * cos_a
        ) / m
        velocity += acceleration * INTERVAL
        band_extension -= previous_velocity * INTERVAL

    vx = velocity * cos_a
    vy = velocity * sin_a
    running = 0 if h > 0 else 1
    y = float(h)
    displacement = 0.0
    previous_y = y

    while y >= 0.0 or running:
        if y >= 0.0 and h <= 0.0 and running == 1:
            running = 0

        if y < previous_y and y < 0.0 and running == 1:
            return -1.0

        old_vx = vx
        old_vy = vy
        speed = math.hypot(vx, vy)

        vy = vy - (g + coeff * speed * vy) * INTERVAL
        vx = vx - coeff * speed * vx * INTERVAL

        previous_y = y
        y += old_vy * INTERVAL
        displacement += old_vx * INTERVAL

    return displacement


def aproximate(p, c, a, m, k, u, h, g, decision, coordinateX, coordinateZ, strength):
    """Return candidate angle matches for the target displacement."""
    if decision != 1:
        raise ValueError("Only decision == 1 is supported in the optimised implementation.")

    target_distance = math.hypot(float(coordinateX), float(coordinateZ))
    band_extension = float(strength)
    matches = []

    for i in range(0, 45001):
        angle_deg = i / 500.0
        value = model(
            p,
            c,
            a,
            math.radians(angle_deg),
            m,
            k,
            band_extension,
            u,
            h,
            g,
        )
        if abs(value - target_distance) <= TOLERANCE:
            matches.append([value, angle_deg])

    return matches


def solve(coordinateX, coordinateZ, strength, displacement):
    """Solve for the required angle(s) for the target displacement."""
    h = float(displacement)
    solution = aproximate(P, C, A, M, K, U, h, G, 1, coordinateX, coordinateZ, strength)

    if not solution:
        return [0.0, 0.0]

    angles = [item[1] for item in solution]
    if len(angles) == 1:
        return [angles[0], 0.0]

    first_angle = angles[0]
    group_one = [angle for angle in angles if abs(angle - first_angle) <= 1.0]
    group_two = [angle for angle in angles if angle not in group_one]

    angle1 = sum(group_one) / len(group_one) if group_one else 0.0
    angle2 = sum(group_two) / len(group_two) if group_two else 0.0
    return [angle1, angle2]


if __name__ == "__main__":
    # Small example so the file can be executed directly.
    print(find_xzangle(3, 4))
    print(model(P, C, A, math.radians(30), M, K, 0.1, U, 0.0, G))
