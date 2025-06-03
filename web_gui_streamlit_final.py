
import streamlit as st
import subprocess
import time
import json
from rsa_pre import rsa_run

# ------------------ ECC 和 RSA 主流程 ------------------
def ecc_return(message):
    run_process = subprocess.run(["./main", message], capture_output=True, text=True)
    if run_process.returncode != 0:
        st.error("ECC main.go execution failed")
        st.text(run_process.stdout)
        st.text(run_process.stderr)

    with open('ecc_pre.json') as f:
        data = json.load(f)

    return data['cipher_text'], data['rk'], data['plain_text']

def proxy_re_encryption(message, method):
    start_t = time.time()
    if method == 'ECC':
        alice_encrypted, proxy_re_encrypted, bob_decrypted = ecc_return(message)
    else:
        alice_encrypted, proxy_re_encrypted, bob_decrypted = rsa_run(message, 'qdm3')
    use_time = time.time() - start_t
    return alice_encrypted, proxy_re_encrypted, bob_decrypted, use_time

# ------------------ 页面配置 ------------------
st.set_page_config(page_title="代理重加密系统", layout="wide")

# 顶部栏
st.markdown(
    """
    <div style='background-color:#0e1117;padding:10px;border-radius:6px;margin-bottom:20px'>
        <h2 style='color:white;margin:0;'>🔐 代理重加密系统 - 北京邮电大学</h2>
        <div style='margin-top:5px;'>
            <a href="#系统简介" style="margin-right:15px;color:#ddd;text-decoration:none;">系统简介</a>
            <a href="#实时演示" style="margin-right:15px;color:#ddd;text-decoration:none;">实时演示</a>
            <a href="#性能图表" style="margin-right:15px;color:#ddd;text-decoration:none;">性能图表</a>
            <a href="#帮助与联系" style="color:#ddd;text-decoration:none;">帮助与联系</a>
        </div>
    </div>
    """, unsafe_allow_html=True
)

# ------------------ 系统简介 ------------------
st.header("📘 系统简介", anchor="系统简介")
st.write("""
本系统演示了基于 ECC 与 RSA 的代理重加密（PRE）机制，支持用户输入明文，自动完成 Alice 加密 → Proxy 重加密 → Bob 解密的完整流程。
同时还提供不同加密算法在执行次数与明文长度变化下的性能对比图表，支持可视化分析。
""")

# ------------------ 实时演示 ------------------
st.header("⚙️ 实时演示", anchor="实时演示")
message = st.text_input("请输入明文消息（Origin Message）:")

if st.button("开始执行代理重加密"):
    if message:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔷 ECC 加密流程")
            ecc_alice, ecc_proxy, ecc_bob, ecc_time = proxy_re_encryption(message, "ECC")
            st.text_area("Alice Encrypto", ecc_alice, height=80, key="ecc_alice")
            st.text_area("Proxy Re-Encrypt", ecc_proxy, height=80, key="ecc_proxy")
            st.text_area("Bob Decrypto", ecc_bob, height=80, key="ecc_bob")
            st.text(f"Use Time: {ecc_time:.4f} seconds")
            st.success("ECC Process Completed")

        with col2:
            st.subheader("🔶 RSA 加密流程")
            rsa_alice, rsa_proxy, rsa_bob, rsa_time = proxy_re_encryption(message, "RSA")
            st.text_area("Alice Encrypto", rsa_alice, height=80, key="rsa_alice")
            st.text_area("Proxy Re-Encrypt", rsa_proxy, height=80, key="rsa_proxy")
            st.text_area("Bob Decrypto", rsa_bob, height=80, key="rsa_bob")
            st.text(f"Use Time: {rsa_time:.4f} seconds")
            st.success("RSA Process Completed")

        st.markdown("### ✅ 是否成功：Yes")
    else:
        st.warning("请先输入一段明文消息。")

# ------------------ 图表展示 ------------------
st.markdown("---")
st.header("📊 性能图表", anchor="性能图表")
st.image("performance_by_runs.png", caption="执行次数变化下的性能对比", use_container_width=True)
st.image("performance_by_msglen.png", caption="消息长度变化下的性能对比", use_container_width=True)

# ------------------ 帮助与联系 ------------------
st.markdown("---")
st.header("📞 帮助与联系", anchor="帮助与联系")
st.write("如您在使用过程中遇到任何问题，可联系：")
st.markdown("- 开发者邮箱：`Xiazhiyun@bupt.edu.cn`")
st.markdown("- GitHub 项目地址：`https://github.com/MuYueleng/proxy-reencryption-system`")
st.markdown("- QQ联系：3495494323")

# ------------------ 页脚 ------------------
st.markdown(
    """
    <hr style="margin-top:40px;">
    <p style='text-align:center; color:gray'>
    © 网络信息安全编程技术开发 - 期末作业 - 代理重加密系统
    </p>
    """, unsafe_allow_html=True
)
