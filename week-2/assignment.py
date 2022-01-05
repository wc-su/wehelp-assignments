# 要求一:函式與流程控制
# 在函式中使用迴圈計算最小值到最大值之間，所有整數的總和
def calculate(min, max):
    # 請用你的程式補完這個函式的區塊
    total = 0
    for i in range(min, max + 1):
        total += i
    print(total)
calculate(1, 3) # 你的程式要能夠計算 1+2+3，最後印出 6
calculate(4, 8) # 你的程式要能夠計算 4+5+6+7+8，最後印出 30


# 要求二:Python 字典與列表、JavaScript 物件與陣列
# 正確計算出員工的平均薪資，請考慮員工數量會變動的情況
def avg(data):
    avgSalary = 0
    for item in data["employees"]:
        avgSalary += item["salary"];
    avgSalary = avgSalary / data["count"]
    print(avgSalary)
avg({
    "count":3,
    "employees":[
        {
            "name":"John",
            "salary":30000
        },
        {
            "name":"Bob",
            "salary":60000
        },
        {
            "name":"Jenny",
            "salary":50000
        }
    ]
}) # 呼叫 avg 函式


# 要求三:演算法
# 找出至少包含兩筆整數的列表 (Python) 或陣列 (JavaScript) 中，兩兩數字相乘後的最大值
def maxProduct(nums):
    nums.sort(reverse = True)
    print(nums[0] * nums[1])
maxProduct([5, 20, 2, 6]) # 得到 120
maxProduct([10, -20, 0, 3]) # 得到 30
maxProduct([-1, 2]) # 得到 -2
maxProduct([-1, 0, 2]) # 得到 0


# 要求四 ( 請閱讀英文 ):演算法
def twoSum(nums, target):
    result = []
    subtract = None;
    for indexX, num in enumerate(nums):
        subtract = target - num;
        for indexY in range(indexX + 1, len(nums)):
            if(subtract == nums[indexY]):
                result.append(indexX)
                result.append(indexY)
                break
        if(len(result) == 2):
            break;
    return result
result=twoSum([2, 11, 7, 15], 9)
print(result) # show [0, 2] because nums[0]+nums[2] is 9


# 要求五 ( Optional ):演算法
# 計算連續出現 0 的最大長度
def maxZeros(nums):
    count = 0
    maxCount = 0
    for num in nums:
        if(num == 0):
            count += 1
        else:
            if(maxCount < count):
                maxCount = count
            count = 0
    if(maxCount < count):
        maxCount = count
    print(maxCount)
maxZeros([0, 1, 0, 0]) # 得到 2
maxZeros([1, 0, 0, 0, 0, 1, 0, 1, 0, 0]) # 得到 4
maxZeros([1, 1, 1, 1, 1]) # 得到 0
maxZeros([0, 0, 0, 1, 1]) # 得到 3