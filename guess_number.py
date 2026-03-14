import random
import sys


def generate_random_number():
    """生成1-100之间的随机整数"""
    return random.randint(1, 100)


def get_user_input():
    """处理用户输入，返回有效数字或None表示退出"""
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
        target = generate_random_number()
        count = 0
        
        print("\n" + "=" * 30)
        print("=== 猜数字小游戏开始 ===")
        print("系统已生成1-100之间的整数")
        print("=" * 30 + "\n")
        
        while True:
            guess = get_user_input()
            
            if guess is None:
                print("\n游戏已退出，欢迎下次再来！")
                sys.exit()
            
            count += 1
            
            if guess < target:
                print("猜小了！")
            elif guess > target:
                print("猜大了！")
            else:
                print(f"\n🎉 恭喜你猜对了！")
                print(f"正确数字：{target}")
                print(f"猜测次数：{count} 次")
                break
        
        if not ask_play_again():
            print("\n游戏结束，感谢参与！")
            break


def ask_play_again():
    """询问是否重新开始游戏"""
    while True:
        choice = input("\n是否重新开始？(Y/N)：").strip().upper()
        if choice == "Y":
            return True
        elif choice == "N":
            return False
        else:
            print("提示：请输入Y或N！")


if __name__ == "__main__":
    play_game()
