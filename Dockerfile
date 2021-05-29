FROM python:3.8.1
EXPOSE 5000
WORKDIR /opt/project
COPY requirements.txt ./
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . /opt/project
CMD python manage.py runserver