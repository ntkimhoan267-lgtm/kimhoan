#!/usr/bin/env bash
# Tải video từ Google Drive theo ID về một thư mục (bỏ qua file đã có).
#
#   bash scripts/drive_fetch.sh work/raw 1e2f-eybAJ98yY_nC80ugsKabIh9mtF7n:1793381895296.mp4 ...
#
# Mỗi tham số là ID hoặc ID:tên_file. ID lấy từ projects/<dự án>/catalog.md hoặc search_files của Drive.
# Công cụ Drive (download_file_content) chỉ tải được file < 10MB, nên dùng script này cho file lớn.
# Thư mục chứa file phải đang bật "Bất kỳ ai có đường liên kết – Người xem"; tải xong nhắc người dùng tắt.
# File riêng tư trả về trang đăng nhập HTML: script báo lỗi thay vì lưu file hỏng.
set -euo pipefail
out=${1:?cần thư mục đích}; shift
mkdir -p "$out"
for spec in "$@"; do
  id=${spec%%:*}; name=${spec#*:}; [ "$name" = "$spec" ] && name="$id.mp4"
  f="$out/$name"
  [ -s "$f" ] && { echo "đã có $f"; continue; }
  curl -sS -L --retry 4 -o "$f.part" "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
  if head -c 512 "$f.part" | grep -qi "<html"; then
    rm -f "$f.part"; echo "LỖI $id: file chưa bật chia sẻ bằng link (Drive trả trang đăng nhập)" >&2; continue
  fi
  mv "$f.part" "$f"; echo "-> $f"
done
