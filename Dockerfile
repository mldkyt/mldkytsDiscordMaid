FROM python:3.11-alpine
WORKDIR /bot
RUN pip install py-cord
RUN pip install requests
COPY . .
ENTRYPOINT [ "python3", "main.py" ]
