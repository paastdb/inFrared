import cv2
from moviepy.editor import VideoFileClip

def apply_infrared(frame):
    processed_frame = infared_effect(frame)

    return processed_frame

def infared_effect(frame):
    cimg = frame
    plt_image = cv2.cvtColor(cimg, cv2.COLOR_BGR2RGB)
     
    inv_cimg = ~cimg.copy()
    inv_cimg[:, :, 1] = 0
    inv_cimg[:, :, 2] = 0
    
    plt_image = cv2.cvtColor(inv_cimg, cv2.COLOR_BGR2RGB)
    
    inv_hsv = cv2.cvtColor(inv_cimg, cv2.COLOR_BGR2HSV)
    img_hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)

    dst = cv2.addWeighted(inv_hsv[:, :, 0] , .9, img_hsv[:, :, 0] , .9, 0)
    img_hsv[:, :, 0] = dst
    hue_cimg = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    plt_image = hue_cimg
    
    plt_image = cv2.cvtColor(hue_cimg, cv2.COLOR_BGR2RGB)
    frame = plt_image

    return frame

def main():
    # Open video file
    input_video_path = 'D:\Downloads\Past Lands\Infrared\FPV Drone Flight through Beautiful Iceland Canyon.mp4'
    cap = cv2.VideoCapture(input_video_path)
    
    # Check if video file opened successfully
    if not cap.isOpened():
        print("Error: Unable to open video file")
        return

    # Get input video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    codec = cv2.VideoWriter_fourcc(*'mp4v')

    # Define codec and create VideoWriter object
    out = cv2.VideoWriter('video-output.mp4', codec, fps, (width, height))

    # Process each frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Apply night vision effect to the frame
        processed_frame = apply_infrared(frame)

        # Write the processed frame to output video
        out.write(processed_frame)

        # Display the processed frame
        cv2.imshow('Infrared', processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    # Merge processed video with original audio using moviepy
    original_clip = VideoFileClip(input_video_path)
    processed_clip = VideoFileClip('video-output.mp4')
    final_clip = processed_clip.set_audio(original_clip.audio)
    final_clip.write_videofile('video-output-audio.mp4', codec='libx264', audio_codec='aac')


if __name__ == "__main__":
    main()