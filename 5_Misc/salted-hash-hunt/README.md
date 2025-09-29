# Salted Hash Hunt

- 想定難易度: Easy

- 正解フラグ: `JohnInTheBox8657`

## 問題文

あなたは情報セキュリティ研究者として、最近発生した2つのシステム漏洩事件の調査を依頼されました。幸いなことに、これらの漏洩データは**単独では復元不可能**な形式で保存されていましたが、両方のデータセットを**組み合わせることで**パスワードを特定できる可能性があります。

調査の目標は、ターゲットユーザー `matsuki` の平文パスワードを特定することです。

ZIPのハッシュ値(SHA256): `f11a69e79b6cc9c2d23fbe8baca042a6aecc50c016ddb27b86444bbb807386ca`

## 流出データ形式

### System A: 認証システム
ファイル: `systemA_auth.csv`
- フォーマット: `salt_hex,iter,hash`
- salt_hex: 5バイト（10桁の16進数）
- iter: 反復回数（10,000または1,000,000）
- hash: PBKDF2-HMAC-SHA256ハッシュ（16進数形式）
- 例: `a1b2c3d4e5,100,f6g7h8i9j0...`

### System B: ユーザー管理システム
ファイル: `systemB_fingerprint.csv`
- フォーマット: `fingerprint,username`
- fingerprint: パスワードのSHA1ハッシュの先頭5桁（16進数）
- username: ユーザー名
- 例: `a1b2c,tanaka`

## フラグ形式

パスワードを見つけたら、コピーしてそのまま提出してください。
例: パスワードが「Password123!」の場合、`Password123!` と提出します。

## 基本ヒント

1. 最初に System B のデータからターゲットユーザー `matsuki` のフィンガープリントを見つけましょう
2. そのフィンガープリントに一致するパスワード候補を `rockyou.txt` から抽出します
3. 候補ごとに System A のデータを使って PBKDF2-HMAC-SHA256 を計算し、一致するものを探します
4. 低反復回数（iter=10,000）のエントリから先に検証すると計算時間を大幅に短縮できます

Python の標準ライブラリを使った解法例：

```python
# SHA1フィンガープリントの計算
fingerprint = hashlib.sha1(password.encode('utf-8')).hexdigest()[:5]

# PBKDF2-HMAC-SHA256ハッシュの計算
hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                                salt_bytes, iterations)
hash_hex = hash_bytes.hex()
```
