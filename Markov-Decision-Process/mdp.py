import sys
import collections
import numpy as np
import time

# from typing import List, Any

gird_size = 0  # type: int
number_of_cars = 0  # type: int
number_of_obstacles = 0  # type: int
location_of_obstacles = []  # type: List[Any]
location_of_car_start = []
location_of_car_terminal = []
gameBoard = {}
cost_of_moving = -1
destination_reward = 100
obstacle_reward = -100
validStates = []
gamma = 0.9
epsilon = 0.1
compareEpsilon = epsilon * (1 - gamma) / gamma
a = ""

# global grid_size, number_of_cars, number_of_obstacles,location_of_obstacles,location_of_car_start,location_of_car_terminal,gameBoard

def RewardCalulation(grid_size, location_of_obstacles, location_of_car_terminal):
    global cost_of_moving, destination_reward,obstacle_reward
    for i in range(0,grid_size):
        for j in range(0, grid_size):
            gameBoard[tuple((j,i))] = cost_of_moving
    for obstacle in location_of_obstacles:
        gameBoard[obstacle] = gameBoard[obstacle] + obstacle_reward
        # print(obstacle)
    gameBoard[location_of_car_terminal] =  gameBoard[location_of_car_terminal] + destination_reward
    # print(gameBoard)
    return gameBoard


def parseFile():
    global grid_size, number_of_cars, number_of_obstacles,location_of_obstacles,location_of_car_start,location_of_car_terminal
    f = open("/Users/parth/Downloads/grading_case/input14.txt")
    lines = f.readlines()
    lines = map(lambda each: each.strip("\r\n"), lines)
    grid_size = int(lines[0])
    # print(grid_size)
    number_of_cars = lines[1]
    # print(number_of_cars)
    number_of_obstacles = lines[2]
    # print(number_of_obstacles)
    j = 3
    for i in range(j, j + int(number_of_obstacles)):
        temp_obstacle_list = lines[i].split(",")
        location_of_obstacles.append(tuple((int(temp_obstacle_list[0]),int(temp_obstacle_list[1]))))
        # print(location_of_obstacles)
    j = j + int(number_of_obstacles)
    for i in range(j, j + int(number_of_cars)):
        temp_car_list = lines[i].split(",")
        location_of_car_start.append(tuple((int(temp_car_list[0]), int(temp_car_list[1]))))
        # print(location_of_car_start)
    j = j + int(number_of_cars)
    for i in range(j, j + int(number_of_cars)):
        temp_car_list_terminal = lines[i].split(",")
        location_of_car_terminal.append(tuple((int(temp_car_list_terminal[0]), int(temp_car_list_terminal[1]))))
    # print(location_of_car_terminal)
    # print(lines)

def UtilityCalulation(init_reward, location_of_car_terminal):
    global validStates, gamma, compareEpsilon
    # print(location_of_car_terminal)
    validStates = init_reward.keys()
    possibleDirections = ["North", "South", "East", "West"]
    # print(validStates)
    # print(init_reward)
    utilNew = {}
    policyNew = {}
    for state in validStates:
        utilNew[state] = 0
        policyNew[state] = 0

    # print(util1)
    # print(init_reward[(0, 1)])


    while True:
        util = utilNew.copy()
        policy = policyNew.copy()
        delta = 0
        for state in validStates:
            if state == location_of_car_terminal:
                continue
            # [N,S,E,W]
            list_of_all_direction =allDirectionValueCalculation(state,util)
            # print(list_of_all_direction)
            # partemp = tuple((700,900))
            # if state == partemp:
            #     print(state)
            #     print(list_of_all_direction)
            maximumValueForCell = max(list_of_all_direction)
            # maximumValueForCellDirection = max(list_of_all_direction, key=lambda item:item[0])
            maximumValueForCellDirection = possibleDirections[list_of_all_direction.index(maximumValueForCell)]
            cellValue = init_reward[state] + (gamma * maximumValueForCell)
            utilNew[state] = cellValue
            policyNew[state] = maximumValueForCellDirection
            # print(state, " ", maximumValueForCellDirection)
        utilNew[location_of_car_terminal] = init_reward[location_of_car_terminal]

        for cell in util:
            delta = max(delta, abs(utilNew[cell] - util[cell]))

        # print("OK")
        # print(policyNew)
        if delta < compareEpsilon:
            # print(policy)
            # print(util)
            return policy

def turn_left(direction):
   if direction == "North":
       return "West"
   if direction == "South":
       return "East"
   if direction == "East":
       return "North"
   if direction == "West":
       return "South"

def turn_right(direction):
    if direction == "North":
        return "East"
    if direction == "South":
        return "West"
    if direction == "East":
        return "South"
    if direction == "West":
        return "North"


def go(state,direction):
    global validStates
    if direction == "North":
        newState = tuple((state[0],state[1]-1))
    elif direction == "South":
        newState = tuple((state[0], state[1] + 1))
    elif direction == "East":
        newState = tuple((state[0] + 1, state[1]))
    elif direction == "West":
        newState = tuple((state[0] - 1, state[1]))

    # print(state)

    if newState in validStates:
        # print(newState, " ", direction)
        return newState
    # print(state, " ", direction)
    return state


def allDirectionValueCalculation(state,util):
    possibleDirections = ["North", "South", "East", "West"]
    directionValuesList = []
    for direction in possibleDirections:
        if direction == "North":
            directionValue = np.float64((0.7 * util[go(state,"North")]) + (0.1 * util[go(state,"East")]) + (0.1 * util[go(state,"West")]) + (0.1 * util[go(state,"South")]))
        elif direction == "South":
            directionValue = np.float64((0.7 * util[go(state, "South")]) + (0.1 * util[go(state, "East")]) + (
                        0.1 * util[go(state, "West")]) + (0.1 * util[go(state, "North")]))
        elif direction == "East":
            directionValue = np.float64((0.7 * util[go(state, "East")]) + (0.1 * util[go(state, "North")]) + (
                        0.1 * util[go(state, "West")]) + (0.1 * util[go(state, "South")]))
        elif direction == "West":
            directionValue = np.float64((0.7 * util[go(state, "West")]) + (0.1 * util[go(state, "East")]) + (
                        0.1 * util[go(state, "North")]) + (0.1 * util[go(state, "South")]))
        directionValuesList.append(directionValue)
        # print(directionValue)
    # print(directionValuesList)
    return directionValuesList


def CarSimulation(finalPolicyList,initialRewardList):
    global number_of_cars, location_of_car_start, location_of_car_terminal
    b = initialRewardList
    # print(b)
    rew = np.zeros(shape=(int(number_of_cars),10))
    # print(rew)
    for car in range(0,int(number_of_cars)):
        for j in range(10):
            pos = location_of_car_start[car]
            np.random.seed(j)
            swerve = np.random.random_sample(1000000)
            k = 0
            if pos == location_of_car_terminal[car]:
                rew[car][j] = 100
            else:
                while pos != location_of_car_terminal[car]:
                    move = finalPolicyList[car][pos]
                    if swerve[k] > 0.7:
                        if swerve[k] > 0.8:
                            if swerve[k] > 0.9:
                                move = turn_left(turn_left(move))
                            else:
                                move = turn_right(move)
                        else:
                            move = turn_left(move)
                    pos = go(pos,move)
                    rew[car][j] += initialRewardList[car][pos]
                    # print(initialRewardList[pos])
                    k = k + 1
                # print(pos)
        # print("\n\n\n\n")
    b = np.floor(np.mean(rew, axis=1))
    c = b.astype(int)
    print (c)
    writeToFile(c)

def writeToFile(c):
    global a
    for val in c:
        a += str(val) + "\n"
    with open("output.txt", "w") as f:
        f.write(a)


def main():
    t1 = time.time()
    parseFile()
    final_policy_list = []
    initial_reward_list = []
    # print(location_of_car_terminal)
    for i in range(0, int(number_of_cars)):
        initial_reward = RewardCalulation(grid_size, location_of_obstacles, location_of_car_terminal[i])
        initial_reward_list.append(initial_reward.copy())
        # print(initial_reward)
        final_policy = UtilityCalulation(initial_reward.copy(), location_of_car_terminal[i])
        final_policy_list.append(final_policy.copy())
        initial_reward = {}
    CarSimulation(final_policy_list[:],initial_reward_list[:])
    # print("\n\n\n\n\n")

    # print location_of_car_start
        # print(initial_reward)
        # print(validStates)
    print(time.time() - t1)





if __name__ == "__main__":
    # print(np.info())
    main()
