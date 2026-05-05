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
            "時に頑固に見られることもありますが、それはあなたのブレない軸の表れ。"
            "新しいことへの挑戦を恐れず、常に前を向いて進んでいきます。"
        ),
        "love": (
            "恋愛では情熱的でまっすぐです。好きな人には積極的にアプローチする傾向があります。"
            "ただし自分のペースを大切にするため、パートナーにも自立心を求めます。"
            "対等な関係を築ける相手と最も輝きます。"
            "束縛や依存は苦手なので、お互いの自由を尊重し合えるパートナーシップが理想です。"
        ),
        "work": (
            "仕事では独立・起業・リーダーポジションに向いています。"
            "指示を受けるより自ら決断する立場の方が力を発揮できます。"
            "競争の激しい分野でも臆することなく挑んでいける強さがあります。"
            "周囲の意見を聞く柔軟さも大切にすると、さらに大きな成功へと繋がります。"
        ),
        "lucky_color": "赤・ゴールド",
        "lucky_number": "1・10・19",
        "advice": (
            "あなたの人生テーマは「自立と創造」。"
            "誰かに頼るより、自分の力を信じて進むことで道が開けます。"
            "失敗を恐れず、一歩踏み出す勇気があなたの最大の才能です。"
        ),
    },
    2: {
        "title": "ナンバー 2 ／ 調和の人・サポーター",
        "keyword": "協調・直感・愛",
        "personality": (
            "あなたは繊細な感受性と高い共感力を持つ、心の温かい人です。"
            "場の空気を読む力に長け、周囲との調和を大切にします。"
            "争いを好まず、仲介役として人と人をつなぐことが得意です。"
            "強さより柔らかさで周囲を包み込み、そっと支えるその姿勢が多くの人に愛されます。"
        ),
        "love": (
            "恋愛では献身的で思いやりにあふれたパートナーになります。"
            "相手の気持ちを大切にし、細やかな気遣いができます。"
            "ただし尽くしすぎてしまう傾向があるので、自分の気持ちも大切に。"
            "安心感と信頼を与えてくれる穏やかな関係を望んでいます。"
        ),
        "work": (
            "チームワークを活かせる仕事が向いています。"
            "カウンセラー、看護師、教育者、秘書、コーディネーターなど"
            "人をサポートする職種で実力を発揮します。"
            "縁の下の力持ちとして、組織を支える重要な役割を担います。"
        ),
        "lucky_color": "オレンジ・ピンク",
        "lucky_number": "2・11・20",
        "advice": (
            "あなたの人生テーマは「調和と共感」。"
            "自分を犠牲にせず、自分も相手も大切にするバランスを意識してください。"
            "あなたの優しさは本物の強さです。"
        ),
    },
    3: {
        "title": "ナンバー 3 ／ 表現者・クリエイター",
        "keyword": "創造・表現・喜び",
        "personality": (
            "あなたは豊かな表現力と明るいエネルギーを持つ、周囲を元気にする存在です。"
            "ユーモアのセンスがあり、場を盛り上げるのが得意。"
            "芸術的な才能や独自のアイデアで人々を魅了します。"
            "好奇心旺盛で飽きっぽい一面もありますが、その分多彩な才能の持ち主です。"
        ),
        "love": (
            "恋愛では楽しさと刺激を大切にします。"
            "一緒にいて笑顔になれる相手、会話が弾む相手に惹かれます。"
            "愛情表現はストレートで情熱的。"
            "変化を楽しめる関係性がベストです。"
        ),
        "work": (
            "クリエイティブな仕事で輝きます。"
            "デザイナー、ライター、俳優、ミュージシャン、マーケターなど"
            "表現や発信が伴う職種が向いています。"
            "アイデアを形にすることに喜びを感じ、周囲にもその熱を伝えられます。"
        ),
        "lucky_color": "黄色・ライトブルー",
        "lucky_number": "3・12・21",
        "advice": (
            "あなたの人生テーマは「表現と創造」。"
            "あなたの発信が誰かを笑顔にします。"
            "自分の感性を信じて、思い切り表現することで道が開けます。"
        ),
    },
    4: {
        "title": "ナンバー 4 ／ 堅実な建設者",
        "keyword": "安定・努力・誠実",
        "personality": (
            "あなたは誠実さと堅実さを兼ね備えた、信頼できる人物です。"
            "コツコツと努力を積み重ねることが得意で、どんな困難にも粘り強く向き合います。"
            "計画的で現実的な思考を持ち、物事を着実に進める力があります。"
            "ルールや秩序を大切にし、周囲から「安心できる人」と評価されることが多いでしょう。"
        ),
        "love": (
            "恋愛では真剣で誠実なパートナーになります。"
            "浮ついた関係より、長期的に安定した愛を求めます。"
            "愛情表現は不器用かもしれませんが、行動で誠意を示します。"
            "信頼と安定を築ける相手との関係が最も幸せを感じられます。"
        ),
        "work": (
            "管理職、エンジニア、会計士、建築家など地道な努力が実を結ぶ職種が向いています。"
            "手を抜かずにコツコツ積み上げる姿勢が高く評価され、"
            "長期的に安定したキャリアを築いていけます。"
        ),
        "lucky_color": "グリーン・ネイビー",
        "lucky_number": "4・13・22",
        "advice": (
            "あなたの人生テーマは「安定と構築」。"
            "あなたの努力は必ず報われます。焦らず、一歩一歩着実に進んでください。"
            "たまには肩の力を抜いて、楽しむことも忘れずに。"
        ),
    },
    5: {
        "title": "ナンバー 5 ／ 自由人・冒険家",
        "keyword": "自由・変化・冒険",
        "personality": (
            "あなたは自由を愛し、変化を恐れない冒険者です。"
            "好奇心が旺盛で、新しいことへの適応力が高く、どんな状況でも楽しみを見つけられます。"
            "多才でエネルギッシュ、行動力があり、人生を謳歌する才能があります。"
            "型にはまることを嫌い、独自の生き方を追求していきます。"
        ),
        "love": (
            "恋愛では自由と刺激を大切にします。"
            "束縛を嫌い、お互いの独立性を尊重できる関係を好みます。"
            "情熱的で魅力的ですが、飽きっぽい一面も。"
            "変化を楽しめる柔軟なパートナーと長く続く関係を築けます。"
        ),
        "work": (
            "旅行業、フリーランス、営業、エンターテイナー、記者など"
            "変化や移動が多い仕事が向いています。"
            "ルーティンワークより臨機応変さが求められる環境で実力を発揮します。"
        ),
        "lucky_color": "ターコイズ・シルバー",
        "lucky_number": "5・14・23",
        "advice": (
            "あなたの人生テーマは「自由と変化」。"
            "多くの経験があなたを豊かにします。"
            "ただし、大切なものを手放さないよう、ときには立ち止まる勇気も持ってください。"
        ),
    },
    6: {
        "title": "ナンバー 6 ／ 愛の人・調停者",
        "keyword": "愛・責任・奉仕",
        "personality": (
            "あなたは愛情深く、面倒見のよい人です。"
            "家族や仲間を大切にし、周囲の人が幸せでいられるよう惜しみなく力を注ぎます。"
            "美的センスが高く、調和のとれた環境を好みます。"
            "責任感が強く、頼られることに喜びを感じる人情家です。"
        ),
        "love": (
            "恋愛では深い愛情を持つ献身的なパートナーになります。"
            "愛する人のために何でもしたいという思いが強く、温かい家庭を築くことを夢見ています。"
            "相手の幸せが自分の幸せ。ただし過干渉にならないよう気をつけて。"
        ),
        "work": (
            "教育、医療、福祉、カウンセリング、デザイン、料理など"
            "人の役に立てる仕事や美を追求できる仕事が向いています。"
            "チームの雰囲気をよくし、職場環境を整える力があります。"
        ),
        "lucky_color": "ローズ・ラベンダー",
        "lucky_number": "6・15・24",
        "advice": (
            "あなたの人生テーマは「愛と奉仕」。"
            "まず自分自身を愛することを忘れずに。"
            "自分を満たしてこそ、周囲にも最高の愛を与えられます。"
        ),
    },
    7: {
        "title": "ナンバー 7 ／ 探求者・哲人",
        "keyword": "知恵・探求・神秘",
        "personality": (
            "あなたは深い知性と鋭い洞察力を持つ、魂の探求者です。"
            "表面的なことより本質を追い求め、物事の深いところまで考えます。"
            "内向的で独自の世界観を持ちますが、その知識と洞察は周囲を驚かせます。"
            "スピリチュアルなことや哲学的なテーマへの関心が高い傾向があります。"
        ),
        "love": (
            "恋愛では慎重で相手をよく見極めます。"
            "心の深いところまで理解し合えるパートナーを求めています。"
            "軽い関係より、魂レベルで繋がれる深い愛を望みます。"
        ),
        "work": (
            "研究者、哲学者、科学者、作家、心理士、占い師など"
            "深く探求できる分野で才能を発揮します。"
            "一人で集中して取り組める環境が最も力を引き出します。"
        ),
        "lucky_color": "パープル・ネイビー",
        "lucky_number": "7・16・25",
        "advice": (
            "あなたの人生テーマは「探求と真実」。"
            "あなたの知恵と洞察力は特別な才能です。"
            "時には他者と交流し、孤立しすぎないようにバランスを取ることが大切です。"
        ),
    },
    8: {
        "title": "ナンバー 8 ／ 力強い実現者",
        "keyword": "成功・力・豊かさ",
        "personality": (
            "あなたは強い意志と実行力を持つ、物事を成し遂げる人物です。"
            "目標に向かって突き進む力があり、大きな成功を手にする可能性を秘めています。"
            "リーダーシップとカリスマ性を持ち、周囲に影響力を与えます。"
            "物質的な豊かさと精神的な充実の両方を追い求めます。"
        ),
        "love": (
            "恋愛でも情熱的でパワフルです。"
            "強くて頼りがいのあるパートナーに惹かれる傾向があります。"
            "対等なパワーバランスで支え合える関係が最高の愛の形です。"
        ),
        "work": (
            "経営者、投資家、法律家、金融、管理職など"
            "権限と責任を持つポジションで力を発揮します。"
            "努力と戦略で大きな成功を掴み取ります。"
        ),
        "lucky_color": "ゴールド・ダークレッド",
        "lucky_number": "8・17・26",
        "advice": (
            "あなたの人生テーマは「力と豊かさ」。"
            "あなたには大きな成功を掴む力があります。"
            "お金や地位だけでなく、人との繋がりも大切に。"
        ),
    },
    9: {
        "title": "ナンバー 9 ／ 博愛主義者・完成者",
        "keyword": "博愛・知恵・完成",
        "personality": (
            "あなたは深い慈悲と広い心を持つ、魂の成熟した人物です。"
            "人類や社会全体への愛を持ち、利他的な精神で生きています。"
            "豊かな感受性と芸術的センス、そして普遍的な知恵を持ちます。"
            "過去の経験から多くを学び、その知恵を周囲と分かち合います。"
        ),
        "love": (
            "恋愛では無条件の愛を与えられる人です。"
            "相手の欠点も含めて受け入れる包容力があります。"
            "自分も愛される価値があることを忘れず、受け取ることも大切にしてください。"
        ),
        "work": (
            "医療、福祉、教育、芸術、NGOなど人や社会に貢献できる分野で力を発揮します。"
            "国際的な仕事や、多くの人々の役に立てるスケールの大きな仕事に向いています。"
        ),
        "lucky_color": "ゴールド・ホワイト",
        "lucky_number": "9・18・27",
        "advice": (
            "あなたの人生テーマは「完成と博愛」。"
            "あなたの存在は多くの人に光を与えています。"
            "自分自身の幸せも大切にしながら、世界に愛を広げていってください。"
        ),
    },
    11: {
        "title": "マスターナンバー 11 ／ 直感の覚醒者",
        "keyword": "直感・啓示・霊性",
        "personality": (
            "あなたはマスターナンバー11を持つ、特別な使命を帯びた魂です。"
            "並外れた直感力と霊的な感受性を持ち、見えないものを感じ取る力があります。"
            "理想が高く、芸術・哲学・精神世界への深い関心があります。"
            "その敏感さゆえに生きづらさを感じることもありますが、それが特別な才能の裏返しです。"
        ),
        "love": (
            "魂レベルで繋がる深い愛を求めています。"
            "スピリチュアルな感覚を共有できる相手や、あなたの繊細さを理解してくれる人と最も深く愛し合えます。"
        ),
        "work": (
            "占い師、ヒーラー、芸術家、作家、カウンセラー、先生など"
            "人の心に触れ、インスピレーションを与える仕事が天職です。"
        ),
        "lucky_color": "シルバー・ホワイト",
        "lucky_number": "11・2・29",
        "advice": (
            "あなたの人生テーマは「啓示と覚醒」。"
            "あなたの直感を信じてください。その感覚はとても正確です。"
            "心身を整える時間を大切にし、自分の内なる声に耳を傾けることが開運の鍵です。"
        ),
    },
    22: {
        "title": "マスターナンバー 22 ／ マスタービルダー",
        "keyword": "実現・奉仕・偉大な建設",
        "personality": (
            "あなたはマスターナンバー22を持つ、夢を現実に変える力を持つ存在です。"
            "壮大なビジョンと、それを実現するための実行力を兼ね備えています。"
            "社会や人類に貢献する大きな使命を持っています。"
        ),
        "love": (
            "恋愛でも真剣で誠実です。"
            "パートナーと共に何かを築いていくことに喜びを感じます。"
            "共通の夢や目標を持てる相手と最高のパートナーシップを結べます。"
        ),
        "work": (
            "実業家、建築家、政治家、国際機関など"
            "大きなスケールで世界に影響を与える仕事が向いています。"
            "あなたは夢を語るだけでなく、実際に形にする力を持っています。"
        ),
        "lucky_color": "ゴールド・グリーン",
        "lucky_number": "22・4・13",
        "advice": (
            "あなたの人生テーマは「偉大な建設と奉仕」。"
            "あなたのビジョンは世界を変える力を持っています。"
            "地に足をつけながら、大きな夢に向かって着実に進んでください。"
        ),
    },
    33: {
        "title": "マスターナンバー 33 ／ マスターティーチャー",
        "keyword": "慈悲・癒し・奉仕",
        "personality": (
            "あなたはマスターナンバー33を持つ、深い慈悲と癒しの力を持つ魂です。"
            "すべての人への無条件の愛と奉仕の精神を持ちます。"
            "その存在自体が周囲に光を与え、多くの人の人生に良い影響を与えます。"
        ),
        "love": (
            "愛することが生きる意味そのものです。"
            "見返りを求めない愛を与えますが、時には自分も受け取ることを意識して。"
        ),
        "work": (
            "ヒーラー、精神的指導者、教育者、福祉活動家など"
            "人の魂を癒し、導く仕事が天職です。"
        ),
        "lucky_color": "ホワイト・ゴールド",
        "lucky_number": "33・6・15",
        "advice": (
            "あなたの人生テーマは「無条件の愛と癒し」。"
            "自分自身をしっかり整えながら、その愛を世界に広げていってください。"
        ),
    },
}

# ===== フォント =====
_fonts_ready = False

def setup_fonts():
    global _fonts_ready
    if _fonts_ready:
        return True
    candidates = [
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

# ===== PDF生成（BytesIO） =====
BG     = colors.HexColor("#0f0e17")
ACCENT = colors.HexColor("#ff8906")
WHITE  = colors.HexColor("#fffffe")
GRAY   = colors.HexColor("#a7a9be")
SEC_COLORS = [
    colors.HexColor("#a2d2ff"),
    colors.HexColor("#ffafcc"),
    colors.HexColor("#b5ead7"),
    colors.HexColor("#c8b6ff"),
]

def generate_pdf_bytes(name, year, month, day):
    number = calculate_life_path(year, month, day)
    r = READINGS.get(number, READINGS[9])

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4

    # ===== ページ1: タイトル =====
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(colors.Color(1, 0.537, 0.024, alpha=0.08))
    c.circle(W / 2, H / 2, 180, fill=1, stroke=0)
    c.setFillColor(colors.Color(1, 0.537, 0.024, alpha=0.04))
    c.circle(W / 2, H / 2, 250, fill=1, stroke=0)

    c.setFillColor(ACCENT)
    c.setFont("JFontBold", 20)
    c.drawCentredString(W / 2, H - 60 * mm, "数秘術  ライフパスナンバー鑑定書")

    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.5)
    c.line(40 * mm, H - 65 * mm, W - 40 * mm, H - 65 * mm)

    c.setFillColor(WHITE)
    c.setFont("JFont", 15)
    c.drawCentredString(W / 2, H - 78 * mm, f"〜  {name}  様  〜")

    c.setFillColor(GRAY)
    c.setFont("JFont", 11)
    c.drawCentredString(W / 2, H - 89 * mm, f"生年月日：{year}年{month}月{day}日")

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
    c.drawCentredString(W / 2, H / 2 - 64 * mm,
        f"ラッキーカラー：{r['lucky_color']}　／　ラッキーナンバー：{r['lucky_number']}")

    c.setFillColor(GRAY)
    c.setFont("JFont", 8)
    c.drawCentredString(W / 2, 18 * mm, "※ この鑑定はエンターテインメント目的です。参考程度にお楽しみください。")

    c.showPage()

    # ===== ページ2: 詳細 =====
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(ACCENT)
    c.rect(0, H - 22 * mm, W, 22 * mm, fill=1, stroke=0)
    c.setFillColor(BG)
    c.setFont("JFontBold", 13)
    c.drawString(12 * mm, H - 13 * mm, f"ライフパスナンバー {number}  詳細鑑定  ／  {name} 様")

    margin, cw = 12 * mm, W - 24 * mm
    y = H - 32 * mm

    for i, (sec, content) in enumerate([
        ("あなたの個性・特徴",     r["personality"]),
        ("恋愛・パートナーシップ", r["love"]),
        ("仕事・キャリア",         r["work"]),
        ("あなたへのメッセージ",   r["advice"]),
    ]):
        col = SEC_COLORS[i % len(SEC_COLORS)]
        if y < 38 * mm:
            c.showPage()
            c.setFillColor(BG)
            c.rect(0, 0, W, H, fill=1, stroke=0)
            y = H - 20 * mm

        c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=0.22))
        c.rect(margin, y - 7.5 * mm, cw, 7.5 * mm, fill=1, stroke=0)
        c.setFillColor(col)
        c.setFont("JFontBold", 11)
        c.drawString(margin + 3 * mm, y - 5.2 * mm, f"◆  {sec}")
        y -= 11 * mm

        c.setFillColor(WHITE)
        y = draw_wrapped(c, content, margin + 3 * mm, y, cw - 6 * mm, "JFont", 10, line_gap=4)
        y -= 6 * mm

    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.15))
    c.setLineWidth(0.4)
    c.line(margin, 18 * mm, W - margin, 18 * mm)
    c.setFillColor(GRAY)
    c.setFont("JFont", 8)
    c.drawString(margin, 11 * mm, "数秘術ライフパスナンバー鑑定書")
    c.drawRightString(W - margin, 11 * mm, "※ エンターテインメント目的の鑑定です")

    c.save()
    buf.seek(0)
    return buf.getvalue(), number, r

# ===== Streamlit UI =====
st.set_page_config(page_title="数秘術 鑑定PDF", page_icon="✨", layout="centered")

st.markdown("""
<style>
body { background-color: #0f0e17; }
</style>
""", unsafe_allow_html=True)

st.title("✨ 数秘術 ライフパスナンバー鑑定")
st.caption("生年月日からあなたのライフパスナンバーを診断し、鑑定書PDFをお渡しします。")
st.divider()

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
            pdf_bytes, number, reading = generate_pdf_bytes(name.strip(), int(year), int(month), int(day))

        st.success(f"鑑定が完了しました！")
        st.markdown(f"### ライフパスナンバー：**{number}**")
        st.markdown(f"**{reading['title']}**")
        st.markdown(f"キーワード：{reading['keyword']}")
        st.markdown(f"ラッキーカラー：{reading['lucky_color']}　／　ラッキーナンバー：{reading['lucky_number']}")
        st.divider()
        st.download_button(
            label="📄 鑑定書PDFをダウンロード",
            data=pdf_bytes,
            file_name=f"uranai_{name.strip()}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
