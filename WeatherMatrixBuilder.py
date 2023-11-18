import json
import numpy as np
from scipy.interpolate import LinearNDInterpolator


class WeatherMatrixBuilder:
    def __init__(self, file="stations.json") -> None:
        with open(file) as f:
            s = json.load(f)
            self.indexes = []
            self.latitudes = []
            self.longitudes = []
            self.heights = []
            for i in s.keys():
                self.indexes.append(i)
                self.latitudes.append(s[i][1])
                self.longitudes.append(s[i][2])
                self.heights.append(s[i][3])
            gr1 = np.linspace(min(self.latitudes) - 0.3, max(self.latitudes) + 0.3, num=4096)
            gr2 = np.linspace(min(self.longitudes) - 0.3, max(self.longitudes) + 0.3, num=4096)
            self.x1, self.y1 = np.meshgrid(gr1, gr2)

    def produce(self, time, data="new_data"):
        t = []
        u = []
        for i in self.indexes:
            print(f"{data}/{i}--{time}.json")
            with open(f"{data}/{i}--{time}.json") as f:
                j = json.load(f)
            t.append(j[6]["T"])
            u.append(j[6]["U"])
        t_interpolator = LinearNDInterpolator(list(zip(self.latitudes, self.longitudes)), t)
        u_interpolator = LinearNDInterpolator(list(zip(self.latitudes, self.longitudes)), u)

        z_t = t_interpolator(self.x1, self.y1)
        z_u = u_interpolator(self.x1, self.y1)
        return z_t, z_u