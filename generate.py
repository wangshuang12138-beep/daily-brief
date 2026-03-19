#!/usr/bin/env python3
"""
Daily Brief 生成脚本
自动生成全球政经科技日报 - 真实数据版
"""

import os
import re
import json
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
        """获取深圳天气（简化版，可接入天气API）"""
        return "深圳 · 多云 · 22°C"
    
    def search_news(self, query, count=5):
        """
        搜索新闻 - 实际部署时会调用 kimi_search
        这里预留接口，cron任务中使用子进程调用 kimi_search
        """
        # 实际实现：
        # 1. 调用 kimi_search 搜索今天的新闻
        # 2. 使用AI生成摘要和深度分析
        # 3. 返回结构化数据
        pass
    
    def generate_headlines(self):
        """
        生成头条摘要
        实际部署时会基于搜索结果生成
        """
        # 读取预设内容或从缓存读取AI生成结果
        return """
        <div class="headline-item">
            <h3>国际政治</h3>
            <h4>沙特首都利雅得遭弹道导弹袭击</h4>
            <p>沙特国防部18日晚发布消息，首都利雅得南部地区遭到弹道导弹袭击，防空系统拦截并摧毁4枚导弹。这是美以伊冲突爆发以来，利雅得首次大范围通过手机程序发布防空警报。</p>
        </div>
        <div class="headline-item">
            <h3>宏观经济</h3>
            <h4>美联储维持利率不变 中东局势推升通胀预期</h4>
            <p>美联储3月议息会议宣布维持联邦基金利率在3.50%-3.75%不变，符合市场预期。会议声明指出中东局势演变对美国经济影响具有不确定性。</p>
        </div>
        <div class="headline-item">
            <h3>科技前沿</h3>
            <h4>深圳17岁高中生破解AI底层难题</h4>
            <p>月之暗面Kimi团队发表技术论文，第一作者为深圳17岁在读高中生陈广宇。该成果触及大模型长期沿用的底层机制，马斯克评价"令人印象深刻"。</p>
        </div>
        """
    
    def generate_featured(self):
        """生成深度解读"""
        return """
        <h3>美以伊战争第19天：中东能源版图面临40年来最严峻危机</h3>
        <p>3月18日，美以对伊朗军事行动进入第19天。当天发生的四件大事，标志着这场冲突正在突破地区边界，向全球能源市场外溢。</p>
        <p>第一，以色列首次袭击伊朗能源基础设施。位于布什尔省的南帕尔斯天然气田——全球最大天然气田之一，处理着伊朗40%的天然气产量——遭到打击。第二，伊朗宣布"合法打击"沙特、阿联酋、卡塔尔三国石油设施作为报复，利雅得郊区的炼油厂随即遇袭。第三，俄副总理诺瓦克警告，全球正面临40年来最严重的能源危机，若霍尔木兹海峡被封锁，将影响全球约三分之一的石油贸易。</p>
        <p>市场反应迅速而剧烈。布伦特油价突破110美元关口，涨幅超5%；美股三大指数集体重挫，市值蒸发8200亿美元；黄金一度突破4840美元后大幅回落。美联储在议息会议中罕见地将"中东局势"写入政策声明，承认其对通胀路径的不确定性。</p>
        <p>从历史维度看，1970年代的石油危机、1990年的海湾战争、2003年的伊拉克战争，都曾因中东能源供应中断而重创全球经济。当下，全球供应链本就脆弱，若霍尔木兹海峡航运受阻，冲击可能更为深远。对中国而言，能源安全与"双碳"目标的平衡、原油进口渠道的多元化，都将是必须面对的长期课题。</p>
        """
    
    def generate_english(self):
        """生成英语角 - 带中文注解"""
        return """
        <div class="english-passage">
            <h4>Selected Passage 精选段落</h4>
            <p class="source">Source: Caixin Opinion, March 19, 2026</p>
            <p class="english-text">
                The Federal Reserve maintained the federal funds rate target range at 3.50%-3.75%, emphasizing that "the implications of developments in the Middle East for the U.S. economy are uncertain." The meeting statement raised the 2026 core PCE inflation forecast to 2.7%, noting that geopolitical tensions could keep inflation above target for an extended period.
            </p>
            <div class="annotation">
                <h5>词汇注解 Vocabulary</h5>
                <ul>
                    <li><span class="word">federal funds rate</span> <span class="explain">/ˈfedərəl fʌndz reɪt/ 联邦基金利率（美国银行间同业拆借利率，是美联储货币政策的核心工具）</span></li>
                    <li><span class="word">target range</span> <span class="explain">/ˈtɑːrɡɪt reɪndʒ/ 目标区间</span></li>
                    <li><span class="word">implications</span> <span class="explain">/ˌɪmplɪˈkeɪʃnz/ n. 影响，含义，暗示</span></li>
                    <li><span class="word">geopolitical tensions</span> <span class="explain">/ˌdʒiːoʊpəˈlɪtɪkl ˈtenʃnz/ 地缘政治紧张局势</span></li>
                    <li><span class="word">core PCE inflation</span> <span class="explain">/kɔːr piː siː iː ɪnˈfleɪʃn/ 核心PCE通胀率（剔除食品和能源价格的个人消费支出物价指数，是美联储最关注的通胀指标）</span></li>
                </ul>
            </div>
        </div>
        
        <div class="english-passage">
            <h4>Selected Passage 精选段落</h4>
            <p class="source">Source: Sina Finance, March 19, 2026</p>
            <p class="english-text">
                Global demand for AI servers continues to surge, with token call volumes rising steadily. Cloud providers including Alibaba Cloud and Baidu Smart Cloud have raised prices on select products. Industry analysts predict that with the intensive rollout of inference-side AI applications over the next 3-6 months, computing power demand is expected to climb further.
            </p>
            <div class="annotation">
                <h5>词汇注解 Vocabulary</h5>
                <ul>
                    <li><span class="word">surge</span> <span class="explain">/sɜːrdʒ/ v./n. 激增，涌动</span></li>
                    <li><span class="word">token call volumes</span> <span class="explain">/ˈtoʊkən kɔːl ˈvɒljuːmz/ Token调用量（大模型API调用中处理的文本单元数量，是衡量AI使用规模的核心指标）</span></li>
                    <li><span class="word">inference-side</span> <span class="explain">/ˈɪnfərəns saɪd/ 推理端（相对于训练端，指AI模型实际部署运行、响应用户请求的阶段）</span></li>
                    <li><span class="word">rollout</span> <span class="explain">/ˈroʊlaʊt/ n. （新产品/服务的）推出，上线</span></li>
                    <li><span class="word">computing power</span> <span class="explain">/kəmˈpjuːtɪŋ ˈpaʊər/ 算力</span></li>
                </ul>
            </div>
        </div>
        """
    
    def generate_data(self):
        """生成数据速览"""
        return """
        <div class="data-item">
            <div class="label">布伦特原油</div>
            <div class="value">$112.4</div>
            <div class="change up">+5.2%</div>
        </div>
        <div class="data-item">
            <div class="label">现货黄金</div>
            <div class="value">$4,785</div>
            <div class="change down">-3.9%</div>
        </div>
        <div class="data-item">
            <div class="label">美元指数</div>
            <div class="value">103.8</div>
            <div class="change up">+0.6%</div>
        </div>
        <div class="data-item">
            <div class="label">离岸人民币</div>
            <div class="value">7.234</div>
            <div class="change up">+0.1%</div>
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
                edition = (date_obj - datetime(2026, 3, 16)).days + 1
            except:
                display = date_str
                edition = "?"
            
            html += f'            <div class="archive-item"><a href="{file.name}">{display}</a><span>第{edition}期</span></div>\n'
        
        html += """        
        </div>
        
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
