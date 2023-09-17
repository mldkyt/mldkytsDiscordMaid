FROM python:3
WORKDIR /bot
RUN pip install py-cord
RUN pip install requests
COPY . .
CMD ["python", "main.py"]