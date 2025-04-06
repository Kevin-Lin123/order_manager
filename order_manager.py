# order_manager.py
import json
from typing import List, Dict, Tuple

# 常數定義
INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"

def load_data(filename: str) -> List[Dict]:
    """載入JSON訂單資料"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_orders(filename: str, orders: List[Dict]) -> None:
    """儲存訂單到JSON檔案"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=4, ensure_ascii=False)

def calculate_order_total(order: Dict) -> int:
    """計算訂單總金額"""
    return sum(item["price"] * item["quantity"] for item in order["items"])

def process_order(orders: List[Dict]) -> Tuple[str, Dict]:
    """處理出餐流程"""
    if not orders:
        return "目前沒有待處理訂單。", None

    print("\n======== 待處理訂單列表 ========")
    for i, order in enumerate(orders, 1):
        print(f"{i}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("================================")

    choice = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ").strip()
    if not choice:
        return "出餐流程已取消。", None

    try:
        index = int(choice) - 1
        if 0 <= index < len(orders):
            completed_order = orders.pop(index)
            existing_output = load_data(OUTPUT_FILE)
            save_orders(OUTPUT_FILE, existing_output + [completed_order])
            save_orders(INPUT_FILE, orders)
            return f"訂單 {completed_order['order_id']} 已出餐完成", completed_order
        raise IndexError
    except (ValueError, IndexError):
        return "錯誤：請輸入有效的訂單編號", None

def add_order(orders: List[Dict]) -> str:
    """新增訂單功能"""
    order_id = input("請輸入訂單編號: ").strip().upper()
    if not order_id:
        return "錯誤：訂單編號不可為空"

    if any(o["order_id"] == order_id for o in orders):
        return f"錯誤：訂單編號 {order_id} 已存在"

    customer = input("請輸入顧客姓名: ").strip()
    if not customer:
        return "錯誤：顧客姓名不可為空"

    items = []
    while True:
        name = input("請輸入餐點名稱（直接按 Enter 結束輸入）: ").strip()
        if not name:
            if len(items) == 0:
                print("錯誤：至少需要一項餐點")
                continue
            break

        try:
            price = int(input("請輸入單價: "))
            if price < 0:
                raise ValueError("價格不可為負數")

            quantity = int(input("請輸入數量: "))
            if quantity <= 0:
                raise ValueError("數量必須大於零")

            items.append({"name": name, "price": price, "quantity": quantity})
        except ValueError as e:
            print(f"輸入錯誤: {e}")

    new_order = {
        "order_id": order_id,
        "customer": customer,
        "items": items
    }
    orders.append(new_order)
    save_orders(INPUT_FILE, orders)
    return f"訂單 {order_id} 新增成功"

def print_order_report(orders: List[Dict], title: str = "訂單報表") -> None:
    """顯示訂單報表"""
    print(f"\n{'=' * 24} {title} {'=' * 24}")
    for order in orders:
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("-" * 60)
        print(f"{'品項名稱':<10}{'單價':>8}{'數量':>10}{'小計':>15}")
        print("-" * 60)
        for item in order["items"]:
            subtotal = item["price"] * item["quantity"]
            print(f"{item['name']:<12}{item['price']:>8,}{item['quantity']:>10}{subtotal:>15,}")
        print("-" * 60)
        print(f"訂單總額: {calculate_order_total(order):,}元")
        print("=" * 60 + "\n")

def main_menu() -> None:
    """主選單控制流程"""
    orders = load_data(INPUT_FILE)

    while True:
        print("\n" + "=" * 15 + " 訂單管理系統 " + "=" * 15)
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開系統")
        print("=" * 40)

        choice = input("請輸入選項: ").strip()

        if not choice or choice == "4":
            print("系統已關閉")
            break

        if choice == "1":
            result = add_order(orders)
            print("\n" + "=" * 60)
            print(result)
            print("=" * 60)
        elif choice == "2":
            print_order_report(orders)
        elif choice == "3":
            msg, order = process_order(orders)
            print("\n" + "=" * 60)
            print(msg)
            if order:
                print_order_report([order], "出餐明細")
            print("=" * 60)
        else:
            print("錯誤：無效的選項，請輸入 1-4")

if __name__ == "__main__":
    main_menu()