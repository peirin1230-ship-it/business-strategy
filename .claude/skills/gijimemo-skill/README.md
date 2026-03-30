# 📝 gijimemo-skill

高松智史氏の「議事録進化論」に基づく、**最上レベルの議事メモ**を自動生成する Claude Skills。

会議の文字起こし・要約・走り書きメモを投げるだけで、論点ベースで構造化された議事メモ（ステージ7）が完成します。

---

## 🎯 何ができるか

| 入力 | 出力 |
|------|------|
| Zoom / Teams / otter / notta 等の文字起こし | 論点ベースで構造化された議事メモ |
| 会議の箇条書きメモ・走り書き | 仮説の進化＋ネクスト論点つき議事メモ |
| 既存の議事録（レベルアップ依頼） | ステージ7品質に引き上げた議事メモ |

## 📊 議事録進化論とは

高松智史氏（元BCG、考えるエンジン講座代表）が提唱する議事録の7段階進化モデル。

```
発言録（バリューゼロ）
  ↓
議事録 Lv.1 ─ 全発言が漏れなく記載
議事録 Lv.2 ─ テーマベースで構造化＋ネクストステップ
議事録 Lv.3 ─ 空気感が加味されている
  ↓
議事メモ Lv.4 ─ 論点ベースで構造化        ← ここから別次元
議事メモ Lv.5 ─ 仮説の進化が記録されている
議事メモ Lv.6 ─ ネクスト論点が書かれている
議事メモ Lv.7 ─ 全要素統合＋即時共有      ← このスキルが目指すレベル
```

## 🗂 ファイル構成

```
gijimemo-skill/
├── SKILL.md                        # メインスキル定義（処理フロー・原則）
├── references/
│   ├── stages.md                   # 議事録進化論 7ステージ詳解
│   └── output_format.md            # 出力フォーマット＋記載ルール
├── examples/
│   ├── input_sample.md             # 入力サンプル（文字起こし）
│   └── output_sample.md            # 出力サンプル（議事メモ）
├── README.md
├── LICENSE
└── .gitignore
```

## 🚀 インストール方法

### Claude Code / Cowork で使う場合

```bash
git clone https://github.com/peirin1230-ship-it/gijimemo-skill.git
# スキルフォルダに配置（環境に応じてパスを変更）
cp -r gijimemo-skill /path/to/your/skills/
```

### Claude.ai プロジェクトで使う場合

1. Claude.ai → Projects → 「Create project」
2. プロジェクト名: `議事メモ作成`
3. 「Set custom instructions」に `SKILL.md` の内容をコピー＆ペースト
4. 「Add knowledge」に `references/stages.md` と `references/output_format.md` を追加

## 💡 使い方

以下のようにClaudeに話しかけるだけでスキルが発動します。

```
この会議の文字起こしを議事メモにしてください：
（文字起こしテキストを貼り付け）
```

```
以下のミーティングメモを議事録進化論の最上レベルに引き上げてください：
（既存の議事録を貼り付け）
```

```
Zoomの文字起こしデータを添付しました。議事メモを作成してください。
```

## 🔑 議事メモの5つの核心

このスキルが生成する議事メモの特徴：

1. **論点ベース構造化** — テーマではなく「問い」で整理する
2. **仮説の進化** — 会議前後で認識がどう変わったかを Before/After で明示
3. **ネクスト論点** — TASKだけでなく「次に解くべき問い」を先に記載
4. **空気感の言語化** — 「全力賛成」vs「しぶしぶ賛成」の温度感を伝える
5. **独り歩きできるメモ** — 会議不参加者がこれだけで状況を完全に把握できる

## 📚 参考文献

- 高松智史『コンサルが「最初の3年間」で学ぶコト』（ソシム、2023）
- 高松智史『変える技術、考える技術』（実業之日本社、2021）
- [考えるエンジン講座](https://kanataw.com/)
- [議事録の考え方・作成術のポイント（公式解説）](https://kanataw.com/knowledge/all/becoming-a-consultant/consultant-work-technique/evolution-of-meeting-minutes/)

## 📄 ライセンス

MIT License
