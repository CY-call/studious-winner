import os
import sys

# 请在此输入您的代码
bool = 2025
count = 0
while bool > 0:
    count += 1
    bool -= 5
    if count % 2 == 1:
        bool -= 15
    else:
        bool -= 2
    if count % 3 == 1:
        bool -= 2
    elif count % 3 == 2:
        bool -= 10
    else:
        bool -= 7
print(count)
