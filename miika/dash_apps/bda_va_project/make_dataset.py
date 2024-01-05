import pickle
import requests
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np
import yfinance as yf

# All companies tracked by Inderes
# Had to disable this. Too much for server to handle this time
# Scratch that, the problem was weekend data
COMPANIES = [
    {"name": "Aallon", "yf_ticker": "AALLON.HE", "inderes_name": "Aallon Group"},
    {"name": "Admicom", "yf_ticker": "ADMCM.HE", "inderes_name": "Admicom"},
    {"name": "Administer", "yf_ticker": "ADMIN.HE", "inderes_name": "Administer"},
    {"name": "Aiforia", "yf_ticker": "AIFORIA.HE", "inderes_name": "Aiforia Technologies"},
    {"name": "Aktia", "yf_ticker": "AKTIA.HE", "inderes_name": "Aktia Bank"},
    {"name": "Alexandria", "yf_ticker": "ALEX.HE", "inderes_name": "Alexandria Group"},
    {"name": "Alisa", "yf_ticker": "ALISA.HE", "inderes_name": "Alisa Pankki"},
    {"name": "Alma", "yf_ticker": "ALMA.HE", "inderes_name": "Alma Media"},
    {"name": "Anora", "yf_ticker": "ANORA.HE", "inderes_name": "Anora Group"},
    {"name": "Apetit", "yf_ticker": "APETIT.HE", "inderes_name": "Apetit"},
    {"name": "Aspo", "yf_ticker": "ASPO.HE", "inderes_name": "Aspo"},
    {"name": "Aspocomp", "yf_ticker": "ACG1V.HE", "inderes_name": "Aspocomp Group"},
    {"name": "Asuntosalkku", "yf_ticker": "ASUNTO.HE", "inderes_name": "Asuntosalkku"},
    {"name": "Atria", "yf_ticker": "ATRAV.HE", "inderes_name": "Atria A"},
    {"name": "BBS", "yf_ticker": "BONEH.HE", "inderes_name": "BBS-Bioactive Bone Substitutes"},
    {"name": "Betolar", "yf_ticker": "BETOLAR.HE", "inderes_name": "Betolar"},
    {"name": "Biohit", "yf_ticker": "BIOBV.HE", "inderes_name": "Biohit B"},
    {"name": "Bioretec", "yf_ticker": "BRETEC.HE", "inderes_name": "Bioretec"},
    {"name": "Bittium", "yf_ticker": "BITTI.HE", "inderes_name": "Bittium"},
    {"name": "Boreo", "yf_ticker": "BOREO.HE", "inderes_name": "Boreo"},
    {"name": "CapMan", "yf_ticker": "CAPMAN.HE", "inderes_name": "CapMan"},
    {"name": "Cargotec", "yf_ticker": "CGCBV.HE", "inderes_name": "Cargotec B"},
    {"name": "Componenta", "yf_ticker": "CTH1V.HE", "inderes_name": "Componenta"},
    {"name": "Consti", "yf_ticker": "CONSTI.HE", "inderes_name": "Consti"},
    {"name": "Detection Technology", "yf_ticker": "DETEC.HE", "inderes_name": "Detection Technology"},
    {"name": "Digia", "yf_ticker": "DIGIA.HE", "inderes_name": "Digia"},
    {"name": "Digital Workforce", "yf_ticker": "DWF.HE", "inderes_name": "Digital Workforce"},
    {"name": "Duell", "yf_ticker": "DUELL.HE", "inderes_name": "Duell"},
    {"name": "EcoUp", "yf_ticker": "ECOUP.HE", "inderes_name": "EcoUp"},
    {"name": "Eezy", "yf_ticker": "EEZY.HE", "inderes_name": "Eezy"},
    {"name": "Efecte", "yf_ticker": "EFECTE.HE", "inderes_name": "Efecte"},
    {"name": "Elisa", "yf_ticker": "ELISA.HE", "inderes_name": "Elisa"},
    {"name": "Endomines", "yf_ticker": "PAMPALO.HE", "inderes_name": "Endomines Finland"},
    {"name": "Enento", "yf_ticker": "ENENTO.HE", "inderes_name": "Enento Group"},
    {"name": "Enersense", "yf_ticker": "ESENSE.HE", "inderes_name": "Enersense International"},
    {"name": "eQ", "yf_ticker": "EQV1V.HE", "inderes_name": "eQ"},
    {"name": "Etteplan", "yf_ticker": "ETTE.HE", "inderes_name": "Etteplan"},
    {"name": "Evli", "yf_ticker": "EVLI.HE", "inderes_name": "Evli"},
    {"name": "Exel Composites", "yf_ticker": "EXL1V.HE", "inderes_name": "Exel Composites"},
    {"name": "F-Secure", "yf_ticker": "FSECURE.HE", "inderes_name": "F-Secure"},
    {"name": "Faron", "yf_ticker": "FARON.HE", "inderes_name": "Faron Pharmaceuticals"},
    {"name": "Fifax", "yf_ticker": "FIFAX.HE", "inderes_name": "Fifax"},
    {"name": "Finnair", "yf_ticker": "FIA1S.HE", "inderes_name": "Finnair"},
    {"name": "Fiskars", "yf_ticker": "FSKRS.HE", "inderes_name": "Fiskars A"},
    {"name": "Fodelia", "yf_ticker": "FODELIA.HE", "inderes_name": "Fodelia"},
    {"name": "Fondia", "yf_ticker": "FONDIA.HE", "inderes_name": "Fondia"},
    {"name": "Fortum", "yf_ticker": "FORTUM.HE", "inderes_name": "Fortum"},
    {"name": "Glaston", "yf_ticker": "GLA1V.HE", "inderes_name": "Glaston"},
    {"name": "Gofore", "yf_ticker": "GOFORE.HE", "inderes_name": "Gofore"},
    {"name": "Harvia", "yf_ticker": "HARVIA.HE", "inderes_name": "Harvia"},
    {"name": "Honkarakenne", "yf_ticker": "HONBS.HE", "inderes_name": "Honkarakenne B"},
    {"name": "Huhtamäki", "yf_ticker": "HUH1V.HE", "inderes_name": "Huhtamäki"},
    {"name": "Ilkka", "yf_ticker": "ILKKA1.HE", "inderes_name": "Ilkka Oyj 2"},
    {"name": "Incap", "yf_ticker": "ICP1V.HE", "inderes_name": "Incap"},
    {"name": "Innofactor", "yf_ticker": "IFA1V.HE", "inderes_name": "Innofactor"},
    {"name": "Investors House", "yf_ticker": "INVEST.HE", "inderes_name": "Investors House"},
    {"name": "Kamux", "yf_ticker": "KAMUX.HE", "inderes_name": "Kamux"},
    {"name": "Kemira", "yf_ticker": "KEMIRA.HE", "inderes_name": "Kemira"},
    {"name": "Kempower", "yf_ticker": "KEMPOWR.HE", "inderes_name": "Kempower"},
    {"name": "Kesko", "yf_ticker": "KESKOB.HE", "inderes_name": "Kesko B"},
    {"name": "Kesla", "yf_ticker": "KELAS.HE", "inderes_name": "Kesla A"},
    {"name": "KH", "yf_ticker": "KHG.HE", "inderes_name": "KH Group"},
    {"name": "Kone", "yf_ticker": "KNEBV.HE", "inderes_name": "Kone B"},
    {"name": "Konecranes", "yf_ticker": "KCR.HE", "inderes_name": "Konecranes"},
    {"name": "Koskisen", "yf_ticker": "KOSKI.HE", "inderes_name": "Koskisen"},
    {"name": "Kreate", "yf_ticker": "KREATE.HE", "inderes_name": "Kreate Group"},
    {"name": "Lamor", "yf_ticker": "LAMOR.HE", "inderes_name": "Lamor"},
    {"name": "LapWall", "yf_ticker": "LAPWALL.HE", "inderes_name": "LapWall"},
    {"name": "L&T", "yf_ticker": "LAT1V.HE", "inderes_name": "Lassila & Tikanoja"},
    {"name": "LeadDesk", "yf_ticker": "LEADD.HE", "inderes_name": "LeadDesk"},
    {"name": "Lehto", "yf_ticker": "LEHTO.HE", "inderes_name": "Lehto Group"},
    {"name": "Lemonsoft", "yf_ticker": "LEMON.HE", "inderes_name": "Lemonsoft"},
    {"name": "Loihde", "yf_ticker": "LOIHDE.HE", "inderes_name": "Loihde"},
    {"name": "Mandatum", "yf_ticker": "MANTA.HE", "inderes_name": "Mandatum"},
    {"name": "Marimekko", "yf_ticker": "MEKKO.HE", "inderes_name": "Marimekko"},
    {"name": "Martela", "yf_ticker": "MARAS.HE", "inderes_name": "Martela A"},
    {"name": "Meriaura", "yf_ticker": "MERIH.HE", "inderes_name": "Meriaura Group"},
    {"name": "Merus Power", "yf_ticker": "MERUS.HE", "inderes_name": "Merus Power"},
    {"name": "Metsä Board", "yf_ticker": "METSA.HE", "inderes_name": "Metsä Board B"},
    {"name": "Metso", "yf_ticker": "METSO.HE", "inderes_name": "Metso"},
    {"name": "Modulight", "yf_ticker": "MODU.HE", "inderes_name": "Modulight"},
    {"name": "Neste", "yf_ticker": "NESTE.HE", "inderes_name": "Neste"},
    {"name": "Netum", "yf_ticker": "NETUM.HE", "inderes_name": "Netum"},
    {"name": "Nexstim", "yf_ticker": "NXTMH.HE", "inderes_name": "Nexstim"},
    {"name": "Nightingale", "yf_ticker": "HEALTH.HE", "inderes_name": "Nightingale Health"},
    {"name": "NoHo", "yf_ticker": "NOHO.HE", "inderes_name": "NoHo Partners"},
    {"name": "Nokia", "yf_ticker": "NOKIA.HE", "inderes_name": "Nokia"},
    {"name": "Nokian Renkaat", "yf_ticker": "TYRES.HE", "inderes_name": "Nokian Renkaat"},
    {"name": "Nordea", "yf_ticker": "NDA-FI.HE", "inderes_name": "Nordea Bank"},
    {"name": "Norrhydro", "yf_ticker": "NORRH.HE", "inderes_name": "Norrhydro Group"},
    {"name": "Nurminen Logistics", "yf_ticker": "NLG1V.HE", "inderes_name": "Nurminen Logistics"},
    {"name": "NYAB", "yf_ticker": "NYAB.HE", "inderes_name": "NYAB Oyj"},
    {"name": "OmaSP", "yf_ticker": "OMASP.HE", "inderes_name": "Oma Säästöpankki"},
    {"name": "Optomed", "yf_ticker": "OPTOMED.HE", "inderes_name": "Optomed"},
    {"name": "Oriola", "yf_ticker": "OKDBV.HE", "inderes_name": "Oriola B"},
    {"name": "Orion", "yf_ticker": "ORNBV.HE", "inderes_name": "Orion B"},
    {"name": "Orthex", "yf_ticker": "ORTHEX.HE", "inderes_name": "Orthex"},
    {"name": "Outokumpu", "yf_ticker": "OUT1V.HE", "inderes_name": "Outokumpu"},
    {"name": "Ovaro", "yf_ticker": "OVARO.HE", "inderes_name": "Ovaro Kiinteistösijoitus"},
    {"name": "Pallas Air", "yf_ticker": "PALLAS.HE", "inderes_name": "Pallas Air"},
    {"name": "Panostaja", "yf_ticker": "PNA1V.HE", "inderes_name": "Panostaja"},
    {"name": "Partnera", "yf_ticker": "PARTNE1.HE", "inderes_name": "Partnera Oyj"},
    {"name": "Pihlajalinna", "yf_ticker": "PIHLIS.HE", "inderes_name": "Pihlajalinna"},
    {"name": "Piippo", "yf_ticker": "PIIPPO.HE", "inderes_name": "Piippo"},
    {"name": "Pohjanmaan Arvo", "yf_ticker": "ARVOSK.HE", "inderes_name": "Pohjanmaan Arvo Sijoitusos."},
    {"name": "Ponsse", "yf_ticker": "PON1V.HE", "inderes_name": "Ponsse"},
    {"name": "PunaMusta", "yf_ticker": "PUMU.HE", "inderes_name": "PunaMusta Media"},
    {"name": "Purmo", "yf_ticker": "PURMO.HE", "inderes_name": "Purmo Group C"},
    {"name": "Puuilo", "yf_ticker": "PUUILO.HE", "inderes_name": "Puuilo"},
    {"name": "QPR", "yf_ticker": "QPR1V.HE", "inderes_name": "QPR Software"},
    {"name": "Qt", "yf_ticker": "QTCOM.HE", "inderes_name": "Qt Group"},
    {"name": "Raisio", "yf_ticker": "RAIKV.HE", "inderes_name": "Raisio Vaihto-osake"},
    {"name": "Rapala", "yf_ticker": "RAP1V.HE", "inderes_name": "Rapala VMC"},
    {"name": "Raute", "yf_ticker": "RAUTE.HE", "inderes_name": "Raute"},
    {"name": "Relais", "yf_ticker": "RELAIS.HE", "inderes_name": "Relais Group"},
    {"name": "Remedy", "yf_ticker": "REMEDY.HE", "inderes_name": "Remedy Entertainment"},
    {"name": "Revenio", "yf_ticker": "REG1V.HE", "inderes_name": "Revenio Group"},
    {"name": "Robit", "yf_ticker": "ROBIT.HE", "inderes_name": "Robit"},
    {"name": "Rush Factory", "yf_ticker": "RUSH.HE", "inderes_name": "Rush Factory"},
    {"name": "Sampo", "yf_ticker": "SAMPO.HE", "inderes_name": "Sampo A"},
    {"name": "Sanoma", "yf_ticker": "SANOMA.HE", "inderes_name": "Sanoma"},
    {"name": "Scanfil", "yf_ticker": "SCANFL.HE", "inderes_name": "Scanfil"},
    {"name": "Siili", "yf_ticker": "SIILI.HE", "inderes_name": "Siili Solutions"},
    {"name": "Sitowise", "yf_ticker": "SITOWS.HE", "inderes_name": "Sitowise Group"},
    {"name": "Solteq", "yf_ticker": "SOLTEQ.HE", "inderes_name": "Solteq"},
    {"name": "Solwers", "yf_ticker": "SOLWERS.HE", "inderes_name": "Solwers"},
    {"name": "Springvest", "yf_ticker": "SPRING.HE", "inderes_name": "Springvest"},
    {"name": "SRV", "yf_ticker": "SRV1V.HE", "inderes_name": "SRV Group"},
    {"name": "Stockmann", "yf_ticker": "STOCKA.HE", "inderes_name": "Stockmann"},
    {"name": "Stora Enso", "yf_ticker": "STEAV.HE", "inderes_name": "Stora Enso R"},
    {"name": "Suominen", "yf_ticker": "SUY1V.HE", "inderes_name": "Suominen"},
    {"name": "Taaleri", "yf_ticker": "TAALA.HE", "inderes_name": "Taaleri"},
    {"name": "Talenom", "yf_ticker": "TNOM.HE", "inderes_name": "Talenom"},
    {"name": "Tamtron", "yf_ticker": "TAMTRON.HE", "inderes_name": "Tamtron"},
    {"name": "Tecnotree", "yf_ticker": "TEM1V.HE", "inderes_name": "Tecnotree"},
    {"name": "Teleste", "yf_ticker": "TLT1V.HE", "inderes_name": "Teleste"},
    {"name": "Terveystalo", "yf_ticker": "TTALO.HE", "inderes_name": "Terveystalo"},
    {"name": "Tieto", "yf_ticker": "TIETO.HE", "inderes_name": "Tietoevry"},
    {"name": "Titanium", "yf_ticker": "TITAN.HE", "inderes_name": "Titanium"},
    {"name": "Toivo", "yf_ticker": "TOIVO.HE", "inderes_name": "Toivo Group"},
    {"name": "Tokmanni", "yf_ticker": "TOKMAN.HE", "inderes_name": "Tokmanni Group"},
    {"name": "Tulikivi", "yf_ticker": "TULAV.HE", "inderes_name": "Tulikivi A"},
    {"name": "United Bankers", "yf_ticker": "UNITED.HE", "inderes_name": "United Bankers"},
    {"name": "UPM", "yf_ticker": "UPM.HE", "inderes_name": "UPM-Kymmene"},
    {"name": "Vaisala", "yf_ticker": "VAIAS.HE", "inderes_name": "Vaisala A"},
    {"name": "Valmet", "yf_ticker": "VALMT.HE", "inderes_name": "Valmet"},
    {"name": "Verkkokauppa", "yf_ticker": "VERK.HE", "inderes_name": "Verkkokauppa.com"},
    {"name": "Viafin", "yf_ticker": "VIAFIN.HE", "inderes_name": "Viafin Service"},
    {"name": "Vincit", "yf_ticker": "VINCIT.HE", "inderes_name": "Vincit"},
    {"name": "Wärtsilä", "yf_ticker": "WRT1V.HE", "inderes_name": "Wärtsilä B"},
    {"name": "Wetteri", "yf_ticker": "WETTERI.HE", "inderes_name": "Wetteri"},
    {"name": "WithSecure", "yf_ticker": "WITH.HE", "inderes_name": "WithSecure Corporation"},
    {"name": "Witted", "yf_ticker": "WITTED.HE", "inderes_name": "Witted Megacorp"},
    {"name": "Wulff", "yf_ticker": "WUF1V.HE", "inderes_name": "Wulff Group"},
    {"name": "YIT", "yf_ticker": "YIT.HE", "inderes_name": "YIT Corporation"},
]
# Data we are after from Inderes
INDERES_COLUMNS = [
    # We take latest price from yfinance
    #{"df_name": "", "inderes_name": "Price"},
    {"df_name": "target", "inderes_name": "Target price"},
    {"df_name": "recommendation", "inderes_name": "Recommendation"},
    {"df_name": "risk", "inderes_name": "Risk level"},
    {"df_name": "revenue_2021", "inderes_name": "Revenue#2021"},
    {"df_name": "revenue_2022", "inderes_name": "Revenue#2022"},
    {"df_name": "revenue_2023", "inderes_name": "Revenue#2023"},
    {"df_name": "revenue_2024", "inderes_name": "Revenue#2024"},
    {"df_name": "revenue_2025", "inderes_name": "Revenue#2025"},
    {"df_name": "revenue_2026", "inderes_name": "Revenue#2026"},
    {"df_name": "revenue_2027", "inderes_name": "Revenue#2027"},
    {"df_name": "ebitda", "inderes_name": "EBITDA#2023"},
    {"df_name": "eps", "inderes_name": "EPS#2023"},
    {"df_name": "dividend_ratio", "inderes_name": "Dividend ratio#2023"},
    {"df_name": "margin", "inderes_name": "EBITDA-%#2023"},
    {"df_name": "roe", "inderes_name": "ROE#2023"},
    {"df_name": "mcap", "inderes_name": "MCAP#2023"},
    {"df_name": "ev", "inderes_name": "EV#2023"},
    {"df_name": "equity_ratio", "inderes_name": "Equity ratio#2023"},
]
# Data we are after from yfinance
YF_COLUMNS = [
    {"df_name": "sector", "yf_name": "sector"},
    {"df_name": "industry", "yf_name": "industry"},
    {"df_name": "pb", "yf_name": "priceToBook"},
    {"df_name": "peg", "yf_name": "pegRatio"},
    {"df_name": "volume", "yf_name": "averageVolume"},
    {"df_name": "quick_ratio", "yf_name": "quickRatio"},
    {"df_name": "current_ratio", "yf_name": "currentRatio"},
]

def get_inderes(df, yesterday):
    ind_cols_df = pd.DataFrame(INDERES_COLUMNS)
    # Read in the latest Inderes data
    column_names = []
    # Download a file from Inderes
    with open(f"inderes-stock-comparison-{yesterday}.csv", "wb") as f:
        response = requests.get("https://www.inderes.fi/api/stock-comparison-csv")
        f.write(response.content)
    # Read the column names from the file
    with open(f"inderes-stock-comparison-{yesterday}.csv", "r") as f:
        lines = f.readlines()
        col_heads = lines[0].split(";")
        col_years = lines[1].split(";")
        col_head = ""
        for head, year in zip(col_heads, col_years):
            if head.strip():
                col_head = head.strip()
            if year.strip():
                column_names.append(f"{col_head}#{year.strip()}")
            else:
                column_names.append(col_head)
    inderes_df = pd.read_csv(
        f"inderes-stock-comparison-{yesterday}.csv",
        sep=";", # Separator is semicolon.
        decimal=",", # Decimal is comma. Without these specified. It breaks.
        skiprows=2, # We have the column names unified already
        names=column_names, # here.
        index_col=0
    )
    # Subset just our companies and wanted columns
    inderes_df = inderes_df.loc[df["inderes_name"]][ind_cols_df["inderes_name"]]
    # Rename columns
    inderes_df.columns = ind_cols_df["df_name"]
    return inderes_df

def get_yfinance(df):
    # Fetch ticker data from yfinance
    yf_data = yf.Tickers(" ".join(df["yf_ticker"]))
    yf_cols_df = pd.DataFrame(YF_COLUMNS)
    # Create empty dataframe with columsn YF_COLUMNS["df_name"]
    yf_df = pd.DataFrame(columns=yf_cols_df["df_name"])
    # Fill with ticker info
    for ticker in yf_data.tickers:
        ticker_info = yf_data.tickers[ticker].info
        # Some data is not available for all tickers, replace with None if thats the case
        yf_df.loc[ticker] = [ticker_info.get(col, None) for col in yf_cols_df["yf_name"]]
    return yf_data, yf_df

def stock_data():
    # Yesterday as isoformat
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    DAILY_PICKLE = f"va_project_{yesterday}.pickle"
    if Path(DAILY_PICKLE).is_file():
        with open(DAILY_PICKLE, "rb") as f:
            daily = pickle.load(f)
            return daily["df"], daily["prices"]
    else:
        df = pd.DataFrame(COMPANIES)
        # Fetch Inderes data
        inderes_df = get_inderes(df, yesterday)
        df = df.merge(inderes_df, left_on="inderes_name", right_index=True)
        # Fetch yfinance data
        yf_data, yf_df = get_yfinance(df)
        df = df.merge(yf_df, left_on="yf_ticker", right_index=True)
        # Get prices from yfinance
        # ~250 rows for year x the companies we have (150) x ohlc+v. For exercise, I think that is a good limit
        prices = yf_data.history(period="1y", interval="1d", actions=False)
        # Own additions and calculations to dataframe
        millions = ["revenue_2021", "revenue_2022", "revenue_2023", "revenue_2024", 
                    "revenue_2025", "revenue_2026", "revenue_2027", "ebitda", "mcap", "ev", "volume"]
        df[millions] = np.round(df[millions] / 1000000, 2)
        # Add latest price to df
        df["price"] = [prices["Close"][ticker].iloc[-1] for ticker in df["yf_ticker"]]
        # Calculate P/E
        df["pe"] = np.round((df["price"] / df["eps"]), 2)
        # Calculate EV/EBITDA
        df["ev_ebitda"] = np.round(df["ev"] / df["ebitda"], 2)
        # Trading activity
        df["vmc"] = df["volume"] / df["mcap"] * 100
        # Fill missing values with 0
        df.fillna(0, inplace=True)
        # Pickle the data for daily only fetch
        with open(DAILY_PICKLE, "wb") as f:
            pickle.dump({"df": df, "prices": prices}, f)
        # Return the data
        return df, prices
