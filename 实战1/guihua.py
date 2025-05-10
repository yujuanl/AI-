import streamlit as st
from openai import OpenAI  # pip install openai -i 清华源
import os
from dotenv import load_dotenv  # pip install python-dotenv
load_dotenv()     # 加载环境变量 OPENAI_API_KEY  OPENAI_BASE_URL
client = OpenAI()
from docx import Document


# 设置页面标题
st.title("大模型学习问卷")

# Q1
city = st.text_input("Q1: 您现在在哪个城市, 是否在职, 所从事的工作是什么?")

# Q2
knowledge_level = st.text_area("Q2: 对大模型有多少认知, 了解多少原理与技术点?")

# Q3
core_needs = st.text_area("Q3: 学习大模型的最核心需求是什么?")

# Q4
programming_background = st.text_input("Q4: 是否有python编程基础或者其他编程基础, 有没有写过代码?")

# Q5
study_time = st.text_input("Q5: 每天能花多少时间用于学习, 大致空闲时间点处于什么时段?")

# Q6
additional_questions = st.text_area("Q6: 除以上五点外是否还有其他问题想要补充。如有请按照如下格式进行补充.")

def get_completion(user_input, model="qwen-plus"):
    instruction = "你是一位专业的大模型辅导老师,根据学员提供的信息为学员提供个性化的学习方案,帮助他们更好地掌握大模型知识和技能.以下是学员提供的信息:"
    examples = """
    示例1
        Q:您现在在那个城市,是否在职,所从事的工作是什么?
        A:刚刚高中毕业,现在在湖南长沙,29号去大学,在桂林,目前是个准大学生
        Q:对大模型有多少认知,了解多少原理与技术点?
        A:一张白纸
        Q:学习大模型的最核心需求是什么?
        A:大学期间想利用AI赚钱,实现大学经济独立,大学期间想多实习,学习AI可以增大核心竞争力,本科毕业想直接工作,我认为当下了解AI是必须的。
        Q:是否有python编程基础或者其他编程基础,有没有写过代码?
        A:没有
        Q:每天能花多少时间用于学习,大致空闲时间点处于什么时段?
        A:两小时,应该会在晚上,这个还不太确定,要军训,大学的具体时间安排我还不太清楚
        Q:除以上五点外是否还有其他问题想要补充。如有请按照如下格式进行补充
        
        给学员的回复是
        大模型主要的语言是 Python,这门语言本身也非常简单,班主任发你的预习视频,你可以
        快速过一遍,里面有 Python 基础语法的讲解,预习视频还有一部分大模型的视频,也可以
        提前了解一下,你现在对大模型还没有一个基本的认知,可以在国内的知乎 csdn 等平台继
        续了解有关大模型的知识,主要看一些科普类的文章,你的学习时间比较充裕,前面可以多
        花点时间入门,只要入门了后面的学习就会容易很多,大模型的前景发展还是非常好的,现
        在国内大模型的发展处于刚起步阶段,还是有很多机会的,希望你能在这里学有所成。

    示例2
        Q:您现在在那个城市,是否在职,所从事的工作是什么?
        A:北京,在职,农业相关
        Q:对大模型有多少认知,了解多少原理与技术点?
        A:比较浅薄
        Q:学习大模型的最核心需求是什么?
        A:个人能力提升和业务需要
        Q:是否有python编程基础或者其他编程基础,有没有写过代码?
        A:有
        Q:每天能花多少时间用于学习,大致空闲时间点处于什么时段?
        A:3个小时左右,晚上18点以后
        Q:除以上五点外是否还有其他问题想要补充。如有请按照如下格式进行补充

        给学员的回复是
        作为在北京从事农业相关工作的同学,虽然你对大模型的认知程度比较浅,但你
        拥有 Python 编程基础并且写过代码,这对于学习大模型来说是很好的条件,因
        为 Python 是学习大模型的主要语言。推荐你看一下我们提供的预习课程来补充
        一下知识体系。个人能力提升和业务需要符合当前 AI 在农业领域的发展趋势。
        每天在晚上 18 点以后可以安排约 3 个小时的学习时间,这样的时间安排非常充
        裕。凭借你的编程背景和学习投入,转型为 AI 项目管理是可行的,国内现在 AI
        领域虽然处于起步阶段,但随着人工智能技术的快速发展,其应用前景非常广阔,
        现在正是学习并把握行业发展机遇的好时机
    """

    prompt = f"""
        {instruction}
    
        {examples}
    
        用户输入：
        {user_input}
        限制:
            - 只提供与大模型学习相关的建议,拒绝回答与大模型无关的问题。
            - 建议内容要具体、可行,具有针对性和可操作性。
            - 回答的时候不用加,给学员的回复是,也不用把问题重复输出,第一句不要加,根据您提供的信息,直接给出回复。
        """
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message.content

def replace_text_in_docx(file_path, replacements, output_path):
    # 读取docx文件
    doc = Document(file_path)

    # 遍历文档中的每一个段落
    for paragraph in doc.paragraphs:
        for old_text, new_text in replacements.items():
            if old_text in paragraph.text:
                # 替换文本
                paragraph.text = paragraph.text.replace(old_text, new_text)

    # 保存修改后的文档
    doc.save(output_path)

# 生成按钮
if st.button("生成"):
    # 在这里将用户输入发送给大模型
    user_input = {
        "Q1: 您现在在哪个城市, 是否在职, 所从事的工作是什么?": city,
        "Q2: 对大模型有多少认知, 了解多少原理与技术点?": knowledge_level,
        "Q3: 学习大模型的最核心需求是什么?": core_needs,
        "Q4: 是否有python编程基础或者其他编程基础, 有没有写过代码?": programming_background,
        "Q5: 每天能花多少时间用于学习, 大致空闲时间点处于什么时段?": study_time,
        "Q6: 除以上五点外是否还有其他问题想要补充。如有请按照如下格式进行补充.": additional_questions,
    }

    # 将用户输入显示在屏幕上（或者在这里可以将数据发送到你的大模型处理）
    # st.write("您输入的信息如下:")
    print(user_input)
    # st.json(user_input)

    # 在这里，您可以添加代码来发送 `user_input` 到大模型
    # send_to_model(user_input)  # 伪代码，替换成实际的发送逻辑
    model_response = get_completion(user_input)
    # 使用示例
    if __name__ == "__main__":
        # 要读取的文件路径
        file_path = '学习规划.docx'
        # 替换的字典，键为要替换的文本，值为替换后的文本
        replacements = {
            '[]': model_response,
        }
        # 输出文件路径
        output_path = '学习规划.docx'

    replace_text_in_docx(file_path, replacements, output_path)
    # print("大模型的回复:",model_response)
    # st.write(model_response)
    # 使用示例
    st.success(model_response)
    with open(output_path, "rb") as file:
        btn = st.download_button(
            label="下载学习规划文档",
            data=file,
            file_name="学习规划.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )




