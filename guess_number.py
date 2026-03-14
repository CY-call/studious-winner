import random
import sys


def generate_random_number():
    """生成1-100之间的随机整数
    
    返回值:
        int: 1到100之间的随机整数
    """
    return random.randint(1, 100)


def get_user_input():
    """处理用户输入，验证并返回有效数字或退出信号
    
    返回值:
        int: 用户输入的有效数字（1-100之间）
        None: 用户输入"退出"，表示要结束程序
    """
    while True:
        user_input = input("请输入1-100之间的整数（或输入'退出'结束）：").strip()
        
        if user_input == "退出":
            return None
        
        try:
            guess = int(user_input)
            if 1 <= guess <= 100:
                return guess
            else:
                print("提示：请输入1-100之间的整数！")
        except ValueError:
            print("提示：输入无效，请输入数字或'退出'！")


def play_game():
    """猜数字游戏主逻辑"""
    while True:
        target_number = generate_random_number()
        guess_count = 0
        
        print("\n" + "=" * 30)
        print("=== 猜数字小游戏开始 ===")
        print("系统已生成1-100之间的整数")
        print("=" * 30 + "\n")
        
        while True:
            guess = get_user_input()
            
            if guess is None:
                print("\n游戏已退出，欢迎下次再来！")
                sys.exit()
            
            guess_count += 1
            
            if guess < target_number:
                print("猜小了！")
            elif guess > target_number:
                print("猜大了！")
            else:
                print(f"\n🎉 恭喜你猜对了！")
                print(f"正确数字是：{target_number}")
                print(f"你一共猜了：{guess_count} 次！")
                break
        
        if not play_again():
            print("\n游戏结束，感谢参与！")
            break


def play_again():
    """询问用户是否重新开始游戏
    
    返回值:
        bool: True表示重新开始，False表示结束游戏
    """
    while True:
        choice = input("\n是否重新开始游戏？(Y/N)：").strip().upper()
        if choice == "Y":
            return True
        elif choice == "N":
            return False
        else:
            print("提示：请输入Y或N！")


if __name__ == "__main__":
    play_game()
