import random
import sys


def generate_random_number():
    """生成1-100之间的随机整数"""
    return random.randint(1, 100)


def get_user_input():
    """处理用户输入，返回猜测的数字或退出信号
    
    返回值:
        int: 用户输入的有效数字
        None: 用户输入"退出"结束程序
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
                print("错误：请输入1-100之间的整数！")
        except ValueError:
            print("错误：输入无效，请输入数字或'退出'！")


def play_game():
    """猜数字游戏主逻辑"""
    while True:
        target_number = generate_random_number()
        guess_count = 0
        
        print("\n=== 猜数字小游戏开始 ===")
        print("系统已生成1-100之间的整数，开始猜测吧！")
        
        while True:
            guess = get_user_input()
            
            if guess is None:
                print("游戏已退出，欢迎下次再来！")
                sys.exit()
            
            guess_count += 1
            
            if guess < target_number:
                print("猜小了！")
            elif guess > target_number:
                print("猜大了！")
            else:
                print(f"恭喜你猜对了！正确数字是{target_number}")
                print(f"你一共猜了{guess_count}次！")
                break
        
        if not play_again():
            print("游戏结束，感谢参与！")
            break


def play_again():
    """询问用户是否重新开始游戏
    
    返回值:
        bool: True表示重新开始，False表示结束游戏
    """
    while True:
        choice = input("是否重新开始游戏？(Y/N)：").strip().upper()
        if choice == "Y":
            return True
        elif choice == "N":
            return False
        else:
            print("请输入Y或N！")


if __name__ == "__main__":
    play_game()
