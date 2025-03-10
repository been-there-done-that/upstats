FROM rust:latest AS builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bullseye-slim
WORKDIR /app
COPY --from=builder /app/target/release/pingora-proxy /usr/local/bin/
CMD ["/usr/local/bin/pingora-proxy"]
