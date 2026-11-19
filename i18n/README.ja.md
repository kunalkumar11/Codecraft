<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/logo-dark.png">
    <img src="../assets/logo.png" width="220" alt="CodeCraft、怠け者のシニア開発者">
  </picture>
</p>

<h1 align="center">CodeCraft</h1>

<p align="center">
  <em>彼は何も言わない。一行だけ書く。それで動く。</em>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/50668?utm_source=repository-badge&utm_medium=badge&utm_campaign=badge-repository-50668" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/50668" alt="kunalkumar11%2FCodecraft | Trendshift" width="250" height="55"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/kunalkumar11/Codecraft?style=flat-square&color=111111&label=stars" alt="Stars">
  <img src="https://img.shields.io/github/v/release/kunalkumar11/Codecraft?style=flat-square&color=111111&label=release" alt="Release">
  <img src="https://img.shields.io/npm/v/@kunalkumar11/codecraft?style=flat-square&color=111111&label=npm" alt="npm">
  <img src="https://img.shields.io/badge/works%20with-20%20agents-111111?style=flat-square" alt="Works with 20 agents">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/50668" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/50668/daily" alt="kunalkumar11/Codecraft | Trendshift" width="250" height="55"/></a>
  <a href="https://trendshift.io/repositories/50668" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/50668/weekly" alt="kunalkumar11/Codecraft | Trendshift" width="250" height="55"/></a>
  <a href="https://trendshift.io/repositories/50668?utm_source=trendshift-badge&utm_medium=badge&utm_campaign=badge-trendshift-50668" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/50668/monthly?language=JavaScript" alt="kunalkumar11%2FCodecraft | Trendshift monthly ranking" width="250" height="55"/></a>
</p>

<p align="center">
  <img src="../assets/v5/hero-ja.jpg" width="880" alt="CodeCraft 5、ゼロから作り直した：コード -53%、時間 -41%、コスト -26%、トークン -45%。それでもリスクのあるロジックの 98% にテストが付く。CodeCraft なしでは 68%。">
</p>

<p align="center">
  <strong>CodeCraft 5：ゼロから作り直した。</strong><br>
  <strong>コード -53% &middot; 時間 -41% &middot; コスト -26% &middot; トークン -45%</strong><br>
  <strong>それでも：リスクのあるロジックの 98% にテストが付く。</strong>CodeCraft なしでは 68%。<br>
  <sub>Claude Code でベンチマーク。同じエージェントを skill あり・なしで比較：実際の FastAPI + React リポジトリを含む 39 タスク、Opus 5.5、各 5 回実行。<a href="#numbers">詳細</a>。</sub>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot; <a href="README.es.md">Español</a> &middot; <a href="README.ko.md">한국어</a> &middot; <a href="README.zh-CN.md">简体中文</a> &middot; 日本語</sub><br>
  <sub>英語の README からの翻訳です。内容が異なる場合は<a href="../README.md">英語版</a>が正です。</sub>
</p>

---

<p align="center">
  <a href="https://codecraft.dev/soon"><img src="../assets/waitlist-banner-ja.png" alt="何かが近づいている。ウェイトリストに登録" width="760"></a>
</p>

## CodeCraft で作られたもの

<a href="https://theretriever.app">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/retriever-logo-dark.svg">
    <img src="../assets/retriever-logo-light.svg" height="128" alt="Retriever">
  </picture>
</a>

---

あの人を知っているはずだ。長いポニーテール。楕円の眼鏡。バージョン管理システムより長く会社にいる。五十行を見せると、黙って眺めて、それを一行に置き換える。

CodeCraft は、その人をあなたの AI エージェントの中に入れる。

<a id="numbers"></a>
## 数字

<p align="center">
  <img src="../assets/v5/chart-ja.png" width="880" alt="skill なしのベースラインに対する割合。コード行数：CodeCraft v4.13 52%、CodeCraft 5 47%。出力トークン：57% と 55%。コスト：84% と 74%。時間：62% と 59%。">
</p>

<p align="center">
  <img src="../assets/v5/tests-ja.png" width="880" alt="コードは半分、それでもより良い：リスクのあるロジックの 98% にテストが付く（skill なし 68%）。エージェント自身のテストが、埋め込んだバグの 66% を捕まえる（skill なし 46%）。">
</p>

グラフに表れないことが二つある。ブラインド比較では、CodeCraft 5 の返答が前の CodeCraft の返答に 110 対 67 で勝った。そしてセキュリティの 6 タスク（SQL インジェクション、パストラバーサル、偽造トークン、レート制限、不正な CSV 行、キャッシュ）では、全 30 回の実行に合格した。コードは少なく、安全性は落ちない。手法、タスクごとの表、制約：[benchmarks/results/2026-10-07-agentic.md](../benchmarks/results/2026-10-07-agentic.md)。

**ルールは一度も「トークンを最小に」ではなかった。**ルールはこうだ：タスクに必要なものだけを書き、検証、エラー処理、セキュリティ、アクセシビリティは決して削らない。コードが小さくなるのは必要な分だけだからであって、無理に詰めたからではない。コストとレイテンシの低下は副次的な効果だ。

## ビフォー / アフター

<p align="center">
  <img src="../assets/v5/beforeafter-ja.png" width="880" alt="フロントエンドに日付ピッカーを追加する。skill なし：335 行、カレンダーと日付ピッカーを手作り。CodeCraft 5：リポジトリの Input を type date で再利用する 10 行のファイル一つ。カレンダーはブラウザが用意する。">
</p>

日付ピッカーを頼む。CodeCraft なしだと、エージェントは日付ピッカーのライブラリをインストールするか、カレンダーを丸ごと手で作る。335 行。CodeCraft 5 はまず、すでにあるものを見る。リポジトリには `Input` コンポーネントがあり、どのブラウザにも日付ピッカーがある。その二つを組み合わせる。10 行。

生き残った例は [examples/](../examples/) にもっとある。

## 作り直したレビュー

<p align="center">
  <img src="../assets/v5/review-ja.png" width="880" alt="作り直したレビュー。ベンチマークからの実際の /codecraft-review の指摘：変更でフィールド名が変わり、触れていないファイル src/routes/feed.js がクラッシュするようになった。必ず直す：Atom フィードがすべてのリクエストでクラッシュする。これが何か、問題、直し方、直さないと何が起きるかが書かれている。仕込んだ問題の 100% を発見（skill なし 87%）。diff の外にある問題の 100% を発見（skill なし 78%）。">
</p>

`/codecraft-review` は以前、削れるコードを探すだけだった。今は、壊れたときに呼び出されるシニア開発者のようにレビューする。diff だけでなく変更が触れるコードも読み、バグ、セキュリティ、実際の負荷、足りないテスト、速度、削れるものを確認する。各指摘には、そのコードが何をするか、何が問題か、直し方、直さないと何が起きるかが書かれる。

## 作り直した監査

<p align="center">
  <img src="../assets/v5/audit-ja.png" width="880" alt="リポジトリ全体を、重要な順に。まずこれを直す。倉庫の在庫を管理するリポジトリに対する、ベンチマークからの実際の /codecraft-audit：1 必ず直す、「1,200」と書かれたオフィスのバッチが完全に失敗する。2 必ず直す、インポートが不正な行を黙って飛ばす。3 必ず直す、オフィスのバッチで打ち間違えた SKU が黙って無視される。4 直すべき、リスクのあるコードパスにテストがない。5 できれば直す、オブジェクトでない body で API がクラッシュする。結論：まず 1 を直す。">
</p>

`/codecraft-audit` は同じチェックをリポジトリ全体に対して行う。まずコードの全体像をつかむ：エントリーポイント、データの流れ、プロジェクトが想定する負荷。それから見つけたものを重要な順に並べ、最初に何を直すべきかを教える。以前の監査は、削除するものを一覧にするだけだった。

## 5.3 の新機能：バンド

<p align="center">
  <img src="../assets/band/band.png" width="880" alt="Claude Code のプロンプトの上にある CodeCraft のバンド。詳細モード：コスト $23.80、直近のターン $1.14、1 ターン平均 $0.72。トークン 56.7M、出力 168k、33 ターン。エージェント時間 52m 14s。再利用 71%（既存 5、新規 2）。最後の変更のあとテストは成功。コンパクトモードは同じ内容を 1 行で表示する。">
</p>

Claude Code では、CodeCraft がプロンプトの上にバンドを表示するようになった。いまのタスクのコスト、使ったトークンとエージェント時間、新しいコードを書く代わりに既存のコードをどれだけ再利用したか、最後の変更のあとにテストが通ったか。ボタンでレベルを切り替え、`/codecraft-review` や `/codecraft-audit` を実行し、タスクを Markdown でコピーし、バンドを 1 行にたためる。不要なら `/codecraft band` で隠せる。同じコマンドでまた表示される。Claude Code 2.1.290 以降が必要で、ターミナルかデスクトップアプリで表示される。VS Code のチャットパネル、クラウドセッション、`claude -p` では表示されない。

<p align="center">
  <img src="../assets/band/board.png" width="880" alt="CodeCraft のボード（ローカルページ）：直近 30 日でセッション 61、エージェント時間 20h 13m、$285.30、トークン 492.5M。プロジェクトごとのエージェント時間の推移、テスト結果つきの最近のセッション、作業した日と連続記録。">
</p>

**Board** は、すべてのプロジェクトのタスクをまとめたローカルページを開く。時間ごとのコスト、エージェント時間、トークン、テスト結果つきのセッション一覧、作業した日。デフォルトでは、すべて自分のマシンの `~/.config/codecraft/band/` に残る。`/codecraft band import` で、過去の Claude Code セッションをコスト、エージェント時間、トークンと一緒にボードに追加できる。

## 仕組み

<p align="center">
  <img src="../assets/v5/ladder-ja.png" width="880" alt="コードを書く前に、最初に成り立つ段で止まる：1 それは本当に必要か、2 もうこのコードベースにあるか、3 標準ライブラリでできるか、4 プラットフォームの標準機能、5 インストール済みの依存関係、6 一行で済むか、7 そこで初めて動く最小限のコード。ロジックがあれば小さなテストを一つ。">
</p>

このはしごは問題を理解した*あと*に動く。理解の代わりではない。変更が触れるコードを読み、実際の流れを追ってから段を選ぶ。解決策には怠けるが、読むことには決して怠けない。

怠け者だが、いい加減ではない。信頼境界での入力検証、データ損失への対処、セキュリティ、アクセシビリティは決して削らない。

分岐、ループ、パーサー、お金、セキュリティを含むロジックには、小さなテストを一つ残す。返答の最後には必ず、省いたことや確認していないこと、知っておくべきリスクが書かれる。

## プロンプト

CodeCraft はひとつのプロンプトだ：[`skills/codecraft/SKILL.md`](../skills/codecraft/SKILL.md)。ルールファイルを読むエージェント向けの短縮版は [`AGENTS.md`](../AGENTS.md)。このリポジトリの残りは、すべてそのプロンプトをいろいろなエージェントに読み込ませるためのものだ。

## インストール

**Claude Code**、二つのプロンプトに分けて：

```
/plugin marketplace add kunalkumar11/Codecraft
```
/plugin install codecraft@codecraft
```

**Codex：**

```bash
codex plugin marketplace add kunalkumar11/Codecraft
codex plugin add codecraft@codecraft
```

そのあと Codex で `/hooks` を開き、二つのライフサイクルフックを信頼して、新しいスレッドを始める。

**その他のエージェント：**[`AGENTS.md`](../AGENTS.md) をプロジェクトにコピーするか、エージェントに [`skills/codecraft/SKILL.md`](../skills/codecraft/SKILL.md) を skill としてインストールするよう頼む。Copilot、Cursor、OpenCode、Gemini などの手順（英語）：**[INSTALL.md](../INSTALL.md)**。

これで終わり。彼なら満足するだろう。口には出さないが。

毎セッション有効で、いくつかのコマンドがある（[コマンド](#commands)を参照）。`/codecraft ultra` は、コードベースに個人的に腹が立ったとき用だ。起動時とモード切り替え時に、現在のモードが表示される。

CodeCraft は GitHub の `kunalkumar11/Codecraft` か npm の `@kunalkumar11/codecraft` からだけインストールすること。`.exe` や `.dll` ファイルは決して含まれない。それを含むコピーは私のものではない。

<a id="commands"></a>
## コマンド

| コマンド | 内容 |
|----------|------|
| `/codecraft [lite \| full \| ultra \| off]` | 強度を設定するか、オフにする。引数なしの場合、オフならデフォルトのレベルでオンにし、オンなら現在のレベルを表示する。 |
| `/codecraft band [on \| off]` | Claude Code のみ：プロンプトの上のバンドを隠す、または表示する。引数なしで切り替える。レベルは変わらない。 |
| `/codecraft band import` | Claude Code のみ：過去のセッションをコスト、エージェント時間、トークンと一緒にボードに追加する。 |
| `/codecraft-review` | 壊れたときに呼び出されるシニア開発者のように、現在の diff をレビューする：バグ、セキュリティ、実際の負荷、テストのない危険なコード、遅い処理、削れるもの。各指摘には、そのコードが何をするか、何が問題か、直し方、直さないと何が起きるかが書かれる。範囲を狭めたり広げたりするには、対象を普通の言葉で書く：`uncommitted`、`staged`、`branch`、または PR のリンク。 |
| `/codecraft-audit` | 同じチェックをリポジトリ全体に対して行い、重要な順に並べる。 |
| `/codecraft-debt` | 後回しにした `shortcut:` の近道を一覧にまとめ、「あとで」が「永遠にやらない」にならないようにする。 |
| `/codecraft-gain` | ベンチマークで測定した効果（コード削減、コスト削減、速度向上）をスコアボードで表示する。 |
| `/codecraft-help` | 上記コマンドのクイックリファレンス。 |

コマンドには skill に対応したホストが必要だ（Claude Code、Codex、Devin CLI、OpenCode、Gemini、Antigravity CLI、pi、Hermes Agent、Qoder、Grok Build）。Codex CLI と IDE 拡張では、プラグインの名前空間の下にある skill なので、`$codecraft:codecraft-review` のように呼び出す。[フック](../INSTALL.md#cursor)を使う Cursor では `/codecraft` のレベル切り替えだけが使え、普通のメッセージとして入力する。指示だけのアダプター（Cursor のルールファイル、Windsurf、Cline、Copilot、Kiro、Antigravity の `AGENTS.md` フォールバック）は、コマンドなしで常時有効なルールだけを読み込む。

## よくある質問

**設定ファイルは必要？**
いらない。任意の `~/.config/codecraft/config.json` か環境変数 `CODECRAFT_DEFAULT_MODE` でデフォルトのレベルを設定できるが、必須のものはない。

**なぜ `shortcut:` コメントを書くの？**
意図的な近道と、いつ見直すかを示すため。`/codecraft-debt` がそれを一覧にまとめる。別の単語にしたい、あるいは書かせたくない？ プロジェクトの `CLAUDE.md` か `AGENTS.md` にそう書いて、`/codecraft-debt <好きな単語>` を実行すればいい。

**120 行のキャッシュクラスが本当に必要だったら？**
必要ない。それでも言い張れば作ってくれる。ゆっくり。正確に。あなたを見つめながら。

**スケールする？**
書かなかったコードは無限にスケールする。バグ 0、CVE 0、太古の昔から稼働率 100%。

**なぜ「CodeCraft」？**
理由はよくわかっているはずだ。

## スポンサー

<p align="center">
  <a href="https://greenpt.com/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="../assets/logo-greenpt-dark.svg">
      <img src="../assets/logo-greenpt.svg" width="260" alt="GreenPT">
    </picture>
  </a>
</p>

## ライセンス

[MIT](../LICENSE)。動く中でいちばん短いライセンス。

## スター履歴

<a href="https://www.star-history.com/kunalkumar11/Codecraft#history">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=kunalkumar11/Codecraft&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=kunalkumar11/Codecraft&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=kunalkumar11/Codecraft&type=Date" />
 </picture>
</a>