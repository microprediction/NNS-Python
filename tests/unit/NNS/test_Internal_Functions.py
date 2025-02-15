# -*- coding: utf-8 -*-
import unittest
from collections import namedtuple

import pandas as pd
import pandas.util.testing as pd_test
import numpy as np
import NNS.Internal_Functions


class TestInternalFunctions(unittest.TestCase):
    COMPARISON_PRECISION = 7

    def assertAlmostEqualArray(
        self,
        x: [pd.Series, np.ndarray, list, dict],
        y: [pd.Series, np.ndarray, list, dict],
        places: int = 7,
    ) -> None:
        self.assertEqual(len(x), len(y))
        if isinstance(x, dict):
            for i in x.keys():
                self.assertAlmostEqual(x[i], y[i], places)
        else:
            for i in range(len(x)):
                self.assertAlmostEqual(x[i], y[i], places)

    def test_bw_nrd0(self):
        nt = namedtuple("Test", "dataset")
        x = nt(dataset=self.load_default_data()["x"].values)
        x1 = nt(dataset=self.load_default_data()["x"].values[0:10])
        x2 = nt(dataset=self.load_default_data()["x"].values[10:20])
        x3 = nt(dataset=self.load_default_data()["x"].values[20:30])
        # should work with numpy 1.22.0rc3+
        self.assertAlmostEqual(NNS.Internal_Functions.bw_nrd0(x), 0.08836202, places=5)
        self.assertAlmostEqual(NNS.Internal_Functions.bw_nrd0(x1), 0.1244611, places=5)
        self.assertAlmostEqual(NNS.Internal_Functions.bw_nrd0(x2), 0.1302972, places=5)
        self.assertAlmostEqual(NNS.Internal_Functions.bw_nrd0(x3), 0.1229566, places=5)

    def test_fivenum(self):
        x = self.load_default_data()["x"]
        self.assertAlmostEqualArray(
            NNS.Internal_Functions.fivenum(x),
            [0.01612921, 0.31802595, 0.50612951, 0.69183605, 0.99535848],
            places=3,
        )

    def test_mode(self):
        x = self.load_default_data()["x"]
        x1 = x[0:10]
        x2 = x[10:20]
        x3 = x[20:30]
        self.assertAlmostEqual(NNS.Internal_Functions.mode(x), 0.6175456, delta=0.002)
        self.assertAlmostEqual(NNS.Internal_Functions.mode(x1), 0.4643043, delta=0.001)
        self.assertAlmostEqual(NNS.Internal_Functions.mode(x2), 0.4388948, delta=0.001)
        self.assertAlmostEqual(NNS.Internal_Functions.mode(x3), 0.6733525, delta=0.002)

    def test_mode_class(self):
        x = self.load_default_data()["x"]
        y = np.array([1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])
        y2 = y[::-1]
        self.assertAlmostEqual(NNS.Internal_Functions.mode_class(x), 0.6964692, places=3)
        self.assertAlmostEqual(NNS.Internal_Functions.mode_class(y), 1, places=2)
        self.assertAlmostEqual(NNS.Internal_Functions.mode_class(y2), 1, places=2)

    def test_gravity(self):
        x = self.load_default_data()["x"]
        x1 = x[0:10]
        x2 = x[10:20]
        x3 = x[20:30]
        self.assertAlmostEqual(NNS.Internal_Functions.gravity(x), 0.5430019, delta=0.002)
        self.assertAlmostEqual(NNS.Internal_Functions.gravity(x1), 0.5051103, delta=0.004)
        self.assertAlmostEqual(
            NNS.Internal_Functions.gravity(x2), 0.4115818, delta=0.013
        )  # TODO: Get a better precision (mode fuction)
        self.assertAlmostEqual(
            NNS.Internal_Functions.gravity(x3), 0.6166066, delta=0.006
        )  # TODO: Get a better precision (mode fuction)

    def test_gravity_class(self):
        x = self.load_default_data()["x"]
        x1 = x[0:10]
        x2 = x[10:20]
        x3 = x[20:30]
        self.assertAlmostEqual(NNS.Internal_Functions.gravity_class(x), 0.5033797, delta=0.001)
        self.assertAlmostEqual(NNS.Internal_Functions.gravity_class(x1), 0.5395513, delta=0.001)
        self.assertAlmostEqual(
            NNS.Internal_Functions.gravity_class(x2), 0.404214, delta=0.010
        )  # TODO: Get a better precision (mode fuction)
        self.assertAlmostEqual(
            NNS.Internal_Functions.gravity_class(x3), 0.5406646, delta=0.007
        )  # TODO: Get a better precision (mode fuction)

    def test_alt_cbind(self):
        x = pd.Series([1.0, 2], name="x")
        y = pd.Series([1.0, 2, 3, 4, 5], name="y")
        pd_test.assert_frame_equal(
            NNS.Internal_Functions.alt_cbind(x, y),
            pd.DataFrame(
                {
                    "x": [1.0, 2, 1, 2, 1],
                    "y": [1.0, 2, 3, 4, 5],
                }
            ),
        )
        pd_test.assert_frame_equal(
            NNS.Internal_Functions.alt_cbind(y, x),
            pd.DataFrame(
                {
                    "y": [1.0, 2, 3, 4, 5],
                    "x": [1.0, 2, 1, 2, 1],
                }
            ),
        )
        pd_test.assert_frame_equal(
            NNS.Internal_Functions.alt_cbind(x.values, y.values),
            pd.DataFrame(
                {
                    0: [1.0, 2, 1, 2, 1],
                    1: [1.0, 2, 3, 4, 5],
                }
            ),
        )
        pd_test.assert_frame_equal(
            NNS.Internal_Functions.alt_cbind(y.values, x.values),
            pd.DataFrame(
                {
                    0: [1.0, 2, 3, 4, 5],
                    1: [1.0, 2, 1, 2, 1],
                }
            ),
        )

    def test_factor_2_dummy(self):
        x = pd.Series([1, 1, 1, 2, 2, 3, 3, 3], dtype="category")
        y_full = pd.DataFrame(
            {
                1: [1, 1, 1, 0, 0, 0, 0, 0],
                2: [0, 0, 0, 1, 1, 0, 0, 0],
                3: [0, 0, 0, 0, 0, 1, 1, 1],
            }
        )
        y_full.columns = y_full.columns.astype("category")
        y_full[1] = y_full[1].astype(np.uint8)
        y_full[2] = y_full[2].astype(np.uint8)
        y_full[3] = y_full[3].astype(np.uint8)

        pd_test.assert_frame_equal(NNS.Internal_Functions.factor_2_dummy(x), y_full.iloc[:, 1:])
        pd_test.assert_series_equal(
            NNS.Internal_Functions.factor_2_dummy(x.astype(int)), x.astype(float)
        )

    def test_factor_2_dummy_FR(self):
        x = pd.Series([1, 1, 1, 2, 2, 3, 3, 3], dtype="category")
        y_full = pd.DataFrame(
            {
                1: [1, 1, 1, 0, 0, 0, 0, 0],
                2: [0, 0, 0, 1, 1, 0, 0, 0],
                3: [0, 0, 0, 0, 0, 1, 1, 1],
            }
        )
        y_full.columns = y_full.columns.astype("category")
        y_full[1] = y_full[1].astype(np.uint8)
        y_full[2] = y_full[2].astype(np.uint8)
        y_full[3] = y_full[3].astype(np.uint8)

        pd_test.assert_frame_equal(NNS.Internal_Functions.factor_2_dummy_FR(x), y_full)
        pd_test.assert_series_equal(
            NNS.Internal_Functions.factor_2_dummy_FR(x.astype(int)), x.astype(float)
        )

    def test_generate_vectors(self):
        x = np.arange(1, 101)
        y = {
            "Component.index": {
                "Index.1": np.array(
                    [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                        26,
                        27,
                        28,
                        29,
                        30,
                        31,
                        32,
                        33,
                    ]
                ),
                "Index.2": np.array(
                    [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                    ]
                ),
            },
            "Component.series": {
                "Series.1": np.array(
                    [
                        2,
                        5,
                        8,
                        11,
                        14,
                        17,
                        20,
                        23,
                        26,
                        29,
                        32,
                        35,
                        38,
                        41,
                        44,
                        47,
                        50,
                        53,
                        56,
                        59,
                        62,
                        65,
                        68,
                        71,
                        74,
                        77,
                        80,
                        83,
                        86,
                        89,
                        92,
                        95,
                        98,
                    ]
                ),
                "Series.2": np.array(
                    [
                        1,
                        5,
                        9,
                        13,
                        17,
                        21,
                        25,
                        29,
                        33,
                        37,
                        41,
                        45,
                        49,
                        53,
                        57,
                        61,
                        65,
                        69,
                        73,
                        77,
                        81,
                        85,
                        89,
                        93,
                        97,
                    ]
                ),
            },
        }
        y1 = NNS.Internal_Functions.generate_vectors(x, [3, 4])

        self.assertTrue(isinstance(y1, dict))
        self.assertTrue(len(y1) == 2)
        self.assertTrue("Component.index" in y1)
        self.assertTrue("Component.series" in y1)

        for v in ["Component.index", "Component.series"]:
            self.assertTrue(v in y1)
            self.assertTrue(v in y)
            self.assertTrue(len(y1[v]) == len(y[v]))
            for i in y1[v]:
                self.assertAlmostEqualArray(
                    y[v][i],
                    y1[v][i],
                )
            for i in y[v]:
                self.assertAlmostEqualArray(
                    y[v][i],
                    y1[v][i],
                )

    def test_ARMA_seas_weighting(self):
        x = {
            "all.periods": pd.DataFrame(
                {
                    "Period": [
                        50,
                        37,
                        25,
                        49,
                        11,
                        31,
                        51,
                        22,
                        23,
                        52,
                        48,
                        9,
                        21,
                        18,
                        12,
                        6,
                        30,
                        10,
                    ],
                    "Coefficient.of.Variation": [
                        0.3023024,
                        0.3363729,
                        0.3399940,
                        0.3409024,
                        0.3603019,
                        0.3708753,
                        0.3766443,
                        0.3858888,
                        0.3939718,
                        0.3984879,
                        0.4002249,
                        0.4014819,
                        0.4019060,
                        0.4041052,
                        0.4059923,
                        0.4112121,
                        0.4200857,
                        0.4241736,
                    ],
                    "Variable.Coefficient.of.Variation": [
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                        0.4279947,
                    ],
                }
            ),
            "best.period": 50,
            "periods": [50, 37, 25, 49, 11, 31, 51, 22, 23, 52, 48, 9, 21, 18, 12, 6, 30, 10],
        }
        y_false = {"lag": x["all.periods"]["Period"], "Weights": 1}
        y_true = {"lag": 50, "Weights": 1}
        y1 = NNS.Internal_Functions.ARMA_seas_weighting(False, x)
        y2 = NNS.Internal_Functions.ARMA_seas_weighting(True, x)
        self.assertDictEqual(y_false, y1)
        self.assertDictEqual(y_true, y2)

    def test_lag_mtx(self):
        pass

    def test_RP(self):
        pass

    def test_NNS_meboot_part(self):
        pass

    def test_NNS_meboot_expand_sd(self):
        pass

    def load_default_data(self):
        # R Code:
        # x <- c(0.6964691855978616, 0.28613933495037946, 0.2268514535642031, 0.5513147690828912, 0.7194689697855631, 0.42310646012446096, 0.9807641983846155, 0.6848297385848633, 0.48093190148436094, 0.3921175181941505, 0.3431780161508694, 0.7290497073840416, 0.4385722446796244, 0.05967789660956835, 0.3980442553304314, 0.7379954057320357, 0.18249173045349998, 0.17545175614749253, 0.5315513738418384, 0.5318275870968661, 0.6344009585513211, 0.8494317940777896, 0.7244553248606352, 0.6110235106775829, 0.7224433825702216, 0.3229589138531782, 0.3617886556223141, 0.22826323087895561, 0.29371404638882936, 0.6309761238544878, 0.09210493994507518, 0.43370117267952824, 0.4308627633296438, 0.4936850976503062, 0.425830290295828, 0.3122612229724653, 0.4263513069628082, 0.8933891631171348, 0.9441600182038796, 0.5018366758843366, 0.6239529517921112, 0.11561839507929572, 0.3172854818203209, 0.4148262119536318, 0.8663091578833659, 0.2504553653965067, 0.48303426426270435, 0.985559785610705, 0.5194851192598093, 0.6128945257629677, 0.12062866599032374, 0.8263408005068332, 0.6030601284109274, 0.5450680064664649, 0.3427638337743084, 0.3041207890271841, 0.4170222110247016, 0.6813007657927966, 0.8754568417951749, 0.5104223374780111, 0.6693137829622723, 0.5859365525622129, 0.6249035020955999, 0.6746890509878248, 0.8423424376202573, 0.08319498833243877, 0.7636828414433382, 0.243666374536874, 0.19422296057877086, 0.5724569574914731, 0.09571251661238711, 0.8853268262751396, 0.6272489720512687, 0.7234163581899548, 0.01612920669501683, 0.5944318794450425, 0.5567851923942887, 0.15895964414472274, 0.1530705151247731, 0.6955295287709109, 0.31876642638187636, 0.6919702955318197, 0.5543832497177721, 0.3889505741231446, 0.9251324896139861, 0.8416699969127163, 0.35739756668317624, 0.04359146379904055, 0.30476807341109746, 0.398185681917981, 0.7049588304513622, 0.9953584820340174, 0.35591486571745956, 0.7625478137854338, 0.5931769165622212, 0.6917017987001771, 0.15112745234808023, 0.39887629272615654, 0.24085589772362448, 0.34345601404832493)
        # y <- c(0.9290953494701337, 0.3001447577944899, 0.20646816984143224, 0.7712467017344186, 0.179207683251417, 0.7203696347073341, 0.2978651188274144, 0.6843301478774432, 0.6020774780838681, 0.8762070150459621, 0.7616916032270227, 0.6492402854114879, 0.3486146126960078, 0.5308900543442001, 0.31884300700035195, 0.6911215594221642, 0.7845248814489976, 0.8626202294885787, 0.4135895282244193, 0.8672153808700541, 0.8063467153755893, 0.7473209976914339, 0.08726848196743031, 0.023957638562143946, 0.050611236457549946, 0.4663642370285497, 0.4223981453920743, 0.474489623129292, 0.534186315014437, 0.7809131772951494, 0.8198754325768683, 0.7111791151322316, 0.49975889646204175, 0.5018097125708618, 0.7991356578408818, 0.03560152015693441, 0.921601798248779, 0.2733414160633679, 0.7824828518318679, 0.395582605302746, 0.48270235978971854, 0.5931259692926043, 0.2731798106977692, 0.8570159493264954, 0.5319561444631024, 0.1455315278392807, 0.6755524321238062, 0.27625359167650576, 0.2723010177649897, 0.6810977486565571, 0.9493047259244862, 0.807623816061548, 0.9451528088524095, 0.6402025296719795, 0.8258783277528565, 0.6300644920352498, 0.3893090155420259, 0.24163970305689175, 0.18402759570852467, 0.6031603131688895, 0.6566703304734626, 0.21177484928830181, 0.4359435889362071, 0.22965129132316398, 0.13087653733774363, 0.5989734941782344, 0.6688357426448118, 0.8093723729154483, 0.36209409565006223, 0.8513351315065957, 0.6551606487241549, 0.8554790691017261, 0.13596214615618918, 0.10883347378170816, 0.5448015917555307, 0.8728114143337533, 0.6621652225678912, 0.8701363950944805, 0.8453249339337617, 0.6283199211390311, 0.20690841095962864, 0.5176511518958, 0.6448515562981659, 0.42666354124364536, 0.9718610781333566, 0.24973274985042482, 0.05193778223157797, 0.6469719787522865, 0.3698392148054457, 0.8167218997483684, 0.710280810455504, 0.260673487453131, 0.4218711567383805, 0.793490082297006, 0.9398115107412777, 0.7625379749026492, 0.039750173274282985, 0.040137387046519146, 0.16805410857991787, 0.78433600580123)
        # z <- c(0.19999193561416084,0.6010279101158327,0.9788327513669298,0.8608964619298911,0.7601684508905298,0.12397506746787612,0.5394401401912896,0.8969279890952392,0.3839893553453263,0.5974293052436022,0.06516937735345008,0.15292545930437007,0.533669687225804,0.5430715864428796,0.8676197246411066,0.9298956526581725,0.6460088459791522,0.006548180072424414,0.6025139026895475,0.36841377074834125,0.44801794989436194,0.5048619249681798,0.4000809850582463,0.763740516980946,0.34083865579228434,0.5424284677884146,0.9587984735763967,0.5859672618993342,0.8422555318312421,0.5153219248350965,0.8358609378832195,0.787997995901579,0.2741451405223151,0.6444057500854898,0.02596405447571548,0.2797463018215405,0.10295252828980817,0.4354164588706081,0.26211152577662666,0.6998708543101617,0.37283691796585705,0.3227717548199931,0.1370286323274963,0.8070990185408966,0.7360223497043797,0.34991170542178995,0.9307716779643572,0.8134995545754865,0.32999762541477007,0.7009778150431946,0.9592132203954723,0.285109164298465,0.005404210183425628,0.7840965908154933,0.6534845192821737,0.22306404635944888,0.5599264352651063,0.9126415066887666,0.20749150526588522,0.769668024293192,0.7563728166813091,0.07231316109809582,0.44492578689736473,0.7211553193518122,0.8758657804680099,0.01890807847890197,0.11581293306751883,0.17126277092356368,0.8602241279326432,0.1371855605933343,0.5539492279716964,0.7663649743593801,0.19398868259207802,0.9569799507956978,0.24749785606958874,0.7610819645861326,0.567591973275089,0.7770410669374613,0.0733167994187951,0.845138899921509,0.867602249399254,0.32704688986389774,0.6298085331238098,0.019754547108759235,0.39450735124570824,0.5754821972966637,0.9506549185034494,0.6165089490060033,0.7456130158491189,0.8764042203221318,0.520223244392622,0.8123527374664891,0.8251058874981864,0.6842790562674221,0.4753605948189793,0.7491417107396956,0.4062763059892013,0.5738846393238041,0.32205678990789743,0.5765251949731963)
        return pd.DataFrame(
            {
                "x": [
                    0.6964691855978616,
                    0.28613933495037946,
                    0.2268514535642031,
                    0.5513147690828912,
                    0.7194689697855631,
                    0.42310646012446096,
                    0.9807641983846155,
                    0.6848297385848633,
                    0.48093190148436094,
                    0.3921175181941505,
                    0.3431780161508694,
                    0.7290497073840416,
                    0.4385722446796244,
                    0.05967789660956835,
                    0.3980442553304314,
                    0.7379954057320357,
                    0.18249173045349998,
                    0.17545175614749253,
                    0.5315513738418384,
                    0.5318275870968661,
                    0.6344009585513211,
                    0.8494317940777896,
                    0.7244553248606352,
                    0.6110235106775829,
                    0.7224433825702216,
                    0.3229589138531782,
                    0.3617886556223141,
                    0.22826323087895561,
                    0.29371404638882936,
                    0.6309761238544878,
                    0.09210493994507518,
                    0.43370117267952824,
                    0.4308627633296438,
                    0.4936850976503062,
                    0.425830290295828,
                    0.3122612229724653,
                    0.4263513069628082,
                    0.8933891631171348,
                    0.9441600182038796,
                    0.5018366758843366,
                    0.6239529517921112,
                    0.11561839507929572,
                    0.3172854818203209,
                    0.4148262119536318,
                    0.8663091578833659,
                    0.2504553653965067,
                    0.48303426426270435,
                    0.985559785610705,
                    0.5194851192598093,
                    0.6128945257629677,
                    0.12062866599032374,
                    0.8263408005068332,
                    0.6030601284109274,
                    0.5450680064664649,
                    0.3427638337743084,
                    0.3041207890271841,
                    0.4170222110247016,
                    0.6813007657927966,
                    0.8754568417951749,
                    0.5104223374780111,
                    0.6693137829622723,
                    0.5859365525622129,
                    0.6249035020955999,
                    0.6746890509878248,
                    0.8423424376202573,
                    0.08319498833243877,
                    0.7636828414433382,
                    0.243666374536874,
                    0.19422296057877086,
                    0.5724569574914731,
                    0.09571251661238711,
                    0.8853268262751396,
                    0.6272489720512687,
                    0.7234163581899548,
                    0.01612920669501683,
                    0.5944318794450425,
                    0.5567851923942887,
                    0.15895964414472274,
                    0.1530705151247731,
                    0.6955295287709109,
                    0.31876642638187636,
                    0.6919702955318197,
                    0.5543832497177721,
                    0.3889505741231446,
                    0.9251324896139861,
                    0.8416699969127163,
                    0.35739756668317624,
                    0.04359146379904055,
                    0.30476807341109746,
                    0.398185681917981,
                    0.7049588304513622,
                    0.9953584820340174,
                    0.35591486571745956,
                    0.7625478137854338,
                    0.5931769165622212,
                    0.6917017987001771,
                    0.15112745234808023,
                    0.39887629272615654,
                    0.24085589772362448,
                    0.34345601404832493,
                ],
                "y": [
                    0.9290953494701337,
                    0.3001447577944899,
                    0.20646816984143224,
                    0.7712467017344186,
                    0.179207683251417,
                    0.7203696347073341,
                    0.2978651188274144,
                    0.6843301478774432,
                    0.6020774780838681,
                    0.8762070150459621,
                    0.7616916032270227,
                    0.6492402854114879,
                    0.3486146126960078,
                    0.5308900543442001,
                    0.31884300700035195,
                    0.6911215594221642,
                    0.7845248814489976,
                    0.8626202294885787,
                    0.4135895282244193,
                    0.8672153808700541,
                    0.8063467153755893,
                    0.7473209976914339,
                    0.08726848196743031,
                    0.023957638562143946,
                    0.050611236457549946,
                    0.4663642370285497,
                    0.4223981453920743,
                    0.474489623129292,
                    0.534186315014437,
                    0.7809131772951494,
                    0.8198754325768683,
                    0.7111791151322316,
                    0.49975889646204175,
                    0.5018097125708618,
                    0.7991356578408818,
                    0.03560152015693441,
                    0.921601798248779,
                    0.2733414160633679,
                    0.7824828518318679,
                    0.395582605302746,
                    0.48270235978971854,
                    0.5931259692926043,
                    0.2731798106977692,
                    0.8570159493264954,
                    0.5319561444631024,
                    0.1455315278392807,
                    0.6755524321238062,
                    0.27625359167650576,
                    0.2723010177649897,
                    0.6810977486565571,
                    0.9493047259244862,
                    0.807623816061548,
                    0.9451528088524095,
                    0.6402025296719795,
                    0.8258783277528565,
                    0.6300644920352498,
                    0.3893090155420259,
                    0.24163970305689175,
                    0.18402759570852467,
                    0.6031603131688895,
                    0.6566703304734626,
                    0.21177484928830181,
                    0.4359435889362071,
                    0.22965129132316398,
                    0.13087653733774363,
                    0.5989734941782344,
                    0.6688357426448118,
                    0.8093723729154483,
                    0.36209409565006223,
                    0.8513351315065957,
                    0.6551606487241549,
                    0.8554790691017261,
                    0.13596214615618918,
                    0.10883347378170816,
                    0.5448015917555307,
                    0.8728114143337533,
                    0.6621652225678912,
                    0.8701363950944805,
                    0.8453249339337617,
                    0.6283199211390311,
                    0.20690841095962864,
                    0.5176511518958,
                    0.6448515562981659,
                    0.42666354124364536,
                    0.9718610781333566,
                    0.24973274985042482,
                    0.05193778223157797,
                    0.6469719787522865,
                    0.3698392148054457,
                    0.8167218997483684,
                    0.710280810455504,
                    0.260673487453131,
                    0.4218711567383805,
                    0.793490082297006,
                    0.9398115107412777,
                    0.7625379749026492,
                    0.039750173274282985,
                    0.040137387046519146,
                    0.16805410857991787,
                    0.78433600580123,
                ],
                "z": [
                    0.19999193561416084,
                    0.6010279101158327,
                    0.9788327513669298,
                    0.8608964619298911,
                    0.7601684508905298,
                    0.12397506746787612,
                    0.5394401401912896,
                    0.8969279890952392,
                    0.3839893553453263,
                    0.5974293052436022,
                    0.06516937735345008,
                    0.15292545930437007,
                    0.533669687225804,
                    0.5430715864428796,
                    0.8676197246411066,
                    0.9298956526581725,
                    0.6460088459791522,
                    0.006548180072424414,
                    0.6025139026895475,
                    0.36841377074834125,
                    0.44801794989436194,
                    0.5048619249681798,
                    0.4000809850582463,
                    0.763740516980946,
                    0.34083865579228434,
                    0.5424284677884146,
                    0.9587984735763967,
                    0.5859672618993342,
                    0.8422555318312421,
                    0.5153219248350965,
                    0.8358609378832195,
                    0.787997995901579,
                    0.2741451405223151,
                    0.6444057500854898,
                    0.02596405447571548,
                    0.2797463018215405,
                    0.10295252828980817,
                    0.4354164588706081,
                    0.26211152577662666,
                    0.6998708543101617,
                    0.37283691796585705,
                    0.3227717548199931,
                    0.1370286323274963,
                    0.8070990185408966,
                    0.7360223497043797,
                    0.34991170542178995,
                    0.9307716779643572,
                    0.8134995545754865,
                    0.32999762541477007,
                    0.7009778150431946,
                    0.9592132203954723,
                    0.285109164298465,
                    0.005404210183425628,
                    0.7840965908154933,
                    0.6534845192821737,
                    0.22306404635944888,
                    0.5599264352651063,
                    0.9126415066887666,
                    0.20749150526588522,
                    0.769668024293192,
                    0.7563728166813091,
                    0.07231316109809582,
                    0.44492578689736473,
                    0.7211553193518122,
                    0.8758657804680099,
                    0.01890807847890197,
                    0.11581293306751883,
                    0.17126277092356368,
                    0.8602241279326432,
                    0.1371855605933343,
                    0.5539492279716964,
                    0.7663649743593801,
                    0.19398868259207802,
                    0.9569799507956978,
                    0.24749785606958874,
                    0.7610819645861326,
                    0.567591973275089,
                    0.7770410669374613,
                    0.0733167994187951,
                    0.845138899921509,
                    0.867602249399254,
                    0.32704688986389774,
                    0.6298085331238098,
                    0.019754547108759235,
                    0.39450735124570824,
                    0.5754821972966637,
                    0.9506549185034494,
                    0.6165089490060033,
                    0.7456130158491189,
                    0.8764042203221318,
                    0.520223244392622,
                    0.8123527374664891,
                    0.8251058874981864,
                    0.6842790562674221,
                    0.4753605948189793,
                    0.7491417107396956,
                    0.4062763059892013,
                    0.5738846393238041,
                    0.32205678990789743,
                    0.5765251949731963,
                ],
            }
        )
