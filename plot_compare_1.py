
import pickle
import matplotlib.pyplot as plt

# 设置中文字体（若本地支持，否则可注释）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取性能测试结果文件
with open("result_1.pkl", "rb") as f:
    results = pickle.load(f)

ecc_times = results["ECC"]
rsa_times = results["RSA"]

# X轴标签
run_labels = ["10x100B", "50x100B", "100x100B", "500x100B", "1000x100B"]
length_labels = ["500x1B", "500x100B", "500x1KB", "500x5KB", "500x10KB"]

# -------- 图一：执行次数变化对性能影响 --------
plt.figure(figsize=(10, 6))
plt.plot(run_labels, ecc_times[:5], marker='o', label='ECC', color='orange')
plt.plot(run_labels, rsa_times[:5], marker='s', label='RSA', color='orangered')
plt.title("执行次数变化下的代理重加密性能对比")
plt.xlabel("加密次数 × 消息长度")
plt.ylabel("总执行时间（秒）")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("performance_by_runs.png")
plt.show()

# -------- 图二：消息长度变化对性能影响 --------
plt.figure(figsize=(10, 6))
plt.plot(length_labels, ecc_times[5:], marker='o', label='ECC', color='orange')
plt.plot(length_labels, rsa_times[5:], marker='s', label='RSA', color='orangered')
plt.title("消息长度变化下的代理重加密性能对比")
plt.xlabel("固定加密次数 × 消息长度")
plt.ylabel("总执行时间（秒）")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("performance_by_msglen.png")
plt.show()
