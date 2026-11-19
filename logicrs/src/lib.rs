use pyo3::prelude::*;

#[pymodule]
mod logicrs {
    use std::f64::consts::PI;
    use std::thread;

    use pyo3::prelude::*;

    const P: f64 = 1.225;
    const A: f64 = 0.0025;
    const M: f64 = 0.2;
    const K: f64 = 12000.0;
    const U: f64 = 0.3;
    const G: f64 = 9.80665;
    const TOLERANCE: f64 = 0.01;
    const ANGLE_ACCURACY: f64 = 0.005;
    const INTERVAL: f64 = 0.0005;
    const SPRING_INTERVAL: f64 = 0.000003;
    const M_NEST: f64 = 0.01;
    const M_SPRING: f64 = 0.1;
    /// Mass acted on by gravity during launch (half the spring's mass counts).
    const M_GRAV: f64 = M_NEST + M_SPRING / 2.0 + M;
    /// Effective mass being accelerated by the spring (a third of the spring's mass counts).
    const M_EFF: f64 = M_NEST + M_SPRING / 3.0 + M;
    const AIR_VISCOSITY: f64 = 1.81e-5;

    fn radius() -> f64 {
        (A / (2.0 * PI)).sqrt()
    }

    fn drag_coefficient(speed: f64) -> f64 {
        if speed <= 10.0 {
            return 0.47;
        }
        let re = P * speed * 2.0 * radius() / AIR_VISCOSITY;
        24.0 / re
            + (2.6 * (re / 5.0)) / (1.0 + (re / 5.0).powf(1.52))
            + (0.411 * (re / 2.63e5).powf(-7.94)) / (1.0 + (re / 2.63e5).powf(-8.0))
            + (0.25 * (re / 1e6)) / (1.0 + re / 1e6)
    }

    /// Horizontal distance travelled when launched at angle `a` (radians) with spring
    /// extension `x` from height `h`. Returns 0 if a projectile starting below the target
    /// height starts falling before reaching it.
    fn model(a: f64, mut x: f64, h: f64) -> f64 {
        let (sin_a, cos_a) = a.sin_cos();

        let mut v = 0.0;
        while x >= 0.0 {
            let v0 = v;
            let force = K * x
                - M_GRAV * G * sin_a
                - M * G * cos_a * U
                - 0.5 * P * v * v * drag_coefficient(v) * A;
            v += force / M_EFF * SPRING_INTERVAL;
            x -= (v + v0) / 2.0 * SPRING_INTERVAL;
        }

        let mut vx = v * cos_a;
        let mut vy = v * sin_a;
        let mut y = h;
        let mut s = 0.0;
        let mut below_start = y < 0.0;

        while y >= 0.0 || below_start {
            let (vx0, vy0, y0) = (vx, vy, y);
            let speed = (vx * vx + vy * vy).sqrt();
            let drag = P * drag_coefficient(speed) * A / (2.0 * M);
            vy += (-G - drag * speed * vy) * INTERVAL;
            // Uses the already-updated vy, matching logic.py.
            vx += -drag * (vx * vx + vy * vy).sqrt() * vx * INTERVAL;
            s += (vx + vx0) / 2.0 * INTERVAL;
            y += (vy + vy0) / 2.0 * INTERVAL;

            if below_start {
                if y < y0 {
                    return 0.0;
                }
                if y >= 0.0 {
                    below_start = false;
                }
            }
        }

        s
    }

    /// Angles (degrees), ascending, whose landing distance is within TOLERANCE of the target.
    /// Angles are striped across threads since high angles take longer to simulate.
    fn approximate(coordinate_x: f64, coordinate_z: f64, strength: f64, h: f64) -> Vec<f64> {
        let target = (coordinate_x * coordinate_x + coordinate_z * coordinate_z).sqrt();
        let steps = (90.0 / ANGLE_ACCURACY + 1.0) as usize;
        let threads = thread::available_parallelism().map_or(1, |n| n.get());

        let mut hits: Vec<usize> = thread::scope(|scope| {
            let workers: Vec<_> = (0..threads)
                .map(|t| {
                    scope.spawn(move || {
                        (t..steps)
                            .step_by(threads)
                            .filter(|&i| {
                                let angle = i as f64 * ANGLE_ACCURACY;
                                (model(angle.to_radians(), strength, h) - target).abs() <= TOLERANCE
                            })
                            .collect::<Vec<_>>()
                    })
                })
                .collect();
            workers.into_iter().flat_map(|w| w.join().unwrap()).collect()
        });
        hits.sort_unstable();
        hits.into_iter().map(|i| i as f64 * ANGLE_ACCURACY).collect()
    }

    #[pyfunction]
    fn find_xzangle(x: f64, z: f64) -> f64 {
        z.atan2(x).to_degrees().rem_euclid(360.0)
    }

    /// Returns the two candidate launch angles: the mean of the solutions within 1 degree of
    /// the first, and the mean of the rest. Either is 0 if it has no solutions.
    #[pyfunction]
    fn solve(py: Python<'_>, x: f64, z: f64, strength: f64, displacement: f64) -> Vec<f64> {
        let angles = py.detach(|| approximate(x, z, strength, displacement));
        let Some(&first) = angles.first() else {
            return vec![0.0, 0.0];
        };

        let (near, far): (Vec<f64>, Vec<f64>) =
            angles.into_iter().partition(|angle| (first - angle).abs() <= 1.0);
        let mean = |v: &[f64]| if v.is_empty() { 0.0 } else { v.iter().sum::<f64>() / v.len() as f64 };

        vec![mean(&near), mean(&far)]
    }
}
