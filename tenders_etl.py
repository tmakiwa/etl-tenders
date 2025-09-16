#!/usr/bin/env python3
import argparse, re, sqlite3
import pandas as pd

REQUIRED = ["tender_id","title","issuer","category","province","published_date","closing_date","budget","contact_email","url"]

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input","-i", required=True)
    p.add_argument("--out","-o", default="tenders_clean.csv")
    p.add_argument("--db","-d", default="tenders.db")
    return p.parse_args()

def is_valid_email(email: str) -> bool:
    if not isinstance(email, str):
        return False
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None

def parse_date(s):
    if pd.isna(s): return pd.NaT
    for fmt in ("%Y-%m-%d","%d-%m-%Y","%Y/%m/%d","%d/%m/%Y"):
        try:
            return pd.to_datetime(s, format=fmt, errors="raise")
        except Exception:
            continue
    return pd.to_datetime(s, errors="coerce")

def normalize_budget(x):
    if pd.isna(x): return pd.NA
    s = str(x).strip().lower()
    if "k" in s:
        import re as _re
        num = _re.sub(r"[^0-9.]", "", s)
        try:
            return float(num) * 1000
        except:
            return pd.NA
    import re as _re
    s = _re.sub(r"[^0-9.]", "", s)
    return float(s) if s else pd.NA

def clean(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df.columns = [c.strip() for c in df.columns]
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    df = df.dropna(subset=["tender_id","title"])
    df = df[df["issuer"].astype(str).str.len() > 0]

    df["published_date"] = df["published_date"].apply(parse_date)
    df["closing_date"] = df["closing_date"].apply(parse_date)

    mask_missing_close = df["closing_date"].isna()
    df.loc[mask_missing_close, "closing_date"] = df.loc[mask_missing_close, "published_date"] + pd.to_timedelta(14, unit="D")

    df = df.dropna(subset=["published_date","closing_date"])

    df["budget_amount"] = df["budget"].apply(normalize_budget)

    df = df[df["contact_email"].apply(is_valid_email)]

    df["category"] = df["category"].str.title()
    df["province"] = df["province"].str.Title() if hasattr(str, "Title") else df["province"].str.title()

    df = df.drop_duplicates()

    df = df.sort_values(by=["tender_id","published_date"]).drop_duplicates(subset=["tender_id"], keep="last")

    today = pd.Timestamp.today().normalize()
    df["days_to_close"] = (df["closing_date"] - today).dt.days

    return df

def load_sqlite(df, db_path, table="tenders"):
    conn = sqlite3.connect(db_path)
    try:
        df.to_sql(table, conn, if_exists="replace", index=False)
    finally:
        conn.close()

def main():
    args = parse_args()
    raw = pd.read_csv(args.input)
    print("RAW SHAPE:", raw.shape)
    cleaned = clean(raw)
    print("CLEAN SHAPE:", cleaned.shape)
    cleaned.to_csv(args.out, index=False)
    print("Wrote:", args.out)
    load_sqlite(cleaned, args.db)
    print("Loaded table 'tenders' into:", args.db)
    print(cleaned.head().to_string(index=False))

if __name__ == "__main__":
    main()
