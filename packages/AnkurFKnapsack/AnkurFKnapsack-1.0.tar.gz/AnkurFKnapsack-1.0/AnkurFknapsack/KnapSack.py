

class Item:
    def __init__(self,profit,weight):
        self.profit=profit
        self.weight=weight
        self.ratio=profit/weight


def FKnapsack():
    
    item=[]
    
    print()
    n=int(input("Enter Total Number OF  Item : "))

    for i in range(1,n+1):
        print("Enter PROFIT For ITEM ",i," : ",end="")
        p=int(input())
        print("Enter WEIGHT For ITEM ",i," : ",end="")
        w=int(input())
        item.append(Item(p,w))

    print()
    capacity=int(input("ENTER CAPACITY : "))
    item.sort(key=lambda x: x.ratio , reverse=True)

    total_value=0.0

    for items in item:
        if capacity >= items.weight:
            capacity-=items.weight
            total_value += items.profit
        else:
            total_value += items.ratio * capacity
            break
    
    print()
    print("FRACTIONAL KNAPSACK : GREEDY APPROACH")
    print("-----------------------------------")
    print("MAX PROFIT : ",total_value)
    print("-----------------------------------")
    print()
    print()

