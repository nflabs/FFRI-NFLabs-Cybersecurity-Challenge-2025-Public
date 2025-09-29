# writeup
配布ファイルの `cipher.txt` と `key.txt` から、鍵を使った何らかの暗号文であることが分かります。鍵が意味のある比較的短い英文であることから、使用可能な暗号方式は限定的です。インターネットで検索すると鍵を使った古典暗号「ヴィジュネル暗号」が見つかるでしょう。

ヴィジュネル暗号の復号は、Pythonで [復号スクリプト](solve.py) を書く方法や [CyberChef](https://gchq.github.io/CyberChef/#recipe=Vigen%C3%A8re_Decode('')) を使う方法があります。

 `key.txt` を鍵に指定して `cipher.txt` を復号すると以下の文章を得ることができます（以下の復号文は読みやすいように改行をしていますが、実際には改行されていません）。

```
haru ha akebono youyou shiroku nariyuku yamagiwa sukoshi akarite murasaki 
dachitaru kumo no hosoku tanabikitaru 
natsu ha yoru tsuki no koro ha sara nari yami mo nao hotaru no ooku 
tobichigaitaru mata tada hitotsu futatsu nado honoka ni uchihikarite 
iku mo okashi ame nado furu mo okashi 
aki ha yuugure yuuhi no sashite yama no ha ito chikou naritaru ni karasu 
no nedoko e iku tote mitsu yotsu futatsu mitsu nado tobiisogu sae aware 
nari maite kari nado no tsuranetaru ga ito chiisaku miyuru ha ito okashi 
hi irihatete kaze no oto mushi no ne nado hata iubeki ni arazu 
flag is makuranosoushi 
fuyu ha tsutomete yuki no furitaru wa iubeki nimo arazu shimo no ito shiroki 
mo mata sarademo ito samuki ni hi nado isogi okoshite sumimote wataru mo 
ito tsukizukishi hiru ni narite nuruku yurubi moteikeba hioke no hi mo 
shiroki hai gachi ni narite waroshi
```

文章を読み進めると、中盤に `flag is makuranosoushi` という文字列が出てきます。フラグは `makuranosoushi` です。
