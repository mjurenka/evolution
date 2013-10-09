from calendar import monthrange
from datetime import date
import math

class Shiftplan(object):
    """docstring for Shiftplan"""
    def __init__(self):
        super(Shiftplan, self).__init__()

    # CONSTANTS
    SHIFT_NOSHIFT = 0;
    SHIFT_LATE = 1;
    SHIFT_ONCALL = 2;

    SCORE_PENALIZE_ONCALL = 30
    SCORE_PENALIZE_LATE = 20
    SCORE_PENALIZE_NOSHIFT = 40
    SCORE_PENALIZE_WEEKEND = 30
    SCORE_AWARD = 50
    SCORE_INITIAL = 10

    # class variables
    days = 0
    year = 0
    month = 0
    workers = 0
    shifts = []

    def setParameters(self, Year, Month, numberOfWorkers):
        self.year = Year
        self.month = Month
        self.workers = numberOfWorkers
        self.days = monthrange(Year, Month)[1]

    def loadChromosome(self, ch):
        self.unloadChromosome()
        for i in range(self.days):
            self.shifts.append(ch.chromo[i::self.days])

    def unloadChromosome(self):
        self.shifts = []

    def countShiftsPerDay(self, shiftType, day):
        return self.shifts[day].count(shiftType)

    def evaluate(self, ch):
        self.loadChromosome(ch)

        count = 0
        weekendCount = 0
        score = self.days * len(self.shifts) * self.SCORE_INITIAL

        for i in range(self.days):
            # one late each working day
            if(not self.isWeekend(i)):
                count = self.countShiftsPerDay(self.SHIFT_LATE, i)
                if(count > 1):
                    score -= (count - 1) * self.SCORE_PENALIZE_LATE

            # one oncall every day
            count = self.countShiftsPerDay(self.SHIFT_ONCALL, i)
            if(count > 1):
                score -= (count - 1) * self.SCORE_PENALIZE_ONCALL

            if(count < 1):
                score -= self.SCORE_PENALIZE_NOSHIFT

            count = self.countShiftsPerDay(self.SHIFT_LATE, i)
            # no late on weekend
            if(self.isWeekend(i)):
                weekendCount += 1
                score -= self.SCORE_PENALIZE_WEEKEND
            else:
                if(count < 1):
                    score -= self.SCORE_PENALIZE_NOSHIFT

            # evenly distributed oncall weekends
            # TODO

        # shift every day except weekends
        count = ch.countGenes(self.SHIFT_LATE)
        if(count != (self.days - weekendCount)):
            score -= math.fabs(self.days - count - weekendCount) * self.SCORE_PENALIZE_LATE
            score = 0

        # oncall every day, initial penalization
        count = ch.countGenes(self.SHIFT_ONCALL)
        if(count != self.days):
            score = 0

        if(score < 0):
            return 0
        else:
            return score

    def renderToString(self):
            output = ""

            # header
            for i in range(self.days):
                if(self.isWeekend(i)):
                    output += "W"
                else:
                    output += " "

                output += str(i + 1)
                if(i < 9):
                    output += " "

            output += "\n"

            # days
            s = self.shifts[:]
            for worker in range(self.workers):
                c = ""
                for day in range(self.days):
                    if(s[day][worker] == self.SHIFT_LATE):
                        c = "L"
                    elif(s[day][worker] == self.SHIFT_ONCALL):
                        c = "O"
                    else:
                        c = "-"
                    output += " " + c + " "
                output += "\n"

            return output

    def isWeekend(self, day):
        # days start from 0
        day += 1
        day = day % self.days
        if(day == 0):
            day += 1

        dt = date(self.year, self.month, day)
        if(dt.isoweekday() == 6):
            return True
        elif(dt.isoweekday() == 7):
            return True
        else:
            return False

