import os
import subprocess

# 根目录
base_dir = "/mnt/data/OmniNOCS/objectron/videos/"
output_base_dir = "/mnt/data/OmniNOCS/extracted_frames"  # 在 OmniNOCS 根目录下创建输出文件夹

# 确保输出根目录存在
os.makedirs(output_base_dir, exist_ok=True)

# 遍历所有类别文件夹
for category_name in os.listdir(base_dir):
    category_path = os.path.join(base_dir, category_name)
    
    # 确保是目录
    if not os.path.isdir(category_path):
        continue
    
    # 遍历类别文件夹下的 batch 文件夹
    for batch_dir in os.listdir(category_path):
        batch_path = os.path.join(category_path, batch_dir)
        
        # 确保是目录
        if not os.path.isdir(batch_path):
            continue
        
        # 遍历 batch 文件夹下的数字子文件夹
        for number_dir in os.listdir(batch_path):
            number_path = os.path.join(batch_path, number_dir)
            
            # 确保是目录
            if not os.path.isdir(number_path):
                continue
            
            # 查找视频文件（假设视频文件名为 video.MOV）
            video_path = os.path.join(number_path, "video.MOV")
            if not os.path.exists(video_path):
                print(f"视频文件不存在: {video_path}")
                continue
            
            # 创建输出目录（按类别、batch 和数字子文件夹分类）
            output_dir = os.path.join(output_base_dir, category_name, batch_dir, number_dir)  # 例如：/mnt/data/OmniNOCS/extracted_frames/bike/batch-1/0
            os.makedirs(output_dir, exist_ok=True)
            
            # 使用 ffmpeg 提取帧，并以 frame 开头命名
            command = [
                "ffmpeg",
                "-i", video_path,  # 输入视频文件
                "-vsync", "vfr",   # 可变帧率
                "-vf", "scale=iw/8:ih/8",  # 缩小为原始尺寸的 1/8
                "-start_number", "0",  # 帧编号从 0 开始
                os.path.join(output_dir, "frame%06d.png")  # 输出帧文件名格式
            ]
            
            # 运行命令
            print(f"正在处理: {video_path}")
            subprocess.run(command, check=True)
            print(f"完成处理: {video_path} -> {output_dir}")

print("所有视频处理完成！")