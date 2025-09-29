#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import hashlib
import math
import os
import random
import shutil
import sys
import time
from typing import List, Set, Tuple, Dict

def parse_args():
    """コマンドライン引数をパース"""
    parser = argparse.ArgumentParser(description='Salted Hash Hunt データ生成')
    parser.add_argument('--target-user', default='matsuki', 
                        help='ターゲットユーザー名 (デフォルト: matsuki)')
    parser.add_argument('--hash-count', type=int, default=5000, 
                        help='System A のハッシュエントリ数 (デフォルト: 5000)')
    parser.add_argument('--fp-count', type=int, default=5000, 
                        help='System B のフィンガープリント数 (デフォルト: 5000)')
    parser.add_argument('--high-iter-ratio', type=float, default=0.45, 
                        help='high-iter の割合 0-1 (デフォルト: 0.45)')
    return parser.parse_args()

def select_password(rockyou_path: str) -> str:
    """要件を満たすパスワードをrockyou.txtから選択"""
    valid_passwords = []
    
    with open(rockyou_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            password = line.strip()
            # 12文字以上かつ大文字・小文字・数字をすべて含む
            if (len(password) >= 12 and 
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password)):
                valid_passwords.append(password)
    
    if not valid_passwords:
        raise ValueError("rockyou.txtに条件を満たすパスワードが見つかりませんでした")
    
    return random.choice(valid_passwords)

def generate_unique_salt(used_salts: Set[bytes], max_attempts: int = 3) -> bytes:
    """一意のsaltを生成 (最大3回まで再試行)"""
    for _ in range(max_attempts):
        salt = os.urandom(5)  # 5バイトのランダムなsalt
        if salt not in used_salts:
            return salt
    raise RuntimeError("一意のsaltを生成できませんでした (最大試行回数超過)")

def generate_username_list(target_user: str, count: int) -> List[str]:
    """日本人の姓または名のローマ字表記のリストを生成"""
    # 日本人の姓または名のローマ字表記のサンプル
    japanese_names_base = [
        "tanaka", "suzuki", "sato", "takahashi", "kobayashi", 
        "nakamura", "kato", "yamamoto", "watanabe", "ito",
        "yamada", "sasaki", "yamaguchi", "matsumoto", "inoue", 
        "kimura", "hayashi", "saito", "shimizu", "yamazaki",
        "mori", "ikeda", "hashimoto", "ishikawa", "yamashita",
        "ogawa", "ishii", "hasegawa", "goto", "okada",
        "matsui", "maeda", "fujita", "yoshida", "abe",
        "hirano", "kondo", "nomura", "tamura", "nakajima", 
        "ishida", "sugiyama", "kikuchi", "yagi", "ueda",
        "takagi", "ueno", "sugawara", "morita", "takada",
        "nakano", "kaneko", "yoshikawa", "yokoyama", "kojima"
    ]
    
    # 連番を付けるなど、バリエーションを増やしてユーザーリストを作成
    username_list = []
    
    # まずはターゲットユーザーを追加
    username_list.append(target_user)
    
    # 必要な数だけユーザーを生成
    for i in range(count - 1):
        base_name = japanese_names_base[i % len(japanese_names_base)]
        if i < len(japanese_names_base):
            # 基本名はそのまま使用
            username = base_name
        else:
            # 連番付きの名前を生成
            number = i // len(japanese_names_base) + 1
            username = f"{base_name}{number}"
        
        # ターゲットユーザーと重複しないようにチェック
        if username == target_user:
            username = f"{username}_{random.randint(1000, 9999)}"
        
        username_list.append(username)
    
    # ターゲットユーザー以外をシャッフル
    non_target = username_list[1:]
    random.shuffle(non_target)
    username_list = [target_user] + non_target
    
    return username_list

def generate_system_a_data(password: str, target_user: str, hash_count: int, 
                          high_iter_ratio: float) -> Tuple[List[str], Dict]:
    """System Aのデータを生成"""
    # 各パラメータの計算
    high_count = math.floor(hash_count * high_iter_ratio)
    low_count = hash_count - high_count
    
    # ターゲットエントリの位置計算
    start = high_count + math.floor(low_count * 0.7)
    end = hash_count
    target_index = random.randint(start, end - 1)
    
    used_salts = set()
    data_lines = []
    target_data = {}
    
    start_time = time.time()
    
    for i in range(hash_count):
        # 進捗表示（10%ごと）
        if i % (hash_count // 10) == 0 and i > 0:
            elapsed = time.time() - start_time
            p = i / hash_count
            total = elapsed / p
            remain = total - elapsed
            print(f"[{int(p*100)}%] 残り: {int(remain)}秒")
        
        # 反復回数の決定
        iter_count = 1000000 if i < high_count else 10000  # high-iter or low-iter
        
        # ターゲットかどうか判定
        is_target = (i == target_index)
        
        # パスワード選択（ターゲットの場合は固定）
        pw = password if is_target else f"dummy_password_{i}"
        pw_bytes = pw.encode('utf-8')
        
        # saltの生成
        salt = generate_unique_salt(used_salts)
        used_salts.add(salt)
        salt_hex = salt.hex()
        
        # ハッシュ計算
        hash_bytes = hashlib.pbkdf2_hmac('sha256', pw_bytes, salt, iter_count)
        hash_hex = hash_bytes.hex()
        
        # CSVデータ行の作成
        data_line = f"{salt_hex},{iter_count},{hash_hex}"
        data_lines.append(data_line)
        
        # ターゲットデータを記録
        if is_target:
            target_data = {
                'salt': salt_hex,
                'iter': iter_count,
                'hash': hash_hex,
                'index': i
            }
    
    return data_lines, target_data

def generate_system_b_data(password: str, username_list: List[str], 
                          target_user: str) -> Tuple[List[str], Dict]:
    """System Bのデータを生成"""
    # ターゲットのフィンガープリント計算
    target_fp = hashlib.sha1(password.encode('utf-8')).hexdigest()[:5]
    
    # ユーザー名とパスワードのマッピング作成
    data_lines = []
    user_data = {}
    
    for i, username in enumerate(username_list):
        if username == target_user:
            # ターゲットユーザー
            fp = target_fp
            user_data = {
                'username': username,
                'fp': fp,
                'index': i
            }
        else:
            # ダミーユーザー（一意のフィンガープリント）
            dummy_pw = f"dummy_{i}_{random.randint(10000, 99999)}"
            fp = hashlib.sha1(dummy_pw.encode('utf-8')).hexdigest()[:5]
        
        data_lines.append(f"{fp},{username}")
    
    # データをシャッフル
    random.shuffle(data_lines)
    
    # ユーザーの新しいインデックスを特定
    for i, line in enumerate(data_lines):
        if line.endswith(f",{target_user}"):
            user_data['index'] = i
            break
    
    # ターゲットユーザーが後半30%に配置されるようシャッフル
    while user_data['index'] < len(data_lines) * 0.7:
        random.shuffle(data_lines)
        for i, line in enumerate(data_lines):
            if line.endswith(f",{target_user}"):
                user_data['index'] = i
                break
    
    return data_lines, user_data

def main():
    """メイン処理"""
    args = parse_args()
    
    # データディレクトリの確認
    data_dir = os.path.join("data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # rockyou.txtのパス（カレントディレクトリと親ディレクトリの両方を確認）
    if os.path.exists("rockyou.txt"):
        # カレントディレクトリにある場合はコピー
        shutil.copy("rockyou.txt", os.path.join(data_dir, "rockyou.txt"))
        rockyou_path = os.path.join(data_dir, "rockyou.txt")
    elif os.path.exists(os.path.join("..", "rockyou.txt")):
        # 親ディレクトリにある場合はコピー
        shutil.copy(os.path.join("..", "rockyou.txt"), os.path.join(data_dir, "rockyou.txt"))
        rockyou_path = os.path.join(data_dir, "rockyou.txt")
    else:
        # データディレクトリにすでにある場合
        rockyou_path = os.path.join(data_dir, "rockyou.txt")
        if not os.path.exists(rockyou_path):
            print("エラー: rockyou.txtが見つかりません")
            print("カレントディレクトリ、親ディレクトリ、またはdataディレクトリにrockyou.txtを配置してください")
            sys.exit(1)
    
    # ターゲットパスワードの選択
    print("対象パスワードを選択中...")
    password = select_password(rockyou_path)
    
    # ユーザー名リストの生成
    print(f"ユーザー名リストを生成中（合計 {args.fp_count} 件）...")
    username_list = generate_username_list(args.target_user, args.fp_count)
    
    # System Aのデータ生成
    print(f"System A データを生成中（合計 {args.hash_count} 件）...")
    system_a_data, target_a_data = generate_system_a_data(
        password, args.target_user, args.hash_count, args.high_iter_ratio)
    
    # System Bのデータ生成
    print(f"System B データを生成中（合計 {args.fp_count} 件）...")
    system_b_data, target_b_data = generate_system_b_data(
        password, username_list, args.target_user)
    
    # System A データの書き込み
    with open(os.path.join(data_dir, "systemA_auth.csv"), 'w') as f:
        for line in system_a_data:
            f.write(f"{line}\n")
    
    # System B データの書き込み
    with open(os.path.join(data_dir, "systemB_fingerprint.csv"), 'w') as f:
        # ヘッダコメント
        f.write("# fingerprint,username\n")
        f.write("# SHA1(password)[:5],ユーザー名\n\n")
        for line in system_b_data:
            f.write(f"{line}\n")
    
    # flag.txtの生成
    with open(os.path.join(data_dir, "flag.txt"), 'w') as f:
        f.write(f"flag{{{password}}}\n")
        f.write(f"target-user: {args.target_user}\n")
        f.write(f"hash-count: {args.hash_count}\n")
        f.write(f"fp-count: {args.fp_count}\n")
        f.write(f"high-iter-ratio: {args.high_iter_ratio}\n")
    
    # 結果表示
    print("\n生成完了！以下の内容でデータを生成しました：")
    print(f"flag{{{password}}}")
    print(f"target-user: {args.target_user}")
    print(f"hash-count: {args.hash_count}")
    print(f"fp-count: {args.fp_count}")
    print(f"high-iter-ratio: {args.high_iter_ratio}")
    print(f"\nSystem A内のターゲットインデックス: {target_a_data['index']}")
    print(f"System B内のターゲットインデックス: {target_b_data['index']}")

if __name__ == "__main__":
    main()
