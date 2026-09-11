"""TIL: 리스트/튜플 패킹·언패킹 (2026-09-11) — 개념 설명은 README.md 참고"""

# 언패킹(unpacking) - 리스트를 개별 변수에 나눠 담기
fruits = ["apple", "banana", "cherry"]
item1, item2, item3 = fruits

print(item1)  # apple
print(item2)  # banana
print(item3)  # cherry

# 패킹(packing) - 여러 값을 나열하면 자동으로 튜플로 묶임
data = 1, 2, 3
print(data)  # (1, 2, 3)

print("-" * 80)

# 한 줄로 여러 변수에 동시 대입 (패킹 후 언패킹)
data1, data2, data3 = 1, 2, 3
print(data1, data2, data3)

data1, data2, data3 = (1, 2, 3)
print(data1, data2, data3)