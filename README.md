## 快速入门

### 安装

#### 通过本地路径使用

1. 解压SDK压缩包到你的项目目录旁边，例如：
```
your_project/
├── lib/
└── pubspec.yaml
WuKongIMFlutterSDK/
├── lib/
└── pubspec.yaml
```

2. 在你的项目的`pubspec.yaml`中添加依赖：
```yaml
dependencies:
  wukongimfluttersdk:
    path: ../WuKongIMFlutterSDK  # 根据实际SDK位置调整路径
```

安装完成后，运行以下命令更新依赖：
```bash
flutter pub get
```

### 使用方法

#### 引入
```dart
import 'package:wukongimfluttersdk/wkim.dart';
```

#### 初始化SDK
```dart
WKIM.shared.setup(Options.newDefault('uid', 'token'));
```

#### 初始化IP
```dart
WKIM.shared.options.getAddr = (Function(String address) complete) async {
    // 可通过接口获取后返回
    String ip = await HttpUtils.getIP();
    complete(ip);
};
```

#### 连接
```dart
WKIM.shared.connectionManager.connect();
```

#### 断开
```dart
// isLogout true：退出并不再重连 false：退出保持重连
WKIM.shared.connectionManager.disconnect(isLogout)
```

#### 发消息
```dart
WKIM.shared.messageManager.sendMessage(WKTextContent('我是文本消息'), WKChannel(channelID, channelType));
```

## 监听

#### 连接监听
```dart
WKIM.shared.connectionManager.addOnConnectionStatus('home',
        (status, reason,connectInfo) {
      if (status == WKConnectStatus.connecting) {
        // 连接中
      } else if (status == WKConnectStatus.success) {
        var nodeId = connectInfo?.nodeId; // 节点id
        // 成功
      } else if (status == WKConnectStatus.noNetwork) {
        // 网络异常
      } else if (status == WKConnectStatus.syncMsg) {
        //同步消息中
      } else if (status == WKConnectStatus.syncCompleted) {
        //同步完成
      }
    });
```

#### 消息入库
```dart
WKIM.shared.messageManager.addOnMsgInsertedListener((wkMsg) {
      // todo 展示在UI上
    });
```

#### 收到新消息
```dart
WKIM.shared.messageManager.addOnNewMsgListener('chat', (msgs) {
      // todo 展示在UI上
    });
```

#### 刷新某条消息
```dart
WKIM.shared.messageManager.addOnRefreshMsgListener('chat', (wkMsg) {
      // todo 刷新消息
    });
```

#### 命令消息(cmd)监听
```dart
WKIM.shared.cmdManager.addOnCmdListener('chat', (cmdMsg) {
    // todo 按需处理cmd消息
});
```

> 注意：包含`key`的事件监听均有移除监听的方法，为了避免重复收到事件回调，在退出或销毁页面时通过传入的`key`移除事件。

## 许可证

悟空IM 使用 Apache 2.0 许可证。有关详情，请参阅 LICENSE 文件。