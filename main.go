package main

import (
	"crypto/ecdsa"
	"encoding/json"
	"fmt"
	"goRecrypt/curve"    // 椭圆曲线密钥生成模块
	"goRecrypt/recrypt"  // 代理重加密逻辑实现模块
	"math/big"
	"os"
)

// 定义密文胶囊结构体，包含两个公钥和一个椭圆曲线点
type Capsule struct {
	E *ecdsa.PublicKey
	V *ecdsa.PublicKey
	S *big.Int
}

// 用于最终输出到JSON的数据结构体
type OutputData struct {
	StringPlainText string              `json:"string_plain_text"` // 原始字符串
	APubKey         *ecdsa.PublicKey    `json:"a_pub_key"`         // Alice 公钥
	APriKey         *ecdsa.PrivateKey   `json:"a_pri_key"`         // Alice 私钥
	BPubKey         *ecdsa.PublicKey    `json:"b_pub_key"`         // Bob 公钥
	BPriKey         *ecdsa.PrivateKey   `json:"b_pri_key"`         // Bob 私钥
	CipherText      []byte              `json:"cipher_text"`       // 加密得到的密文
	RK              *big.Int            `json:"rk"`                // 重加密密钥
	PubX            *ecdsa.PublicKey    `json:"pub_x"`             // 中间值 pubX，用于 Bob 解密
	PlainText       string              `json:"plain_text"`        // Bob 解密得到的明文
}

// 封装的密钥生成函数，生成一对椭圆曲线密钥对
func GenerateKey_() (*ecdsa.PrivateKey, *ecdsa.PublicKey) {
	PriKey, PubKey, _ := curve.GenerateKeys()
	return PriKey, PubKey
}

// 主流程逻辑：加密、重加密、解密
func run(m string) (string, *ecdsa.PublicKey, *ecdsa.PrivateKey, *ecdsa.PublicKey, *ecdsa.PrivateKey, []byte, *big.Int, *ecdsa.PublicKey, []byte) {
	// 1. Alice 生成密钥对
	aPriKey, aPubKey := GenerateKey_()
	// 2. Bob 生成密钥对
	bPriKey, bPubKey := GenerateKey_()

	// 打印明文和相关密钥
	fmt.Println("origin message:", m)
	fmt.Println("aPriKey:", aPriKey)
	fmt.Println("aPubKey:", aPubKey)
	fmt.Println("origin message length:", len(m), "bytes")

	// 3. Alice 使用自己的公钥加密明文，得到密文和胶囊
	cipherText, capsule, err := recrypt.Encrypt(m, aPubKey)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("cipherText:", cipherText, len(cipherText))

	// 4. Alice 基于 Bob 的公钥和自己的私钥生成重加密密钥 rk 和 pubX
	rk, pubX, err := recrypt.ReKeyGen(aPriKey, bPubKey)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("rk:", rk)

	// 5. 服务器基于 rk 将原胶囊 re-encrypt 成新的胶囊（中间转换）
	newCapsule, err := recrypt.ReEncryption(rk, capsule)
	if err != nil {
		fmt.Println(err.Error())
	}

	// 6. Bob 使用自己的私钥 + 转换后的胶囊 + pubX 解密密文，恢复明文
	plainText, err := recrypt.Decrypt(bPriKey, newCapsule, pubX, cipherText)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("plainText:", string(plainText))

	// 返回整个流程中的关键中间值
	return string(plainText), aPubKey, aPriKey, bPubKey, bPriKey, cipherText, rk, pubX, plainText
}

// 将运行结果保存为 JSON 文件
func saveToJson(data OutputData) {
	file, err := os.Create("ecc_pre.json")
	if err != nil {
		fmt.Println("Error creating JSON file:", err)
		return
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ") // 设置缩进
	if err := encoder.Encode(data); err != nil {
		fmt.Println("Error encoding JSON:", err)
	}
}

// 主函数：接收命令行输入的明文字符串，并运行整个加密解密流程
func main() {
	if len(os.Args) < 2 {
		fmt.Println("Please provide a message to encrypt.")
		return
	}

	// 读取输入参数作为待加密明文
	m := os.Args[1]

	// 执行流程
	stringPlainText, aPubKey, aPriKey, bPubKey, bPriKey, cipherText, rk, pubX, plainText := run(m)

	// 封装为结构体
	data := OutputData{
		StringPlainText: stringPlainText,
		APubKey:         aPubKey,
		APriKey:         aPriKey,
		BPubKey:         bPubKey,
		BPriKey:         bPriKey,
		CipherText:      cipherText,
		RK:              rk,
		PubX:            pubX,
		PlainText:       string(plainText),
	}

	// 输出到 JSON 文件
	saveToJson(data)
}
