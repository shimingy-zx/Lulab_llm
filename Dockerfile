# 使用一个基础的Python镜像
FROM python:3.11.1

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到镜像的/app目录
COPY . /app

# 安装所需的依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 运行Django服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
