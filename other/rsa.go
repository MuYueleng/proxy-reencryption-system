package main

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/base64"
	"fmt"
)
 
func main(){
	message := "yWdslfXfaFghVG6m"
	fmt.Println("message: ", string(message))
 
	//生成私钥
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		panic(err)
	}
 
	// *rsa.PrivateKey 类型转为base64 字符串
	// 将私钥序列化为DER编码的字节数组
	//derBytes := x509.MarshalPKCS1PrivateKey(privateKey)
	//fmt.Println("derBytes: ", derBytes)
	//fmt.Println("-----------------")
	// 将字节数组编码为Base64字符串
	//b64Str := base64.StdEncoding.EncodeToString(derBytes)
	//fmt.Println("b64Str: ", b64Str)
 
	//生成公钥
	publicKey := privateKey.PublicKey
 
	//根据公钥加密
	encryptedBytes, err := rsa.EncryptOAEP(
		sha256.New(),
		rand.Reader,
		&publicKey,
		[]byte(message), //需要加密的字符串
		nil)
	if err != nil {
		panic(err)
	}
	//fmt.Println("encryptedBytes: ", encryptedBytes)
 
	// 加密后进行base64编码
	encryptBase64 := base64.StdEncoding.EncodeToString(encryptedBytes)
	fmt.Println("加密后进行base64编码: ", encryptBase64)
 
	// 解密
	// base64解码
	decodedBase64, err := base64.StdEncoding.DecodeString(encryptBase64)
	if err != nil {
		panic(err)
	}
	//fmt.Println("decodedBase64: ", decodedBase64)
 
	//根据私钥解密
	decryptedBytes, err := privateKey.Decrypt(nil, decodedBase64, &rsa.OAEPOptions{Hash: crypto.SHA256})
	if err != nil {
		panic(err)
	}
	fmt.Println("decrypted message: ", string(decryptedBytes))
 
}