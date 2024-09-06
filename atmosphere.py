import numpy as np
from matplotlib import pyplot as plt

r0 = 6371 * (10 ** 3)

class Atmosphere:
    Mc = 28.964420 #кг/кмоль
    M97 = 28.910
    M975 = 28.842
    Na = 602.257 * (10**24) #кмоль^-1
    R = 8314.32 #Дж·К^-1 ·кмоль^-1
    R0 = 287.05287 #Дж·кг^-1 ·К^-1
    chi = 1.4
    sigma = 0.365 * (10 ** (-9)) #м
    beta120 = {
        0.: -0.0065,
        11000.: -0.0065,
        20000.: 0.0,
        32000.: 0.0010,
        47000.: 0.0028,
        51000.: 0.0,
        71000.: -0.0028,
        85000.: -0.0020,
        94000.: 0.0,
        102450.: 0.0030,
        117781.54367585888: 0.0110,
    }
    T120 = {
        0.: 288.15,
        11000.: 216.65,
        20000.: 216.65,
        32000.: 228.65,
        47000.: 270.65,
        51000.: 270.65,
        71000.: 214.65,
        85000.: 186.65,
        94000.: 186.525,
        102450.: 212.00,
        117781.54367585888: 380.60
    }
    T1200 = {
        120000.: 334.42,
        140000.: 559.60,
        160000.: 695.60,
        200000.: 834.40,
        250000.: 941.90,
        325000.: 984.65,
        400000.: 995.90,
        600000.: 999.90,
        800000.: 1000.0,
        1200000.: 1000.0
    }
    beta1200 = {
        120000.: 0.011259,
        140000.: 0.006800,
        160000.: 0.003970,
        200000.: 0.001750,
        250000.: 0.000570,
        325000.: 0.0001500,
        400000.: 0.0000200,
        600000.: 0.0000005,
        800000.: 0.0,
        1200000.: 0.0,
    }
    P120 = {
        0.: 0.10132 * (10 ** 6),
        11000.: 0.226999 * (10 ** 5),
        20000.: 5.44333 * 1000,
        32000.: 8.63138 * 100,
        47000.: 1.10219 * 100,
        51000.: 6.70424 * 10,
        71000.: 3.95762,
        85000.: 3.73380 / 10,
        94000.:  7.52834 / 100,
        102450.: 1.67431 / 100,
        117781.54367585888: 2.66618 / 1000,
    }
    H_table = [0., 11000., 20000., 32000., 47000., 51000., 71000., 85000., 94000., 102450., 117781.54367585888]
    h_tab = [120000., 140000., 160000., 200000., 250000., 325000., 400000., 600000., 800000., 1200000.]
    Cp = {
        223.: 1013,
        243.: 1013,
        248.: 1011,
        253.: 1009,
        263.: 1009,
        268.: 1007,
        273.: 1005,
        333.: 1005,
        343.: 1009,
        393.: 1009,
        403.: 1011,
        413.: 1013,
        423.: 1015,
        433.: 1017,
        443.: 1020,
        453.: 1022,
        463.: 1024,
        473.: 1026,
        483.: 1037,
        573.: 1047,
        623.: 1058,
        673.: 1068,
        723.: 1081,
        773.: 1093,
        823.: 1104,
        873.: 1114,
        923.: 1125,
        973.: 1135,
        1023.: 1146
    }
    Tc = [223., 243., 248., 253., 263., 268., 273., 333., 343., 
          393., 403., 413., 423., 433., 443., 453., 463., 473., 483., 
          573., 623., 673., 723., 773., 823., 873., 923., 973., 1023.]

    
    @staticmethod
    def get_H(
        h: float
    )-> float:
        return r0 * h / (r0+ h)
    

    @staticmethod
    def get_upper_ids(
        table: list[float],
        val: float
    )-> int:
        for i in range(len(table)):
            s = val - table[i]
            if s <= 0:
                return i
        raise KeyboardInterrupt("h > 1200km", val)
            

    def get_M(
        self,
        h
    )-> float:
        
        if h <= 94000.:
            return self.Mc
        elif h <= 97000.:
            return 28.82 + 0.158 * ((1 - 7.5 / (10 ** 8) * ((h - 94000) ** 2) ) ** 0.5) - (2.479 / (10 ** 4)) * ((97000 - h ) ** (0.5))
        elif h <= 97500.:
            return self.M97 - 0.00012 *(97500 - h)
        elif h <= 120000.:
            return self.M975 - 0.0001511 * (120000 - h)
        elif h <= 250000.:
            return 46.9083 - 29.71210 / (10 ** 5) * h + 12.08693 / (10 ** 10) * (h ** 2) -1.85675 / (10 ** 15) * (h ** 3)
        elif h <= 400000.:
            return 40.4668 - 15.52722 / (10 ** 5) * h + 3.55735 / (10 ** 10) * (h ** 2) - 3.02340 / (10 ** 16) * (h ** 3)
        elif h <= 650000.:
            return 6.3770 + 6.25497 / (10 ** 5) * h - 1.10144 / (10 ** 10) * (h ** 2) + 3.36907 / (10 ** 17) * (h ** 3)
        elif h <= 900000.:
            return 75.6896 - 17.61243 / (10 ** 5) * h +  1.33603 / (10 ** 10) * (h ** 2) - 2.87884 / (10 ** 17) * (h ** 3)
        elif h <= 1050000.:
            return 112.4838  - 30.68086 / (10 ** 5) * h + 2.90329 / (10 ** 10) * (h ** 2) - 9.20616 / (10 ** 17) * (h ** 3)
        elif h <= 1200000.:
            return 9.8970 - 1.19732 / (10 ** 5) * h + 7.78247 / (10 ** 12) * (h ** 2) - 1.77541 / (10 ** 18) * (h ** 3)
        else:
            raise KeyboardInterrupt("h > 1200km", h)
        

    def T_to_TM(
        self,
        T: float,
        h: float
    )-> float: 
        return T * self.Mc / self.get_M(h)
    

    def TM_to_T(
        self,
        TM: float,
        h: float
    )-> float:
        return TM * self.get_M(h) / self.Mc 
        
    
    def get_T(
        self,
        h: float,
        flag: bool = True
    )-> float:
       
        if h < 120000:
            H = self.get_H(h)
            ir = self.get_upper_ids(self.H_table, H)
         
            if H < 120000:
                TM = self.T120[self.H_table[ir]] + self.beta120[self.H_table[ir]] * (H - self.H_table[ir])
                if flag:
                    return self.TM_to_T(TM, h)
                else: 
                    return TM
        else:
            ir = self.get_upper_ids(self.h_tab, h)
            TM = self.T1200[self.h_tab[ir]] + self.beta1200[self.h_tab[ir]] * (h - self.h_tab[ir])
            return TM
            

    def get_P(
        self,
        h: float
    )-> float:
        if h < 120000:
            H = self.get_H(h)
            ir = self.get_upper_ids(self.H_table, H)

            if self.beta120[self.H_table[ir]] != 0:
                P = (np.exp(np.log(self.P120[self.H_table[ir]]) - 
                        (9.81 * np.log((self.T120[self.H_table[ir]] + 
                        self.beta120[self.H_table[ir]] * (H - self.H_table[ir])) / 
                        self.T120[self.H_table[ir]]) / (self.beta120[self.H_table[ir]] * self.R / self.get_M(h)))))
                return P
            else:
                return (np.exp(np.log(self.P120[self.H_table[ir]]) - 
                        9.81 * 0.434294 * self.get_M(h) * (H - self.H_table[ir]) / self.R / self.get_T(h)))
        else:
            return self.get_n(h) * self.R * self.get_T(h) / self.Na


    def get_n(
        self,
        h: float
    ) -> float:
        if h <= 150000.:
            return (0.210005867 * (10 ** 4) - 0.5618444757 / 10 * h + 
                    0.5663986231 / (10 ** 6) * (h ** 2) - 
                    0.2547466858 / (10 ** 11) * (h ** 3) + 
                    0.4309844119 / (10 ** 17) * (h ** 4)) * (10 ** 17)
        elif h <= 200000.:
            return (0.10163937 * (10 ** 4) - 0.2119530830 / 10 * h + 
                    0.1671627815 / (10 ** 6) * (h ** 2) - 
                    0.5894237068 / (10 ** 12) * (h ** 3) + 
                    0.7826684089 / (10 ** 18) * (h ** 4)) * (10 ** 16)
        elif h <= 250000.:
            return (0.7631575 * (10 ** 3) - 0.1150600844 / 10 * h + 
                    0.6612598428 / (10 ** 7) * (h ** 2) - 
                    0.1708736137 / (10 ** 12) * (h ** 3) + 
                    0.1669823114 / (10 ** 18) * (h ** 4)) * (10 ** 15)
        elif h <= 350000.:
            return (0.1882203 * (10 ** 3) - 0.2265999519 / 100 * h + 
                    0.1041726141 / (10 ** 7) * (h ** 2) - 
                    0.2155574922 / (10 ** 13) * (h ** 3) + 
                    0.1687430962 / (10 ** 19) * (h ** 4)) * (10 ** 15)
        elif h <= 450000.:
            return (0.2804823 * (10 ** 3) - 0.2432231125 / 100 * h + 
                    0.8055024663 / (10 ** 8) * (h ** 2) - 
                    0.1202418519 / (10 ** 13) * (h ** 3) + 
                    0.6805101379 / (10 ** 20) * (h ** 4)) * (10 ** 14)
        elif h <= 600000.:
            return (0.5599362 * (10 ** 3) - 0.3714141392 / 100 * h + 
                    0.9358870345 / (10 ** 8) * (h ** 2) - 
                    0.1058591881 / (10 ** 13) * (h ** 3) + 
                    0.4525531532 / (10 ** 20) * (h ** 4)) * (10 ** 13)
        elif h <= 800000.:
            return (0.8358756 * (10 ** 3) - 0.4265393073 / 100 * h + 
                    0.8252842085 / (10 ** 8) * (h ** 2) - 
                    0.7150127437 / (10 ** 14) * (h ** 3) + 
                    0.2335744331 / (10 ** 20) * (h ** 4)) * (10 ** 12)
        elif h <= 1000000.:
            return (0.8364965 * (10 ** 2) - 0.3162492458 / (10 ** 3) * h + 
                    0.4602064246 / (10 ** 9) * (h ** 2) - 
                    0.3021858469 / (10 ** 15) * (h ** 3) + 
                    0.7512304301 / (10 ** 22) * (h ** 4)) * (10 ** 12)
        elif h <= 1200000.:
            return (0.383220 * (10 ** 2) - 0.50980 / (10 ** 4) * h + 
                    0.18100 / (10 ** 10) * (h ** 2)) * (10 ** 11)
        else:
            return 0


    def get_rho(
        self,
        h: float
    )-> float:
        return self.get_P(h) * self.get_M(h) / (self.R * self.get_T(h))


    def get_Cp(
        self,
        h: float
    )-> float:
        T = self.get_T(h)

        buffer = []

        for i in range(len(self.Tc) - 1):
            buffer.append((self.Cp[self.Tc[i+1]] - self.Cp[self.Tc[i]])/(self.Tc[i+1] - self.Tc[i]))
        buffer.append(buffer[-1])

        if T < self.Tc[0]:
            return self.Cp[self.Tc[0]]
        
        for i in range(len(self.Tc) - 1):
            if (self.Tc[i] <= T and T < self.Tc[i+1]):
                return self.Cp[self.Tc[i]] + buffer[i] * (T - self.Tc[i])
            
        return self.Cp[self.Tc[-1]]
    

    def get_Cv(
        self,
        h: float
    )-> float:
        Cp = self.get_Cp(h)
        M = self.get_M(h)
        Ri = self.R / self.Mc
        return Cp - Ri
    

    def get_gamma(
        self,
        h: float
    )-> float:
        return self.get_Cp(h) / self.get_Cv(h)
    

    def get_Vs(
        self,
        h: float
    ) -> float:
        return np.sqrt(self.get_gamma(h) * self.R * self.get_T(h) / self.Mc)



if __name__ == "__main__":
    H = np.linspace(0, 1200000, 10000)
    atm = Atmosphere()

    T = []
    for i in H:
        T.append(atm.get_T(i))
    
    fig = plt.figure(figsize=(10,12))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(H, T)
    ax1.set_xlabel('h')
    ax1.set_ylabel('T')
    ax1.grid(True)
    plt.show()

