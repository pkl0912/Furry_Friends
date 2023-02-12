package com.k_bootcamp.furry_friends.util.dialog

import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.view.View
import androidx.activity.result.ActivityResultLauncher
import com.k_bootcamp.furry_friends.R
import com.k_bootcamp.furry_friends.util.etc.getCameraImage
import com.k_bootcamp.furry_friends.util.etc.getGalleryImage
import com.k_bootcamp.furry_friends.view.MainActivity
import com.shashank.sony.fancydialoglib.Animation
import com.shashank.sony.fancydialoglib.FancyAlertDialog

fun setFancyDialog(
    context: Context,
    mainActivity: MainActivity,
    permissionLauncher: ActivityResultLauncher<String>,
    getCameraImageLauncher: ActivityResultLauncher<Intent>,
    getGalleryImageLauncher: ActivityResultLauncher<Intent>
): FancyAlertDialog = FancyAlertDialog.Builder
        .with(context)
        .setBackgroundColor(Color.parseColor("#00BD56"))
        .setTitle("이미지 선택")
        .setMessage("사진 가져올 곳을 선택해주세요")
        .setPositiveBtnText("카메라")
        .onPositiveClicked {
            it.dismiss()
            getCameraImage(mainActivity, permissionLauncher, getCameraImageLauncher)
        }
        .setPositiveBtnBackgroundRes(R.color.main_color)
        .setNegativeBtnText("갤러리")
        .onNegativeClicked {
            it.dismiss()
            getGalleryImage(mainActivity, permissionLauncher, getGalleryImageLauncher)
        }
        .setNegativeBtnBackgroundRes(R.color.main_color)
        .isCancellable(true)
        .setAnimation(Animation.SLIDE)
        .setIcon(R.drawable.ic_image_36, View.VISIBLE)
        .build()