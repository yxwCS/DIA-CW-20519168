import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

# 加载数据并预处理
data = pd.read_excel(r'C:\Users\takeoff\Desktop\chat_dataset.xlsx')
data = data.drop('response_id', axis=1)  # drop 'response_id'

# X = data['content']
y = data['label']
print("Unique labels:", y.unique())

# BE AWARE OF THE DATA TYPE OF y !!!
label_map = {
    "query_cooking_time": 1,
    "query_recipe": 2,
    "query_ingredients": 3,
    "Not_Found": 0
}


def classify_request_test(user_input):
    user_input = user_input.lower()
    if "how long" in user_input:
        return 1
    elif "how to cook" in user_input:
        return 2
    elif "ingredient" in user_input:
        return 3
    else:
        return 0

# run the classifier on the test set
data['predicted_label'] = data['content'].apply(classify_request_test)

# 分割数据集
X_train, X_test, y_train, y_test = train_test_split(data['content'], data['label'], test_size=0.2, random_state=42)

# 运行分类器生成预测标签
y_pred = [classify_request_test(x) for x in X_test]


# 计算并打印分类报告
report = classification_report(y_test, y_pred)
print(report)

# 计算混淆矩阵
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()


# usecase
def test_classify_request_test():
    test_cases = [
        "What is the cooking time for kebab?",
        "How to cook kebab, Chef?",
        "What are the ingredients for chocolat?"
    ]
    for test_case in test_cases:
        print(f"Test input: {test_case} - Predicted label: {classify_request_test(test_case)}")


# test3
print("Test classify_request_test()")
test_classify_request_test()
