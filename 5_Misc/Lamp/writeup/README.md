# Lamp - 解説
- 想定難易度：Easy
- 正解フラグ：flag{pico_gpio_master}

# 1.設計意図
GPIOピンや回路図の読み解き、サンプルプログラムと実際の接続を照らし合わせて論理的に正解にたどり着いていただく出題構成です。
ハードウェアCTFやセキュリティバッジの設計に見られる手法と同様、初学者に「自分で動かす→考える→理解する」循環を体験いただく意図となります。

# 2.解法
1. ピンオブジェクトは、特定のI/Oピンを一意に指定する識別子を用いて構築されます。参考：[class Pin](https://docs.micropython.org/en/latest/library/machine.Pin.html)
2. プログラムを見ると led = Pin(18, Pin.OUT) と記載されています。Pin 関数は、第1引数に使用するGPIO（Raspberry Pi上に搭載されている信号ピン）、第2引数にピンモード（ピンをどのように使うか）を指定しています。今回のプログラムでは、GPIO 18 を出力端子として設定していることがわかります。
3. Raspberry Pi PicoのどのPIN番号に接続するかを確認するため、「Raspberry Pi Pico PIN」などのキーワードで調査を行います。参考：[Raspberry Pi Pico Datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf )
4. [Raspberry Pi Pico Datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf )のp4に記載されているピン配置図によると、GPIO18は物理的なピン番号24に対応していることが確認できます。つまり、Pin(18, Pin.OUT)と指定すると、ボード上のヘッダーピン24番を実際に制御することができます。
5. 既にピン番号23(GND)に配線されておりますが、回路図に示されているLEDはPIN24に接続されていません。正しくLEDを点灯させるには、PIN24を使って接続することで回路が完成します。
6. Webページの解答欄に`24`と入力するとflagが入手できます。


