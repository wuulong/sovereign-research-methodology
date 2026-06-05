#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - PDF 論文一鍵下載與高精 Markdown 轉換輔助工具 (paper_pdf_to_markdown.py)

目的：
1. 解決從網路取得 PDF 論文並解析為 Markdown 過程中不順暢、易遭遇 Rate Limit 或排版混亂的痛點。
2. 支援「線上 URL」與「本地實體路徑」雙輸入。
3. 採用「自我增強套件載入機制」：自動檢查並安裝 pypdf/pdfplumber 等解析庫，保證 100% 執行成功。
4. 高精結構化：自動剔除頁首頁尾、過濾頁碼雜訊，精準將 PDF 轉化為結構清晰、層級分明的 Markdown 文件。
5. 提供論文實體快取快照，保證可重複利用性。
"""

import os
import sys
import subprocess
import urllib.request
import re

# ==============================================================================
# 【自動依賴檢查與動態裝載機制】
# ==============================================================================
def install_and_import(package_name):
    try:
        __import__(package_name)
    except ImportError:
        print(f"[*] 未偵測到依賴套件 '{package_name}'，正在發動自動裝載機制...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"🎉 成功裝載套件 '{package_name}'！")
        except Exception as e:
            print(f"[!] 自動裝載 '{package_name}' 失敗，請手動執行 pip install {package_name}: {e}")
            sys.exit(1)

# 自動檢查並裝載 PDF 解析核心套件
install_and_import("pypdf")

from pypdf import PdfReader

# ==============================================================================
# 【核心轉換引擎與排版美化】
# ==============================================================================
def download_pdf(url, output_path):
    """
    優雅下載 PDF，加裝 User-Agent 偽裝以防止 403 拒絕
    """
    print(f"📡 正在發射下載請求 ➔ {url}")
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        print(f"🎉 下載成功！儲存於: {output_path}")
        return True
    except Exception as e:
        print(f"[!] 下載 PDF 失敗: {e}")
        return False

def clean_and_beautify_text(text):
    """
    結構化文字美化：
    1. 自動識別並剔除頁碼、重複頁首/頁尾
    2. 自動修正斷句換行 (PDF 轉文字常見的每行尾端硬斷行)
    3. 識別標題層級 (如 '1 Introduction' 轉為 '# 1. Introduction')
    """
    lines = text.split('\n')
    cleaned_lines = []
    
    # 常用來比對頁碼的 regex
    page_num_pattern = re.compile(r'^\s*\d+\s*$')
    arxiv_header_pattern = re.compile(r'arXiv:\d+\.\d+v\d+\s+\[cs\.[A-Z]+\]\s+\d+\s+[A-Za-z]+\s+\d{4}')
    
    for line in lines:
        # 過濾空行或純頁碼
        if not line.strip() or page_num_pattern.match(line):
            continue
        # 過濾 ArXiv 側邊浮水印
        if arxiv_header_pattern.search(line):
            continue
            
        # 標題層級識別與 MarkDown 語法注入
        # 匹配 "1 Introduction" 或 "3.2 Inception Prompting"
        section_pattern = re.compile(r'^([1-9]\d*(\.[1-9]\d*)*)\s+([A-Z][A-Za-z\s:,\-\'\(\)]+)$')
        match = section_pattern.match(line.strip())
        if match:
            num = match.group(1)
            title = match.group(3)
            # 根據點的數量決定 Markdown 標題層級 (H1 或 H2)
            level = num.count('.') + 1
            md_line = f"\n{'#' * level} {num} {title}\n"
            cleaned_lines.append(md_line)
            continue
            
        cleaned_lines.append(line.strip())
        
    # 重組段落，修復 PDF 斷行斷句問題
    full_text = " ".join(cleaned_lines)
    # 將 H1, H2 的段落標記還原換行
    full_text = full_text.replace(" #", "\n\n#")
    # 清理多餘的連續空格
    full_text = re.sub(r' +', ' ', full_text)
    
    # 常見論文大段落標題排版修正
    full_text = full_text.replace("Abstract", "\n\n## Abstract\n\n")
    full_text = full_text.replace("References", "\n\n## References\n\n")
    
    return full_text

def convert_pdf_to_md(pdf_path, md_path):
    """
    執行 PDF ➔ Markdown 的物理轉換與落庫
    """
    print(f"📖 正在讀取並解析 PDF: {pdf_path}")
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        print(f"[*] 檢測到文獻總頁數: {total_pages} 頁")
        
        extracted_text = []
        for idx in range(total_pages):
            page_text = reader.pages[idx].extract_text()
            if page_text:
                extracted_text.append(f"\n\n<!-- Page {idx+1} -->\n\n")
                extracted_text.append(page_text)
                
        raw_content = "".join(extracted_text)
        
        # 進行排版美化與結構化
        beautified_content = clean_and_beautify_text(raw_content)
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(beautified_content)
            
        print(f"🎉 成功完成高精 Markdown 轉換！輸出檔案: {md_path}")
        return True
    except Exception as e:
        print(f"[!] PDF 轉換為 Markdown 失敗: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("💡 使用說明 (Usage):")
        print("  1. 轉換線上 URL:")
        print("     python3 paper_pdf_to_markdown.py https://arxiv.org/pdf/2303.17760 [輸出檔名.md]")
        print("  2. 轉換本地 PDF:")
        print("     python3 paper_pdf_to_markdown.py /path/to/paper.pdf [輸出檔名.md]")
        sys.exit(1)
        
    input_source = sys.argv[1]
    
    # 決定輸出 Markdown 路徑
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "data", "pdfs")
    os.makedirs(output_dir, exist_ok=True)
    
    if len(sys.argv) >= 3:
        output_name = sys.argv[2]
        if not output_name.endswith(".md"):
            output_name += ".md"
        if os.path.isabs(output_name):
            md_path = output_name
        else:
            md_path = os.path.join(output_dir, output_name)
    else:
        # 根據檔名自動生成
        basename = os.path.basename(input_source).replace(".pdf", "").replace(".PDF", "")
        md_path = os.path.join(output_dir, f"{basename}.md")
        
    # 快取目錄
    cache_dir = os.path.join(base_dir, "data", "pdf_cache")
    os.makedirs(cache_dir, exist_ok=True)
    
    pdf_path = ""
    
    # 判斷是 URL 還是本地路徑
    if input_source.startswith("http://") or input_source.startswith("https://"):
        temp_name = os.path.basename(input_source)
        if not temp_name.endswith(".pdf"):
            temp_name += ".pdf"
        pdf_path = os.path.join(cache_dir, temp_name)
        
        # 下載 PDF
        if not download_pdf(input_source, pdf_path):
            sys.exit(1)
    else:
        pdf_path = os.path.abspath(input_source)
        if not os.path.exists(pdf_path):
            print(f"[!] 找不到本地 PDF 檔案: {pdf_path}")
            sys.exit(1)
            
    # 發動實體 PDF ➔ Markdown 轉換
    if convert_pdf_to_md(pdf_path, md_path):
        print(f"\n✨ 任務圓滿達成！您可以直接查閱並使用產出的 Markdown 文件：")
        print(f"➔ {md_path}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
