import os
from natsort import natsorted

def rename_images_in_folders():
    # 현재 디렉토리 기준으로 폴더 내 이미지 이름을 0000000000 부터 시작하도록 변경
    for folder in natsorted(os.listdir()):
        if os.path.isdir(folder):  # 폴더인 경우
            # 해당 폴더 안의 이미지 파일 탐색 및 정렬
            images = natsorted(os.listdir(folder))
            for idx, image_name in enumerate(images):
                if image_name.endswith(('.png', '.jpg', '.jpeg')):  # 이미지 파일인 경우
                    # 확장자 추출
                    ext = os.path.splitext(image_name)[1]
                    # 새로운 이미지 이름 생성
                    new_image_name = f"{str(idx).zfill(10)}{ext}"
                    # 파일 경로 생성
                    old_image_path = os.path.join(folder, image_name)
                    new_image_path = os.path.join(folder, new_image_name)
                    # 파일 이름 변경
                    os.rename(old_image_path, new_image_path)
                    print(f"Renamed: {old_image_path} -> {new_image_path}")

# 실행
rename_images_in_folders()
