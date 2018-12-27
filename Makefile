web_run:
	docker build -t photobooth_web . && docker run -it -v `pwd`/images:/images -p=8666:8666 photobooth_web

web_daemon:
	docker build -t photobooth_web . && docker run -d --restart=always -v `pwd`/images:/images -p=8666:8666 photobooth_web

download_run:
	docker build -t photobooth_download -f Dockerfile.downloader . && docker run -it --env-file=.env -v `pwd`/images:/images photobooth_download

download_daemon:
	docker build -t photobooth_download -f Dockerfile.downloader  . && docker run -d --restart=always --env-file=.env -v `pwd`/images:/images photobooth_download

