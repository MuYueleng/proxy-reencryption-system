
import time
import random
import string
import pickle
from tqdm import tqdm
from gui import proxy_re_encryption  # 确保 proxy_re_encryption 函数可导入

def generate_message(length):
    """生成指定长度的随机消息"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def benchmark(method, run_counts, message_lengths):
    """性能测试核心函数"""
    total_time_by_run = []
    total_time_by_length = []

    print(f"\n>>> Testing {method} - Varying run counts (fixed message length: 100)")
    for runs in run_counts:
        start = time.time()
        for _ in tqdm(range(runs), desc=f"{method} {runs} runs"):
            msg = generate_message(100)
            proxy_re_encryption(msg, method)
        end = time.time()
        total_time_by_run.append(end - start)

    print(f"\n>>> Testing {method} - Varying message lengths (fixed run count: 500)")
    for msg_len in message_lengths:
        start = time.time()
        for _ in tqdm(range(500), desc=f"{method} 500x{msg_len}B"):
            msg = generate_message(msg_len)
            proxy_re_encryption(msg, method)
        end = time.time()
        total_time_by_length.append(end - start)

    return total_time_by_run + total_time_by_length

def main():
    run_counts = [10, 50, 100, 500, 1000]         # 测试次数维度
    message_lengths = [1, 100, 1024, 5120, 10240] # 测试消息长度维度（B）

    results = {
        'ECC': benchmark('ECC', run_counts, message_lengths),
        'RSA': benchmark('RSA', run_counts, message_lengths)
    }

    with open('result_1.pkl', 'wb') as f:
        pickle.dump(results, f)

    print("\nPerformance testing completed and results saved to results_1.pkl.")

if __name__ == '__main__':
    main()
