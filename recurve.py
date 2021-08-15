class RECurve:
    # period - a complete investment time section
    # time   - point of the curve
    # i_risk - initial risk (curve start)
    # f_risk - highest risk (curve end)
    def __init__(self, period, i_risk, f_risk):
        self.period = period
        self.i_risk = i_risk
        self.f_risk = f_risk
        self.offset = self.i_risk
        self.time = 0
        self.curve = 0

    def set_time(self, time):
        if time >= self.period:
            print("Error, time must be within the period!")
            return -1
        else:
            self.time = time
            return 0

    def get_risk(self, time):
        if 0 > self.set_time(time):
            return -1
        else:
            if 0 != self.period:
                self.curve = (self.f_risk - self.i_risk) / self.period
                return self.curve * self.time + self.i_risk
            else:
                return 0


class RECurveSQR(RECurve):

    def __init__(self, period, i_risk, f_risk):
        RECurve.__init__(self, period, i_risk, f_risk)

    def get_risk(self, time):
        if 0 > self.set_time(time):
            return -1
        else:
            if 0 != self.period:
                self.curve = (self.f_risk - self.i_risk) / self.period
                return self.curve * self.time * self.time + self.i_risk
            else:
                return 0
