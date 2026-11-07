#!/usr/bin/env python3
"""週次Instagram分析用のデータセット生成とグラフ出力。

対象期間: 2026-10-31 00:00 〜 2026-11-06 23:59 (JST)
取得方法: Instagram公開ページ（ログアウト状態）のプロフィール／投稿ページ。
数値は2026-11-07 14:20 JST時点の公開値。
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "reports"
ASSET_DIR = ROOT / "assets"
DATA_DIR.mkdir(exist_ok=True)
ASSET_DIR.mkdir(exist_ok=True)

WINDOW = "2026-10-31〜2026-11-06"
CRAWLED_AT = "2026-11-07T14:20+09:00"

ACCOUNTS = [
    {
        "handle": "placehome",
        "name": "プレースホーム｜佐賀・福岡注文住宅 / リノベ",
        "followers": 3401,
        "following": 143,
        "posts": [
            {
                "date": "2026-10-31", "type": "image", "shortcode": "DfJu6Irk3pM",
                "likes": 23, "comments": 0,
                "tags": ["佐賀注文住宅", "佐賀家づくり", "ハイドア", "垂れ壁", "洗面"],
                "hook": "黒と木目調が織りなす、上質で心地よい住まい。シンプルモダン【2階建】約34坪",
            },
            {
                "date": "2026-11-04", "type": "image", "shortcode": "DfUCF2mk5Uv",
                "likes": 13, "comments": 0,
                "tags": ["佐賀注文住宅", "佐賀家づくり", "キッチン", "和室", "カウンター"],
                "hook": "黒と木目調が織りなす、上質で心地よい住まい。シンプルモダン【2階建】約34坪",
            },
            {
                "date": "2026-11-06", "type": "image", "shortcode": "DfZS-8xk-Ll",
                "likes": 15, "comments": 0,
                "tags": ["佐賀注文住宅", "佐賀家づくり", "キッチン", "見学会", "下り天井"],
                "hook": "完成見学会のお知らせ📢 Rの曲線が美しい、オーガニックモダンな【平屋】",
            },
        ],
    },
    {
        "handle": "kicocochi_kobo",
        "name": "株式会社 木ここち建築工房 【八女市星野村の工務店】",
        "followers": 3022,
        "following": 602,
        "posts": [
            {
                "date": "2026-11-03", "type": "image", "shortcode": "DfTsPI1msfi",
                "likes": 29, "comments": 0,
                "tags": ["木ここち建築工房", "八女市星野村の工務店", "庭と一体の暮らし", "星野村"],
                "hook": "雨の日にも、楽しみを。軒先から鎖樋を伝い、小さなビオトープへと流れる雨水。",
            },
            {
                "date": "2026-11-06", "type": "image", "shortcode": "DfZLVx7mvaM",
                "likes": 21, "comments": 0,
                "tags": ["木ここち建築工房", "八女市星野村の工務店", "庭と一体の暮らし", "星野村"],
                "hook": "外で過ごす時間を、もっと。薪をくべて料理を楽しむピザ窯。",
            },
        ],
    },
    {
        "handle": "irodori8223",
        "name": "彩 irodori｜暮らしを彩る家づくり",
        "followers": 770,
        "following": 529,
        "posts": [
            {
                "date": "2026-11-03", "type": "image", "shortcode": "DfRv-_rkwfG",
                "likes": 19, "comments": 0,
                "tags": ["ルイスポールセン", "パテラ", "ldk", "薪ストーブのある暮らし", "ダイニング"],
                "hook": "ルイスポールセン パテラ／斜め下45度に明かりが灯り 空間を理想的なバランスで照らしてくれる",
            },
        ],
    },
    {
        "handle": "torikaihome",
        "name": "トリカイホーム｜KIYAMALIVE ∥佐賀県基山町∥自然素材の木のお家づくり",
        "followers": 2341,
        "following": 848,
        "posts": [
            {
                "date": "2026-11-01", "type": "image", "shortcode": "DfD_iFVkf-Y",
                "likes": 22, "comments": 0,
                "tags": ["トリカイホーム", "佐賀注文住宅", "アーチのある家", "造作カウンター", "ペンダントライト"],
                "hook": "曲線の奥に、小さな居場所。階段を上がった先に小さなカウンタースペースを",
            },
            {
                "date": "2026-11-03", "type": "image", "shortcode": "DfD_jJ3EeHE",
                "likes": 24, "comments": 0,
                "tags": ["トリカイホーム", "佐賀注文住宅", "玄関ポーチ", "植栽のある暮らし", "外構照明"],
                "hook": "家に入る前から、心地よく。軒下の天井とドアに木目を合わせ、そばには植栽を添えました。",
            },
            {
                "date": "2026-11-05", "type": "image", "shortcode": "DfYl4mnE8GO",
                "likes": 10, "comments": 0,
                "tags": ["トリカイホーム", "佐賀注文住宅", "玄関アプローチ", "植栽のある暮らし", "外観デザイン"],
                "hook": "買い物帰りも、仕事を終えた日も。玄関へと続くアプローチに、庭の緑が彩りを添えます。",
            },
        ],
    },
    {
        "handle": "eda_kensetsu", "name": "佐賀鳥栖建築新築一戸建てなら江田建設",
        "followers": 1414, "following": 1176, "posts": [],
        "last_post": "2026-09-03",
    },
    {
        "handle": "rokka_staff", "name": "六花スタッフ",
        "followers": 477, "following": 104, "posts": [],
        "last_post": "2026-10-26",
    },
    {
        "handle": "hooop.inc", "name": "株式会社HOOOP",
        "followers": 1397, "following": 405, "posts": [],
        "last_post": "2025-11-27",
    },
    {
        "handle": "eternal_designlife", "name": "株式会社ETERNAL | 佐賀県唐津市",
        "followers": 602, "following": 620, "posts": [],
        "last_post": "2026-07-27",
    },
    {
        "handle": "tiida_saga",
        "name": "🪸サンゴのぬり壁の家｜美ゅら家ulu（ティーダ建築工房）",
        "is_own": True,
        "followers": 566,
        "following": 1633,
        "posts": [
            {
                "date": "2026-11-02", "type": "carousel", "shortcode": "DfO_KzhFXJX",
                "likes": 3, "comments": 0,
                "tags": ["ティーダ建築工房", "玄関ドア", "玄関リフォーム", "住まいの相談", "佐賀リフォーム",
                          "鳥栖市", "みやき町", "家づくり", "くらしサポート展", "トスプロ"],
                "hook": "玄関ドアの「開けづらい」。相談するとき、どんなことを伝えればいいか迷いませんか？",
            },
            {
                "date": "2026-11-03", "type": "image", "shortcode": "DfRngFJFKmv",
                "likes": 5, "comments": 0,
                "tags": ["美ゅら家uluサンゴの塗り壁", "ティーダ建築工房", "佐賀工務店", "佐賀暮らし", "外観"],
                "hook": "洗練の外観✨",
            },
            {
                "date": "2026-11-05", "type": "reel", "shortcode": "DfXJkQeAcZ5",
                "likes": 1, "comments": 0,
                "tags": ["ティーダ建築工房", "くらしサポート展", "トスプロ", "鳥栖市", "みやき町",
                          "企画住宅", "新築", "リフォーム相談", "土地探し", "佐賀の工務店"],
                "hook": "「何から相談したらいいか分からない」という方へ。",
            },
            {
                "date": "2026-11-06", "type": "image", "shortcode": "DfZV4lWjVrp",
                "likes": 2, "comments": 0,
                "tags": ["美ゅら家uluサンゴの塗り壁", "ティーダ建築工房", "佐賀工務店", "佐賀暮らし"],
                "hook": "リゾートな暮らし🏝",
            },
        ],
    },
    {
        "handle": "kazu_ai_terasu", "name": "かず｜建設業の事務ラクAI",
        "is_own": True,
        "followers": 9,
        "following": 38,
        "posts": [
            {
                "date": "2026-11-04", "type": "image", "shortcode": "DfUZc-FlawD",
                "likes": 0, "comments": 0,
                "tags": ["建設業", "工務店", "日報", "AI活用", "業務改善", "建設業DX"],
                "hook": "【日報の下書き、音声メモから】現場の作業を終えてから、今日の出来事を思い出しながら日報を書く。",
            },
        ],
    },
]


def enrich(account: dict) -> dict:
    posts = account["posts"]
    total_likes = sum(p["likes"] for p in posts)
    total_comments = sum(p["comments"] for p in posts)
    n = len(posts)
    account["post_count"] = n
    account["total_likes"] = total_likes
    account["total_comments"] = total_comments
    account["avg_likes"] = round(total_likes / n, 2) if n else 0
    account["avg_comments"] = round(total_comments / n, 2) if n else 0
    account["engagement_rate_pct"] = (
        round((total_likes + total_comments) / n / account["followers"] * 100, 3) if n else 0
    )
    for p in posts:
        p["url"] = f"https://www.instagram.com/{account['handle']}/p/{p['shortcode']}/"
        p["tag_count"] = len(p["tags"])
    return account


def main() -> None:
    accounts = [enrich(a) for a in ACCOUNTS]
    payload = {
        "window": WINDOW,
        "crawled_at_jst": CRAWLED_AT,
        "source": "Instagram公開ページ（ログアウト）",
        "note": "保存数・シェア・リーチ・再生数・正確な投稿時刻は公開ページから取得不可。",
        "accounts": accounts,
    }
    out = DATA_DIR / "data_20261107.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out}")

    for a in accounts:
        print(f"{a['handle']:>22} f={a['followers']:>5} n={a['post_count']} "
              f"avg_like={a['avg_likes']:>6} er={a['engagement_rate_pct']:>6}%")


if __name__ == "__main__":
    main()
