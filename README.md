# VisionDigital
Проект тестировался в системе Linux Ubuntu 22.04, для инференса использовался фотобокс, мультиметр DTXXXXXX, источник тока для генерации сигнала, видеокамера logitech c920.
Для запуска проекта необходимо:
1. Скачать библиотеку EasyOCR https://github.com/JaidedAI/EasyOCR.git
2. Установить необходимые библиотеки из файла ./VisionDigital/requiments.txt
3. В консоле запустить /bin/python3 "~/VisionDigital/visiondigital.py"  -easyocr_path "~/EasyOCR/easyocr/" -model_path "~/VisionDigital/saved_models/" -user_network_path "~/VisionDigital/model" -recog_network "digital"
