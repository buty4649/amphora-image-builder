keepalived-status-check
=======================

keepalivedのステータスをチェックし、MASTER昇格時にNeutron APIを叩きport情報を更新する。

なぜ必要か？
-----------

OpenStack MitakaでDVR構成を使っているとVIPポートがホストにbindingされない。
また、bindingされてもMASTER側のAmphoraと同じホストにbindされないとうまく通信できない。
このelementではこの問題を解決を行う。

使い方
------

以下の環境変数を設定しbuild.shを実行する。

* `$OS_USERNAME`
* `$OS_PASSWORD`
* `$OS_AUTH_URL`
