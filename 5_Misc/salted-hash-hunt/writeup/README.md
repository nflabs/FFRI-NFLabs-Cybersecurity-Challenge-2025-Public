# Salted Hash Hunt - 解説

## 0. flag

```
$ python3 smart_solver.py
JohnInTheBox8657
所要時間: 42秒

$ python3 basic_solver.py
JohnInTheBox8657
所要時間: 3211秒
```

## 1. 設計意図

この問題は、以下の重要なセキュリティ概念を高校「情報I」レベルの知識で学習できるように設計されています：

- **ハッシュ関数の基本**：一方向性関数でデータを固定長の文字列に変換する技術
- **ソルトの役割**：同じパスワードでも異なるハッシュ値を生成し、辞書攻撃を困難にする技術
- **反復ハッシュ（キーストレッチング）**：総当たり攻撃に対する耐性を高める技術
- **漏洩データの組み合わせ攻撃**：複数の情報源からデータを突き合わせるリスク

特に重要なのは、単独では安全に見える情報でも、複数の情報源を組み合わせることでリスクが生じる点です。これは実社会のデータ漏洩においても頻繁に見られる問題で、この演習を通じてその危険性を実感できます。

## 2. ステップバイステップ解法

### 2.1 問題の分析

1. **System A** (`systemA_auth.csv`)
   - ソルト、反復回数、ハッシュ値のリスト
   - PBKDF2-HMAC-SHA256 による強力なハッシュ化
   - 高反復回数(1000000)と低反復回数(10000)の混在

2. **System B** (`systemB_fingerprint.csv`)
   - パスワードの「指紋」とユーザー名のマッピング
   - 指紋 = SHA1ハッシュの先頭5桁（20ビット）

### 2.2 基本的な解法手順

1. **System Bからの情報収集**
   ```python
   # matsukiのフィンガープリントを特定
   fp_to_user = parse_system_b("systemB_fingerprint.csv")
   target_fp = None
   for fp, username in fp_to_user.items():
       if username == "matsuki":
           target_fp = fp
           break
   ```

2. **パスワード候補の生成**
   ```python
   # rockyou.txtから候補を抽出
   for password in open("rockyou.txt", encoding="utf-8", errors="ignore"):
       password = password.strip()
       fp = hashlib.sha1(password.encode()).hexdigest()[:5]
       if fp == target_fp:
           # 候補を検証
   ```

3. **System Aで候補検証**
   ```python
   # 各saltとiterでPBKDF2を計算
   for salt, iter_count, expected_hash in system_a_data:
       calculated_hash = hashlib.pbkdf2_hmac("sha256", 
                                            password.encode(), 
                                            salt, 
                                            iter_count).hex()
       if calculated_hash == expected_hash:
           return True  # 正解
   ```

### 2.3 実行結果と評価

基本的な解法は機能しますが、全ての候補に対して全てのソルトと反復回数の組み合わせを試すため、計算コストが高くなります。特に反復回数が1000000の場合は処理に時間がかかります。

## 3. 最適化技法

データ構造を工夫して低反復回数（10000）の検証を先に行います：

```python
# 低反復回数のエントリを先に検証
for index, (hash_hex, salt, iter_count) in enumerate(sorted(hash_salt_count, key=lambda x: x[2])):
    ...
    for password in password_candidates:
       pw_bytes = password.encode('utf-8')
       computed_hash = hashlib.pbkdf2_hmac('sha256', pw_bytes, salt, iter_count).hex()
       if computed_hash == hash_hex:
             return password
```

この最適化により、ターゲットが低反復回数のエントリにある場合（これに該当するよう設計されています）、高反復回数の検証をスキップできます。

## 4. Solver性能比較データ

| 実装方法 | 時間計測 | 絞り込み効率 |
|---------|---------|------------|
| basic_solver | ~3600秒 | フィンガープリント一致のみ |
| smart_solver | ~60秒 | フィンガープリント + 低反復回数優先 |

最適化によるパフォーマンス改善：
- 低反復回数優先検証により計算量を平均90%以上削減

※処理時間はマシンスペックやデータセットサイズによって異なります

## 5. 補足事項

### 5.1 5バイトソルトの脆弱性

この問題では5バイトのソルトを使用していますが、これは教育目的のためであり、**PBKDFでは脆弱**です。[NIST Special Publication 800-132 Recommendation for Password-Based Key Derivation Part 1: Storage Applications](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-132.pdf) 5.1 The Salt (S) では、以下が記述されています：

- ソルトは**安全な乱数生成器**で生成すること
- ソルト長は**16バイト（128ビット）以上**であること

5バイトのソルトでは、特に大規模なユーザーベースの場合、衝突の可能性が高まり、レインボーテーブル攻撃に対する耐性が低くなります。

### 5.2 SHA-1の危殆化

System Bでは指紋生成にSHA-1を使用していますが、SHA-1は**現在は安全でない**と考えられています：

- 2017年に**初の完全な衝突攻撃**が実証される [SHAttered](https://shattered.io/)
- 2020年には**選択プレフィックス衝突攻撃**が実演される [SHA-1 is a Shambles](https://sha-mbles.github.io/)
- セキュリティ標準ではSHA-2やSHA-3が推奨されている [NIST Special Publication 800-57 Part 1 Revision 5 Recommendation for Key Management: Part 1 – General](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf) Table 3: Maximum security strengths for hash and hash-based functions

実際のシステムでは、SHA-1を認証に使用すべきではありません。

### 5.3 パスワードの安全な保存

[Password Storage - OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)記述の、実際のシステムでパスワードを安全に保存するためのベストプラクティス：

1. **専用のパスワードハッシュ関数を使用する**
   - Argon2id（推奨）、scrypt、bcrypt、PBKDF2 など
   - 通常のハッシュ関数（SHA-256など）は単体では不十分

2. **適切なパラメータを設定する**
   - CPU/メモリコスト（Argon2, scrypt）
   - スレッド並列度（Argon2, scrypt）
   - 反復回数（全アルゴリズム）

3. **定期的にパラメータを見直す**
   - ハードウェアの高性能化や廉価化に合わせて反復回数を増やす

## 6. まとめ

この問題通じて学べる重要な教訓：

1. 複数の情報漏洩は組み合わせると危険性が高まる
2. ハッシュにはソルトと適切な反復回数が不可欠
3. 低反復回数はブルートフォース攻撃の標的になりやすい
4. 現代のパスワード保存には専用アルゴリズムとベストプラクティスが必要
