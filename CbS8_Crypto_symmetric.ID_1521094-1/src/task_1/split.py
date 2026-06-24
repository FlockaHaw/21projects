import string

prntbl = str(string.printable)
ms1 = []
ms2 = []
dict = {}

ct1 = "0c318c942012106f9093d54a405ab56fecf16b372ddb6122585a5347d6a175899e3f821f5bc54aa0d2c8541cecfa0091b9a1470c7471bf087cefe2c8e575ed4728d43e67f61c16830c539ef854af384f482bb5cd35c81dfda48a5e7e90880b58cd954905d348e1bb2407ba89db5d09e5718e2cf75b6fccbd81b4e095d1c6429c148964a24b566c7b028c0717c6cfaa58fc568b381375cd68a09fba8adaebbe661ca72544d2fa26bf528f2634355bcd03d5278668dab99ad0d586437908008739b9441f8f3c5c981eb055c6372b0f2c43a2bfe10b945097a78b64f1a925f37f273a7097b7c874cf06cdfd76839c0c691d8ddf73cb9a388efcf2c354a77dd1f055669420faaeb041ffe749cd247ea592fbba21d45a8a7a69ba22f4cddb6ad77b47f79aef93bcc9781c03af3c93c290783095599b6028978beecae02be5e443d174fe72314bd4baf0a5ea480cefc443150d34a13f0596feb5f1b6cbc87b17b1aa0c64ec8afffb94081ec930b4f4a91a8ecb21d8ac319d0fa6f5298155c7e60b6bf11992dc019501ce5b0a06df0efb6f3f15d717cdd31bfec3687491909d8ae06b59d33737a055712067f775d8790d947b5f4215842b9d5ccf167653409543e247a54b13b28eb153b2d6b5a981e7ec778072877520e18bc5e16e8aaeb3fc3bd23c1dbc4a573cb04eb53da0b778fb2c727b1be49134ca888f27061975cb4a8a6da647349a13f796f644b9ddd4471ca24d3aa53a3ca4175290624ac2df158b304ac2e97bd14d9736924bd97115e2686719d3b830930726f871bf07eb334bd14a1dba9c628c7cea0a4ffe11dda4873f3d301578fe8f8490aae2870afca1ca02bd3f3c08a6c59e659a581a56c276f264a0ec3b9972b2adc4ba719839249e39bafa4b17e1413328d62c561752d909068887d00beac0e7bee12d9cd14cbcc4fd7513cc0e5797d4ef33f8fa34b4feb7363f9798e65762c76cf61a18f16797ab1b5867603d0bd49865706148cbea1bd2e92bc5125f5246b1da1db6fd8c0d42efe5842c4387f89764c803a04e3b841d7386603debb484d277c452d1b49345fbef437e4791c35899d720a09a6da4ce6790265bbfddfaf693db531704e74d34b9c67b294835f16f"
len_ct1 = int(len(ct1))

ct2 = "4215842b9d5ccf16ecf16b372ddb61229093d54a405ab56f46b1da1db6fd8c0d482bb5cd35c81dfd8b64f1a925f37f27718e2cf75b6fccbdd49865706148cbeaba21d45a8a7a69bab9441f8f3c5c981e8ddf73cb9a388efcd49865706148cbea3a7097b7c874cf068ddf73cb9a388efc8b64f1a925f37f27718e2cf75b6fccbdd49865706148cbea482bb5cd35c81dfda48a5e7e90880b58b9441f8f3c5c981e8ddf73cb9a388efccdfd76839c0c691dd49865706148cbeacdfd76839c0c691d028c0717c6cfaa58fc568b381375cd683a7097b7c874cf06d49865706148cbea482bb5cd35c81dfd528f2634355bcd03148964a24b566c7bb9441f8f3c5c981ec0e7bee12d9cd14c9764c803a04e3b84"
len_ct2 = int(len(ct2))


print("Printable chars:")
print(prntbl)


iterator = 0
tmp = ""

for letter in ct1:
	iterator += 1
	tmp += letter
	if iterator == 8:
		ms1.append(tmp)
		tmp = ""
		iterator = 0

print(f"Lenght of ct1: {len_ct1} hex symbols -> {len_ct1 / 2} Bite -> {(len_ct1 / 2) / 8} blocks of 8 Bites")
print(f"Lenght of str: {len(prntbl)}")
print(f"ms1: {ms1}")

keys = prntbl
values = ms1
iterator = 0
for iterator in range(len(keys)):
	dict[prntbl[iterator]] = values[iterator]

print("Sorted dict:")
print(dict)

iterator = 0
for letter in ct2:
	iterator += 1
	tmp += letter
	if iterator == 8:
		ms2.append(tmp)
		tmp = ""
		iterator = 0

print(f"Lenght of ct2: {len_ct2} hex symbols -> {len_ct2 / 2} Bite -> {(len_ct2 / 2) / 8} blocks of 8 Bites")
print(f"ms2: {ms2}")

FLAG = ""
for i in range(len(ms2)):
	# FLAG = FLAG + key for key, value in dict.items() if value == ms2[i]
	for key, value in dict.items():
		if str(value) == str(ms2[i]):
			FLAG += key

print(f"FLAG FINNALU: {FLAG}")
