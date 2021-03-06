# 导入库
import urllib.request
import bs4
from bs4 import BeautifulSoup


def get_cf_problem_detail(problemSet, problemId):

    try:
        # 题目链接
        url = f"https://codeforces.com/problemset/problem/{problemSet}/{problemId}"
        # 获取网页内容
        html = urllib.request.urlopen(url).read()
        # 格式化
        soup = BeautifulSoup(html, 'lxml')

        # 存储
        data_dict = {}
        # 找到主体内容
    except Exception:
        return None
    try:
        mainContent = soup.find_all(
            name="div", attrs={"class": "problem-statement"})[0]
        sideBox = soup.find_all(
            name="div", attrs={"class": "roundbox sidebox"})[0]

        # Limit
        # 找到题目标题、时间、和内存限制
        # Title
        data_dict['Title'] = f"CodeForces {problemSet} " + mainContent.find_all(
            name="div", attrs={"class": "title"})[0].contents[-1]
        data_dict['Title'] = data_dict['Title'].split('.')[1].strip()

        # Time Limit
        data_dict['Time Limit'] = mainContent.find_all(
            name="div", attrs={"class": "time-limit"})[0].contents[-1]
        # Memory Limit
        data_dict['Memory Limit'] = mainContent.find_all(
            name="div", attrs={"class": "memory-limit"})[0].contents[-1]

        temp = soup.find_all(
            name="span", attrs={"class": "tag-box", "title": "Difficulty"})
        if len(temp) == 0:
            data_dict["difficulty"] = 0
        else:
            data_dict['difficulty'] = temp[0]
            data_dict['difficulty'] = data_dict["difficulty"].contents[0].strip()[
                1:]

    except Exception:
        return None

    def divTextProcess(div):
        """
        处理<div>标签中<p>的文本内容
        """
        strBuffer = ''
        # 遍历处理每个<p>标签

        templi = div.find_all(["li"])

        for each in div.find_all(["p", "li"]):
            flag = False
            if each in templi:
                flag = True
            for content in each.contents:
                # 如果不是第一个，加换行符
                if (strBuffer != ''):
                    strBuffer += '\n\n'

                textBuffer = ''

                # 处理
                if (type(content) != bs4.element.Tag):
                    # 如果是文本，添加至字符串buffer中
                    textBuffer += content.replace("       ",
                                                  " ").replace("$$$", "$")
                else:
                    # 如果是html元素，如span等，加上粗体
                    textBuffer += "**" + \
                        content.contents[0].replace(
                            "       ", " ").replace("$$$", "$") + "**"
                if flag == True and textBuffer.startswith(' '):
                    strBuffer += '-'
                strBuffer += textBuffer
        # 返回结果
        strBuffer.replace("\n**", "**")
        return strBuffer

    try:
        # 处理题目描述
        data_dict['Problem Description'] = divTextProcess(
            mainContent.find_all("div")[10])

        # 处理输入描述
        div = mainContent.find_all(
            name="div", attrs={"class": "input-specification"})[0]
        data_dict['Input'] = divTextProcess(div)

        # 处理输出描述
        div = mainContent.find_all(
            name="div", attrs={"class": "output-specification"})[0]
        data_dict['Output'] = divTextProcess(div)

        # Input Example
        divInput = mainContent.find_all(name="div", attrs={"class": "input"})
        divOutput = mainContent.find_all(name="div", attrs={"class": "output"})

        sample_list = []
        for i in range(min(len(divInput), len(divOutput))):
            divIn = divInput[i]
            divOut = divOutput[i]
            tempTuple = ("```" + divIn.find_all("pre")[0].contents[0] + '```',
                         "```" + divOut.find_all("pre")[0].contents[0] + '```')
            tempTuple = (tempTuple[0].replace(
                '```\n\n', '```\n'), tempTuple[1].replace('```\n\n', '```\n'))
            sample_list.append(tempTuple)

        data_dict['Example'] = sample_list

        # 若有样例说明
        if(len(mainContent.find_all(name="div", attrs={"class": "note"})) > 0):
            div = mainContent.find_all(name="div", attrs={"class": "note"})[0]
            data_dict['Note'] = divTextProcess(div)

        # 题目链接
        data_dict['Source'] = '[' + data_dict['Title'] + ']' + '(' + url + ')'
    except Exception:
        return None

    for each in data_dict.keys():
        if type(data_dict[each]) is not str:
            pass
        else:
            data_dict[each] = data_dict[each].replace(
                "\n\n**", "**").replace("**\n\n", "**")

    return data_dict


if __name__ == '__main__':
    data_dict = get_cf_problem_detail('1648', 'B')

    for each in data_dict.keys():
        print('### ' + each + '\n')
        print(data_dict[each])

    # for each in data_dict.keys():
    #     print('### ' + each + '\n')
    #     if type(data_dict[each]) is list:
    #         print(data_dict[each])
    #     else:
    #         print(data_dict[each].replace(
    #             "\n\n**", "**").replace("**\n\n", "**") + '\n')
