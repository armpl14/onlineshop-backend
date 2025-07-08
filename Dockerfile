FROM kalilinux/kali-rolling:latest
RUN apt update && apt install -y aircrack-ng
