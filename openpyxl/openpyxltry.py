import openpyxl
from openpyxl.styles import Font, Border, Side, PatternFill

# 创建一个新的工作簿
wb = openpyxl.Workbook()

# 获取活动的工作表
ws = wb.active

# 设置工作表的标题
ws.title = "99乘法表"

# 设置工作表标签的颜色
ws.sheet_properties.tabColor = "f05654"

# 定义行的颜色
row_color = ["f05654", "ff2121", "dc3023", "ff3300", "cb3a56", "a98175", "b36d61", "ef7a82", "ff0097"]

# 写入数据并设置样式
for row in range(1, 10):
    for column in range(1, row + 1):
        # 计算单元格值
        cell_value = f"{column}×{row}={column * row}"
        
        # 获取单元格
        cell = ws.cell(row=row, column=column)
        
        # 设置单元格值
        cell.value = cell_value
        
        # 设置字体样式
        font_set = Font(name='Arial', size=14, italic=True, color='000000', bold=True)
        cell.font = font_set
        
        # 设置边框
        border = Border(
            top=Side(border_style="thin", color="FF000000"),
            bottom=Side(border_style="thin", color="FF000000"),
            left=Side(border_style="thin", color="FF000000"),
            right=Side(border_style="thin", color="FF000000")
        )
        cell.border = border
        
        # 设置填充颜色
        fill = PatternFill("solid", fgColor=row_color[row - 1])
        cell.fill = fill

# 保存工作簿
wb.save("九九乘法表.xlsx")
