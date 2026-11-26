# 道可道之孟子 · Android APK 打包工程

WebView 宿主 + 全站 assets（261 章页、261 图）。包名 `com.runze.daokedaomengzi`，minSdk 21，targetSdk 35。

- 构建：GitHub Actions `.github/workflows/apk.yml`（手工装 commandlinetools、platforms;android-35、build-tools;35.0.0，JDK 17 temurin，`gradlew assembleDebug`）。
- 产物：`道可道之孟子-v0.37.0.apk`，随 workflow artifact 下载，再挂 `docs/dl/` 与总站 `apk/`。
- 更新站点时：`cp docs/index.html docs/book.html assets` 重灌 `app/src/main/assets/`，升 `versionCode`／`versionName`。
