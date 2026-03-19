#!/usr/bin/env python3
"""
Daily Brief 生成脚本
自动生成全球政经科技日报
"""

import os
import re
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# 配置
TEMPLATE_FILE = "template.html"
OUTPUT_FILE = "index.html"
ARCHIVE_DIR = "archive"
ASSETS_DIR = "assets"

class DailyBriefGenerator:
    def __init__(self):
        self.date = datetime.now()
        self.date_str = self.date.strftime("%Y-%m-%d")
        self.display_date = self.date.strftime("%Y年%m月%d日 %A")
        self.edition_no = (self.date - datetime(2026, 3, 16)).days + 1
        
    def get_weather(self):
        """获取深圳天气（简化版）"""
        return "深圳 · 多云 · 22°C"
    
    def search_news(self, query, count=5):
        """搜索新闻"""
        try:
            # 使用 kimi_search 或 web_search
            # 这里用简单的模拟，实际部署时会调用搜索 API
            return []
        except:
            return []
    
    def generate_headlines(self):
        """生成头条摘要"""
        # 实际实现会调用搜索和 AI 生成
        return """
        <div class="headline-item">
            <h3>国际政治</h3>
            <h4>美俄会谈取得阶段性进展</h4>
            <p>双方在日内瓦进行了为期三天的闭门谈判，就乌克兰问题达成初步共识...</p>
        </div>
        <div class="headline-item">
            <h3>宏观经济</h3>
            <h4>美联储暗示年内或降息两次</h4>
            <p>最新会议纪要显示，多数委员支持在通胀回落背景下调整货币政策...</p>
        </div>
        <div class="headline-item">
            <h3>科技前沿</h3>
            <h4>OpenAI 发布 GPT-5 技术预览</h4>
            <p>新一代模型在多模态理解和推理能力上实现重大突破...</p>
        </div>
        """
    
    def generate_featured(self):
        """生成深度解读"""
        return """
        <h3>全球科技监管：从放任到收紧的转折点</h3>
        <p>过去十年，科技行业享受着近乎放任的监管环境。从硅谷的车库创业到万亿市值的科技巨头，"快速行动、打破陈规"（Move fast and break things）曾是行业的黄金法则。然而，这种自由正在迅速收窄。</p>
        <p>欧盟《数字市场法》的全面生效标志着一个时代的结束。这部被称为"史上最严"的科技监管法案，直接针对苹果、谷歌、Meta 等数字巨头，要求它们开放生态系统、允许用户卸载预装应用、禁止自我偏好。违规企业将面临全球营业额 10% 的罚款。</p>
        <p>美国方面，虽然联邦层面的统一立法进展缓慢，但各州纷纷出手。加州、纽约、德克萨斯等州针对数据隐私、算法透明度、儿童网络安全推出了一系列法案。FTC 主席莉娜·汗（Lina Khan）更是以激进的反垄断立场著称，亚马逊、Meta 相继遭遇重大诉讼。</p>
        <p>对于普通用户而言，这些变化意味着什么？短期内，可能会感受到服务体验的细微变化——更多的权限提示、更长的隐私政策、更繁琐的登录流程。但长期来看，一个更规范的数字生态或许能让技术创新回归到真正服务人类的轨道上，而非仅仅追求增长和变现。</p>
        """
    
    def generate_english(self):
        """生成英语角"""
        return """
        <div class="english-passage">
            <h4>精选段落</h4>
            <p class="source">Source: The Economist, March 2026</p>
            <p class="english-text">
                The era of unchecked technological expansion is drawing to a close. Regulators worldwide are moving from a posture of benign neglect to one of active oversight, driven by mounting concerns over market concentration, data privacy, and the societal impact of artificial intelligence.
            </p>
            <div class="annotation">
                <h5>词汇注解</h5>
                <ul>
                    <li><span class="word">unchecked</span> <span class="explain">/ˌʌnˈtʃekt/ adj. 未受约束的，无节制的</span></li>
                    <li><span class="word">expansion</span> <span class="explain">/ɪkˈspænʃn/ n. 扩张，扩展</span></li>
                    <li><span class="word">drawing to a close</span> <span class="explain">习语：接近尾声，即将结束</span></li>
                    <li><span class="word">benign neglect</span> <span class="explain">放任政策，善意忽视（故意不干预）</span></li>
                    <li><span class="word">mounting concerns</span> <span class="explain">日益增长的担忧</span></li>
                </ul>
            </div>
        </div>
        """
    
    def generate_data(self):
        """生成数据速览"""
        return """
        <div class="data-item">
            <div class="label">上证指数</div>
            <div class="value">3,245.60</div>
            <div class="change up">+0.82%</div>
        </div>
        <div class="data-item">
            <div class="label">纳斯达克</div>
            <div class="value">18,432.15</div>
            <div class="change down">-0.34%</div>
        </div>
        <div class="data-item">
            <div class="label">美元兑人民币</div>
            <div class="value">7.2345</div>
            <div class="change down">-0.12%</div>
        </div>
        <div class="data-item">
            <div class="label">比特币</div>
            <div class="value">$68,420</div>
            <div class="change up">+2.15%</div>
        </div>
        """
    
    def generate(self):
        """生成日报"""
        # 读取模板
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # 替换变量
        content = template.replace('{{DATE}}', self.display_date)
        content = content.replace('{{EDITION_NO}}', str(self.edition_no))
        content = content.replace('{{WEATHER}}', self.get_weather())
        content = content.replace('{{HEADLINES}}', self.generate_headlines())
        content = content.replace('{{FEATURED}}', self.generate_featured())
        content = content.replace('{{ENGLISH}}', self.generate_english())
        content = content.replace('{{DATA}}', self.generate_data())
        
        # 确保目录存在
        Path(ARCHIVE_DIR).mkdir(exist_ok=True)
        
        # 保存到首页
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 保存到归档
        archive_file = Path(ARCHIVE_DIR) / f"{self.date_str}.html"
        with open(archive_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 更新归档索引
        self.update_archive_index()
        
        print(f"✅ Generated: {OUTPUT_FILE}")
        print(f"✅ Archived: {archive_file}")
    
    def update_archive_index(self):
        """更新归档索引页面"""
        archive_files = sorted(Path(ARCHIVE_DIR).glob("*.html"), reverse=True)
        
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Brief - 历史归档</title>
    <link rel="stylesheet" href="../assets/style.css">
    <style>
        .archive-list { max-width: 600px; margin: 40px auto; }
        .archive-item { 
            display: flex; 
            justify-content: space-between;
            padding: 15px;
            border-bottom: 1px solid #ddd;
        }
        .archive-item:hover { background: #f5f5f0; }
        .archive-item a { color: #8b0000; text-decoration: none; }
    </style>
</head>
<body>
    <div class="newspaper">
        <header class="masthead">
            <h1 class="title" style="font-size: 2rem;">ARCHIVE</h1>
            <p class="subtitle">历史归档 · Past Issues</p>
        </header>
        
        <div class="archive-list">
"""
        
        for file in archive_files:
            date_str = file.stem
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                display = date_obj.strftime("%Y年%m月%d日")
            except:
                display = date_str
            
            html += f'            <div class="archive-item"><a href="{file.name}">{display}</a><span>第{(date_obj - datetime(2026, 3, 16)).days + 1}期</span></div>\n'
        
        html += """        </div>
        
        <footer class="footer">
            <p><a href="../">← 返回今日简报</a></p>
        </footer>
    </div>
</body>
</html>
"""
        
        with open(Path(ARCHIVE_DIR) / "index.html", 'w', encoding='utf-8') as f:
            f.write(html)

if __name__ == "__main__":
    generator = DailyBriefGenerator()
    generator.generate()
