# amphora-image-builder
OpenStack Octaviaのamphora用イメージ作成ツール
Ubuntu 16.04(Xenial)で動作検証した

## Usage

```
$ git clone https://github.com/buty4649/amphora-image-builder
$ cd amphora-image-builder
$ vagrant up
$ vagrant ssh
# sudo OS_USERNAME=<username> OS_PASSWORD=<password> OS_AUTH_URL=<auth url> ./build.sh
```

## Tips

### /tmp/dib_build.******/mnt is not a directory というエラーがでる

自ホストのhostnameが正しく引けるように/etc/hostsを設定してください。
例えば、以下のようなコマンドで解決します。

```
$ sudo bash -c "echo $(hostname) >> /etc/hosts"
```

原因としては、内部的に `sudo losetup --show` を実行していて1行目にマウントパスが来ることを期待しています。しかしながら、hostnameが引けない場合はsudoの警告が出るためにエラーとなります。
sudoのエラー警告メッセージ例

```
sudo: unable to resolve host tuboyaki
```
