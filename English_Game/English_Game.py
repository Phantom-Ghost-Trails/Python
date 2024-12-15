import tkinter as tk
import pandas as pd
import random
from fuzzywuzzy import process

# 读取单词数据
file_path = 'D:\\冯文喜\\家用\\代码\\Python\\.vs\\English_Game\\words.csv'
words_df = pd.read_csv(file_path)
words_list = words_df.to_dict(orient='records')

# 初始化变量
current_word_index = 0
score = 0
correct_answers_needed = 20
similarity_threshold = 80  # 设置相似度阈值

def show_next_word():
    global current_word_index
    if current_word_index < len(words_list):
        word = words_list[current_word_index]['word']
        translation_entry.delete(0, tk.END)
        label.config(text=f"单词: {word}")
    else:
        label.config(text="所有单词已复习完毕！")
        check_button.config(state=tk.DISABLED)

def check_answer():
    global current_word_index, score
    user_translation = translation_entry.get().strip()
    correct_translation = words_list[current_word_index]['translation']
    
    # 使用 fuzzywuzzy 进行模糊匹配
    match, similarity = process.extractOne(user_translation, [correct_translation])
    
    if similarity >= similarity_threshold:
        feedback_label.config(text="正确！", fg="green")
        score += 1
        current_word_index += 1
        
        if score >= correct_answers_needed:
            label.config(text="恭喜！你已经答对了20个单词！")
            check_button.config(state=tk.DISABLED)
            return
    else:
        feedback_label.config(text=f"错误。正确答案是: {correct_translation}", fg="red")
        current_word_index += 1
    
    score_label.config(text=f"得分: {score}/{20}")
    show_next_word()

# 创建主窗口
root = tk.Tk()
root.title("英语单词复习工具")

# 创建标签
label = tk.Label(root, text="", font=("Arial", 14))
label.pack(pady=10)

# 创建输入框
translation_entry = tk.Entry(root, font=("Arial", 12))
translation_entry.pack(pady=10)

# 创建检查按钮
check_button = tk.Button(root, text="检查答案", command=check_answer, font=("Arial", 12))
check_button.pack(pady=10)

# 创建反馈标签
feedback_label = tk.Label(root, text="", font=("Arial", 12))
feedback_label.pack(pady=10)

# 创建分数标签
score_label = tk.Label(root, text=f"得分: {score}/{20}", font=("Arial", 12))
score_label.pack(pady=10)

# 显示第一个单词
show_next_word()

# 启动主循环
root.mainloop()
