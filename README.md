# 如何正确更新MPV

项目地址(https://github.com/hooke007/mpv_PlayKit)

1. 下载最新release的exe和vsNV.7z到要安装的文件夹中
2. 重命名旧的mpv文件夹做备份
3. 先exe后vsNV.7z，其中vsNV.7z使用覆盖解压
> exe本质是便携化解压缩的安装
4. 将旧的portable config的.git文件夹放到新的，并用git逐个比对前后设置的异同
> 建议一个commit针对conf的这些设置，另一个commit针对滤镜文件的改动