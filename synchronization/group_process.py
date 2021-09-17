import os

dir1 = './path/paper'
files = os.listdir(dir1)
i = 0
for file in files:
	if not(file.endswith('.mp4') or file.endswith('.mkv')):
		continue
	#print(file)
	#if i == 1:
	#	continue
	i = 1
	name = file[:-3]
	print(name)
	if not(name == '060_zoom_wifi_zh_obs1.' or name == '060_tencent_wifi_zh_obs1.' or name == '060_zoom_4g_zh_obs1.'):
		continue
	os.system("python myrun_pipeline.py --videofile ./path/paper/"+file+" --reference "+name+" --data_dir ./path/paper/output")
	os.system("python myrun_syncnet.py --videofile ./path/paper/"+file+" --reference "+name+" --data_dir ./path/paper/output")
