#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ===== 鑑定内容 =====
READINGS = {
    1: {
        "title": "ナンバー 1 ／ 開拓者・リーダー",
        "keyword": "独立・挑戦・創造",
        "personality": (
            "あなたは生まれながらのリーダーです。強い意志と独自の視点を持ち、自らの道を切り開く力があります。"
            "周囲に流されず、自分の信念に従って行動できる強さが最大の武器です。"
            "新しいことへの挑戦を恐れず、常に前を向いて進んでいきます。"
        ),
        "love": (
            "恋愛では情熱的でまっすぐです。対等な関係を築ける相手と最も輝きます。"
            "束縛や依存は苦手なので、お互いの自由を尊重し合えるパートナーシップが理想です。"
        ),
        "work": (
            "独立・起業・リーダーポジションに向いています。"
            "自ら決断する立場の方が力を発揮でき、競争の激しい分野でも臆することなく挑めます。"
        ),
        "lucky_color": "赤・ゴールド",
        "lucky_number": "1・10・19",
        "advice": "あなたの人生テーマは「自立と創造」。失敗を恐れず一歩踏み出す勇気があなたの最大の才能です。",
        "talent": (
            "あなたの最大の才能は「先頭に立つ力」です。誰もやったことのないことに挑む開拓者精神、"
            "強烈な集中力と行動力は、周囲の人々を鼓舞します。"
            "また、物事の本質を素早く見抜く直観力も大きな強みです。"
        ),
        "challenge": (
            "頑固になりすぎて周囲の意見を聞けなくなることがあります。"
            "「一人でやり遂げたい」気持ちが強すぎて、助けを求めることを苦手に感じるかもしれません。"
            "信頼できる仲間に任せる勇気を持つことが、さらなる成長への鍵です。"
        ),
        "love_detail": (
            "恋愛においては、追いかけることに燃えるタイプです。"
            "ただし、手に入れた後に情熱が冷めやすい傾向があります。"
            "相手への尊敬と好奇心を持ち続けることが長続きの秘訣。"
            "相性の良い相手はナンバー3・5・9で、特に3との組み合わせは創造性が高まります。"
        ),
        "work_detail": (
            "起業家・経営者・プロジェクトリーダーとして最高の力を発揮します。"
            "スポーツ選手、パイロット、外科医など、プレッシャー下で実力を出す仕事も向いています。"
            "苦手なのは細かいルーティン作業や、誰かの指示に従い続けること。"
            "自分でゴールを設定できる環境を選びましょう。"
        ),
        "fortune_2026": (
            "2026年はあなたにとって「新しいサイクルの幕開け」の年です。"
            "数秘術的に見ても、今年は種まきに最適なタイミング。"
            "春から夏にかけて新しいチャレンジを始めると吉。"
            "仕事面では大きな転換点が訪れる可能性があります。勇気を持って飛び込んでください。"
            "健康面では無理をしすぎる傾向があるため、睡眠と休息を意識的に取ることが大切です。"
        ),
        "theme_2026": "新しい扉を開く年",
        "compatible": "3・5・9",
        "lucky_stone": "ルビー・ガーネット",
        "lucky_day": "火曜日・日曜日",
        "lucky_direction": "東・南東",
    },
    2: {
        "title": "ナンバー 2 ／ 調和の人・サポーター",
        "keyword": "協調・直感・愛",
        "personality": (
            "あなたは繊細な感受性と高い共感力を持つ、心の温かい人です。"
            "場の空気を読む力に長け、周囲との調和を大切にします。"
            "強さより柔らかさで周囲を包み込み、そっと支えるその姿勢が多くの人に愛されます。"
        ),
        "love": (
            "恋愛では献身的で思いやりにあふれたパートナーになります。"
            "ただし尽くしすぎてしまう傾向があるので、自分の気持ちも大切に。"
            "安心感と信頼を与えてくれる穏やかな関係を望んでいます。"
        ),
        "work": (
            "チームワークを活かせる仕事が向いています。"
            "カウンセラー、看護師、教育者など人をサポートする職種で実力を発揮します。"
        ),
        "lucky_color": "オレンジ・ピンク",
        "lucky_number": "2・11・20",
        "advice": "あなたの人生テーマは「調和と共感」。自分も相手も大切にするバランスを意識してください。",
        "talent": (
            "あなたの才能は「人の心を読む力」です。言葉にならない気持ちを察知し、"
            "そっと寄り添える存在として多くの人に頼られます。"
            "また、仲介・調停の才能も抜群で、対立する双方の立場を理解し橋渡しができます。"
        ),
        "challenge": (
            "相手を優先しすぎて、自分の気持ちや意見を後回しにしてしまいがちです。"
            "NOと言えずに溜め込み、突然爆発してしまうことも。"
            "「自分の意見を伝えることも相手への思いやり」と心がけましょう。"
        ),
        "love_detail": (
            "恋愛では相手に尽くすことに喜びを感じます。"
            "ただし、自己犠牲が強くなりすぎると関係が不健全になることも。"
            "「ありがとう」と「ごめんなさい」が素直に言える相手を選びましょう。"
            "相性の良い相手はナンバー6・8・9で、特に6との安心感は格別です。"
        ),
        "work_detail": (
            "カウンセラー、心理士、保育士、医療従事者、外交官、秘書などが向いています。"
            "縁の下でチームを支える役割で真価を発揮します。"
            "評価されにくい環境だとモチベーションが下がりやすいため、"
            "感謝を大切にしてくれる職場・上司を選ぶことが重要です。"
        ),
        "fortune_2026": (
            "2026年は「人間関係が豊かになる年」です。"
            "新しい出会いが増え、特に秋以降に重要なパートナーシップが生まれる予感があります。"
            "仕事では縁の下の力持ちとしての活躍が評価される時期。"
            "恋愛面では自分の気持ちを正直に伝えることで関係が深まります。"
            "健康面では感情のデトックスを意識して。日記や瞑想が吉です。"
        ),
        "theme_2026": "絆を深める年",
        "compatible": "6・8・9",
        "lucky_stone": "ムーンストーン・ローズクォーツ",
        "lucky_day": "月曜日・金曜日",
        "lucky_direction": "西・北西",
    },
    3: {
        "title": "ナンバー 3 ／ 表現者・クリエイター",
        "keyword": "創造・表現・喜び",
        "personality": (
            "あなたは豊かな表現力と明るいエネルギーを持つ、周囲を元気にする存在です。"
            "芸術的な才能や独自のアイデアで人々を魅了します。"
            "好奇心旺盛で飽きっぽい一面もありますが、その分多彩な才能の持ち主です。"
        ),
        "love": (
            "恋愛では楽しさと刺激を大切にします。一緒にいて笑顔になれる相手に惹かれます。"
            "愛情表現はストレートで情熱的。変化を楽しめる関係性がベストです。"
        ),
        "work": (
            "デザイナー、ライター、俳優、ミュージシャンなど表現や発信が伴う職種が向いています。"
            "アイデアを形にすることに喜びを感じます。"
        ),
        "lucky_color": "黄色・ライトブルー",
        "lucky_number": "3・12・21",
        "advice": "あなたの人生テーマは「表現と創造」。自分の感性を信じて思い切り表現することで道が開けます。",
        "talent": (
            "あなたの才能は「喜びを生み出す力」です。言葉、音楽、アート、ユーモアなど"
            "あらゆる表現手段であなたのエネルギーは輝きます。"
            "また、初対面の人とすぐに打ち解けるコミュニケーション力も天賦の才です。"
        ),
        "challenge": (
            "楽しいことに集中しすぎて、やりかけのことを放置してしまいがちです。"
            "感情の波が激しく、落ち込む時は極端に落ち込むことも。"
            "「完成させる力」を意識的に鍛えることが人生の大きなテーマです。"
        ),
        "love_detail": (
            "恋愛では楽しさと新鮮さを求めます。マンネリを感じると気持ちが離れやすいのが課題。"
            "相手を褒めること、驚かせることが得意で、モテる要素をたくさん持っています。"
            "長続きするには、楽しいだけでなく深い話ができる相手を選ぶことが大切です。"
            "相性の良い相手はナンバー1・5・9で、特に9との深い精神的な繋がりは最高です。"
        ),
        "work_detail": (
            "クリエイター、エンターテイナー、コピーライター、俳優、YouTuber、デザイナーが天職。"
            "自分のアイデアや個性を活かせる場所が最高の職場です。"
            "ルーティンが多い事務職などは長続きしません。"
            "副業やフリーランスでの成功事例が多いナンバーでもあります。"
        ),
        "fortune_2026": (
            "2026年は「才能が開花する年」です。"
            "これまで温めてきたアイデアや作品を世に出す絶好のタイミング。"
            "SNSやオンラインでの発信が特に吉。夏から秋にかけて大きなチャンスが訪れます。"
            "恋愛面では出会いが豊富な年。直感を信じて積極的に動いて。"
            "健康面では散漫になりがちなので、一日一つだけ目標を決める習慣が効果的です。"
        ),
        "theme_2026": "才能が開花する年",
        "compatible": "1・5・9",
        "lucky_stone": "シトリン・アメジスト",
        "lucky_day": "水曜日・木曜日",
        "lucky_direction": "南・南西",
    },
    4: {
        "title": "ナンバー 4 ／ 堅実な建設者",
        "keyword": "安定・努力・誠実",
        "personality": (
            "あなたは誠実さと堅実さを兼ね備えた、信頼できる人物です。"
            "コツコツと努力を積み重ねることが得意で、どんな困難にも粘り強く向き合います。"
            "ルールや秩序を大切にし、周囲から「安心できる人」と評価されます。"
        ),
        "love": (
            "恋愛では真剣で誠実なパートナーになります。"
            "愛情表現は不器用かもしれませんが、行動で誠意を示します。"
            "信頼と安定を築ける相手との関係が最も幸せを感じられます。"
        ),
        "work": (
            "管理職、エンジニア、会計士、建築家など地道な努力が実を結ぶ職種が向いています。"
            "長期的に安定したキャリアを築いていけます。"
        ),
        "lucky_color": "グリーン・ネイビー",
        "lucky_number": "4・13・22",
        "advice": "あなたの人生テーマは「安定と構築」。焦らず一歩一歩着実に進んでください。",
        "talent": (
            "あなたの才能は「確実に積み上げる力」です。一度決めたことを諦めない持続力と"
            "几帳面さは、長期的なプロジェクトで絶大な威力を発揮します。"
            "また、リスク管理の能力が高く、問題が起きる前に察知して対処できます。"
        ),
        "challenge": (
            "完璧主義が行き過ぎて、前に進めなくなることがあります。"
            "また、変化を恐れて古いやり方に固執してしまう場面も。"
            "「80点で動き出す勇気」を持つことが成長のカギです。"
        ),
        "love_detail": (
            "恋愛では非常に慎重です。じっくり相手を見極めてから動くため、告白が遅くなりがちです。"
            "一度好きになったら深く愛し、安定した関係を大切にします。"
            "浮気や嘘には非常に敏感で、裏切られると立ち直るのに時間がかかります。"
            "相性の良い相手はナンバー2・6・8で、特に8との現実的なパートナーシップは最強です。"
        ),
        "work_detail": (
            "建築士、エンジニア、会計士、法律家、プロジェクトマネージャーが向いています。"
            "「きちんとやる」ことが求められる分野で頭角を現します。"
            "創造性より手順と品質が重視される環境が最適です。"
            "副業よりも一つの仕事を深堀りする方が成果が出やすいタイプです。"
        ),
        "fortune_2026": (
            "2026年は「努力が実を結ぶ年」です。"
            "これまでコツコツ続けてきたことが形になり、周囲からの評価が高まります。"
            "仕事面では昇進や資格取得など具体的な成果が期待できます。"
            "恋愛面では安定志向が吉と出る年。真剣交際や結婚を意識した動きも◎。"
            "健康面では運動不足になりやすいため、毎日少しの散歩を心がけて。"
        ),
        "theme_2026": "努力が実を結ぶ年",
        "compatible": "2・6・8",
        "lucky_stone": "エメラルド・ジェイド",
        "lucky_day": "土曜日・火曜日",
        "lucky_direction": "北・北東",
    },
    5: {
        "title": "ナンバー 5 ／ 自由人・冒険家",
        "keyword": "自由・変化・冒険",
        "personality": (
            "あなたは自由を愛し、変化を恐れない冒険者です。"
            "好奇心が旺盛で、新しいことへの適応力が高く、どんな状況でも楽しみを見つけられます。"
            "型にはまることを嫌い、独自の生き方を追求していきます。"
        ),
        "love": (
            "恋愛では自由と刺激を大切にします。束縛を嫌い、お互いの独立性を尊重できる関係を好みます。"
            "変化を楽しめる柔軟なパートナーと長く続く関係を築けます。"
        ),
        "work": (
            "旅行業、フリーランス、営業など変化や移動が多い仕事が向いています。"
            "複数のスキルを活かしたマルチな働き方も得意です。"
        ),
        "lucky_color": "ターコイズ・シルバー",
        "lucky_number": "5・14・23",
        "advice": "あなたの人生テーマは「自由と変化」。多くの経験があなたを豊かにします。",
        "talent": (
            "あなたの才能は「どんな環境にも適応できる柔軟性」です。"
            "変化の激しい時代において最も輝くタイプで、複数の分野を横断するマルチな才能があります。"
            "また、言語や文化の壁を軽々と越えるコミュニケーション力も天賦の才です。"
        ),
        "challenge": (
            "一つのことを続けることが苦手で、飽きると突然やめてしまいがちです。"
            "責任から逃げたくなる衝動に負けることも。"
            "「自由には責任が伴う」ことを意識し、やり抜く経験を積むことが大切です。"
        ),
        "love_detail": (
            "恋愛では自由を与えてくれる相手を求めます。"
            "支配的な相手や束縛が多い関係は長続きしません。"
            "旅行や冒険を共に楽しめる、同じ感性のパートナーが理想です。"
            "相性の良い相手はナンバー1・3・7で、特に7との知的な刺激は格別です。"
        ),
        "work_detail": (
            "フリーランス、起業家、旅行ガイド、記者、コンサルタント、営業職が向いています。"
            "デスクに座りっぱなしの仕事よりも、外に出て動き回る仕事が向いています。"
            "副業や複業での成功率が高いナンバーです。"
            "飽きたらすぐ辞める傾向があるので、短期集中型のプロジェクトを選ぶのも賢明です。"
        ),
        "fortune_2026": (
            "2026年は「世界が広がる年」です。"
            "新しい場所、新しい人、新しい経験があなたを待っています。"
            "特に海外や異文化との接点が運を開くキーになりそうです。"
            "仕事面では独立や転職のチャンスが訪れます。直感を信じて動いてみて。"
            "健康面では不規則な生活に注意。食事と睡眠のリズムを整えることが吉です。"
        ),
        "theme_2026": "世界が広がる年",
        "compatible": "1・3・7",
        "lucky_stone": "ターコイズ・アクアマリン",
        "lucky_day": "水曜日・金曜日",
        "lucky_direction": "東・南東",
    },
    6: {
        "title": "ナンバー 6 ／ 愛の人・調停者",
        "keyword": "愛・責任・奉仕",
        "personality": (
            "あなたは愛情深く、面倒見のよい人です。"
            "家族や仲間を大切にし、美的センスが高く、調和のとれた環境を好みます。"
            "責任感が強く、頼られることに喜びを感じる人情家です。"
        ),
        "love": (
            "恋愛では深い愛情を持つ献身的なパートナーになります。"
            "相手の幸せが自分の幸せ。ただし過干渉にならないよう気をつけて。"
        ),
        "work": (
            "教育、医療、福祉、デザインなど人の役に立てる仕事や美を追求できる仕事が向いています。"
        ),
        "lucky_color": "ローズ・ラベンダー",
        "lucky_number": "6・15・24",
        "advice": "あなたの人生テーマは「愛と奉仕」。まず自分自身を愛することを忘れずに。",
        "talent": (
            "あなたの才能は「愛で人を癒す力」です。"
            "傷ついた人の心に寄り添い、安心感を与える能力は他の追随を許しません。"
            "また、美的センスが高く、空間や人をより美しく整える才能も持っています。"
        ),
        "challenge": (
            "「完璧な愛」を求めすぎて、理想と現実のギャップに苦しむことがあります。"
            "また、人の問題を自分のことのように背負いすぎて疲弊することも。"
            "「人は最終的に自分で解決する力がある」と信じることが大切です。"
        ),
        "love_detail": (
            "恋愛では理想のパートナー像が高く、妥協が難しいタイプです。"
            "愛する人のためなら何でもしてあげたい気持ちが強い反面、"
            "見返りを求めてしまう矛盾に悩むことも。"
            "相性の良い相手はナンバー2・4・9で、特に9との深い精神的な繋がりは運命的です。"
        ),
        "work_detail": (
            "保育士、教師、デザイナー、インテリアコーディネーター、栄養士、医師が向いています。"
            "「美しいもの・心地よいもの」を生み出す仕事でも才能を発揮します。"
            "チームを家族のようにまとめるリーダーシップも持っています。"
        ),
        "fortune_2026": (
            "2026年は「愛と美の年」です。"
            "人間関係が充実し、特に家族や身近な人との絆が深まります。"
            "恋愛面では真剣な交際や結婚に向けた動きが活発になる年。"
            "仕事面では美的センスや人を癒す仕事で評価が高まります。"
            "健康面では自分を大切にすることを最優先に。過労に注意して。"
        ),
        "theme_2026": "愛と美が輝く年",
        "compatible": "2・4・9",
        "lucky_stone": "ローズクォーツ・パール",
        "lucky_day": "金曜日・月曜日",
        "lucky_direction": "西・南西",
    },
    7: {
        "title": "ナンバー 7 ／ 探求者・哲人",
        "keyword": "知恵・探求・神秘",
        "personality": (
            "あなたは深い知性と鋭い洞察力を持つ、魂の探求者です。"
            "表面的なことより本質を追い求め、内向的で独自の世界観を持ちます。"
            "スピリチュアルなことや哲学的なテーマへの関心が高い傾向があります。"
        ),
        "love": (
            "恋愛では慎重で相手をよく見極めます。"
            "軽い関係より、魂レベルで繋がれる深い愛を望みます。"
        ),
        "work": (
            "研究者、科学者、作家、占い師など深く探求できる分野で才能を発揮します。"
            "一人で集中して取り組める環境が最も力を引き出します。"
        ),
        "lucky_color": "パープル・ネイビー",
        "lucky_number": "7・16・25",
        "advice": "あなたの人生テーマは「探求と真実」。時には他者と交流しバランスを取ることが大切です。",
        "talent": (
            "あなたの才能は「真実を見抜く眼力」です。"
            "表面だけ見て判断せず、本質を探り続ける深い思考力は他の追随を許しません。"
            "また、直感と論理の両方を使いこなせる稀有な存在でもあります。"
        ),
        "challenge": (
            "思考が深すぎて行動に移せないことがあります。"
            "また、孤立を好みすぎて人間関係が希薄になりがちです。"
            "「完璧な答えが出てから動く」より「動きながら考える」姿勢が人生を豊かにします。"
        ),
        "love_detail": (
            "恋愛では相手を深く理解してから動くため、交際まで時間がかかります。"
            "一度心を開いた相手には深い愛情を注ぎます。"
            "会話の質を大切にし、哲学や人生観を語り合える相手が理想です。"
            "相性の良い相手はナンバー2・5・9で、特に9との魂レベルの繋がりは運命的です。"
        ),
        "work_detail": (
            "研究者、哲学者、占い師、精神科医、作家、データサイエンティストが向いています。"
            "深く一つのことを極める専門家タイプです。"
            "雑務が多い環境や、表面的な人付き合いが多い職場は合いません。"
            "リモートワークや一人で集中できる環境が最大限の力を引き出します。"
        ),
        "fortune_2026": (
            "2026年は「内なる知恵が開く年」です。"
            "学びや研究に投資することで、後半に大きなリターンが期待できます。"
            "スピリチュアルな探求や瞑想実践が特に吉。"
            "仕事面では専門性を高めることがキャリアアップの近道になります。"
            "恋愛面はゆっくり進める年。焦らず縁を信じて待つことが吉です。"
        ),
        "theme_2026": "内なる知恵が開く年",
        "compatible": "2・5・9",
        "lucky_stone": "アメジスト・ラピスラズリ",
        "lucky_day": "月曜日・土曜日",
        "lucky_direction": "北・北西",
    },
    8: {
        "title": "ナンバー 8 ／ 力強い実現者",
        "keyword": "成功・力・豊かさ",
        "personality": (
            "あなたは強い意志と実行力を持つ、物事を成し遂げる人物です。"
            "リーダーシップとカリスマ性を持ち、物質的な豊かさと精神的な充実の両方を追い求めます。"
        ),
        "love": (
            "恋愛でも情熱的でパワフルです。"
            "対等なパワーバランスで支え合える関係が最高の愛の形です。"
        ),
        "work": (
            "経営者、投資家、法律家など権限と責任を持つポジションで力を発揮します。"
            "努力と戦略で大きな成功を掴み取ります。"
        ),
        "lucky_color": "ゴールド・ダークレッド",
        "lucky_number": "8・17・26",
        "advice": "あなたの人生テーマは「力と豊かさ」。バランスを保つことがさらなる豊かさへの鍵です。",
        "talent": (
            "あなたの才能は「成功を引き寄せる力」です。"
            "目標を設定し、それを実現するための戦略を立て、実行する一連の能力が際立っています。"
            "また、お金やリソースを動かす感覚が鋭く、ビジネスの世界で輝きます。"
        ),
        "challenge": (
            "成功への執着が強くなりすぎて、周囲との人間関係が壊れることがあります。"
            "また、白黒思考が強く、失敗を極端に恐れる傾向も。"
            "「プロセスも楽しむ」余裕が人生を豊かにします。"
        ),
        "love_detail": (
            "恋愛では強くてしっかりした相手に惹かれます。"
            "対等に渡り合える相手との関係が最も充実します。"
            "お互いの目標を応援し合える、成長し合えるパートナーシップが理想です。"
            "相性の良い相手はナンバー2・4・6で、特に4との現実的な安定は最高の基盤です。"
        ),
        "work_detail": (
            "経営者、投資家、金融アドバイザー、弁護士、不動産業者が向いています。"
            "権限と裁量が与えられる立場で最大の力を発揮します。"
            "サラリーマンより独立・起業の方が能力を活かせるタイプです。"
            "失敗を恐れず、大きなリスクを取れる勇気が最大の武器です。"
        ),
        "fortune_2026": (
            "2026年は「豊かさが拡大する年」です。"
            "財運が高まり、これまでの努力が金銭的な成果として現れやすい時期です。"
            "仕事面では昇進・独立・事業拡大などの大きな動きが吉。"
            "恋愛面では真剣な関係に進展しやすい年。プロポーズや入籍の吉年でもあります。"
            "健康面では働きすぎに注意。定期的な運動でストレスを発散して。"
        ),
        "theme_2026": "豊かさが拡大する年",
        "compatible": "2・4・6",
        "lucky_stone": "タイガーアイ・オニキス",
        "lucky_day": "土曜日・日曜日",
        "lucky_direction": "南・東",
    },
    9: {
        "title": "ナンバー 9 ／ 博愛主義者・完成者",
        "keyword": "博愛・知恵・完成",
        "personality": (
            "あなたは深い慈悲と広い心を持つ、魂の成熟した人物です。"
            "豊かな感受性と芸術的センス、そして普遍的な知恵を持ちます。"
            "過去の経験から多くを学び、その知恵を周囲と分かち合います。"
        ),
        "love": (
            "恋愛では無条件の愛を与えられる人です。"
            "自分も愛される価値があることを忘れず、受け取ることも大切にしてください。"
        ),
        "work": (
            "医療、福祉、教育、芸術など人や社会に貢献できる分野で力を発揮します。"
        ),
        "lucky_color": "ゴールド・ホワイト",
        "lucky_number": "9・18・27",
        "advice": "あなたの人生テーマは「完成と博愛」。自分の幸せも大切にしながら愛を広げていってください。",
        "talent": (
            "あなたの才能は「すべてを包み込む愛と知恵」です。"
            "どんな人の痛みも理解できる深い共感力と、長い経験から得た普遍的な知恵が"
            "多くの人の道しるべになります。"
        ),
        "challenge": (
            "与えすぎて自分を消耗させてしまうことがあります。"
            "また、過去に縛られ、手放すことができずに前進できない時期も。"
            "「手放すことで新しいものが入ってくる」という宇宙の法則を信じましょう。"
        ),
        "love_detail": (
            "恋愛では相手のすべてを受け入れようとします。"
            "それが美しい愛の形である一方、都合よく使われるリスクもあります。"
            "自分を大切にしてくれる相手を選ぶ「目」を育てることが大切です。"
            "相性の良い相手はナンバー3・6・7で、特に6との深い愛の絆は最強です。"
        ),
        "work_detail": (
            "医師、看護師、社会福祉士、芸術家、作家、国際支援活動家が向いています。"
            "人や世界のために何かをしたいという気持ちが仕事の原動力になります。"
            "お金より「意味」を求める傾向があるため、使命感を感じられる職場選びが重要です。"
        ),
        "fortune_2026": (
            "2026年は「手放して新しく始まる年」です。"
            "古い習慣・関係・価値観を手放すことで、新しい可能性の扉が開きます。"
            "スピリチュアルな探求や芸術活動が運を高めます。"
            "恋愛面では過去の傷を癒し、新しい愛に向かって心を開く年になりそうです。"
            "健康面ではデトックスが吉。食事の見直しや断食などが効果的です。"
        ),
        "theme_2026": "手放して生まれ変わる年",
        "compatible": "3・6・7",
        "lucky_stone": "オパール・クリアクォーツ",
        "lucky_day": "木曜日・金曜日",
        "lucky_direction": "南・西",
    },
    11: {
        "title": "マスターナンバー 11 ／ 直感の覚醒者",
        "keyword": "直感・啓示・霊性",
        "personality": (
            "あなたはマスターナンバー11を持つ、特別な使命を帯びた魂です。"
            "並外れた直感力と霊的な感受性を持ち、見えないものを感じ取る力があります。"
        ),
        "love": (
            "魂レベルで繋がる深い愛を求めています。"
            "あなたの繊細さを理解してくれる人と最も深く愛し合えます。"
        ),
        "work": (
            "占い師、ヒーラー、芸術家、カウンセラーなど人の心に触れる仕事が天職です。"
        ),
        "lucky_color": "シルバー・ホワイト",
        "lucky_number": "11・2・29",
        "advice": "あなたの人生テーマは「啓示と覚醒」。あなたの直感を信じてください。",
        "talent": (
            "あなたの才能は「インスピレーションを受け取り伝える力」です。"
            "アイデアやビジョンが降ってくる感覚は、高次元からのメッセージかもしれません。"
            "芸術、音楽、文章など表現を通じてその才能を世界と共有できます。"
        ),
        "challenge": (
            "感受性が高すぎて、他人のエネルギーを受け取りすぎてしまいます。"
            "また、理想が高すぎて現実に落とし込めず、夢想家で終わってしまうことも。"
            "グラウンディング（地に足をつける）の習慣が非常に重要です。"
        ),
        "love_detail": (
            "恋愛では魂の繋がりを求めます。フィーリングが合わない相手とは続きません。"
            "初めて会った瞬間に「この人だ」という感覚が走ることが多い直感型です。"
            "敏感すぎるため、相手の感情を受け取りすぎて疲弊しないよう注意が必要です。"
            "相性の良い相手はナンバー2・6・9で、特に9との運命的な出会いは人生を変えます。"
        ),
        "work_detail": (
            "占い師、ヒーラー、アーティスト、ミュージシャン、詩人、霊的指導者が向いています。"
            "一般的なビジネスより、魂を込められる仕事でこそ輝けます。"
            "二重性（11→1+1=2）があるため、サポート役とリーダー役を状況に応じて使い分けられます。"
        ),
        "fortune_2026": (
            "2026年は「覚醒が加速する年」です。"
            "直感や霊感が一層鋭くなり、見えない世界からのサポートを感じやすくなります。"
            "スピリチュアルな学びや実践が人生を大きく好転させます。"
            "仕事面では使命感を感じる活動に集中することで才能が開花します。"
            "健康面ではエネルギー管理が重要。瞑想や自然との接触を増やして。"
        ),
        "theme_2026": "使命が明確になる年",
        "compatible": "2・6・9",
        "lucky_stone": "セレナイト・クリアクォーツ",
        "lucky_day": "月曜日・日曜日",
        "lucky_direction": "北・南",
    },
    22: {
        "title": "マスターナンバー 22 ／ マスタービルダー",
        "keyword": "実現・奉仕・偉大な建設",
        "personality": (
            "あなたはマスターナンバー22を持つ、夢を現実に変える力を持つ存在です。"
            "壮大なビジョンと実現するための実行力を兼ね備え、社会に貢献する大きな使命を持ちます。"
        ),
        "love": (
            "パートナーと共に何かを築いていくことに喜びを感じます。"
            "深い信頼と安定を大切にします。"
        ),
        "work": (
            "大きなスケールで世界に影響を与える仕事が向いています。"
            "夢を語るだけでなく、実際に形にする力を持っています。"
        ),
        "lucky_color": "ゴールド・グリーン",
        "lucky_number": "22・4・13",
        "advice": "あなたの人生テーマは「偉大な建設と奉仕」。地に足をつけながら大きな夢に向かって進んでください。",
        "talent": (
            "あなたの才能は「ビジョンを現実に変える圧倒的な力」です。"
            "夢想家でありながら、それを実現するための具体的な計画を立て実行できる稀有な存在です。"
            "大規模なプロジェクトをまとめる力は群を抜いています。"
        ),
        "challenge": (
            "大きすぎる責任感に押しつぶされそうになることがあります。"
            "また、完璧を求めすぎて行動が遅くなりがちです。"
            "「世界を変える」という使命と「今この瞬間を楽しむ」バランスが大切です。"
        ),
        "love_detail": (
            "恋愛でも建設的な関係を求めます。二人で何かを作り上げ、成長し合えるパートナーが理想です。"
            "安定と信頼を最重視するため、軽い恋愛には向きません。"
            "相性の良い相手はナンバー4・6・8で、特に4との堅実な土台は揺るぎない絆になります。"
        ),
        "work_detail": (
            "実業家、建築士、政治家、NPO代表、国際機関勤務が向いています。"
            "個人の利益より社会全体への貢献を意識した仕事で真価を発揮します。"
            "規模の大きなプロジェクトほど燃えるタイプです。"
        ),
        "fortune_2026": (
            "2026年は「大きなビジョンが動き出す年」です。"
            "長年温めてきたプランが実現に向けて動き始める予感があります。"
            "仕事面では人生最大の転換点になる可能性があります。勇気を持って挑んでください。"
            "恋愛面では安定した関係をより深化させる年。共通の目標を持つことが吉です。"
            "健康面では過労注意。心身のバランスを意識的に保って。"
        ),
        "theme_2026": "大きなビジョンが動く年",
        "compatible": "4・6・8",
        "lucky_stone": "ダイヤモンド・マラカイト",
        "lucky_day": "土曜日・木曜日",
        "lucky_direction": "北東・南西",
    },
    33: {
        "title": "マスターナンバー 33 ／ マスターティーチャー",
        "keyword": "慈悲・癒し・奉仕",
        "personality": (
            "あなたはマスターナンバー33を持つ、深い慈悲と癒しの力を持つ魂です。"
            "その存在自体が周囲に光を与え、多くの人の人生に良い影響を与えます。"
        ),
        "love": (
            "愛することが生きる意味そのものです。"
            "見返りを求めない愛を与えますが、自分も受け取ることを意識して。"
        ),
        "work": (
            "ヒーラー、精神的指導者、教育者など人の魂を癒し導く仕事が天職です。"
        ),
        "lucky_color": "ホワイト・ゴールド",
        "lucky_number": "33・6・15",
        "advice": "あなたの人生テーマは「無条件の愛と癒し」。自身を整えながら愛を世界に広げていってください。",
        "talent": (
            "あなたの才能は「無条件の愛で世界を癒す力」です。"
            "その存在だけで周囲に安心感と温かさをもたらします。"
            "教えること、導くことへの天賦の才を持ち、多くの人の人生に灯台のような存在になります。"
        ),
        "challenge": (
            "自分を犠牲にしすぎて、完全に燃え尽きてしまうことがあります。"
            "また、「すべてを救わなければ」という使命感の重さに押しつぶされることも。"
            "「自分を愛することが、世界を愛する第一歩」という真実を常に思い出してください。"
        ),
        "love_detail": (
            "恋愛では相手のすべてを包み込む深い愛を与えます。"
            "ただし、一方的に与えるだけの関係は長続きしません。"
            "あなたの深い愛を受け取れる、器の大きな相手との縁を大切に育てて。"
            "相性の良い相手はナンバー6・9・11で、特に11との魂の共鳴は宇宙レベルです。"
        ),
        "work_detail": (
            "ヒーラー、宗教的指導者、教師、セラピスト、ホスピスワーカーが向いています。"
            "「人の魂に触れる」仕事でのみ本当の充実感を得られます。"
            "お金や地位より、意味と愛を大切にした仕事選びが人生の満足度を高めます。"
        ),
        "fortune_2026": (
            "2026年は「愛の光が最大に輝く年」です。"
            "あなたの存在が必要とされる場面が増え、使命感を強く感じる出来事が起きます。"
            "スピリチュアルな活動や癒しのワークが特に吉。"
            "恋愛面では魂の伴侶との出会いや、深まりがある年です。"
            "健康面では自分へのケアを最優先に。セルフラブが運気の鍵です。"
        ),
        "theme_2026": "愛の光が最大に輝く年",
        "compatible": "6・9・11",
        "lucky_stone": "セレナイト・アンジェライト",
        "lucky_day": "金曜日・日曜日",
        "lucky_direction": "南・北",
    },
}

# ===== フォント =====
_fonts_ready = False

def setup_fonts():
    global _fonts_ready
    if _fonts_ready:
        return True
    base = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        (os.path.join(base, "fonts", "NotoSansJP-Regular.ttf"),
         os.path.join(base, "fonts", "NotoSansJP-Bold.ttf")),
        (r"C:\Windows\Fonts\meiryo.ttc",  r"C:\Windows\Fonts\meiryob.ttc"),
        (r"C:\Windows\Fonts\YuGothM.ttc", r"C:\Windows\Fonts\YuGothB.ttc"),
        (r"C:\Windows\Fonts\msgothic.ttc", r"C:\Windows\Fonts\msgothic.ttc"),
        ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
         "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
        ("/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
         "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Bold.otf"),
    ]
    for regular, bold in candidates:
        if os.path.exists(regular):
            try:
                pdfmetrics.registerFont(TTFont("JFont",     regular, subfontIndex=0))
                pdfmetrics.registerFont(TTFont("JFontBold", bold if os.path.exists(bold) else regular, subfontIndex=0))
                _fonts_ready = True
                return True
            except Exception:
                continue
    return False

# ===== 数秘術計算 =====
def calculate_life_path(year, month, day):
    total = sum(int(d) for d in f"{year}{month:02d}{day:02d}")
    while total > 9 and total not in (11, 22, 33):
        total = sum(int(d) for d in str(total))
    return total

# ===== テキスト折り返し =====
def draw_wrapped(c, text, x, y, max_width, font_name, font_size, line_gap=4):
    line_h = font_size + line_gap
    c.setFont(font_name, font_size)
    current, lines = "", []
    for ch in text:
        if c.stringWidth(current + ch, font_name, font_size) <= max_width:
            current += ch
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    for line in lines:
        c.drawString(x, y, line)
        y -= line_h
    return y

# ===== デザイン定数 =====
BG     = colors.HexColor("#0f0e17")
ACCENT = colors.HexColor("#ff8906")
WHITE  = colors.HexColor("#fffffe")
GRAY   = colors.HexColor("#a7a9be")
SEC_COLORS = [
    colors.HexColor("#a2d2ff"),
    colors.HexColor("#ffafcc"),
    colors.HexColor("#b5ead7"),
    colors.HexColor("#c8b6ff"),
    colors.HexColor("#ffd6a5"),
    colors.HexColor("#a2d2ff"),
]

def draw_bg(c, W, H):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def draw_section(c, title, content, x, y, width, col):
    c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=0.22))
    c.rect(x, y - 7.5 * mm, width, 7.5 * mm, fill=1, stroke=0)
    c.setFillColor(col)
    c.setFont("JFontBold", 11)
    c.drawString(x + 3 * mm, y - 5.2 * mm, f"◆  {title}")
    y -= 11 * mm
    c.setFillColor(WHITE)
    y = draw_wrapped(c, content, x + 3 * mm, y, width - 6 * mm, "JFont", 10, line_gap=4)
    return y - 5 * mm

def page_break_if_needed(c, y, W, H, threshold=38):
    if y < threshold * mm:
        c.showPage()
        draw_bg(c, W, H)
        return H - 20 * mm
    return y

# ===== タイトルページ =====
def draw_title_page(c, W, H, name, year, month, day, number, r, mode_label):
    draw_bg(c, W, H)
    c.setFillColor(colors.Color(1, 0.537, 0.024, alpha=0.08))
    c.circle(W / 2, H / 2, 180, fill=1, stroke=0)
    c.setFillColor(colors.Color(1, 0.537, 0.024, alpha=0.04))
    c.circle(W / 2, H / 2, 250, fill=1, stroke=0)

    c.setFillColor(ACCENT)
    c.setFont("JFontBold", 20)
    c.drawCentredString(W / 2, H - 58 * mm, "数秘術  ライフパスナンバー鑑定書")

    c.setFillColor(GRAY)
    c.setFont("JFont", 9)
    c.drawCentredString(W / 2, H - 65 * mm, mode_label)

    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.5)
    c.line(40 * mm, H - 69 * mm, W - 40 * mm, H - 69 * mm)

    c.setFillColor(WHITE)
    c.setFont("JFont", 15)
    c.drawCentredString(W / 2, H - 80 * mm, f"〜  {name}  様  〜")
    c.setFillColor(GRAY)
    c.setFont("JFont", 11)
    c.drawCentredString(W / 2, H - 90 * mm, f"生年月日：{year}年{month}月{day}日")

    c.setFillColor(ACCENT)
    c.setFont("JFontBold", 100)
    c.drawCentredString(W / 2, H / 2 - 15 * mm, str(number))

    c.setFillColor(WHITE)
    c.setFont("JFontBold", 16)
    c.drawCentredString(W / 2, H / 2 - 38 * mm, r["title"])
    c.setFillColor(ACCENT)
    c.setFont("JFont", 12)
    c.drawCentredString(W / 2, H / 2 - 51 * mm, f"キーワード：{r['keyword']}")
    c.setFillColor(GRAY)
    c.setFont("JFont", 10)
    c.drawCentredString(W / 2, H / 2 - 63 * mm,
        f"ラッキーカラー：{r['lucky_color']}　／　ラッキーナンバー：{r['lucky_number']}")

    c.setFillColor(GRAY)
    c.setFont("JFont", 8)
    c.drawCentredString(W / 2, 18 * mm, "※ この鑑定はエンターテインメント目的です。参考程度にお楽しみください。")

# ===== ヘッダーバー =====
def draw_header(c, W, H, text):
    c.setFillColor(ACCENT)
    c.rect(0, H - 22 * mm, W, 22 * mm, fill=1, stroke=0)
    c.setFillColor(BG)
    c.setFont("JFontBold", 13)
    c.drawString(12 * mm, H - 13 * mm, text)

def draw_footer(c, W, margin):
    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.15))
    c.setLineWidth(0.4)
    c.line(margin, 18 * mm, W - margin, 18 * mm)
    c.setFillColor(GRAY)
    c.setFont("JFont", 8)
    c.drawString(margin, 11 * mm, "数秘術ライフパスナンバー鑑定書")
    c.drawRightString(W - margin, 11 * mm, "※ エンターテインメント目的の鑑定です")

# ===== 簡易版PDF =====
def generate_simple_pdf(name, year, month, day):
    number = calculate_life_path(year, month, day)
    r = READINGS.get(number, READINGS[9])
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4
    margin, cw = 12 * mm, W - 24 * mm

    draw_title_page(c, W, H, name, year, month, day, number, r, "【 簡易版 】")
    c.showPage()

    draw_bg(c, W, H)
    draw_header(c, W, H, f"ライフパスナンバー {number}  基本鑑定  ／  {name} 様")
    y = H - 32 * mm

    for i, (sec, content) in enumerate([
        ("あなたの個性・特徴",     r["personality"]),
        ("恋愛・パートナーシップ", r["love"]),
        ("仕事・キャリア",         r["work"]),
        ("あなたへのメッセージ",   r["advice"]),
    ]):
        y = page_break_if_needed(c, y, W, H)
        y = draw_section(c, sec, content, margin, y, cw, SEC_COLORS[i % len(SEC_COLORS)])

    draw_footer(c, W, margin)
    c.save()
    buf.seek(0)
    return buf.getvalue(), number, r

# ===== 本格版PDF =====
def generate_full_pdf(name, year, month, day):
    number = calculate_life_path(year, month, day)
    r = READINGS.get(number, READINGS[9])
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4
    margin, cw = 12 * mm, W - 24 * mm

    # ページ1: タイトル
    draw_title_page(c, W, H, name, year, month, day, number, r, "【 本格版 】")
    c.showPage()

    # ページ2: 基本鑑定 + 才能・課題
    draw_bg(c, W, H)
    draw_header(c, W, H, f"ライフパスナンバー {number}  基本鑑定  ／  {name} 様")
    y = H - 32 * mm

    for i, (sec, content) in enumerate([
        ("あなたの個性・特徴",     r["personality"]),
        ("才能と強み",             r["talent"]),
        ("課題と成長のヒント",     r["challenge"]),
        ("恋愛・パートナーシップ", r["love_detail"]),
        ("仕事・キャリア",         r["work_detail"]),
    ]):
        y = page_break_if_needed(c, y, W, H)
        if y == H - 20 * mm:
            draw_header(c, W, H, f"ライフパスナンバー {number}  基本鑑定  ／  {name} 様")
            y = H - 32 * mm
        y = draw_section(c, sec, content, margin, y, cw, SEC_COLORS[i % len(SEC_COLORS)])

    draw_footer(c, W, margin)
    c.showPage()

    # ページ3: 2026年運勢 + ラッキーアイテム + メッセージ
    draw_bg(c, W, H)
    draw_header(c, W, H, f"2026年の運勢  ／  {name} 様")
    y = H - 32 * mm

    y = draw_section(c, f"2026年のテーマ：{r['theme_2026']}", r["fortune_2026"],
                     margin, y, cw, SEC_COLORS[0])
    y = page_break_if_needed(c, y, W, H)

    # ラッキーアイテムボックス
    box_h = 44 * mm
    if y - box_h < 30 * mm:
        c.showPage()
        draw_bg(c, W, H)
        y = H - 20 * mm

    c.setFillColor(colors.Color(1, 0.537, 0.024, alpha=0.1))
    c.rect(margin, y - box_h, cw, box_h, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.setFont("JFontBold", 12)
    c.drawString(margin + 4 * mm, y - 7 * mm, "◆  ラッキーアイテム一覧")
    items = [
        ("ラッキーカラー",   r["lucky_color"]),
        ("ラッキーナンバー", r["lucky_number"]),
        ("ラッキーストーン", r["lucky_stone"]),
        ("ラッキーデー",     r["lucky_day"]),
        ("ラッキー方位",     r["lucky_direction"]),
        ("相性の良い数字",   r["compatible"]),
    ]
    col1_x = margin + 4 * mm
    col2_x = W / 2 + 2 * mm
    row_h  = 6 * mm
    for idx, (label, val) in enumerate(items):
        col_x = col1_x if idx % 2 == 0 else col2_x
        row_y = y - 14 * mm - (idx // 2) * row_h
        c.setFillColor(GRAY)
        c.setFont("JFont", 9)
        c.drawString(col_x, row_y, f"{label}：")
        c.setFillColor(WHITE)
        c.setFont("JFontBold", 9)
        c.drawString(col_x + 28 * mm, row_y, val)

    y -= box_h + 6 * mm
    y = page_break_if_needed(c, y, W, H)
    y = draw_section(c, "あなたへのメッセージ", r["advice"], margin, y, cw, SEC_COLORS[5])

    draw_footer(c, W, margin)
    c.save()
    buf.seek(0)
    return buf.getvalue(), number, r

# ===== Streamlit UI =====
st.set_page_config(page_title="数秘術 鑑定PDF", page_icon="✨", layout="centered")

st.title("✨ 数秘術 ライフパスナンバー鑑定")
st.caption("生年月日からあなたのライフパスナンバーを診断し、鑑定書PDFをお渡しします。")
st.divider()

mode = st.radio(
    "鑑定タイプを選んでください",
    ["簡易版（2ページ）", "本格版（3ページ）"],
    horizontal=True,
)

with st.form("uranai_form"):
    name = st.text_input("お名前（ニックネーム可）", placeholder="例：さくら")
    col1, col2, col3 = st.columns(3)
    with col1:
        year  = st.number_input("生まれた年", min_value=1920, max_value=2010, value=1990, step=1)
    with col2:
        month = st.number_input("月", min_value=1, max_value=12, value=1, step=1)
    with col3:
        day   = st.number_input("日", min_value=1, max_value=31, value=1, step=1)

    submitted = st.form_submit_button("🔮 鑑定する", use_container_width=True)

if submitted:
    if not name.strip():
        st.error("お名前を入力してください。")
    elif not setup_fonts():
        st.error("フォントの読み込みに失敗しました。環境を確認してください。")
    else:
        with st.spinner("鑑定中..."):
            if "簡易版" in mode:
                pdf_bytes, number, reading = generate_simple_pdf(
                    name.strip(), int(year), int(month), int(day))
                label = "簡易版"
            else:
                pdf_bytes, number, reading = generate_full_pdf(
                    name.strip(), int(year), int(month), int(day))
                label = "本格版"

        st.success("鑑定が完了しました！")
        st.markdown(f"### ライフパスナンバー：**{number}**")
        st.markdown(f"**{reading['title']}**")
        st.markdown(f"キーワード：{reading['keyword']}")
        st.markdown(f"2026年のテーマ：{reading['theme_2026']}")
        st.divider()
        st.download_button(
            label=f"📄 鑑定書PDF（{label}）をダウンロード",
            data=pdf_bytes,
            file_name=f"uranai_{name.strip()}_{label}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
