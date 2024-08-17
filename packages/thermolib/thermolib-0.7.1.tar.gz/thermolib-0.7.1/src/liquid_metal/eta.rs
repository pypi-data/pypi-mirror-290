use super::{LiquidMetalErr, Metals};
use anyhow::anyhow;
use lazy_static::lazy_static;
use std::collections::HashMap;
#[allow(non_snake_case)]
pub struct EtaParams {
    Tmin: f64,
    Tmax: f64,
    a0: f64,
    a1: f64,
    eta0: f64,
}
#[allow(non_snake_case)]
impl EtaParams {
    pub fn calc(&self, T: f64) -> anyhow::Result<f64> {
        if T < self.Tmin {
            Err(anyhow!(LiquidMetalErr::TisTooMin))
        } else if T > self.Tmax {
            Err(anyhow!(LiquidMetalErr::TisTooMax))
        } else {
            Ok(10.0_f64.powf(self.a0 + self.a1 / T) * self.eta0)
        }
    }
}
lazy_static! {
    pub static ref METALS_TO_ETAPARAMS: HashMap<Metals, EtaParams> = HashMap::from([
        (
            Metals::Al,
            EtaParams {
                Tmin: 933.0,
                Tmax: 1270.0,
                a0: -0.7324,
                a1: 803.49,
                eta0: 1.0,
            },
        ),
        (
            Metals::Si,
            EtaParams {
                Tmin: 1685.0,
                Tmax: 1900.0,
                a0: -1.0881,
                a1: 1478.7,
                eta0: 1.0
            }
        ),
        (
            Metals::Fe,
            EtaParams {
                Tmin: 1809.0,
                Tmax: 2480.0,
                a0: -0.7209,
                a1: 2694.85,
                eta0: 1.0
            }
        ),
        (
            Metals::Co,
            EtaParams {
                Tmin: 1768.0,
                Tmax: 2100.0,
                a0: -0.903,
                a1: 2808.7,
                eta0: 1.0
            }
        ),
        (
            Metals::Ni,
            EtaParams {
                Tmin: 1728.0,
                Tmax: 2100.0,
                a0: -0.505,
                a1: 2108.2,
                eta0: 1.0
            }
        ),
        (
            Metals::Cu,
            EtaParams {
                Tmin: 1356.0,
                Tmax: 1970.0,
                a0: -0.422,
                a1: 1393.4,
                eta0: 1.0
            }
        ),
        (
            Metals::Zn,
            EtaParams {
                Tmin: 695.0,
                Tmax: 1100.0,
                a0: -0.3291,
                a1: 631.12,
                eta0: 1.0
            }
        ),
        (
            Metals::Ga,
            EtaParams {
                Tmin: 304.0,
                Tmax: 800.0,
                a0: -0.4465,
                a1: 204.03,
                eta0: 1.0
            }
        ),
        (
            Metals::Ag,
            EtaParams {
                Tmin: 1235.0,
                Tmax: 1500.0,
                a0: -0.258,
                a1: 1081.8,
                eta0: 1.0
            }
        ),
        (
            Metals::Cd,
            EtaParams {
                Tmin: 900.0,
                Tmax: 1300.0,
                a0: -0.4239,
                a1: 513.89,
                eta0: 1.0
            }
        ),
        (
            Metals::In,
            EtaParams {
                Tmin: 429.0,
                Tmax: 1000.0,
                a0: -0.3621,
                a1: 272.06,
                eta0: 1.0
            }
        ),
        (
            Metals::Sn,
            EtaParams {
                Tmin: 506.0,
                Tmax: 1280.0,
                a0: -0.408,
                a1: 343.4,
                eta0: 1.0
            }
        ),
        (
            Metals::Sb,
            EtaParams {
                Tmin: 900.0,
                Tmax: 1300.0,
                a0: -0.637,
                a1: 712.5,
                eta0: 1.0
            }
        ),
        (
            Metals::Hg,
            EtaParams {
                Tmin: 234.0,
                Tmax: 600.0,
                a0: -0.2561,
                a1: 132.29,
                eta0: 1.0
            }
        ),
        (
            Metals::Tl,
            EtaParams {
                Tmin: 577.0,
                Tmax: 800.0,
                a0: -0.3017,
                a1: 412.84,
                eta0: 1.0
            }
        ),
        (
            Metals::Pb,
            EtaParams {
                Tmin: 601.0,
                Tmax: 1400.0,
                a0: -0.295,
                a1: 427.1,
                eta0: 1.0
            }
        ),
        (
            Metals::Bi,
            EtaParams {
                Tmin: 545.0,
                Tmax: 1000.0,
                a0: -0.345,
                a1: 321.4,
                eta0: 1.0
            }
        )
    ]);
}
