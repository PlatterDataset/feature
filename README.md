# feature
## video features
In video_features.py, there are metrics of blur, noise and freeze. You can modify the main function to test your own video.
 In our study, we define four metrics for evaluating the quality of video calls.
1. **Blur** in a video call may be caused by poor camera capture quality, object movement, adaptive streaming, etc.Here we use a method based on Fast Fourier Transform [1] to measure the blur in video call sessions.
2.  **Freeze** of video frames represents the case when a video frame is stuck, and the following frames cannot be timely loaded,given poorbandwidthornetworkcongestion. It can be determined by the magnitude of the frame difference. Taking account of video compression and network transmission, we use a threshold method as in [2] to detect freezing frames.
3. **Noise** in an image is random variation of brightness or color information. Assuming Gaussian noise in a short video session, the difference of two consecutive frames can be summed by two parts: the part caused by object movement, and the part of difference of noise in frames. We manage to filter out the noise difference part, of which the distribution is positively correlated to the distribution of a single frame, hence being able to evaluate the video frames’ noise level.

## synchronization
 We use a pre-trained model called SyncNet [4,5] to detect the offset between audio signals and video frames in a video call session. We modify the code of the original one to support our need. The length of a clip in the output file is usually 4s. In the output file, a line contains three numbers, a number of frame N meaning the clip contains N+1 frames of 0.04s, an offset number meaning the offset of the clip: closing to 0 means no out-of-sync and a confidence number meaning the accuracy of the test: the bigger, the better.
 To use the code provided, run download_model.sh first
 Then add video to ./path/paper and run group_process.py
