# -*- coding: utf-8 -*-
import os
import PyPDF2  # 需要建立在安装pip install PyPDF2
# 在搜素下知道，要写这方面的文件资料，需要下载这个。

def organize_papers(directory): #异常处理和文件IO的实作
  
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            try:
                with open(os.path.join(directory, filename), 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    # 获取PDF元数据中的标题
                    title = reader.metadata.get('/Title', 'Unknown_Title')
                    # 清理非法字符并重命名
                    safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).strip()
                    new_name = f"{safe_title}.pdf"
                    
                    print(f"Renaming: {filename} -> {new_name}")
                    # 实际操作时取消注释：os.rename(...)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# 调用示例
# organize_papers("./my_unorganized_papers")
