### 20240412
### 由于vpy只能调用一个，故整合使放大SR_ESRGAN_NV.vpy和补帧MEMC_RIFE_NV.vpy同时开启。先放大再补帧。
### 也可以合并为并集关系
### https://github.com/hooke007/MPV_lazy/discussions/313#discussioncomment-5968181

import vapoursynth as vs
from vapoursynth import core
import k7sfunc as k7f

clip = video_in

### 放大SR_ESRGAN_NV.vpy

SR = {
    'H_Pre': 720,  # 整数，预降低处理源高度
    'Lt_Hd': False,  # <True|False> 是否对超过HD分辨率（720P）的源进行处理
    'Model': 5008,  # <0|2|5005|5006|5007> 使用的模型
    'Gpu': 0,  # 使用的显卡序号，0为排序一号
    'Gpu_T': 2,  # <1|2|3> 使用的显卡线程数
    'St_Eng':
    False,  # <True|False> 是否使用静态引擎（需要对不同分辨率的源各进行预处理）；动态引擎自适应不同分辨率（QVGA→DCI4K）
    'Ws_Size': 0,  # <0~1024> 约束显存（MiB），静态引擎的最小值为128（动态引擎自动双倍），设为低于此数的值即为不限制
    'H_Max': 1440,  # 整数，输出高度限制（填你的显示器高度）
    'Lk_Fmt': False  # <True|False> 是否锁定像素格式为yuv420p8
}

if clip.height <= 1200:
    clip = k7f.FMT_CTRL(clip,
                        h_max=SR['H_Pre'],
                        fmt_pix=1 if SR['Lk_Fmt'] else 0)
    clip = k7f.ESRGAN_NV(clip,
                         lt_hd=SR['Lt_Hd'],
                         model=SR['Model'],
                         gpu=SR['Gpu'],
                         gpu_t=SR['Gpu_T'],
                         st_eng=SR['St_Eng'],
                         ws_size=SR['Ws_Size'])
    clip = k7f.FMT_CTRL(clip,
                        h_max=SR['H_Max'],
                        fmt_pix=1 if SR['Lk_Fmt'] else 0)

### 补帧MEMC_RIFE_NV.vpy

MEMC = {
    'H_Pre': 1440,  # 整数，预降低处理源高度（填你的显示器高度）
    'Lt_D2k': True,  # <True|False> 是否对超过DCI2K分辨率的源进行补帧
    # 改为True，对放大后的进行补帧
    'Model': 46,  # <46|415|4151> 使用的模型
    'Ext_Proc': False,  # <True|False> 是否使用外部的填充裁切处理
    'T_Tta': False,  # <True|False> 是否使用ensemble版模型
    'Fps_Num': 2,  # 整数，Fps_Num/Fps_Den 的值即帧率倍数
    'Fps_Den': 1,  # 整数
    'Sc_Mode': 1,  # <0|1|2> 场景切换检测的模式，0为禁用
    'Gpu': 0,  # 使用的显卡序号，0为排序一号
    'Gpu_T': 2,  # <1|2|3> 显卡线程数
    'St_Eng':
    False,  # <True|False> 是否使用静态引擎（需要对不同分辨率的源各进行预处理）；动态引擎自适应不同分辨率（QVGA→DCI4K）
    'Ws_Size': 0,  # 整数，约束显存（MiB），静态引擎的最小值为128（动态引擎自动双倍），设为低于此数的值即最大化利用
    'Lk_Fmt': False  # <True|False> 锁定像素格式为yuv420p8
}

if container_fps <= 32:
    clip = k7f.FMT_CTRL(clip,
                        h_max=MEMC['H_Pre'],
                        fmt_pix=1 if MEMC['Lk_Fmt'] else 0)
    clip = k7f.RIFE_NV(clip,
                       lt_d2k=MEMC['Lt_D2k'],
                       model=MEMC['Model'],
                       ext_proc=MEMC['Ext_Proc'],
                       t_tta=MEMC['T_Tta'],
                       fps_in=container_fps,
                       fps_num=MEMC['Fps_Num'],
                       fps_den=MEMC['Fps_Den'],
                       sc_mode=MEMC['Sc_Mode'],
                       gpu=MEMC['Gpu'],
                       gpu_t=MEMC['Gpu_T'],
                       st_eng=MEMC['St_Eng'],
                       ws_size=MEMC['Ws_Size'])
if not (clip == video_in):
    clip.set_output()
