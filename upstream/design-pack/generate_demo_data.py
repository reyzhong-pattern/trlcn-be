"""Synthetic multi-platform demo dataset for TrendVision Live Performance Analytics.
All values are synthetic. Douyin parameters are calibrated loosely to the staging app (Mar-Apr 2026).
"""
import sys, os, json
import numpy as np, pandas as pd
from datetime import date, datetime, timedelta

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20261028)

START, END = date(2025, 9, 1), date(2026, 10, 27)   # completed sessions
AS_OF = date(2026, 10, 27)
WINDOW = 90
MIN_BENCH = 20

def logit(p): return np.log(p / (1 - p))
def expit(x): return 1 / (1 + np.exp(-x))

# platform x type params: exposure median, entry, prodexp, ctr, c2p, retention, aov multiplier
P = {
 ("douyin","Self-operated"): dict(exp=9000,  entry=.09, pexp=.89, ctr=.25, c2p=.10, ret=.75, aov=1.00),
 ("douyin","Influencer"):    dict(exp=25000, entry=.14, pexp=.22, ctr=.10, c2p=.06, ret=.80, aov=1.05),
 ("red","Self-operated"):    dict(exp=3000,  entry=.12, pexp=.75, ctr=.18, c2p=.12, ret=.88, aov=1.35),
 ("red","Influencer"):       dict(exp=8000,  entry=.18, pexp=.45, ctr=.14, c2p=.10, ret=.90, aov=1.30),
 ("tmall","Self-operated"):  dict(exp=5000,  entry=.22, pexp=.85, ctr=.30, c2p=.12, ret=.84, aov=1.15),
 ("tmall","Influencer"):     dict(exp=12000, entry=.20, pexp=.60, ctr=.20, c2p=.09, ret=.82, aov=1.10),
 ("jd","Self-operated"):     dict(exp=6000,  entry=.15, pexp=.88, ctr=.25, c2p=.20, ret=.92, aov=1.20),
 ("jd","Influencer"):        dict(exp=9000,  entry=.16, pexp=.65, ctr=.18, c2p=.14, ret=.90, aov=1.15),
}
BRAND_AOV = {"Thorne": 279, "KELO-COTE": 269, "Swanson": 189}
TOPICS = {
 "Thorne": ["鱼油溯源专场", "运动营养答疑", "睡眠营养夜话", "镁元素科普", "肠道健康专场", "备孕营养课"],
 "KELO-COTE": ["疤痕护理答疑", "剖腹产疤痕修复专场", "宝宝磕碰护理", "痘印修复课", "术后护理指南"],
 "Swanson": ["维生素D科普", "叶黄素护眼专场", "关节养护课", "全家营养补给", "益生菌专场"],
}
SEASON_TOPIC = {11: "双11囤货指南", 6: "618大促专场", 3: "38女神节专场", 12: "双12返场"}

# accounts: (brand, platform, type, name, sessions_per_week, special)
A = []
def add(brand, plat, typ, names, freq):
    for n in names:
        f = freq(n) if callable(freq) else freq
        A.append(dict(brand=brand, platform=plat, type=typ, account_name=n, freq=f))

add("Thorne","douyin","Self-operated",["Thorne悦恩运动极限海外店"],2.0)
add("Thorne","douyin","Self-operated",["Thorne悦恩自营直播间"],1.5)
add("Thorne","douyin","Influencer",["LisaWang（15号悦恩活动）","弓老师","说真话的营养师Steven","小小欢叔_Zmyyhs",
    "李娜老师讲修行(臻健来)","娜儿-生活智慧商津聚","阿文看大脑（6月睡眠招募）","首彬悦读","文娇和朋友们","康姐的小管家","环球健选","嘉媛食养"],
    lambda n: 3.0 if "Steven" in n else (1.2 if "LisaWang" in n else rng.uniform(.25, 1.0)))
add("KELO-COTE","douyin","Self-operated",["KELO-COTE芭克母婴海外"],6.0)
add("KELO-COTE","douyin","Self-operated",["KELO-COTE芭克母婴海外直播间"],1.0)
add("KELO-COTE","douyin","Influencer",["我是芒果【孕期知识分享】","西福芦（想当辣妈版）","万子疤痕管理","孙火火甲友(十年)","明心自我",
    "印迹指导专场","莹莹吖带娃记","🌻不发脾气只发财🤑","一只李李（变美版）","金美丽吖","香港🇭🇰百佳港货老板娘","🐶小小小冯🐶"],
    lambda n: 2.5 if "芒果" in n else rng.uniform(.25, 1.0))
add("Swanson","douyin","Self-operated",["Swanson斯旺森官方旗舰店"],4.0)
add("Swanson","douyin","Influencer",["营养科普·陈医生","宝妈小课堂·露露","健身达人·Max","养生堂·刘姐","护眼科普·小林",
    "银发生活·老周","全家健康·佳佳","打工人补给站","学霸妈妈·Tina"], lambda n: rng.uniform(.3, 1.2))
add("Thorne","red","Self-operated",["Thorne悦恩营养研究所"],1.5)
add("Thorne","red","Influencer",["营养师小雅","健身教练阿Ken","睡眠研究员Momo","跑者日记Coco","轻体食堂Yuki",
    "30+女性健康笔记","运动康复师Leo","营养学硕士Jo"], lambda n: rng.uniform(.3, 1.0))
add("KELO-COTE","red","Self-operated",["KELO-COTE疤痕护理研究室"],1.0)
add("KELO-COTE","red","Influencer",["产后修复师Nina","新手妈妈日记","皮肤科医生小周","疤痕修复打卡","宝妈好物分享",
    "医美后护理笔记","二胎妈妈Vivi"], lambda n: rng.uniform(.3, 0.9))
add("Thorne","tmall","Self-operated",["Thorne海外旗舰店"],5.0)
add("Thorne","tmall","Self-operated",["Thorne天猫国际直播间"],2.0)
add("Thorne","tmall","Influencer",["淘宝主播·安安","健康好物·大雄","营养师直播间·晴天","全球购·Mandy","运动补剂·老K",
    "银发健康·王姐","家庭营养·小敏"], lambda n: rng.uniform(.3, 1.0))
add("KELO-COTE","tmall","Self-operated",["KELO-COTE海外旗舰店"],3.0)
add("KELO-COTE","tmall","Influencer",["母婴主播·果果","宝妈严选·糖糖","育儿好物·小米粥"], 0.35)  # thin group -> benchmark building
add("Swanson","tmall","Self-operated",["Swanson海外旗舰店"],4.0)
add("Swanson","tmall","Influencer",["淘宝主播·豆豆","全球好物·Cici","营养管家·阿伟","护眼专家·Dr.Wu","健康生活·May",
    "家庭药箱·老陈","中老年健康·秦姐","学生党补给·小北"], lambda n: rng.uniform(.3, 1.0))
add("Thorne","jd","Self-operated",["Thorne京东国际自营店"],2.0)
add("Thorne","jd","Influencer",["JD健康主播·阿杰","京东超市·小鹿","健康管家·Helen","营养顾问·Sam"], lambda n: rng.uniform(.5, 1.2))
add("Swanson","jd","Self-operated",["Swanson京东国际旗舰店"],2.0)
add("Swanson","jd","Influencer",["京东健康·果冻","营养师·大鹏","居家健康·Anna","运动营养·Rocky"], lambda n: rng.uniform(.5, 1.2))

acc = pd.DataFrame(A)
acc.insert(0, "account_id", [f"ACC{i+1:03d}" for i in range(len(acc))])
total_days = (END - START).days + 1
# account random effects and active windows
acc["re_exp"] = [rng.lognormal(0, .4 if t == "Self-operated" else .8) for t in acc.type]
acc["re_aov"] = [rng.lognormal(0, .05 if (b == "KELO-COTE" and t == "Influencer") else .22) for b, t in zip(acc.brand, acc.type)]
acc.loc[acc.account_name.str.contains("LisaWang"), ["re_aov", "re_exp"]] = [7.5, 2.5]
acc["re_rate"] = [rng.normal(0, .3, 5) for _ in range(len(acc))]
starts, ends = [], []
for t in acc.type:
    if t == "Self-operated":
        starts.append(START); ends.append(END)
    else:
        s = START + timedelta(days=int(rng.integers(0, total_days * .6)))
        e = min(END, s + timedelta(days=int(rng.integers(120, total_days))))
        starts.append(s); ends.append(e)
acc["active_from"], acc["active_to"] = starts, ends
# make sure most influencers are active in the last 90 days (rich current view)
recent = acc.type.eq("Influencer") & (rng.random(len(acc)) < .8)
acc.loc[recent, "active_to"] = END

def season(d):
    m, dd = d.month, d.day
    if (m == 10 and dd >= 20) or (m == 11 and dd <= 11): return 1.6, 1.2
    if m == 6 and dd <= 18: return 1.5, 1.15
    if m == 12 and dd <= 12: return 1.2, 1.05
    if m == 2: return .7, .9
    if m == 3 and dd <= 8: return 1.2, 1.05
    return 1.0, 1.0

rows = []
sid = 0
for a in acc.itertuples():
    p = P[(a.platform, a.type)]
    d = a.active_from
    while d <= a.active_to:
        # sessions per day ~ Poisson(freq/7), capped at 2
        k = min(2, rng.poisson(a.freq / 7))
        for j in range(k):
            sid += 1
            ex_m, cv_m = season(d)
            hour = int(rng.choice([10, 14, 19, 20, 21])) if j == 0 else 22
            start = datetime(d.year, d.month, d.day, hour, int(rng.choice([0, 30])))
            dur = int(np.clip(rng.normal(150 if a.type == "Self-operated" else 120, 40), 45, 300))
            exposed = int(max(300, p["exp"] * a.re_exp * ex_m * rng.lognormal(0, .5) * dur / 150))
            r = [expit(logit(base) + a.re_rate[i] + rng.normal(0, .35)) for i, base in
                 enumerate([p["entry"], p["pexp"], p["ctr"], p["c2p"], p["ret"]])]
            r[3] = min(.6, r[3] * cv_m)
            entered = rng.binomial(exposed, r[0])
            pexp = rng.binomial(entered, r[1])
            clk = rng.binomial(pexp, r[2])
            paid = rng.binomial(clk, r[3])
            kept = rng.binomial(paid, r[4])
            orders = paid + rng.binomial(paid, .08)
            aov = BRAND_AOV[a.brand] * p["aov"] * a.re_aov * rng.lognormal(0, .12)
            gmv = round(orders * aov, 2)
            m = d.month
            topic = SEASON_TOPIC.get(m) if (m in SEASON_TOPIC and rng.random() < .5) else rng.choice(TOPICS[a.brand])
            rows.append(dict(session_id=f"S{sid:05d}", brand=a.brand, platform=a.platform, account_id=a.account_id,
                account_name=a.account_name, type=a.type, start_time=start.isoformat(timespec="minutes"),
                duration_min=dur, live_topic=f"{a.account_name.split('（')[0][:10]}·{topic}",
                exposed_uv=exposed, entered_uv=entered, product_exposed_uv=pexp, product_click_uv=clk,
                paid_buyers=paid, kept_buyers=kept, paid_orders=orders, refund_orders=paid - kept,
                gmv_cny=gmv, avg_watch_sec=int(np.clip(rng.normal(70 if a.type == "Influencer" else 55, 25), 15, 300)),
                status="ok"))
        d += timedelta(days=1)

s = pd.DataFrame(rows).sort_values("start_time").reset_index(drop=True)
# data quality flags
q = rng.choice(len(s), size=int(len(s) * .01), replace=False)
s.loc[q, "status"] = "quarantined"
# a session currently live (excluded from benchmarks/tiers)
live = s.iloc[-1].copy(); live["session_id"] = "S99999"; live["start_time"] = "2026-10-28T14:00"
live["status"] = "live"; live["account_name"] = "KELO-COTE芭克母婴海外"
live["account_id"] = acc.loc[acc.account_name == "KELO-COTE芭克母婴海外", "account_id"].iloc[0]
live["brand"], live["platform"], live["type"] = "KELO-COTE", "douyin", "Self-operated"
s = pd.concat([s, live.to_frame().T], ignore_index=True)

for c in ["exposed_uv","entered_uv","product_exposed_uv","product_click_uv","paid_buyers","kept_buyers","paid_orders","refund_orders","duration_min","avg_watch_sec"]:
    s[c] = s[c].astype(int)
s["gmv_cny"] = s.gmv_cny.astype(float)
s["date"] = pd.to_datetime(s.start_time).dt.date

STAGES = ["entry_rate","product_exposure_rate","product_click_rate","click_to_pay_rate","retention_rate"]
NUM = ["exposed_uv","entered_uv","product_exposed_uv","product_click_uv","paid_buyers"]
def rates(df):
    out = pd.DataFrame(index=df.index)
    out["entry_rate"] = df.entered_uv / df.exposed_uv
    out["product_exposure_rate"] = df.product_exposed_uv / df.entered_uv.where(df.entered_uv > 0)
    out["product_click_rate"] = df.product_click_uv / df.product_exposed_uv.where(df.product_exposed_uv > 0)
    out["click_to_pay_rate"] = df.paid_buyers / df.product_click_uv.where(df.product_click_uv > 0)
    out["retention_rate"] = df.kept_buyers / df.paid_buyers.where(df.paid_buyers > 0)
    out["cvr"] = df.paid_buyers / df.entered_uv.where(df.entered_uv > 0)
    out["aov_cny"] = df.gmv_cny / df.paid_orders.where(df.paid_orders > 0)
    return out
R = rates(s)
s = pd.concat([s, R], axis=1)
# gradeable mask per stage (small-sample rule)
inputs = {"entry_rate": "exposed_uv", "product_exposure_rate": "entered_uv", "product_click_rate": "product_exposed_uv",
          "click_to_pay_rate": "product_click_uv"}
def gradeable(df, st):
    if st == "retention_rate": return df.paid_buyers >= 3
    return df[inputs[st]] >= 30
valid = s.status.eq("ok")

def tier_of(v, p25, p50, p75):
    if pd.isna(v): return None
    return "STAR" if v >= p75 else "GOOD" if v >= p50 else "MID" if v >= p25 else "WEAK"

# per-session scoring against rolling benchmark ending the day before the session (vectorised)
for c in [f"tier_{x}" for x in STAGES] + ["session_tier", "session_tier_cvr", "weakest_stage", "benchmark_n"]:
    s[c] = None
s["recoverable_cny"] = 0.0
INP = {"entry_rate": "exposed_uv", "product_exposure_rate": "entered_uv", "product_click_rate": "product_exposed_uv",
       "click_to_pay_rate": "product_click_uv", "retention_rate": "paid_buyers"}
MINI = {k: (3 if k == "retention_rate" else 30) for k in INP}
TIERS = ["WEAK", "MID", "GOOD", "STAR"]
for (b, pl, t), g in s.groupby(["brand", "platform", "type"]):
    g = g.copy()
    gd = pd.to_datetime(g.date).values
    V = g[STAGES].to_numpy(dtype=float)
    OK = np.column_stack([(g[INP[st]].to_numpy() >= MINI[st]) & ~np.isnan(V[:, i]) for i, st in enumerate(STAGES)])
    isok = g.status.eq("ok").to_numpy()
    LOST = np.column_stack([g.exposed_uv - g.entered_uv, g.entered_uv - g.product_exposed_uv,
                            g.product_exposed_uv - g.product_click_uv, g.product_click_uv - g.paid_buyers,
                            g.paid_buyers - g.kept_buyers]).astype(float)
    CV = g.cvr.to_numpy(dtype=float)
    for k, idx in enumerate(g.index):
        if not isok[k]: continue
        d = gd[k]
        wm = isok & (gd < d) & (gd >= d - np.timedelta64(WINDOW, "D"))
        s.at[idx, "benchmark_n"] = int(wm.sum())
        if wm.sum() < MIN_BENCH: continue
        Wv, Wok = V[wm], OK[wm]
        sorted_cols = [np.sort(Wv[Wok[:, i], i]) for i in range(5)]
        def prank(i, x):
            col = sorted_cols[i]
            return max(np.searchsorted(col, x, side="left") / len(col), 0.01)
        pr, worst = [], None
        for i, st in enumerate(STAGES):
            if not OK[k, i] or len(sorted_cols[i]) < MIN_BENCH: continue
            p25, p50, p75 = np.percentile(sorted_cols[i], [25, 50, 75])
            tr = tier_of(V[k, i], p25, p50, p75)
            s.at[idx, f"tier_{st}"] = tr
            pr.append(prank(i, V[k, i]))
            key = (TIERS.index(tr), -LOST[k, i])
            if worst is None or key < worst[0]: worst = (key, i + 1)
        if pr:
            comp = len(pr) / sum(1 / x for x in pr)
            Wc = []
            for r_ in range(len(Wv)):
                prs = [prank(i, Wv[r_, i]) for i in range(5) if Wok[r_, i] and len(sorted_cols[i]) >= MIN_BENCH]
                if prs: Wc.append(len(prs) / sum(1 / x for x in prs))
            c25, c50, c75 = np.percentile(Wc, [25, 50, 75])
            s.at[idx, "session_tier"] = tier_of(comp, c25, c50, c75)
            s.at[idx, "weakest_stage"] = worst[1] if worst else None
        cv = CV[wm]; cv = cv[~np.isnan(cv)]
        row = g.iloc[k]
        if len(cv) >= MIN_BENCH and row.entered_uv > 0:
            p25c, p50c, p75 = np.percentile(cv, [25, 50, 75])
            s.at[idx, "session_tier_cvr"] = tier_of(row.cvr, p25c, p50c, p75)
            if row.paid_buyers > 0:
                gpb = row.gmv_cny / row.paid_buyers
            else:  # no buyers: fall back to the window's median GMV per buyer
                wg = g[wm]; wg = wg[wg.paid_buyers > 0]
                gpb = float(np.median(wg.gmv_cny / wg.paid_buyers))
            s.at[idx, "recoverable_cny"] = round(row.entered_uv * max(0, p75 - row.cvr) * gpb, 2)

# benchmarks snapshot as of AS_OF
bm = []
w_from = AS_OF - timedelta(days=WINDOW - 1)
cur = s[(s.date >= w_from) & (s.date <= AS_OF)]
for (b, pl, t), g in s.groupby(["brand", "platform", "type"]):
    gw = cur[(cur.brand == b) & (cur.platform == pl) & (cur.type == t)]
    gv = gw[gw.status == "ok"]
    rec = dict(as_of=AS_OF.isoformat(), window_from=w_from.isoformat(), window_to=AS_OF.isoformat(),
               brand=b, platform=pl, type=t, n_sessions=len(gv), n_excluded=int((gw.status != "ok").sum()),
               n_accounts=gv.account_id.nunique(), status="ready" if len(gv) >= MIN_BENCH else "building")
    gv = gv.assign(exposure_per_session=gv.exposed_uv)
    for m in STAGES + ["cvr", "aov_cny", "exposure_per_session"]:
        vals = gv[m].dropna() if m not in STAGES else gv.loc[gradeable(gv, m), m].dropna()
        for q_, lab in zip([25, 50, 75], ["p25", "p50", "p75"]):
            rec[f"{m}_{lab}"] = round(float(np.percentile(vals, q_)), 4) if len(vals) else None
    bm.append(rec)
bm = pd.DataFrame(bm)

# host tags as of AS_OF (influencers only), thresholds = benchmark P50 of exposure/session and AOV
h = []
for a in acc.itertuples():
    g = cur[(cur.account_id == a.account_id) & (cur.status == "ok")]
    B = bm[(bm.brand == a.brand) & (bm.platform == a.platform) & (bm.type == a.type)].iloc[0]
    n = len(g)
    rec = dict(account_id=a.account_id, brand=a.brand, platform=a.platform, type=a.type, account_name=a.account_name,
               sessions=n, gmv_cny=round(g.gmv_cny.sum(), 2), paid_orders=int(g.paid_orders.sum()),
               exposed_uv=int(g.exposed_uv.sum()))
    rec["gmv_per_session_cny"] = round(rec["gmv_cny"] / n, 2) if n else None
    rec["aov_cny"] = round(rec["gmv_cny"] / rec["paid_orders"], 2) if rec["paid_orders"] else None
    rec["exposure_per_session"] = round(rec["exposed_uv"] / n) if n else None
    tot = g[NUM + ["kept_buyers"]].sum()
    rec["entry_rate"] = tot.entered_uv / tot.exposed_uv if tot.exposed_uv else None
    rec["product_exposure_rate"] = tot.product_exposed_uv / tot.entered_uv if tot.entered_uv else None
    rec["product_click_rate"] = tot.product_click_uv / tot.product_exposed_uv if tot.product_exposed_uv else None
    rec["click_to_pay_rate"] = tot.paid_buyers / tot.product_click_uv if tot.product_click_uv else None
    rec["retention_rate"] = tot.kept_buyers / tot.paid_buyers if tot.paid_buyers else None
    rec["cvr"] = tot.paid_buyers / tot.entered_uv if tot.entered_uv else None
    for k in STAGES + ["cvr"]:
        if rec[k] is not None: rec[k] = round(float(rec[k]), 4)
    rec["last_live"] = max(g.date).isoformat() if n else None
    tag, border = None, False
    if a.type != "Influencer":
        tag = "Not tagged (self-operated)"
    elif B.status != "ready":
        tag = "Benchmark building"
    elif n < 3 or rec["paid_orders"] < 10:
        tag = "Not enough data"
    else:
        hi_r = rec["exposure_per_session"] >= B.exposure_per_session_p50
        hi_a = rec["aov_cny"] >= B.aov_cny_p50
        tag = {(True, True): "Flagship", (True, False): "Traffic Engine", (False, True): "Premium Niche",
               (False, False): "Under Review"}[(hi_r, hi_a)]
        border = bool(abs(rec["exposure_per_session"] / B.exposure_per_session_p50 - 1) <= .10 or
                      abs(rec["aov_cny"] / B.aov_cny_p50 - 1) <= .10)
    rec["tag"], rec["borderline"] = tag, border
    rec["cvr_tier"] = tier_of(rec["cvr"], B.cvr_p25, B.cvr_p50, B.cvr_p75) if (B.status == "ready" and n >= 3 and rec["cvr"] is not None) else None
    h.append(rec)
h = pd.DataFrame(h)

# connections + annual GMV (from platform MCP) + users
conn = []
connected = {"Thorne": ["douyin","red","tmall","jd"], "KELO-COTE": ["douyin","red","tmall"], "Swanson": ["douyin","tmall","jd"]}
for b in BRAND_AOV:
    for pl in ["douyin","red","tmall","jd"]:
        on = pl in connected[b]
        last12 = s[(s.brand == b) & (s.platform == pl) & (s.date > AS_OF - timedelta(days=365))].gmv_cny.sum()
        conn.append(dict(brand=b, platform=pl, status="connected" if on else "not_connected",
                         last_sync="2026-10-28T08:00" if on else None,
                         annual_gmv_cny_from_mcp=round(last12 * rng.uniform(3.5, 5.0), -3) if on else None))
conn = pd.DataFrame(conn)

users = pd.DataFrame([
 dict(user_id="U001", name="Demo Admin", email="admin.demo@example.com", role="Admin", brands="Thorne;KELO-COTE;Swanson", status="Active", source="Manual", last_active="2026-10-28"),
 dict(user_id="U002", name="Chen Yu", email="chen.yu@example.com", role="Operator", brands="Thorne", status="Active", source="Okta", last_active="2026-10-27"),
 dict(user_id="U003", name="Lin Mei", email="lin.mei@example.com", role="Operator", brands="KELO-COTE", status="Active", source="Okta", last_active="2026-10-28"),
 dict(user_id="U004", name="Zhao Hao", email="zhao.hao@example.com", role="Operator", brands="Thorne;Swanson", status="Active", source="Okta", last_active="2026-10-21"),
 dict(user_id="U005", name="Wang Xin", email="wang.xin@example.com", role="Operator", brands="Swanson", status="Invited", source="Okta", last_active=None),
 dict(user_id="U006", name="Liu Jia", email="liu.jia@example.com", role="Operator", brands="", status="Active", source="Okta", last_active="2026-10-15"),
 dict(user_id="U007", name="Sun Qi", email="sun.qi@example.com", role="Admin", brands="KELO-COTE", status="Deactivated", source="Okta", last_active="2026-08-30"),
])

s = s.drop(columns=["date"])
acc_out = acc.drop(columns=["re_exp","re_aov","re_rate","freq"])
for df, name in [(acc_out,"accounts"),(s,"sessions"),(bm,"benchmarks"),(h,"host_tags"),(conn,"platform_connections"),(users,"users")]:
    df.to_csv(os.path.join(OUT, f"{name}.csv"), index=False, encoding="utf-8-sig")

summary = dict(
  sessions=len(s), accounts=len(acc),
  by_platform=s.groupby("platform").size().to_dict(),
  by_brand_platform=s.groupby(["brand","platform"]).size().astype(int).to_dict(),
  benchmark_status=bm[["brand","platform","type","n_sessions","status"]].to_dict("records"),
  tags=h.tag.value_counts().to_dict(),
)
print(json.dumps({k:(str(v) if k=="by_brand_platform" else v) for k,v in summary.items()}, ensure_ascii=False, indent=1, default=str))
