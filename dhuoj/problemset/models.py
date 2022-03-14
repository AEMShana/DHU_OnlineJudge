from django.db import models


class Problem(models.Model):
    problemID = models.CharField(max_length=30)  # 题目编号
    title = models.CharField(max_length=100)    # 题目名称
    problem_background = models.TextField()   # 题目背景
    problem_description = models.TextField()  # 题目描述
    problem_input = models.TextField()  # 输入
    problem_output = models.TextField()  # 输入
    problem_note = models.TextField()  # 提示
    time_limit = models.IntegerField()  # 时间限制
    memory_limit = models.IntegerField()  # 内存限制
    problem_difficulty = models.IntegerField()  # 题目难度
    problem_source = models.CharField(max_length=100)  # 题目来源

    def __str__(self):
        return self.problemID + ' ' + self.title


class ProblemExample(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_example = models.TextField()  # 输入样例
    output_example = models.TextField()  # 输出样例
