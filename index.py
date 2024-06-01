import random
import matplotlib.pyplot as plt

def resetCounter():
    return 0, 0, 0

def getThreeStar(pity4Count, pity5Count, counter):
    return pity4Count + 1, pity5Count + 1, counter + 1

def getFourStar(pity4Count, pity5Count, counter):
    return 0, pity5Count + 1, counter + 1

def getFiveStar(pity4Count, pity5Count, counter):
    return 0, 0, counter + 1

# incorrect estimate method
def runOne(X, Y):
    # output list (the result of each summon for 1 run)
    output = list()
    # guaranteed for four star
    pity4Count = 0
    # guaranteed for five star
    pity5Count = 0
    # count for each stars
    threeCount, fourCount, fiveCount = resetCounter()

    # 1-80 summons
    for _ in range(0, 80):
        # guaranteed system
        # for 5 star character
        if pity5Count >= 79:
            output.append('5')
            pity4Count, pity5Count, fiveCount = getFiveStar(pity4Count, pity5Count, fiveCount)
            continue
        # for 4 star character
        if pity4Count >= 9:
            output.append('4')
            pity4Count, pity5Count, fourCount = getFourStar(pity4Count, pity5Count, fourCount)
            continue
        
        summon = round(random.uniform(0, 1), 3) * 100
        # summon (original rate)
        if pity5Count <= X:
            if 0 <= summon and summon <= 0.8:
                output.append('5')
                pity4Count, pity5Count, fiveCount = getFiveStar(pity4Count, pity5Count, fiveCount)
            elif 0.8 < summon and summon <= 6.8:
                output.append('4')
                pity4Count, pity5Count, fourCount = getFourStar(pity4Count, pity5Count, fourCount)
            else:
                output.append('3')
                pity4Count, pity5Count, threeCount = getThreeStar(pity4Count, pity5Count, threeCount)

        # pity system (linear additional rate)
        else:
            additional_rate = (pity5Count - X) * Y
            five_star_rate = min(0.8 + additional_rate, 100)
            four_star_rate = 6.0
            if 0 <= summon and summon <= five_star_rate:
                output.append('5')
                pity4Count, pity5Count, fiveCount = getFiveStar(pity4Count, pity5Count, fiveCount)
            elif five_star_rate < summon and summon <= four_star_rate + five_star_rate:
                output.append('4')
                pity4Count, pity5Count, fourCount = getFourStar(pity4Count, pity5Count, fourCount)
            else:
                output.append('3')
                pity4Count, pity5Count, threeCount = getThreeStar(pity4Count, pity5Count, threeCount)
    return output, threeCount, fourCount, fiveCount

def SetXYPairLinear(testFrom, testTo):
    # generate X, Y pair
    X_values = []
    Y_values = []
    initial = 0.8
    final = 100
    for i in range(testFrom, testTo):
        gap = 80 - i
        X_values.append(i)
        Y_values.append((final - initial) / gap)
    return X_values, Y_values, testFrom, testTo

def SetXYPairMIHOYO(testFrom, testTo):
    # generate X, Y pair
    X_values = []
    Y_values = []
    for i in range(testFrom, testTo):
        X_values.append(i)
        Y_values.append(8)
    return X_values, Y_values, testFrom, testTo

def drawLineChart(X_values, ratio, officalRatio, mode, starLevel):
    plt.figure()
    plt.plot(X_values, ratio, color='r', marker='o')
    plt.plot(X_values, officalRatio, color='b', marker='o')
    plt.xlabel("X")
    plt.ylabel(f"{starLevel}-star summon ratio (%)")
    plt.title(f"{starLevel}-star summon ratio")
    plt.savefig(f"./{mode.lower()}/{starLevel}-star summon ratio {mode}.png")
    plt.close()

def drawBarChart(X_values, ratio, mode, index):
    plt.figure()
    plt.bar(range(1, 81), ratio, color='b')
    plt.xlabel("Summon")
    plt.ylabel("5-star summon ratio (%)")
    plt.title("5-star summon ratio per summon")
    plt.savefig(f"./{mode.lower()}/5-star ratio per summon {mode} X={X_values[index]}.png")
    plt.close()

# incorrect estimate method
def GetAnswer(X_values, Y_values, testFrom, testTo, mode):
    assert mode == "linear" or mode == "miHoYo", "mode should be either 'linear' or 'miHoYo'"

    threeStarRatio, fourStarRatio, fiveStarRatio = list(), list(), list()
    threeStarOfficalRatio = [86.2] * (testTo - testFrom)
    fourStarOfficalRatio = [12] * (testTo - testFrom)
    fiveStarOfficalRatio = [1.8] * (testTo - testFrom)
    
    for i in range(len(X_values)):
        X = X_values[i]
        Y = Y_values[i]
        totalThree, totalFour, totalFive = 0, 0, 0
        totalFivePerSummon = [0] * 80
        runCount = 100000
        for _ in range(runCount):
            output, threeCount, fourCount, fiveCount = runOne(X, Y)
            totalThree += threeCount
            totalFour += fourCount
            totalFive += fiveCount
            for j in range(0, 80):
                if output[j] == '5':
                    totalFivePerSummon[j] += 1
        totalFivePerSummon = [x * 10000 / runCount / 80 for x in totalFivePerSummon]
        writingResults = f"X = {X}, Y = {Y}%\n\
3-star: {totalThree * 100 / runCount / 80}%\n\
4-star: {totalFour * 100 / runCount / 80}%\n\
5-star: {totalFive * 100 / runCount / 80}%\n\n"

        with open(f"./{mode.lower()}/{mode.lower()}.txt", "a") as f:
            f.write(writingResults)

        threeStarRatio.append(totalThree * 100 / runCount / 80)
        fourStarRatio.append(totalFour * 100 / runCount / 80)
        fiveStarRatio.append(totalFive * 100 / runCount / 80)

        # five star ratio per summon
        drawBarChart(X_values, totalFivePerSummon, mode, i)

        print("mode:", mode, "| X:", X, "finished!")

    # star ratio for 3, 4, 5 stars
    drawLineChart(X_values, threeStarRatio, threeStarOfficalRatio, mode, 3)
    drawLineChart(X_values, fourStarRatio, fourStarOfficalRatio, mode, 4)
    drawLineChart(X_values, fiveStarRatio, fiveStarOfficalRatio, mode, 5)

def setGap(testFrom, testTo):
    gapLinear = [round(99.2 / (80 - x), 10) for x in range(testFrom, testTo)]
    gapMIHOYO = [8] * 80
    return gapLinear, gapMIHOYO

def runCalculation(testFrom, testTo):
    gapLinear, gapMIHOYO = setGap(testFrom, testTo)

    linearEstimatedAvgProbabilityList = list()
    miHoYoEstimatedAvgProbabilityList = list()
    officalAvgProbabilityList = list()
    for xValue in range(testFrom, testTo):
        # linear
        linearStar5Probability = [0.8] * xValue + [0.8 + gapLinear[xValue - testFrom] * (x + 1) for x in range(80 - xValue)]
        linearStar5Probability[-1] = 100
        linearNotStar5Probability = [100 - x for x in linearStar5Probability]
        linearStar5WhenGotcha = [1] * 80
        for i in range(1, 81):
            for j in range(i - 1):
                linearStar5WhenGotcha[i - 1] *= linearNotStar5Probability[j] / 100
            linearStar5WhenGotcha[i - 1] *= linearStar5Probability[i - 1] / 100
            linearStar5WhenGotcha[i - 1] *= 100
        linearExpectationValue = [linearStar5WhenGotcha[i] * (i + 1) / 100 for i in range(0, 80)]
        linearFinalExpectationValue = sum(linearExpectationValue)
        linearEstimatedAvgProbability = 100 / linearFinalExpectationValue
        linearEstimatedAvgProbabilityList.append(linearEstimatedAvgProbability)

        # miHoYo
        miHoYoStar5Probability = [0.8] * xValue + [0.8 + gapMIHOYO[x] * (x + 1) for x in range(80 - xValue)]
        miHoYoStar5Probability[-1] = 100
        miHoYoNotStar5Probability = [100 - x for x in miHoYoStar5Probability]
        miHoYoStar5WhenGotcha = [1] * 80
        for i in range(1, 81):
            for j in range(i - 1):
                miHoYoStar5WhenGotcha[i - 1] *= miHoYoNotStar5Probability[j] / 100
            miHoYoStar5WhenGotcha[i - 1] *= miHoYoStar5Probability[i - 1] / 100
            miHoYoStar5WhenGotcha[i - 1] *= 100
        miHoYoExpectationValue = [miHoYoStar5WhenGotcha[i] * (i + 1) / 100 for i in range(0, 80)]
        miHoYoFinalExpectationValue = sum(miHoYoExpectationValue)
        miHoYoEstimatedAvgProbability = 100 / miHoYoFinalExpectationValue
        miHoYoEstimatedAvgProbabilityList.append(miHoYoEstimatedAvgProbability)

        officalAvgProbabilityList.append(1.8)

        if xValue == 69:
            plt.figure(figsize=(12, 6))
            plt.bar(range(1, 81), linearStar5WhenGotcha, color='r', label='Linear')
            plt.xlabel("X")
            plt.ylabel("Estimated 5-star summon ratio (%)")
            plt.title("Estimated 5-star summon ratio")
            plt.legend()
            plt.savefig(f"./Estimated 5-star summon ratio bar linear.png")
            plt.close()

            plt.figure(figsize=(12, 6))
            plt.bar(range(1, 81), miHoYoStar5WhenGotcha, color='g', label='miHoYo')
            plt.xlabel("X")
            plt.ylabel("Estimated 5-star summon ratio (%)")
            plt.title("Estimated 5-star summon ratio")
            plt.legend()
            plt.savefig(f"./Estimated 5-star summon ratio bar mihoyo.png")
            plt.close()

    plt.figure(figsize=(12, 6))
    plt.plot(range(testFrom, testTo), linearEstimatedAvgProbabilityList, color='r', marker='o', label='Linear')
    plt.plot(range(testFrom, testTo), miHoYoEstimatedAvgProbabilityList, color='g', marker='o', label='miHoYo')
    plt.plot(range(testFrom, testTo), officalAvgProbabilityList, color='b', marker='o', label='Offical')
    plt.xlabel("X")
    plt.ylabel("Estimated 5-star summon ratio (%)")
    plt.title("Estimated 5-star summon ratio")
    plt.legend()
    plt.savefig(f"./Estimated 5-star summon ratio linear.png")
    plt.close()
        
    for i in range(1, len(linearStar5WhenGotcha)):
        linearStar5WhenGotcha[i] += linearStar5WhenGotcha[i - 1]
        miHoYoStar5WhenGotcha[i] += miHoYoStar5WhenGotcha[i - 1]

    plt.figure(figsize=(12, 6))
    plt.plot(range(1, 81), linearStar5WhenGotcha, color='r', label='Linear')
    plt.plot(range(1, 81), miHoYoStar5WhenGotcha, color='g', label='miHoYo')
    plt.xlabel("Gotcha")
    plt.ylabel("5-star summon ratio (%)")
    plt.title("5-star summon ratio")
    plt.legend()
    plt.savefig(f"./5-star summon ratio linear.png")
    plt.close()

    # for i in range(testFrom, testTo):
    #     print(f"X = {i}, Linear: {linearEstimatedAvgProbabilityList[i - testFrom]}, miHoYo: {miHoYoEstimatedAvgProbabilityList[i - testFrom]}, Offical: {officalAvgProbabilityList[i - testFrom]}")

if __name__ == "__main__":
    # X_values, Y_values, testFrom, testTo = SetXYPairLinear(40, 76)
    # GetAnswer(X_values, Y_values, testFrom, testTo, mode='linear')

    # X_values, Y_values, testFrom, testTo = SetXYPairMIHOYO(40, 76)
    # GetAnswer(X_values, Y_values, testFrom, testTo, mode='miHoYo')

    runCalculation(40, 76)
