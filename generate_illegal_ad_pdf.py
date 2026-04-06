import fitz  # PyMuPDF

def generate_illegal_ad_pdf(filename="illegal_ad_test.pdf"):
    doc = fitz.open()
    page = doc.new_page()
    
    # 模拟一个非常不合规的视觉布局
    # 1. 夸大标题
    page.insert_text((50, 100), "GUARANTEED 30% ANNUAL RETURN!", fontsize=24, color=(1, 0, 0))
    
    # 2. 诱导性正文
    body = (
        "Forget about low-interest bank accounts. Our AI trading bot "
        "never loses money. This is a risk-free investment opportunity "
        "only available for the next 2 hours."
    )
    page.insert_textbox((50, 150, 500, 250), body, fontsize=14)
    
    # 3. 故意缩小的风险提示
    disclaimer = "Risk: None. Principal is 100% protected by our internal insurance."
    page.insert_text((50, 800), disclaimer, fontsize=4, color=(0.8, 0.8, 0.8))
    
    doc.save(filename)
    doc.close()
    print(f"✅ 已生成违规广告测试文件: {filename}")

# 生成文件
generate_illegal_ad_pdf()