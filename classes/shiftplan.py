from calendar import monthrange
from datetime import date
from bitstring import BitArray
import math

class Shiftplan(object):
    """docstring for Shiftplan"""
    def __init__(self):
        super(Shiftplan, self).__init__()

    # CONSTANTS
    SHIFT_NOSHIFT = 0;
    SHIFT_LATE = 1;
    SHIFT_ONCALL = 2;

    SPACING_ONCALL = 1
    SPACING_LATE = 1


    SCORE_INITIAL = 1000

    SCORE_PENALIZE_LATE_OVER_LIMIT = -10
    SCORE_PENALIZE_LATE_WEEKEND = -20
    SCORE_PENALIZE_LATE_UNDER_LIMIT = -20

    SCORE_PENALIZE_ONCALL_OVER_LIMIT = -10
    SCORE_PENALIZE_ONCALL_UNDER_LIMIT = -20

    SCORE_PENALIZE_SPACING_ONCALL = -50
    SCORE_PENALIZE_SPACING_LATE = -50

    SCORE_AWARD_LATE_EXACT_LIMIT = 0
    SCORE_AWARD_ONCALL_EXACT_LIMIT = 0


    # class variables
    days = 0
    year = 0
    month = 0
    workers = 0
    bitSize = 0
    shifts = []
    shiftsWorkers = []

    def setParameters(self, Year, Month, numberOfWorkers, bitSize):
        self.year = Year
        self.month = Month
        self.workers = numberOfWorkers
        self.days = monthrange(Year, Month)[1]
        self.bitSize = bitSize

    def getParameterCount(self):
        return self.days * self.workers

    def loadChromosome(self, ch):
        processedChromo = []
        iterator = 0
        traitStart = 0
        for i in range(self.days * self.workers * self.bitSize):
            if i % self.bitSize == 0:
                binaryString = ''
                for j in ch.getChromo()[traitStart:i]:
                    binaryString = binaryString + str(j)

                b = BitArray(bin=binaryString)
                b.uint
            else:
                traitStart = i
            

        self.unloadChromosome()
        for i in range(self.days):
            self.shifts.append(processedChromo[i::self.days])
        for i in range(self.workers):
            start = i * self.days
            end = start + self.days
            self.shiftsWorkers.append(processedChromo[start:end])

    def unloadChromosome(self):
        self.shifts = []

    def countShiftsPerDay(self, shiftType, day):
        return self.shifts[day].count(shiftType)

    def countShiftsPerWorker(self, shiftType, worker):
        return self.shiftsWorkers[worker].count(shiftType)

    def checkEqualAmount(self, chromosome, traitToCheck, allowedDifference):
        # values = []
        # for i in range(self.workers):
        #     values.append(self.countShiftsPerWorker)
        pass

    def checkProximitySameTraits(self, chromosome, checkTrait, minProximity):
        indexes = [i for i, x in enumerate(chromosome.chromo) if x == checkTrait]
        first = True
        for i, x in enumerate(indexes):
            if(not first):
                if( (x - indexes[i - 1]) > minProximity):
                    # print("false")
                    return False
            else:
                first = False
        return True


    def evaluate(self, ch):
        self.loadChromosome(ch)

        count = 0
        weekendCount = 0
        score = self.SCORE_INITIAL

        # one late each day
        # one oncall each day
        # no late on weekend
        # force oncall on weekend

        for i in range(self.days):
            if(self.isWeekend(i)):
                weekendCount += 1

            # ---------- LATE -------------
            # one late day
            count = self.countShiftsPerDay(self.SHIFT_LATE, i)

            if(count > 1):
                score += count * self.SCORE_PENALIZE_LATE_OVER_LIMIT
            elif(count == 1):
                score += self.SCORE_AWARD_LATE_EXACT_LIMIT
            else:
                score += self.SCORE_PENALIZE_LATE_UNDER_LIMIT

            # no late on weekend
            if(self.isWeekend(i)):
                if(count > 0):
                    score += self.SCORE_PENALIZE_LATE_WEEKEND

            # ---------- ONCALL -------------
            # one oncall each day
            count = self.countShiftsPerDay(self.SHIFT_ONCALL, i)
            if(count > 1):
                score += count * self.SCORE_PENALIZE_ONCALL_OVER_LIMIT
            elif(count == 1):
                score += self.SCORE_AWARD_ONCALL_EXACT_LIMIT
            else:
                score += self.SCORE_PENALIZE_ONCALL_UNDER_LIMIT

            # evenly distributed oncall weekends
            # TODO

        # SPACING
        for worker in range(self.workers):
            if(not(self.checkProximitySameTraits(ch, self.SHIFT_LATE, self.SPACING_LATE))):
                score += self.SCORE_PENALIZE_SPACING_LATE

            if(not(self.checkProximitySameTraits(ch, self.SHIFT_ONCALL, self.SPACING_ONCALL))):
                score += self.SCORE_PENALIZE_SPACING_ONCALL


        # late shift every day except weekends
        # count = ch.countGenes(self.SHIFT_LATE)
        # if(count != (self.days - weekendCount)):
        #     score = 0

        # # oncall every day, initial penalization
        # count = ch.countGenes(self.SHIFT_ONCALL)
        # if(count != self.days):
        #     score = 0

        if(score < 0):
            return 0
        else:
            return score

    def renderToString(self):
            output = ""
            oncallCount = 0
            lateCount = 0
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
                        lateCount += 1
                    elif(s[day][worker] == self.SHIFT_ONCALL):
                        c = "O"
                        oncallCount += 1
                    else:
                        c = "-"
                    output += " " + c + " "
                output += "\n"

            output += "O: " + str(oncallCount) + "\nL: " + str(lateCount)

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

