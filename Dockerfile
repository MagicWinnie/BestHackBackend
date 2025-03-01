FROM python:3.13-alpine3.21

WORKDIR /app

COPY certs/ certs/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

RUN addgroup --system user && \
    adduser --system --ingroup user user && \
    chown -R user:user /app
USER user

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]