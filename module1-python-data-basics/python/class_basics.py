"""TIL: 클래스, 상속, 메서드 오버라이딩 (2026-09-11) — 개념 설명은 README.md 참고"""

# "Customer(고객)"라는 이름의 커스텀 자료형(클래스) 만들기
class Customer:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def purchase(self, price, product_name):
        print(f"{self.name} 고객님이 {price}원 상당의 {product_name}제품을 구매하셨습니다.")

# Customer 클래스 이용 -> 구체적인 데이터(객체) 생성
client1 = Customer(name="김철수", age=24, gender="남성")
client2 = Customer(name="홍길동", age=52, gender="남성")
client3 = Customer(name="이미도", age=35, gender="여성")

# 데이터 꺼내기
print(client1.name)
print(client2.age)
print(client3.gender)

# 전용 기능(메서드) 실행
client1.purchase(900000, "아이패드")

# 자식 클래스 생성 및 메서드 오버라이딩
class VIPCustomer(Customer):
    def __init__(self, name, age, gender, discount_rate=0.1):
        super().__init__(name, age, gender)
        self.discount_rate = discount_rate

    def purchase(self, price, product_name):
        discount_price = int(price * (1 - self.discount_rate))
        print(f"[VIP] {self.name} 고객님이 {self.discount_rate*100:.0f}% 할인받아 {discount_price:,}원에 {product_name}를 구매하셨습니다.")

# 일반 고객(부모)와 VIP 고객(자식) 객체 생성
vip_customer = VIPCustomer(name="김짱구", age=5, gender="여성", discount_rate=0.2)

# 기본 메서드(부모) vs 오버라이딩 메서드(자식) 비교
client2.purchase(price=100000, product_name="아이패드")
print("-" * 80)
vip_customer.purchase(price=1000000, product_name="아이패드")