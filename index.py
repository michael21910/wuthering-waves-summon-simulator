import random
import matplotlib.pyplot as plt

def setGap(testFrom, testTo, addProbability, garenteed5StarCount, initial5StarProbability):
    gapLinear = [round((100 - initial5StarProbability) / (garenteed5StarCount - x), 10) for x in range(testFrom, testTo)]
    gapFixedLinear = [addProbability] * 80
    return gapLinear, gapFixedLinear

def runCalculation(testFrom, testTo, addProbability, garenteed5StarCount, initial5StarProbability, officalAverage5StarProbability):
    gapLinear, gapFixedLinear = setGap(testFrom, testTo, addProbability, garenteed5StarCount, initial5StarProbability)

    linearEstimatedAvgProbabilityList = list()
    FixedLinearEstimatedAvgProbabilityList = list()
    officalAvgProbabilityList = list()
    for xValue in range(testFrom, testTo):
        # linear
        linearStar5Probability = [initial5StarProbability] * xValue + [initial5StarProbability + gapLinear[xValue - testFrom] * (x + 1) for x in range(garenteed5StarCount - xValue)]
        linearStar5Probability[-1] = 100
        linearNotStar5Probability = [100 - x for x in linearStar5Probability]
        linearStar5WhenGotcha = [1] * garenteed5StarCount
        for i in range(1, garenteed5StarCount + 1):
            for j in range(i - 1):
                linearStar5WhenGotcha[i - 1] *= linearNotStar5Probability[j] / 100
            linearStar5WhenGotcha[i - 1] *= linearStar5Probability[i - 1] / 100
            linearStar5WhenGotcha[i - 1] *= 100
        linearExpectationValue = [linearStar5WhenGotcha[i] * (i + 1) / 100 for i in range(0, garenteed5StarCount)]
        linearFinalExpectationValue = sum(linearExpectationValue)
        linearEstimatedAvgProbability = 100 / linearFinalExpectationValue
        linearEstimatedAvgProbabilityList.append(linearEstimatedAvgProbability)

        # FixedLinear
        FixedLinearStar5Probability = [initial5StarProbability] * xValue + [initial5StarProbability + gapFixedLinear[x] * (x + 1) for x in range(garenteed5StarCount - xValue)]
        FixedLinearStar5Probability[-1] = 100
        FixedLinearNotStar5Probability = [100 - x for x in FixedLinearStar5Probability]
        FixedLinearStar5WhenGotcha = [1] * garenteed5StarCount
        for i in range(1, garenteed5StarCount + 1):
            for j in range(i - 1):
                FixedLinearStar5WhenGotcha[i - 1] *= FixedLinearNotStar5Probability[j] / 100
            FixedLinearStar5WhenGotcha[i - 1] *= FixedLinearStar5Probability[i - 1] / 100
            FixedLinearStar5WhenGotcha[i - 1] *= 100
        FixedLinearExpectationValue = [FixedLinearStar5WhenGotcha[i] * (i + 1) / 100 for i in range(0, garenteed5StarCount)]
        FixedLinearFinalExpectationValue = sum(FixedLinearExpectationValue)
        FixedLinearEstimatedAvgProbability = 100 / FixedLinearFinalExpectationValue
        FixedLinearEstimatedAvgProbabilityList.append(FixedLinearEstimatedAvgProbability)

        officalAvgProbabilityList.append(officalAverage5StarProbability)

        # if xValue == 69:
        #     plt.figure(figsize=(12, 6))
        #     plt.bar(range(1, 91), linearStar5WhenGotcha, color='r', label='Linear')
        #     plt.xlabel("X")
        #     plt.ylabel("Estimated 5-star summon ratio (%)")
        #     plt.title("Estimated 5-star summon ratio")
        #     plt.legend()
        #     plt.savefig(f"./Estimated 5-star summon ratio bar linear.png")
        #     plt.close()

        #     plt.figure(figsize=(12, 6))
        #     plt.bar(range(1, 91), FixedLinearStar5WhenGotcha, color='g', label='FixedLinear')
        #     plt.xlabel("X")
        #     plt.ylabel("Estimated 5-star summon ratio (%)")
        #     plt.title("Estimated 5-star summon ratio")
        #     plt.legend()
        #     plt.savefig(f"./Estimated 5-star summon ratio bar mihoyo.png")
        #     plt.close()

    plt.figure(figsize=(12, 6))
    plt.plot(range(testFrom, testTo), linearEstimatedAvgProbabilityList, color='r', marker='o', label='Linear')
    plt.plot(range(testFrom, testTo), FixedLinearEstimatedAvgProbabilityList, color='g', marker='o', label='FixedLinear')
    plt.plot(range(testFrom, testTo), officalAvgProbabilityList, color='b', marker='o', label='Offical')
    plt.xlabel("X")
    plt.ylabel("Estimated 5-star summon ratio (%)")
    plt.title("Estimated 5-star summon ratio")
    plt.legend()
    plt.savefig(f"./Estimated 5-star summon ratio linear.png")
    plt.close()
        
    for i in range(1, len(linearStar5WhenGotcha)):
        linearStar5WhenGotcha[i] += linearStar5WhenGotcha[i - 1]
        FixedLinearStar5WhenGotcha[i] += FixedLinearStar5WhenGotcha[i - 1]

    plt.figure(figsize=(12, 6))
    plt.plot(range(1, garenteed5StarCount + 1), linearStar5WhenGotcha, color='r', label='Linear')
    plt.plot(range(1, garenteed5StarCount + 1), FixedLinearStar5WhenGotcha, color='g', label='FixedLinear')
    plt.xlabel("Gotcha")
    plt.ylabel("5-star summon ratio (%)")
    plt.title("5-star summon ratio")
    plt.legend()
    plt.savefig(f"./5-star summon ratio linear.png")
    plt.close()

    print(f"Linear: {linearEstimatedAvgProbabilityList}")
    print(f"FixedLinear: {FixedLinearEstimatedAvgProbabilityList}")

if __name__ == "__main__":
    runCalculation(
        testFrom = 60,
        testTo = 75,
        addProbability = 8,
        garenteed5StarCount = 80,
        initial5StarProbability = 0.8,
        officalAverage5StarProbability = 1.8
    )