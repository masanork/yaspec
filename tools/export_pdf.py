#!/usr/bin/env python3
import yaml
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import argparse
from datetime import datetime
import locale
import os

# 日本語フォントの設定
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont('Arial', FONT_PATH))

class EstimatePDFExporter:
    def __init__(self, yaml_file, output_file):
        self.data = self._load_yaml(yaml_file)
        self.doc = SimpleDocTemplate(
            output_file,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _load_yaml(self, yaml_file):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _setup_styles(self):
        self.styles.add(ParagraphStyle(
            name='Japanese',
            fontName='Arial',
            fontSize=10,
            leading=14
        ))
        self.styles.add(ParagraphStyle(
            name='JapaneseTitle',
            fontName='Arial',
            fontSize=16,
            leading=20,
            alignment=1  # 中央揃え
        ))
        self.styles.add(ParagraphStyle(
            name='JapaneseSmall',
            fontName='Arial',
            fontSize=8,
            leading=10
        ))

    def _format_currency(self, amount):
        return f"¥{amount:,}"

    def _create_header(self):
        estimate = self.data['見積書']
        issuer = next(p for p in self.data['関係者'] if p['役割'] == 'issuer')
        client = next(p for p in self.data['関係者'] if p['役割'] == 'client')

        elements = []
        
        # タイトルと見積番号
        elements.append(Paragraph(f"御見積書", self.styles['JapaneseTitle']))
        elements.append(Paragraph(f"No. {estimate['見積番号']}", self.styles['Japanese']))
        elements.append(Spacer(1, 10*mm))

        # 顧客情報
        elements.append(Paragraph(
            f"{client['会社名']} 御中<br/>"
            f"{client['部署名']}<br/>"
            f"{client['担当者名']} 様",
            self.styles['Japanese']
        ))
        elements.append(Spacer(1, 10*mm))

        # 発行者情報
        elements.append(Paragraph(
            f"{issuer['会社名']}<br/>"
            f"{issuer['部署名']}<br/>"
            f"{issuer['住所']}<br/>"
            f"TEL: {issuer['電話番号']}<br/>"
            f"担当: {issuer['担当者名']}",
            self.styles['Japanese']
        ))
        elements.append(Spacer(1, 10*mm))

        # 見積日と有効期限
        elements.append(Paragraph(
            f"発行日: {estimate['発行日']}<br/>"
            f"有効期限: {estimate['有効期限']}",
            self.styles['Japanese']
        ))
        elements.append(Spacer(1, 5*mm))

        # 件名
        elements.append(Paragraph(f"件名: {estimate['件名']}", self.styles['Japanese']))
        elements.append(Spacer(1, 10*mm))

        return elements

    def _create_items_table(self):
        # テーブルヘッダー
        headers = ['No.', '項目', '数量', '単位', '単価', '金額', '備考']
        data = [headers]

        # 明細行
        for item in self.data['明細']:
            amount = item['数量'] * item['単価']
            if item['値引種別'] == 'percentage':
                discount = amount * (item['値引額'] / 100)
                amount -= discount
                discount_note = f"{item['値引額']}%引"
            elif item['値引種別'] == 'amount':
                discount = item['値引額']
                amount -= discount
                discount_note = f"¥{discount:,}引"
            else:
                discount_note = ''

            data.append([
                str(item['項番']),
                item['品名'],
                f"{item['数量']:,}",
                item['単位'],
                self._format_currency(item['単価']),
                self._format_currency(amount),
                discount_note
            ])

        # 合計行
        totals = self.data['金額集計']
        data.extend([
            ['', '小計', '', '', '', self._format_currency(totals['小計']), ''],
            ['', '値引', '', '', '', f"-{self._format_currency(totals['値引合計'])}", ''],
            ['', '消費税', '', '', '', self._format_currency(totals['消費税合計']), ''],
            ['', '合計', '', '', '', self._format_currency(totals['合計金額']), '']
        ])

        # テーブルスタイル
        table = Table(data, colWidths=[20*mm, 70*mm, 25*mm, 20*mm, 30*mm, 30*mm, 30*mm])
        style = TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Arial'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (2, 1), (6, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -2), 1, colors.black),
            ('BOX', (0, -1), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('SPAN', (1, -1), (4, -1)),
        ])
        table.setStyle(style)
        return table

    def _create_footer(self):
        estimate = self.data['見積書']
        elements = []
        
        elements.append(Spacer(1, 10*mm))
        elements.append(Paragraph("【備考】", self.styles['Japanese']))
        elements.append(Paragraph(estimate['備考'], self.styles['Japanese']))
        elements.append(Spacer(1, 5*mm))
        elements.append(Paragraph("【お支払条件】", self.styles['Japanese']))
        elements.append(Paragraph(estimate['支払条件'], self.styles['Japanese']))
        elements.append(Spacer(1, 5*mm))
        elements.append(Paragraph("【納品条件】", self.styles['Japanese']))
        elements.append(Paragraph(estimate['納品条件'], self.styles['Japanese']))

        return elements

    def export(self):
        elements = []
        elements.extend(self._create_header())
        elements.append(self._create_items_table())
        elements.extend(self._create_footer())
        self.doc.build(elements)

def main():
    parser = argparse.ArgumentParser(description='Export estimate YAML to PDF')
    parser.add_argument('yaml_file', help='Input YAML file path')
    parser.add_argument('--output', '-o', help='Output PDF file path')
    args = parser.parse_args()

    if not args.output:
        base_name = os.path.splitext(args.yaml_file)[0]
        args.output = f"{base_name}.pdf"

    exporter = EstimatePDFExporter(args.yaml_file, args.output)
    exporter.export()
    print(f"PDF exported to: {args.output}")

if __name__ == '__main__':
    main()
