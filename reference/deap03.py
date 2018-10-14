# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 12:39:30 2018
@author: Ping-Chen Lin revised
"""
import random
import math
from deap import base
from deap import creator
from deap import tools
import matplotlib.pyplot as plt
import numpy as np
#設定極大化適應函數
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
#設定染色體為list資料型別
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
#編碼方式採用亂數整數0或1內容值方式 
toolbox.register("attr_bool", random.randint, 0, 1)
# 初始化設定, 染色體基因素設5
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_bool, 5) #染色體基因個數
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#適應函數
def evalOneMax(individual):
    indstr = ''
    for i in range(0, len(individual)):
        indstr = indstr + str(individual[i])
    decvalue = int(indstr,2)
    fitnessvalue = int(math.pow(decvalue,2))
    return fitnessvalue,
#畫圖
def showplot(fitmena):
    x = np.arange(1, len(fitmean)+1)
    y = fitmean
    l = plt.plot(x, y, 'ro')
    plt.setp(l, markersize=8)
    plt.setp(l, markerfacecolor='C0')
    plt.title('Average fitness value per generation ')
    plt.xlabel('Generations')
    plt.ylabel('Fitness value')          
    plt.show()
#設定執行那個適應函數
toolbox.register("evaluate", evalOneMax)
#設定2點交配
toolbox.register("mate", tools.cxTwoPoint)
#設定字完反轉的突變方法
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
#設定tournament選擇方法
toolbox.register("select", tools.selTournament, tournsize=3)
#主程式
def main(terminal, fitmean):
    #設定族群大小
    pop = toolbox.population(n=50) #放群大小
    # 評估一代的所有族群染色體的適應函數值
    fitnesses = list(map(toolbox.evaluate, pop))
    print(fitnesses)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    # CXPB  是兩條染色體被選做交配的機率
    # MUTPB 是個別染色體逐一基因被選做突變的機率
    CXPB, MUTPB = 0.5, 0.2 
    # 取出所有染色體的適應函數值
    fits = [ind.fitness.values[0] for ind in pop]
    # g做為代數的追踪變數
    g = 0
    # 開始進迴圈演化
    while max(fits) < 1000 and g < terminal:
        # 下一代
        g = g + 1
        print("-- Generation %i --" % g)
        # 選出下一代的族群
        offspring = toolbox.select(pop, len(pop))
        # 繁殖被選到的染色體
        offspring = list(map(toolbox.clone, offspring))
        # 子代做交配與突變
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # 評估適應力差的染色體(沒有被選上為下一代的染色體)
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        pop[:] = offspring
        #收集所有染色體的適應函數值於list再印出統計數據
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        fitmean.append(mean)
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
if __name__ == "__main__":  
    #結束代數
    terminal = 30
    #每代平均代數
    fitmean=[]
    p = main(terminal, fitmean) 
    showplot(fitmean)
