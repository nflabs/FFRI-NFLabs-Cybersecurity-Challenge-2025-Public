#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import hashlib
import os
import time
from typing import Dict, List, Tuple

def parse_args():
    """コマンドライン引数をパース"""
    parser = argparse.ArgumentParser(description='Salted Hash Hunt 最適化ソルバー')
    parser.add_argument('--target-user', default='matsuki', 
                        help='ターゲットユーザー名 (デフォルト: matsuki)')
    return parser.parse_args()

def parse_system_b(filepath: str) -> Dict[str, str]:
    """System Bデータの解析 (フィンガープリント→ユーザー名マッピング)"""
    fingerprint_to_user = {}
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # コメント行または空行をスキップ
            if not line or line.startswith('#'):
                continue
            
            parts = line.split(',')
            if len(parts) == 2:
                fingerprint, username = parts
                fingerprint_to_user[fingerprint] = username
    
    return fingerprint_to_user

def parse_system_a(filepath: str) -> Dict[str, List[Tuple[bytes, int]]]:
    """System Aデータの解析 (hash→[(salt, iter)]マッピング)"""
    hash_to_salt_iter = {}
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(',')
            if len(parts) == 3:
                salt_hex, iter_count, hash_hex = parts
                salt = bytes.fromhex(salt_hex)
                iter_count = int(iter_count)
                
                # ハッシュをキーとしてsaltとiterのリストを保持
                if hash_hex not in hash_to_salt_iter:
                    hash_to_salt_iter[hash_hex] = []
                hash_to_salt_iter[hash_hex].append((salt, iter_count))
    
    return hash_to_salt_iter

def check_password_optimized(password_candidates: List[str],
                             hash_to_salt_iter: Dict[str, List[Tuple[bytes, int]]]) -> str:
    """最適化されたパスワード検証（低反復回数優先）"""
    
    start_time = time.time()

    hash_salt_count = []
    for hash_hex, salt_iter_list in hash_to_salt_iter.items():
        for salt, iter_count in salt_iter_list:
            hash_salt_count.append((hash_hex, salt, iter_count))

    # 低反復回数のエントリを先に検証
    for index, (hash_hex, salt, iter_count) in enumerate(sorted(hash_salt_count, key=lambda x: x[2])):
        # 進捗表示（10%ごと）
        if (index + 1) % (len(hash_salt_count) // 10) == 0:
            elapsed = time.time() - start_time
            p = (index + 1) / len(hash_salt_count)
            total = elapsed / p
            remain = total - elapsed
            print(f"[{int(p*100)}%] パスワード検証 残り: {int(remain)}秒", file=os.sys.stderr)

        for password in password_candidates:
            pw_bytes = password.encode('utf-8')
            computed_hash = hashlib.pbkdf2_hmac('sha256', pw_bytes, salt, iter_count).hex()
            if computed_hash == hash_hex:
                return password
    
    print(f"エラー: パスワードが見つかりませんでした")
    return ""

def main():
    """メイン処理"""
    args = parse_args()
    target_user = args.target_user
    
    # データファイルのパス
    data_dir = os.path.join("data")
    rockyou_path = os.path.join(data_dir, "rockyou.txt")
    system_a_path = os.path.join(data_dir, "systemA_auth.csv")
    system_b_path = os.path.join(data_dir, "systemB_fingerprint.csv")
    
    # System Bデータの解析
    fp_to_user = parse_system_b(system_b_path)
    
    # ターゲットユーザーのフィンガープリントを検索
    target_fp = None
    for fp, username in fp_to_user.items():
        if username == target_user:
            target_fp = fp
            break
    
    if not target_fp:
        print(f"エラー: ターゲットユーザー '{target_user}' が見つかりませんでした")
        return
    
    # System Aデータの解析（最適化形式）
    hash_to_salt_iter = parse_system_a(system_a_path)
    
    # パスワードの検証ループ
    start_time = time.time()
    password_found = None
    
    with open(rockyou_path, 'r', encoding='utf-8', errors='ignore') as f:
        password_count = sum(1 for _ in f)
    
    with open(rockyou_path, 'r', encoding='utf-8', errors='ignore') as f:
        processed = 0

        # パスワード候補
        password_candidates = []
        
        for line in f:
            processed += 1
            
            # 進捗表示（10%ごと）
            if processed % (password_count // 10) == 0:
                elapsed = time.time() - start_time
                p = processed / password_count
                total = elapsed / p
                remain = total - elapsed
                print(f"[{int(p*100)}%] フィンガープリント計算 残り: {int(remain)}秒", file=os.sys.stderr)
            
            password = line.strip()
            
            # フィンガープリントの計算（SHA1の先頭5桁）
            fp = hashlib.sha1(password.encode('utf-8')).hexdigest()[:5]
            
            # ターゲットのフィンガープリントと一致する場合のみ保持
            if fp == target_fp:
                password_candidates.append(password)

        # 最適化: 低反復回数優先で検証
        password_found = check_password_optimized(password_candidates, hash_to_salt_iter)
    
    # 結果出力
    if password_found:
        print(password_found)
    else:
        print("パスワードが見つかりませんでした")
    
    elapsed_time = time.time() - start_time
    print(f"所要時間: {int(elapsed_time)}秒")

if __name__ == "__main__":
    main()
