use pyo3::prelude::*;

#[pymodule]
mod logicrs {
    use pyo3::prelude::*;

    const INTERVAL: f64 = 0.001;
    const P: f64 = 1.225;
    const C: f64 = 0.4;
    const A: f64 = 0.0025;
    const M: f64 = 0.4;
    const K: f64 = 12000.0;
    const U: f64 = 0.3;
    const G: f64 = 9.80665;
    const TOLERANCE: f64 = 0.001;

    fn model(p: f64, c: f64, a_value: f64, a: f64, m: f64, k: f64, x: f64, u: f64, h: f64, g: f64) -> f64 {
        let spring_interval = 0.0001;
        let mut s = 0.0;
        let mut v0 = 0.0;
        let mut y = h;
        let mut x_value = x;

        while x_value >= 0.0 {
            let acceleration = |extension: f64, velocity: f64| {
                (
                    k * extension
                    - m * u * g * a.cos()
                    - 0.5 * p * c * a_value * velocity * velocity
                    - m * g * a.sin()
                ) / m
            };

            let a1 = acceleration(x_value, v0);
            let x_mid = x_value - 0.5 * v0 * spring_interval;
            let v_mid = v0 + 0.5 * a1 * spring_interval;
            let a_mid = acceleration(x_mid, v_mid);
            let x_new = x_value - v_mid * spring_interval;
            let v_new = v0 + a_mid * spring_interval;

            if x_new <= 0.0 {
                let fraction = x_value / (x_value - x_new);
                v0 += fraction * (v_new - v0);
                break;
            }

            x_value = x_new;
            v0 = v_new;
        }

        let mut vx = v0 * a.cos();
        let mut vy = v0 * a.sin();
        let mut run = if h > 0.0 { 0 } else { 1 };
        let mut l = y;

        while y >= 0.0 || run != 0 {
            if y >= 0.0 && h <= 0.0 && run == 1 {
                run = 0;
            }

            if y < l && y < 0.0 && run == 1 {
                return -1.0;
            }

            let b = vy;
            let d = vx;
            let speed = (vx * vx + vy * vy).sqrt();
            let coeff = (p * c * a_value) / (2.0 * m);

            vy = (-g - coeff * speed * vy) * INTERVAL + vy;
            vx = (-coeff * speed * vx) * INTERVAL + vx;
            l = y;
            y = b * INTERVAL + y;
            s = d * INTERVAL + s;
        }

        s
    }

    fn approximate(
        p: f64,
        c: f64,
        a_value: f64,
        m: f64,
        k: f64,
        u: f64,
        h: f64,
        g: f64,
        coordinate_x: f64,
        coordinate_z: f64,
        strength: f64,
    ) -> Vec<Vec<f64>> {
        
        let mut list = Vec::new();
        let x = strength;
        let displacement = (coordinate_x * coordinate_x + coordinate_z * coordinate_z).sqrt();

        for i in 0..=45000 {
            let angle = i as f64 / 500.0;
            let value = model(p, c, a_value, angle.to_radians(), m, k, x, u, h, g);

            if (value - displacement).abs() <= TOLERANCE {
                let mut values2 = Vec::new();
                values2.push(value);
                values2.push(angle);
                list.push(values2);
            }
        }

        list
    }

    #[pyfunction]
    fn find_xzangle(x: f64, z: f64) -> PyResult<f64> {
        let mut angle = z.atan2(x).to_degrees();
        if angle < 0.0 {
            angle += 360.0;
        }
        Ok(angle)
    }

    #[pyfunction]
    fn solve(x: f64, z: f64, strength: f64, displacement: f64) -> PyResult<Vec<f64>> {
        let h = displacement;
        let solution = approximate(P, C, A, M, K, U, h, G, x, z, strength);

        if solution.is_empty() {
            return Ok(vec![0.0, 0.0]);
        }

        let mut t1 = 0.0;
        let mut n1 = 0usize;
        let mut t2 = 0.0;
        let mut n2 = 0usize;

        for item in &solution {
            let angle = item[1];
            if (solution[0][1] - angle).abs() <= 1.0 {
                t1 += angle;
                n1 += 1;
            } else {
                t2 += angle;
                n2 += 1;
            }
        }

        let mut angle1 = 0.0;
        let mut angle2 = 0.0;

        if n1 != 0 {
            angle1 = t1 / n1 as f64;
        }
        if n2 != 0 {
            angle2 = t2 / n2 as f64;
        }

        Ok(vec![angle1, angle2])
    }
}

