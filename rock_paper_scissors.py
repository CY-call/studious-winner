import random


def generate_computer_choice():
    """生成电脑的随机出拳
    
    返回值:
        str: 电脑出拳结果（石头/剪刀/布）
    """
    choices = ["石头", "剪刀", "布"]
    return random.choice(choices)


def normalize_input(user_input):
    """标准化用户输入，兼容中文和拼音大小写
    
    参数:
        user_input: 用户原始输入
    返回值:
        str: 标准化后的输入（石头/剪刀/布）或 None（退出）
    """
    user_input = user_input.strip().lower()
    
    if user_input == "退出":
        return None
    
    input_map = {
        "石头": "石头", "shitou": "石头", "st": "石头",
        "剪刀": "剪刀", "jiandao": "剪刀", "jd": "剪刀",
        "布": "布", "bu": "布"
    }
    
    return input_map.get(user_input)


def judge_result(user_choice, computer_choice):
    """判断比赛结果
    
    参数:
        user_choice: 用户出拳
        computer_choice: 电脑出拳
    返回值:
        str: 比赛结果（赢/输/平局）
    """
    if user_choice == computer_choice:
        return "平局"
    
    win_conditions = {
        "石头": "剪刀",
        "剪刀": "布",
        "布": "石头"
    }
    
    if win_conditions[user_choice] == computer_choice:
        return "赢"
    else:
        return "输"


def play_game():
    """石头剪刀布游戏主循环"""
    stats = {"赢": 0, "输": 0, "平局": 0}
    
    print("=" * 30)
    print("欢迎来到石头剪刀布小游戏！")
    print("支持输入：石头/剪刀/布 或拼音(shitou/jiandao/bu)")
    print("输入'退出'结束游戏")
    print("=" * 30)
    
    while True:
        user_input = input("\n请出拳：")
        user_choice = normalize_input(user_input)
        
        if user_choice is None:
            print(f"\n游戏结束！最终战绩：赢{stats['赢']} 输{stats['输']} 平局{stats['平局']}")
            print("感谢参与！")
            break
        
        if user_choice not in ["石头", "剪刀", "布"]:
            print("错误：请输入石头/剪刀/布 或拼音！")
            continue
        
        computer_choice = generate_computer_choice()
        result = judge_result(user_choice, computer_choice)
        
        print(f"你出了：{user_choice}")
        print(f"电脑出了：{computer_choice}")
        
        if result == "赢":
            print("🎉 恭喜！你赢了！")
        elif result == "输":
            print("😔 很遗憾，你输了！")
        else:
            print("🤝 平局！")
        
        stats[result] += 1
        print(f"当前战绩：赢{stats['赢']} 输{stats['输']} 平局{stats['平局']}")
        
        while True:
            continue_choice = input("是否继续游戏？(Y/N)：").strip().upper()
            if continue_choice == "N":
                print(f"\n游戏结束！最终战绩：赢{stats['赢']} 输{stats['输']} 平局{stats['平局']}")
                print("感谢参与！")
                return
            elif continue_choice == "Y":
                break
            else:
                print("请输入Y或N！")


if __name__ == "__main__":
    play_game()
