import xarray as xr


class Simulation:
    def __init__(
        self, CWP, CF, NCCN, albedo, albd_clear, SOLIN, sw_dwn_profile=None, inv_idx=None
    ):
        self.quantities = self.Quantities(
            CWP, CF, NCCN, albedo, albd_clear, SOLIN, sw_dwn_profile, inv_idx
        )
        self.calc = self.Calculations(self.quantities)

    class Calculations:
        def __init__(self, quantities):
            self.q = quantities

        def cloud_albedo(self):
            # Calculate the cloud albedo (A2)
            self.q.cloud_albedo = (
                self.q.albedo - (1 - self.q.CF) * self.q.albd_clear
            ) / self.q.CF

        def free_trop_transmissivity(self):
            if self.q.inv_idx is not None:
                self.q.ft_transmissivity = self.q.sw_dwn_profile / self.q.SOLIN
            else:
                self.q.ft_transmissivity = 0.8

        def scene_albedo(self, a_ft=0.05):
            """a_ft = albedo free troposphere."""
            if self.q.ft_transmissivity is None:
                self.free_trop_transmissivity()
            T_ft = self.q.ft_transmissivity
            self.q.scene_albedo = (self.q.cloud_albedo - a_ft) / (
                T_ft**2 + self.q.cloud_albedo * a_ft - a_ft**2
            )

        def cre(self, level="cloud_layer", a_ft=0.05):
            """Calculation of cloud radiative effect (CRE)

            level : str
                cloud_layer: remove free-tropospheric effect with simple approx.
                toa: cloud radiative effect measured at top-of-atmosphere
            """
            if level == "cloud_layer":
                if self.q.scene_albedo is None:
                    self.scene_albedo(a_ft=a_ft)
                cre = -self.q.scene_albedo * self.q.SOLIN * self.q.CF
            elif level == "toa":
                cre = (
                    -1
                    * (self.q.cloud_albedo - self.q.albd_clear)
                    * self.q.SOLIN
                    * (self.q.CF)
                )
            return cre

    class Quantities:
        def __init__(
            self, CWP, CF, NCCN, albedo, albd_clear, SOLIN, sw_dwn_profile, inv_idx
        ):
            self.CWP = CWP
            self.CF = CF
            self.albedo = albedo
            self.albd_clear = albd_clear
            self.NCCN = NCCN
            self.SOLIN = SOLIN
            self.sw_dwn_profile = sw_dwn_profile
            self.inv_idx = inv_idx
            self.cloud_albedo = None
            self.ft_transmissivity = None
            self.scene_albedo = None
            self.cre = None


class CRE_Decompositer:
    def __init__(self, simulation1, simulation2):
        self.simulation1 = simulation1
        self.simulation2 = simulation2
        self.cre_scaling = True
        self.cloud_cre_change = None

    def cre_change(self, factor, cre_scaling=False):
        if self.simulation1.quantities.cre is None:
            self.simulation1.quantities.cre = self.simulation1.calc.cre()
        if self.simulation2.quantities.cre is None:
            self.simulation2.quantities.cre = self.simulation2.calc.cre()
        if cre_scaling:
            cre_direct = self.simulation1.calc.cre(level="toa")
            scale = cre_direct / self.simulation1.quantities.cre
            self.cre_scaling = scale
            self.simulation1.quantities.cre *= scale
            self.simulation2.quantities.cre *= scale
        self.CRE_change = factor * (
            self.simulation2.quantities.cre - self.simulation1.quantities.cre
        )

    def albedo_change(self):
        self.alb_change = (
            self.simulation2.quantities.cloud_albedo
            - self.simulation1.quantities.cloud_albedo
        )

    def cre_cloud_change(self, factor=-1):
        """CRE change due to changes in cloud properties.

        This is a more direct way to calculate the CRE change due to
        changes in cloud properties and should ideally match the sum of
        CRE changes due to LWP adjustment and twomey effect.
        """
        s1 = self.simulation1.quantities
        s2 = self.simulation2.quantities
        if self.cloud_cre_change is None:
            self.albedo_change()
        self.cloud_cre_change = factor * self.alb_change * s2.SOLIN * s1.CF

    def _integral(self, factor, albedo, x, sign=-1):
        a = albedo + sign * albedo * (1 - albedo) * (x ** (factor) - 1) / (
            1 + albedo * (x**factor - 1)
        )
        return a

    def _single_layer_model(self, Acld, alb, T):
        alpha = alb + (Acld * T**2) / (1 - alb * Acld)
        return alpha

    def twomey_effect(self, factor=-1, a_ft=0.05):
        s1 = self.simulation1.quantities
        s2 = self.simulation2.quantities
        rN = s2.NCCN / s1.NCCN  # .max(dim='height') / s1.NCCN.max(dim='height')
        self.twomey_rN = rN
        self.twomey_cld_albedo_change = self._integral(
            factor=1 / 3, albedo=s1.scene_albedo, x=rN, sign=factor
        )
        self.twomey_scene_albedo_change = self._single_layer_model(
            alb=a_ft, Acld=self.twomey_cld_albedo_change, T=s1.ft_transmissivity
        )
        self.twomey_cre_change = (
            -(self.twomey_scene_albedo_change - s1.cloud_albedo)
            * s2.SOLIN
            * s1.CF
            * self.cre_scaling
        )

    def LWP_adjustment(self, factor=-1, a_ft=0.05):
        s1 = self.simulation1.quantities
        s2 = self.simulation2.quantities
        rL = s2.CWP / s1.CWP
        self.LWP_rL = rL
        self.LWP_cld_albedo_change = self._integral(
            factor=5 / 6, albedo=s1.scene_albedo, x=rL, sign=factor
        )
        self.LWP_scene_albedo_change = self._single_layer_model(
            alb=a_ft, Acld=self.LWP_cld_albedo_change, T=s1.ft_transmissivity
        )
        self.LWP_cre_change = (
            -(self.LWP_scene_albedo_change - s1.cloud_albedo)
            * s2.SOLIN
            * s1.CF
            * self.cre_scaling
        )

    def CF_adjustment(self, factor=-1):
        s1 = self.simulation1.quantities
        s2 = self.simulation2.quantities
        A_CF = self.twomey_scene_albedo_change.copy()
        for i in range(len(s1.CF)):
            if (
                s2.CF[i] > s1.CF[i]
            ):  # what is the reasoning behind this? depending on the run with the higher cloud fraction, the albedo change to its reference is used. Works if clear-sky fluxes are available in cloudy columns.
                A_CF[i] = s1.cloud_albedo[i] + (s2.CF[i] - s1.CF[i]) * (
                    s2.cloud_albedo[i] - s2.albd_clear[i]
                )
            else:
                A_CF[i] = s1.cloud_albedo[i] + (s2.CF[i] - s1.CF[i]) * (
                    s1.cloud_albedo[i] - s1.albd_clear[i]
                )  # A1 gets added

        self.CF_albedo_change = A_CF
        self.CF_cre_change = (
            factor * (A_CF - s1.cloud_albedo) * s2.SOLIN * -1 * self.cre_scaling
        )

    def decompose(self, factor=-1, a_ft=0.05, cre_scaling=False):
        self.simulation1.calc.cloud_albedo()
        self.simulation2.calc.cloud_albedo()
        self.simulation1.calc.scene_albedo()
        self.simulation2.calc.scene_albedo()
        self.simulation1.quantities.cre = self.simulation1.calc.cre()
        self.simulation2.quantities.cre = self.simulation2.calc.cre()
        self.cre_change(factor=factor, cre_scaling=cre_scaling)
        self.albedo_change()
        self.cre_cloud_change(factor=factor)
        self.twomey_effect(factor=factor, a_ft=a_ft)
        self.LWP_adjustment(factor=factor, a_ft=a_ft)
        self.CF_adjustment(factor=factor)

        self.A_rs = (
            self.twomey_scene_albedo_change
            + self.LWP_scene_albedo_change
            + self.CF_albedo_change
            - self.alb_change
        )
        self.CRE_rs = (
            self.twomey_cre_change
            + self.LWP_cre_change
            + self.CF_cre_change
            - self.CRE_change
        )

        self.rC = self.simulation2.quantities.CF / self.simulation1.quantities.CF

    def to_dataset(self):
        """Return decomposition as dataset."""
        ds_cre = xr.Dataset(
            {
                "dCRE_total": self.CRE_change,
                "dCRE_CF": self.CF_cre_change,
                "dCRE_cloud": self.cloud_cre_change,
                "dCRE_CDNC": self.twomey_cre_change,
                "dCRE_LWP": self.LWP_cre_change,
                "dCRE_rs": self.CRE_rs,
            }
        )
        ds_alb = xr.Dataset(
            {
                "dA_total": self.alb_change,
                "dA_CF": self.CF_albedo_change,
                "dA_CDNC": self.twomey_scene_albedo_change,
                "dA_LWP": self.LWP_scene_albedo_change,
                "dA_rs": self.A_rs,
            }
        )
        ds_sim1 = xr.Dataset({"A_cloud_sim1": self.simulation1.quantities.cloud_albedo})
        ds_sim2 = xr.Dataset({"A_cloud_sim2": self.simulation2.quantities.cloud_albedo})
        ds = xr.merge([ds_cre, ds_alb, ds_sim1, ds_sim2])
        return ds

    def return_erfani_2022(self, otype="tuple"):
        """Matching return of quant_CRE_alltime."""
        if otype == "tuple":
            return (
                self.twomey_rN,
                self.LWP_rL,
                self.rC,
                self.CRE_change,
                self.twomey_cre_change,
                self.LWP_cre_change,
                self.CF_cre_change,
                self.CRE_rs,
                self.simulation1.quantities.cloud_albedo,
                self.twomey_scene_albedo_change,
                self.LWP_scene_albedo_change,
                self.CF_albedo_change,
                self.A_rs,
                self.simulation1.quantities.cre,
                self.simulation2.quantities.cre,
                self.simulation1.quantities.CF,
            )
        elif otype == "dict":
            return {
                "rN": self.twomey_rN,
                "rL": self.LWP_rL,
                "rC": self.rC,
                "CRE_M": self.CRE_change,
                "CRE_T": self.twomey_cre_change,
                "CRE_L": self.LWP_cre_change,
                "CRE_CF": self.CF_cre_change,
                "CRE_rs": self.CRE_rs,
                "A1": self.simulation1.quantities.cloud_albedo,
                "A_T": self.twomey_scene_albedo_change,
                "A_L": self.LWP_scene_albedo_change,
                "A_CF": self.CF_albedo_change,
                "A_rs": self.A_rs,
                "CRE1": self.simulation1.quantities.cre,
                "CRE2": self.simulation2.quantities.cre,
                "CF1": self.simulation1.quantities.CF,
            }
