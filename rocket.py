
class StageOne:
    m = 42000 #kg


    def __init__(
        self,
        fuel_m = None
    ) -> None:
        
        if fuel_m is None:
            self.fuel_m = 399400 #kg
        else:
            self.fuel_m = fuel_m

        self.dot_m = 8 * 346.68 #kg/s
        self.v_a = 2729.388 # m/s
        self.F_a = 8 * 0.98 #m^2
        self.p_a = 4.36 * (10 ** 6) / 69.567
        self.engine_time = self.fuel_m / self.dot_m


    def get_current_total_m(
        self,
        t: float
    ):
        return self.m + self.fuel_m - self.dot_m * t
    

    def get_thirst_vals(
        self
    ):
        return (self.dot_m, self.v_a, self.F_a, self.p_a)
        

class StageTwo:
    m = 10600 #kg

    def __init__(
        self,
        fuel_m = None
    ) -> None:
        if fuel_m is None:
            self.fuel_m = 103600 #kg
        else:
            self.fuel_m = fuel_m

        self.dot_m = 246.45 #kg/s
        self.v_a = 3974.22 # m/s
        self.F_a = 2.01 #m^2
        self.p_a = 5.366 * (10 ** 6) / 279.233
        self.engine_time = self.fuel_m / self.dot_m


    def get_current_total_m(
        self,
        t: float
    ):
        return self.m + self.fuel_m - self.dot_m * t


    def get_thirst_vals(
        self
    ):
        return (self.dot_m, self.v_a, self.F_a, self.p_a)


class Rocket: 
    S = 34.315695095
    m = 20170 # kg
    Cx = {
        0.1:{
            0:0.2060,
            10:0.2077,
            20:0.2249,
            30:0.1989,
            40:0.2893,
            60:0.4845
            },
        0.3:{
            0:0.1989,
            10:0.2073,
            20:0.2119,
            30:0.2330,
            40:0.2325,
            60:0.3441
            },
        0.5:{
            0:0.1840,
            10:0.1914,
            20:0.1948,
            30:0.2127,
            40:0.2033,
            60:0.2890
            },
        0.7:{
            0:0.2061,
            10:0.2061,
            20:0.2240,
            30:0.2316,
            40:0.2185,
            60:0.2902
        },
        0.8:{
            0:0.2368,
            10:0.2434,
            20:0.2541,
            30:0.2611,
            40:0.2469,
            60:0.3138
        },
        0.9:{
            0:0.2766,
            10:0.2834,
            20:0.2944,
            30:0.3013,
            40:0.2856,
            60:0.3505
        },
        1.0:{
            0:0.3242,
            10:0.3308,
            20:0.3415,
            30:0.3479,
            40:0.3317,
            60:0.3931
        },
        1.1:{
            0:0.3742,
            10:0.3807,
            20:0.3910,
            30:0.3971,
            40:0.3805,
            60:0.4389
        },
        1.3:{
            0:0.4845,
            10:0.4906,
            20:0.5002,
            30:0.5057,
            40:0.5379,
            60:0.5424
        },
        1.5:{
            0:0.4973,
            10:0.5031,
            20:0.5122,
            30:0.5171,
            40:0.5469,
            60:0.5501
        },
        2.0:{
            0:0.4988,
            10:0.5037,
            20:0.5116,
            30:0.5156,
            40:0.5405,
            60:0.5428
        },
        2.5:{
            0:0.4851,
            10:0.4895,
            20:0.4963,
            30:0.5056,
            40:0.5206,
            60:0.5237
        },
        3.0:{
            0:0.4789,
            10:0.4827,
            20:0.4886,
            30:0.4973,
            40:0.5160,
            60:0.5138
        },
        3.5:{
            0:0.4617,
            10:0.4650,
            20:0.4702,
            30:0.4778,
            40:0.4940,
            60:0.4939
        },
        4.0:{
            0:0.4391,
            10:0.4420,
            20:0.4466,
            30:0.4532,
            40:0.4673,
            60:0.4692
        },
        4.5:{
            0:0.4321,
            10:0.4347,
            20:0.4387,
            30:0.4446,
            40:0.4570,
            60:0.4606
        },
        5.0:{
            0:0.4226,
            10:0.4261,
            20:0.4313,
            30:0.4423,
            40:0.4473,
            60:0.4492
        },
    }
    mach_table = [0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.3, 1.5, 2.0, 3.0, 3.5, 4.0, 4.5, 5.0]
    h_table = [0, 10, 20, 30, 40, 60]
    
    def __init__(
        self,
        stage_one: StageOne = None,
        stage_two: StageTwo = None,
        payload: bool = False,
    )-> None:
        if stage_one is None:
            stage_one = StageOne()
        if stage_two is None:
            stage_two = StageTwo()
        if payload:
            self.payload_m = 21000 #kg
        else:
            self.payload_m = 0
        self.stage_one = stage_one
        self.stage_two = stage_two
        self.engine_time = self.stage_one.engine_time + self.stage_two.engine_time
        self.is_active = True
        self.inactive_time = 0.
    

    def get_current_total_m(
        self,
        t: float
    )-> float:
        if self.inactive_time < 0.:
            t = -self.inactive_time
        else:
            t -= self.inactive_time

        if t <= self.stage_one.engine_time:
            fsm = self.stage_one.get_current_total_m(t)
            ssm = self.stage_two.m + self.stage_two.fuel_m
        elif t <= self.engine_time:
            fsm = 0
            ssm = self.stage_two.get_current_total_m(t - self.stage_one.engine_time)
        else:
            fsm = 0
            ssm = 0

        return self.payload_m + self.m + fsm + ssm
    

    def get_aero_cf(
        self,
        mach: float,
        h
    )-> float:
        buffer = []
        dmax = 1e+15
        for i in self.h_table:
            s = abs(h-i)
            if s < dmax:
                dmax = s
                table_h = i

        for i in range(len(self.mach_table) - 1):
            buffer.append((self.Cx[self.mach_table[i+1]][table_h] - self.Cx[self.mach_table[i]][table_h])/((self.mach_table[i+1] - self.mach_table[i]) * 1000))
        buffer.append(buffer[-1])
        for i in range(len(self.mach_table) - 1):
            if (self.mach_table[i] <= mach and mach < self.mach_table[i+1]):
                return self.Cx[self.mach_table[i]][table_h] + buffer[i] * (mach - self.mach_table[i])
        return self.Cx[self.mach_table[-1]][table_h]

    def get_thirst_vals(
        self, 
        t: float
    ) -> float:
        
        t -= self.inactive_time

        if t < self.stage_one.engine_time and self.is_active:
            return self.stage_one.get_thirst_vals()
        elif t < self.engine_time and self.is_active: 
            return self.stage_two.get_thirst_vals()
        else: 
            return (0, 0, 0, 0)
        

if __name__ == "__main__":
    st = StageOne()
    st2 = StageTwo()
    print(st.engine_time + st2.engine_time / 5)
        