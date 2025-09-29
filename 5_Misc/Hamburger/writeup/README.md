# Hamburger - 解説

## 1. 設計意図
与えられた情報（日時、場所など）をもとに、現実世界の公開情報を調査し、それらを関連づけながら目的の資料へとたどり着くプロセスを体験することで、「連想力」と「調査の深堀りを行う力」を養うことを目的としています。

またこの問題を通して、「ネット上に公開されている情報だけでも、丁寧に辿っていくことでより詳細な情報にアクセスできる」ことを実感してもらうと同時に、「情報の扱い方やその責任」について考えるきっかけとなることも意図しています。

## 2. 解法
1. 「株式会社エヌ・エフ・ラボラトリーズ（以下、NFLabs.）」の社員がハンバーガーを食べたレストランと、その日付を調査します。
2. 「NFLabs. hamburger」などのキーワードで検索したり、2024年8月以降のNFLabs.のエンジニアブログを確認すると、以下の記事が見つかります：  
   [はじめての海外のカンファレンスに行ってきました@DEF CON](https://blog.nflabs.jp/entry/2024/09/19/133000)
3. 記事の内容から、NFLabs.の社員がラスベガスにあるカフェ「Cafe 325」でハンバーガーを食べたことが確認できます。
4. 記事に掲載されたハンバーガーの写真のEXIF情報を確認すると、撮影日は2024年8月10日であることがわかります：  
   [ハンバーガーの画像](https://cdn-ak.f.st-hatena.com/images/fotolife/k/ka_miyazawa/20240906/20240906145042.jpg)
5. 問題文にはNFLabs.の株主会社への言及があるため、NFLabs.の株主会社を調査すると、以下のページが見つかります：
   [会社情報 | N.F.Laboratories Inc.](https://nflabs.jp/company/)
6. ページ内容から、NFLabs.の株主は「NTTドコモビジネス株式会社（以下、ドコモビジネス）」と「株式会社ＦＦＲＩセキュリティ（以下、FFRI）」の2社が該当することがわかります。
7. 以上の情報と問題文の内容から、以下の条件すべてを満たすイベントを特定する必要があります：
   * 2024年8月8日にラスベガスで開催されていること
   * NFLabs.の社員は参加していないこと
   * ドコモビジネスまたはFFRIの社員が講演を行っていたこと
8. ドコモビジネスについて検索しても、上記条件を満たす記事は見つかりません。一方で「FFRI Las Vegas」などのキーワードで検索すると、以下の記事が見つかります：  
[弊社リサーチエンジニアがBlack Hat USA 2024に登壇します！](https://www.ffri.jp/blog/2024/06/2024-06-21.htm)
9. 上記記事の内容から、「Black Hat USA 2024」は2024年8月3日から8日まで開催されていたことがわかります。
10. また、解法手順3で見つけた記事内には、NFLabs.の社員が「Black Hat への参加を見送った」との記述があるため、「Black Hat USA 2024」は解法手順7の条件をすべて満たすイベントであることが確認できます。
11. 「FFRI Black Hat USA 2024」などのキーワードで検索すると、次の記事が見つかります：  
   [Black Hat USA 2024 の登壇経緯・感想・発表紹介](https://engineers.ffri.jp/entry/2024/11/25/000000)
12. 記事内のリンクから、「Black Hat USA 2024」の講演詳細ページへ遷移することができます：  
   [You've Already Been Hacked: What if There Is a Backdoor in Your UEFI OROM?](https://www.blackhat.com/us-24/briefings/schedule/#you39ve-already-been-hacked-what-if-there-is-a-backdoor-in-your-uefi-orom-39579)
13. ページ内の「Presentation Materials」リンクを開くと、当該講演で使用されたスライドを確認できます：  
   [講演で使用されたスライド](https://i.blackhat.com/BH-US-24/Presentations/US24-Matsuo-Youve-Already-Been-Hacked-What-if-There-Is-a-Backdoor-in-Your-UEFI-OROM-Thursday.pdf)
14. スライドの15ページ目に、フラグが記載されているため、それをそのままの形式で提出します。
