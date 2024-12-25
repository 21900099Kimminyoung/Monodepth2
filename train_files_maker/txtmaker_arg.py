import os
from natsort import natsorted
import argparse

def save_folder_image_info_to_txt(input_dir, output_txt_path):
    # 지정된 디렉토리의 폴더와 이미지 이름 저장
    with open(output_txt_path, 'w') as file:
        # 지정된 디렉토리의 모든 폴더 탐색
        for folder in natsorted(os.listdir(input_dir)):
            folder_path = os.path.join(input_dir, folder)
            if os.path.isdir(folder_path):  # 폴더인 경우
                # 해당 폴더 안의 이미지 파일 탐색 및 정렬
                image_files = natsorted([img for img in os.listdir(folder_path) if img.endswith(('.png', '.jpg', '.jpeg'))])
                
                # 이미지가 2개 이상일 때만 첫 번째와 마지막 파일을 제외하고 처리
                if len(image_files) > 2:
                    # 첫 번째와 마지막 이미지를 제외한 목록 순회
                    for image_name in image_files[1:-1]:
                        # 이미지 이름에서 확장자를 제거한 후 기록
                        image_name_without_ext = os.path.splitext(image_name)[0]
                        file.write(f"{folder} {image_name_without_ext} l\n")
                elif len(image_files) == 2:
                    print(f"Skipping folder '{folder}' because it has only 2 images.")
                else:
                    print(f"Skipping folder '{folder}' because it has fewer than 2 images.")

    print(f"Folder and image info saved to {output_txt_path}")

if __name__ == "__main__":
    # ArgumentParser를 사용해 커맨드라인 인자를 처리
    parser = argparse.ArgumentParser(description="Save folder and image info to a txt file.")
    
    # input_path와 output_path를 커맨드라인 인자로 받음
    parser.add_argument('--input_path', type=str, required=True, help="Path to the input directory containing folders of images.")
    parser.add_argument('--output_path', type=str, required=True, help="Path to the output txt file.")

    # 인자 파싱
    args = parser.parse_args()

    # 함수 호출
    save_folder_image_info_to_txt(args.input_path, args.output_path)