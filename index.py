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
        
        summon = round(random.uniform(0, 1), 6) * 100
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

def SetXYPairLinear():
    # generate X, Y pair
    X_values = []
    Y_values = []
    initial = 0.8
    final = 100
    testFrom = 40
    testTo = 76
    for i in range(testFrom, testTo):
        gap = 80 - i
        X_values.append(i)
        Y_values.append((final - initial) / gap)
    return X_values, Y_values, testFrom, testTo

def SetXYPairMIHOYO():
    # generate X, Y pair
    X_values = []
    Y_values = []
    testFrom = 40
    testTo = 76
    for i in range(testFrom, testTo):
        X_values.append(i)
        Y_values.append(8)
    return X_values, Y_values, testFrom, testTo

def GetAnswer(X_values, Y_values, testFrom, testTo, mode):
    assert mode == "linear" or mode == "miHoYo", "mode should be either 'linear' or 'miHoYo'"

    threeStarRatio = list()
    fourStarRatio = list()
    fiveStarRatio = list()
    threeStarOfficalRatio = [86.2] * (testTo - testFrom)
    fourStarOfficalRatio = [12] * (testTo - testFrom)
    fiveStarOfficalRatio = [1.8] * (testTo - testFrom)
    
    for i in range(len(X_values)):
        X = X_values[i]
        Y = Y_values[i]
        totalThree = 0
        totalFour = 0
        totalFive = 0
        totalThreePerSummon = [0] * 80
        totalFourPerSummon = [0] * 80
        totalFivePerSummon = [0] * 80
        runCount = 100000
        for _ in range(runCount):
            output, threeCount, fourCount, fiveCount = runOne(X, Y)
            totalThree += threeCount
            totalFour += fourCount
            totalFive += fiveCount
            for j in range(0, 80):
                if output[j] == '3':
                    totalThreePerSummon[j] += 1
                elif output[j] == '4':
                    totalFourPerSummon[j] += 1
                elif output[j] == '5':
                    totalFivePerSummon[j] += 1
        # totalThreePerSummon = [x * 100 / runCount / 80 for x in totalThreePerSummon]
        # totalFourPerSummon = [x * 100 / runCount / 80 for x in totalFourPerSummon]
        totalFivePerSummon = [x * 100 * 100 / runCount / 80 for x in totalFivePerSummon]
        print(f"X={X}, Y={Y}%")
        print(f"3-star: {totalThree * 100 / runCount / 80}%")
        print(f"4-star: {totalFour * 100 / runCount / 80}%")
        print(f"5-star: {totalFive * 100 / runCount / 80}%")
        threeStarRatio.append(totalThree * 100 / runCount / 80)
        fourStarRatio.append(totalFour * 100 / runCount / 80)
        fiveStarRatio.append(totalFive * 100 / runCount / 80)
        print("X =", X_values[i], "finished!\n")

        # five star ratio per summon
        plt.figure()
        plt.bar(range(1, 81), totalFivePerSummon, color='b')
        plt.xlabel("Summon")
        plt.ylabel("5-star summon ratio (%)")
        plt.title("5-star summon ratio per summon")
        plt.savefig(f"./{mode.lower()}/5-star ratio per summon {mode} X={X_values[i]}.png")
        plt.close()

    # three star ratio
    plt.figure()
    plt.plot(X_values, threeStarRatio, color='r', marker='o')
    plt.plot(X_values, threeStarOfficalRatio, color='b', marker='o')
    plt.xlabel("X")
    plt.ylabel("3-star summon ratio (%)")
    plt.title("3-star summon ratio")
    plt.savefig(f"./{mode.lower()}/3-star summon ratio {mode}.png")
    plt.close()

    # four star ratio
    plt.figure()
    plt.plot(X_values, fourStarRatio, color='r', marker='o')
    plt.plot(X_values, fourStarOfficalRatio, color='b', marker='o')
    plt.xlabel("X")
    plt.ylabel("4-star summon ratio (%)")
    plt.title("4-star summon ratio")
    plt.savefig(f"./{mode.lower()}/4-star summon ratio {mode}.png")
    plt.close()

    # five star ratio
    plt.figure()
    plt.plot(X_values, fiveStarRatio, color='r', marker='o')
    plt.plot(X_values, fiveStarOfficalRatio, color='b', marker='o')
    plt.xlabel("X")
    plt.ylabel("5-star summon ratio (%)")
    plt.title("5-star summon ratio")
    plt.savefig(f"./{mode.lower()}/5-star summon ratio {mode}.png")
    plt.close()

if __name__ == "__main__":
    X_values, Y_values, testFrom, testTo = SetXYPairLinear()
    GetAnswer(X_values, Y_values, testFrom, testTo, mode='linear')

    X_values, Y_values, testFrom, testTo = SetXYPairMIHOYO()
    GetAnswer(X_values, Y_values, testFrom, testTo, mode='miHoYo')