from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
import io
from datetime import datetime

DARK = colors.HexColor("#0a0f2e")
CARD = colors.HexColor("#111827")
BLUE = colors.HexColor("#6366f1")
BLUE_LIGHT = colors.HexColor("#818cf8")
GREEN = colors.HexColor("#10b981")
AMBER = colors.HexColor("#f59e0b")
RED = colors.HexColor("#ef4444")
CYAN = colors.HexColor("#06b6d4")
PURPLE = colors.HexColor("#8b5cf6")
WHITE = colors.HexColor("#ffffff")
LIGHT = colors.HexColor("#e2e8f0")
MUTED = colors.HexColor("#94a3b8")
BORDER = colors.HexColor("#1e3a5f")
ROW1 = colors.HexColor("#111827")
ROW2 = colors.HexColor("#0d1520")

def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(DARK)
    canvas.rect(0, h-50, w, 50, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(40, h-32, "FinSight")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(120, h-32, "AI-Powered Financial Intelligence Platform")
    canvas.setFillColor(MUTED)
    canvas.drawRightString(w-40, h-32, datetime.now().strftime("%d %B %Y"))
    canvas.setFillColor(DARK)
    canvas.rect(0, 0, w, 35, fill=1, stroke=0)
    canvas.setFillColor(BORDER)
    canvas.rect(0, 35, w, 1, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(40, 12, "For educational and analytical purposes only. Not financial advice.")
    canvas.drawRightString(w-40, 12, f"Page {doc.page}")
    canvas.restoreState()

def generate_pdf_report(company_name, industry, ticker, live, baseline, benchmark):
    buffer = io.BytesIO()
    doc = BaseDocTemplate(
        buffer, pagesize=A4,
        rightMargin=40, leftMargin=40,
        topMargin=70, bottomMargin=50,
    )
    frame = Frame(40, 50, A4[0]-80, A4[1]-120, id="main")
    template = PageTemplate(id="main", frames=frame, onPage=header_footer)
    doc.addPageTemplates([template])

    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle("T1", fontSize=20, fontName="Helvetica-Bold", textColor=LIGHT, spaceAfter=4)
    sub_style = ParagraphStyle("T2", fontSize=10, fontName="Helvetica", textColor=MUTED, spaceAfter=20)
    section_style = ParagraphStyle("S1", fontSize=13, fontName="Helvetica-Bold", textColor=BLUE_LIGHT, spaceAfter=10, spaceBefore=16)
    small_style = ParagraphStyle("SM", fontSize=8, fontName="Helvetica", textColor=MUTED, alignment=TA_CENTER)

    def fmt_cr(val):
        if not val: return "N/A"
        if val >= 100000: return f"Rs {val/100000:.2f}L Cr"
        elif val >= 1000: return f"Rs {val/1000:.1f}K Cr"
        else: return f"Rs {val:.0f} Cr"

    resilience = baseline.get("resilience", 0)
    res_label = "Resilient" if resilience >= 70 else "Moderate" if resilience >= 40 else "Vulnerable"
    res_color = GREEN if resilience >= 70 else AMBER if resilience >= 40 else RED

    revenue = live.get("revenue") or 1000
    ebitda = live.get("ebitda") or 0
    net_income = live.get("net_income") or 0
    total_debt = live.get("total_debt") or 0
    total_assets = live.get("total_assets") or revenue * 1.5
    equity = total_assets - total_debt
    market_cap = live.get("market_cap") or 0
    ebit_val = live.get("ebit") or ebitda
    company_pe = live.get("pe_ratio") or 0
    cash = live.get("cash") or 0

    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"Financial Analysis Report", title_style))
    elements.append(Paragraph(f"{company_name}  •  {industry}  •  {ticker}", sub_style))
    elements.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=16))

    # KPI boxes
    elements.append(Paragraph("Executive Summary", section_style))
    kpi_data = [
        [
            Paragraph(f"<font color='#94a3b8' size='8'>REVENUE</font><br/><font color='#6366f1' size='14'><b>{fmt_cr(live.get('revenue'))}</b></font>", styles["Normal"]),
            Paragraph(f"<font color='#94a3b8' size='8'>EBITDA</font><br/><font color='#10b981' size='14'><b>{fmt_cr(live.get('ebitda'))}</b></font>", styles["Normal"]),
            Paragraph(f"<font color='#94a3b8' size='8'>MARKET CAP</font><br/><font color='#f59e0b' size='14'><b>{fmt_cr(live.get('market_cap'))}</b></font>", styles["Normal"]),
            Paragraph(f"<font color='#94a3b8' size='8'>RESILIENCE</font><br/><font color='#{res_color.hexval()[2:]}' size='14'><b>{resilience:.0f}/100</b></font>", styles["Normal"]),
        ]
    ]
    kpi_table = Table(kpi_data, colWidths=[1.6*inch]*4)
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CARD),
        ("BOX", (0,0), (-1,-1), 1, BORDER),
        ("INNERGRID", (0,0), (-1,-1), 0.5, BORDER),
        ("PADDING", (0,0), (-1,-1), 14),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 12),
        ("LINEABOVE", (0,0), (0,-1), 3, BLUE),
        ("LINEABOVE", (1,0), (1,-1), 3, GREEN),
        ("LINEABOVE", (2,0), (2,-1), 3, AMBER),
        ("LINEABOVE", (3,0), (3,-1), 3, res_color),
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 12))

    # Full metrics table
    metrics_data = [
        ["Metric", "Value", "Metric", "Value"],
        ["Net Income", fmt_cr(net_income), "P/E Ratio", f"{company_pe}x"],
        ["Total Debt", fmt_cr(total_debt), "P/B Ratio", f"{live.get('pb_ratio', 'N/A')}x"],
        ["Cash & Equiv.", fmt_cr(cash), "ROE", f"{live.get('roe', 0):.1f}%"],
        ["Total Assets", fmt_cr(total_assets), "Dividend Yield", f"{live.get('dividend_yield', 0):.1f}%"],
        ["Current Price", f"Rs {live.get('current_price', 0):,.0f}" if live.get('current_price') else "N/A", "52W High", f"Rs {live.get('52w_high', 0):,.0f}" if live.get('52w_high') else "N/A"],
        ["Resilience Score", f"{resilience:.0f}/100", "Status", res_label],
    ]
    mt = Table(metrics_data, colWidths=[1.6*inch, 1.8*inch, 1.6*inch, 1.6*inch])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 9),
        ("BACKGROUND", (0,1), (-1,-1), ROW1),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [ROW1, ROW2]),
        ("TEXTCOLOR", (0,1), (-1,-1), LIGHT),
        ("TEXTCOLOR", (0,1), (0,-1), MUTED),
        ("TEXTCOLOR", (2,1), (2,-1), MUTED),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (2,1), (2,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,1), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("PADDING", (0,0), (-1,-1), 8),
        ("ALIGN", (1,0), (1,-1), "RIGHT"),
        ("ALIGN", (3,0), (3,-1), "RIGHT"),
    ]))
    elements.append(mt)
    elements.append(Spacer(1, 16))

    # Advanced ratios
    elements.append(Paragraph("Advanced Financial Ratios", section_style))

    ev = market_cap + total_debt - cash
    ev_ebitda = round(ev / max(ebitda, 1), 2) if ebitda > 0 else 0
    interest_coverage = round(ebit_val / max(total_debt * 0.08, 1), 2) if ebit_val else 0
    working_capital_ratio = round(cash / max(total_debt * 0.3, 1), 2)
    earnings_yield = round(1 / max(company_pe, 0.1) * 100, 2) if company_pe else 0
    asset_turnover = round(revenue / total_assets, 2) if total_assets else 0
    debt_to_assets = round(total_debt / total_assets, 2) if total_assets else 0

    if total_assets > 0:
        z = round(1.2*(cash/total_assets) + 1.4*(net_income/total_assets) + 3.3*(ebit_val/total_assets) + 0.6*(market_cap/max(total_debt,1)) + revenue/total_assets, 2)
    else:
        z = 0
    z_label = "Safe Zone" if z > 2.99 else "Grey Zone" if z > 1.81 else "Distress Zone"
    z_color = GREEN if z > 2.99 else AMBER if z > 1.81 else RED

    eps = net_income / 100 if net_income else 0
    bvps = equity / 100 if equity else 0
    graham = round((22.5 * max(eps,0) * max(bvps,0))**0.5, 2) if eps > 0 and bvps > 0 else 0
    current_price = live.get("current_price") or 0

    ratio_data = [
        ["Ratio", "Value", "Signal", "Interpretation"],
        ["Altman Z-Score", str(z), z_label, "Bankruptcy predictor — higher is safer"],
        ["Graham Number", f"Rs {graham:,.0f}", "Undervalued" if graham > current_price > 0 else "Overvalued", f"vs Current Price Rs {current_price:,.0f}"],
        ["EV/EBITDA", f"{ev_ebitda}x", "Cheap" if ev_ebitda < 15 else "Fair" if ev_ebitda < 25 else "Expensive", "Enterprise value multiple"],
        ["Interest Coverage", f"{interest_coverage}x", "Safe" if interest_coverage > 3 else "Risky", "Ability to service debt"],
        ["Working Capital Ratio", f"{working_capital_ratio}x", "Liquid" if working_capital_ratio > 1 else "Tight", "Short-term liquidity"],
        ["Earnings Yield", f"{earnings_yield}%", "High" if earnings_yield > 5 else "Low", "Return relative to price"],
        ["Asset Turnover", f"{asset_turnover}x", "Efficient" if asset_turnover > 0.5 else "Low", "Revenue per Rs of assets"],
        ["Debt to Assets", f"{debt_to_assets}x", "Conservative" if debt_to_assets < 0.4 else "Leveraged", "Financial risk indicator"],
    ]

    rt = Table(ratio_data, colWidths=[1.6*inch, 1.0*inch, 1.1*inch, 2.9*inch])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [ROW1, ROW2]),
        ("TEXTCOLOR", (0,1), (-1,-1), LIGHT),
        ("TEXTCOLOR", (0,1), (0,-1), MUTED),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,1), (-1,-1), 8),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("PADDING", (0,0), (-1,-1), 7),
    ]))
    elements.append(rt)
    elements.append(Spacer(1, 16))

    # Industry benchmark
    elements.append(Paragraph("Industry Benchmark Comparison", section_style))
    company_ebitda_margin = round(ebitda/revenue*100, 1) if revenue else 0
    company_roe = live.get("roe") or round(net_income/max(equity,1)*100, 1)
    company_de = round(total_debt/max(equity,1), 2)

    bench_data = [
        ["Metric", "Company", "Industry Avg", "vs Industry"],
        ["EBITDA Margin", f"{company_ebitda_margin}%", f"{benchmark.get('avg_ebitda_margin',0)}%",
         "Above Avg +" if company_ebitda_margin > benchmark.get('avg_ebitda_margin',0) else "Below Avg -"],
        ["ROE", f"{company_roe:.1f}%", f"{benchmark.get('avg_roe',0)}%",
         "Above Avg +" if company_roe > benchmark.get('avg_roe',0) else "Below Avg -"],
        ["P/E Ratio", f"{company_pe}x", f"{benchmark.get('avg_pe',0)}x",
         "Premium" if company_pe > benchmark.get('avg_pe',0)*1.2 else "Fair Value"],
        ["Debt/Equity", f"{company_de}x", f"{benchmark.get('avg_debt_equity',0)}x",
         "Conservative" if company_de < benchmark.get('avg_debt_equity',0) else "Leveraged"],
    ]

    bt = Table(bench_data, colWidths=[1.8*inch, 1.4*inch, 1.4*inch, 2.0*inch])
    bt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [ROW1, ROW2]),
        ("TEXTCOLOR", (0,1), (-1,-1), LIGHT),
        ("TEXTCOLOR", (0,1), (0,-1), MUTED),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,1), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("PADDING", (0,0), (-1,-1), 8),
        ("ALIGN", (3,1), (3,-1), "CENTER"),
    ]))
    elements.append(bt)
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"Top companies in {industry}: {', '.join(benchmark.get('top_companies', []))}", small_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer
