#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import hashlib
import os
import time
from typing import Dict, List, Tuple

def parse_args():
    """コマンドライン引数をパース"""
    parser = argparse.ArgumentParser(description='Salted Hash Hunt 基本ソルバー')
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

def parse_system_a(filepath: str) -> List[Tuple[bytes, int, str]]:
    """System Aデータの解析 (salt, iter, hash)"""
    system_a_data = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(',')
            if len(parts) == 3:
                salt_hex, iter_count, hash_hex = parts
                # hexからbytesに変換
                salt = bytes.fromhex(salt_hex)
                iter_count = int(iter_count)
                system_a_data.append((salt, iter_count, hash_hex))
    
    return system_a_data

def check_password(password: str, system_a_data: List[Tuple[bytes, int, str]]) -> bool:
    """System Aに対してパスワードを検証"""
    pw_bytes = password.encode('utf-8')
    
    for salt, iter_count, expected_hash in system_a_data:
        # PBKDF2-HMAC-SHA256でハッシュ計算
        computed_hash = hashlib.pbkdf2_hmac('sha256', pw_bytes, salt, iter_count).hex()
        
        # 一致確認
        if computed_hash == expected_hash:
            return True
    
    return False

def main():
    """メイン処理"""
    args = parse_args()
    target_user = args.target_user
    
    # データファイルのパス
    data_dir = os.path.join("data")
    system_a_path = os.path.join(data_dir, "systemA_auth.csv")
    system_b_path = os.path.join(data_dir, "systemB_fingerprint.csv")
    
    # rockyou.txtの場所を検索
    if os.path.exists("rockyou.txt"):
        rockyou_path = "rockyou.txt"
    elif os.path.exists(os.path.join("..", "rockyou.txt")):
        rockyou_path = os.path.join("..", "rockyou.txt")
    elif os.path.exists(os.path.join(data_dir, "rockyou.txt")):
        rockyou_path = os.path.join(data_dir, "rockyou.txt")
    else:
        print("エラー: rockyou.txtが見つかりません")
        print("カレントディレクトリ、親ディレクトリ、またはdataディレクトリにrockyou.txtを配置してください")
        sys.exit(1)
    
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
    
    # System Aデータの解析
    system_a_data = parse_system_a(system_a_path)
    
    # パスワードの検証ループ
    start_time = time.time()
    total_candidates = 0
    match_count = 0
    password_found = None
    
    with open(rockyou_path, 'r', encoding='utf-8', errors='ignore') as f:
        password_count = sum(1 for _ in f)
    
    with open(rockyou_path, 'r', encoding='utf-8', errors='ignore') as f:
        processed = 0
        
        for line in f:
            processed += 1
            
            # 進捗表示（10%ごと）
            if processed % (password_count // 10) == 0:
                elapsed = time.time() - start_time
                p = processed / password_count
                total = elapsed / p
                remain = total - elapsed
                print(f"[{int(p*100)}%] 残り: {int(remain)}秒", file=os.sys.stderr)
            
            password = line.strip()
            
            # フィンガープリントの計算（SHA1の先頭5桁）
            fp = hashlib.sha1(password.encode('utf-8')).hexdigest()[:5]
            
            # ターゲットのフィンガープリントと一致する場合のみ検証
            if fp == target_fp:
                total_candidates += 1
                
                # 候補パスワードをSystem Aで検証
                if check_password(password, system_a_data):
                    match_count += 1
                    password_found = password
                    break
    
    # 結果出力
    if password_found:
        print(password_found)
    else:
        print("パスワードが見つかりませんでした")
    
    elapsed_time = time.time() - start_time
    print(f"所要時間: {int(elapsed_time)}秒")

if __name__ == "__main__":
    main()
